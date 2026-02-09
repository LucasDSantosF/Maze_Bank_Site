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
from schema.request import Usuario, Login
from schema.response import BaseResponse, ErrorResponseSchema

router = APIRouter(prefix="/auth", tags=["Authentication"])

# --- UTILITÁRIOS ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_current_user(request: Request, db: Session = Depends(get_db)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    if not access_token and not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail={"message": "Nenhum cookie de sessão encontrado", "error_code": "NO_CONTENT"}
        )

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Access token ausente", "error_code": "UNAUTHORIZED"}
        )

    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        cpf: str = payload.get("sub")
        
        if cpf is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail={"message": "Token inválido", "error_code": "UNAUTHORIZED"}
            )
            
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail={"message": "Sessão expirada", "error_code": "UNAUTHORIZED"}
        )

    usuario = db.query(models.Usuario).filter(models.Usuario.cpf == cpf).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail={"message": "Usuário não encontrado", "error_code": "UNAUTHORIZED"}
        )
    
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

@router.post(
    "/register",
    responses={401: {"model": ErrorResponseSchema}}
)
def registrar(usuario: Usuario, db: Session = Depends(get_db)):
    validators.validar_senha_forte(usuario.senha)

    if db.query(models.Usuario).filter(models.Usuario.cpf == usuario.cpf).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail={"message": "CPF já cadastrado", "error_code": "BAD_REQUEST"}
        )
    
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

    return {
        "success": True,
        "message": "Conta criada com sucesso!",
    }

@router.post(
    "/login",
    responses={401: {"model": ErrorResponseSchema}}
)
def login(usuario: Login, response: Response, db: Session = Depends(get_db)):
    sessao = db.query(models.Usuario).filter(models.Usuario.cpf == usuario.cpf).first()
    
    if not sessao or not pwd_context.verify(usuario.senha, sessao.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Credenciais inválidas", "error_code": "UNAUTHORIZED"}
        )
    
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
        domain=None,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh,
        httponly=True,
        secure=False,
        samesite="lax",
        domain=None,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600
    )
    
    return {
        "success": True,
        "message": "Login realizado com sucesso!",
    }

@router.post(
    "/refresh",
    responses={401: {"model": ErrorResponseSchema}}
)
def renovar_acesso(request: Request, response: Response, db: Session = Depends(get_db)):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Cookie de refresh ausente", "error_code": "UNAUTHORIZED"}
        )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        cpf = payload.get("sub")
        usuario = db.query(models.Usuario).filter(
            models.Usuario.cpf == cpf, 
            models.Usuario.refresh_token == token
        ).first()
        
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"message": "Refresh token não reconhecido", "error_code": "UNAUTHORIZED"}
            )

        novo_access = criar_jwt({"sub": cpf}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        response.set_cookie(
            key="access_token",
            value=novo_access,
            httponly=True,
            secure=False,
            samesite="lax",
            domain=None,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
        return {
            "success": True,
            "message": "Token de acesso renovado com sucesso!",
        }
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail={"message": "Token de refresh expirado ou corrompido", "error_code": "UNAUTHORIZED"}
        )

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    
    return {
        "success": True,
        "message": "Sessão encerrada com sucesso!",
    }