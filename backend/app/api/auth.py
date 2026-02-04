from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from decimal import Decimal
from jose import jwt, JWTError
from passlib.context import CryptContext
import random
from config import settings

from models import models
from db.database import get_db
from utils import validators
from models.body import UserCreate, Login

router = APIRouter(prefix="/auth", tags=["Authentication"])

# --- UTILITÁRIOS ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(
            status_code=401, 
            detail="Você não está logado (Cookie ausente)"
        )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        cpf: str = payload.get("sub")
        
        if cpf is None:
            raise HTTPException(status_code=401, detail="Token inválido")
            
    except JWTError:
        raise HTTPException(status_code=401, detail="Sessão expirada")

    usuario = db.query(models.Usuario).filter(models.Usuario.cpf == cpf).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return usuario

def criar_jwt(dados: dict, expires_delta: timedelta):
    para_codificar = dados.copy()
    expiracao = datetime.utcnow() + expires_delta
    para_codificar.update({"exp": expiracao})
    return jwt.encode(para_codificar, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def gerar_numero_conta_com_dv():
    corpo_conta = "".join([str(random.randint(0, 9)) for _ in range(7)])
    
    soma = sum(int(digito) for digito in corpo_conta)
    dv = soma % 10
    
    return f"{corpo_conta}-{dv}"

# --- ROTAS ---

@router.post("/register")
def registrar(usuario: UserCreate, db: Session = Depends(get_db)):
    validators.validar_senha_forte(usuario.senha)

    if db.query(models.Usuario).filter(models.Usuario.cpf == usuario.cpf).first():
        raise HTTPException(status_code=400, detail="CPF já cadastrado")
    
    nova_conta = gerar_numero_conta_com_dv()

    while db.query(models.Usuario).filter(models.Usuario.numero_conta == nova_conta).first():
        nova_conta = gerar_numero_conta_com_dv()

    novo_usuario = models.Usuario(
        nome=usuario.nome,
        sobrenome=usuario.sobrenome,
        email=usuario.email,
        cpf=usuario.cpf,
        senha_hash=pwd_context.hash(usuario.senha),
        numero_conta=nova_conta,
        agencia="0001",
        saldo=Decimal("0.00")
    )
    db.add(novo_usuario)
    db.commit()
    return {"message": "Conta criada com sucesso!"}

@router.post("/login")
def login(usuario: Login, response: Response, db: Session = Depends(get_db)):
    sessao = db.query(models.Usuario).filter(models.Usuario.cpf == usuario.cpf).first()
    
    if not sessao or not pwd_context.verify(usuario.senha, sessao.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    access = criar_jwt({"sub": sessao.cpf}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh = criar_jwt({"sub": sessao.cpf}, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))

    sessao.refresh_token = refresh
    db.commit()

    response.set_cookie(
        key="access_token",
        value=access,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600
    )
    
    return {"message": "Login realizado com sucesso"}

@router.post("/refresh")
def renovar_acesso(request: Request, response: Response, db: Session = Depends(get_db)):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Cookie de refresh ausente")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        cpf = payload.get("sub")
        usuario = db.query(models.Usuario).filter(
            models.Usuario.cpf == cpf, 
            models.Usuario.refresh_token == token
        ).first()
        
        if not usuario:
            raise HTTPException(status_code=401, detail="Refresh token não reconhecido")

        novo_access = criar_jwt({"sub": cpf}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        response.set_cookie(
            key="access_token",
            value=novo_access,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
        return {"message": "Token de acesso renovado"}
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Token de refresh expirado ou corrompido")

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    
    return {"message": "Sessão encerrada"}