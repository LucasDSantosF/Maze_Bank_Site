from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from api.auth import get_current_user
from models import models

router = APIRouter(prefix="/contatos", tags=["Agenda de Contatos"])

@router.get("/")
def listar_contatos(user: models.Usuario = Depends(get_current_user)):
    return user.contatos