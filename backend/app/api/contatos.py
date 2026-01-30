from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from api.auth import get_current_user
from models import models

router = APIRouter(prefix="/contatos", tags=["Agenda de Contatos"])

@router.post("/")
def adicionar_contato(
    nome: str, 
    cpf: str, 
    chave_pix: str = None, 
    tipo_chave: str = None,
    agencia: str = None,
    conta: str = None,
    user: models.Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    novo_contato = models.Contato(
        nome=nome,
        cpf=cpf,
        chave_pix=chave_pix,
        tipo_chave_pix=tipo_chave.upper() if tipo_chave else None,
        agencia=agencia,
        conta=conta,
        usuario_id=user.id
    )
    db.add(novo_contato)
    db.commit()
    return {"message": "Contato salvo com sucesso"}

@router.get("/")
def listar_contatos(user: models.Usuario = Depends(get_current_user)):
    return user.contatos