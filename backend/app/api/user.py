from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from config import settings

import models
from db.database import get_db
from api.auth import oauth2_scheme

router = APIRouter(prefix="/user", tags=["User Profile"])

@router.get("/me")
def obter_meu_perfil(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        cpf: str = payload.get("sub")
        if cpf is None:
            raise HTTPException(status_code=401, detail="Token inválido")
            
    except JWTError:
        raise HTTPException(status_code=401, detail="Sessão expirada ou inválida")

    usuario = db.query(models.Usuario).filter(models.Usuario.cpf == cpf).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return {
        "nome": usuario.nome,
        "sobrenome": usuario.sobrenome,
        "email": usuario.email,
        "cpf": usuario.cpf,
        "detalhes_bancarios": {
            "agencia": usuario.agencia,
            "conta": usuario.numero_conta,
            "saldo": usuario.saldo
        },
        "membro_desde": usuario.data_criacao
    }