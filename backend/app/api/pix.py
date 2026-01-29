import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models import models
from api.auth import  get_current_user

router = APIRouter(prefix="/pix", tags=["PIX"])

@router.get("/chaves")
def listar_chaves(user: models.Usuario = Depends(get_current_user)):
    return user.minhas_chaves

@router.post("/chave")
def criar_chave(tipo: str, valor: str = None, db: Session = Depends(get_db), user: models.Usuario = Depends(get_current_user)):
    if len(user.minhas_chaves) >= 5:
        raise HTTPException(status_code=400, detail="Limite de 5 chaves atingido")
    
    chave_final = valor
    if tipo.upper() == "ALEATORIA":
        chave_final = str(uuid.uuid4())
    elif not valor:
        raise HTTPException(status_code=400, detail="Valor da chave é obrigatório para este tipo")

    if db.query(models.ChavePix).filter(models.ChavePix.chave == chave_final).first():
        raise HTTPException(status_code=400, detail="Esta chave PIX já pertence a alguém")

    nova_chave = models.ChavePix(chave=chave_final, tipo=tipo.upper(), usuario_id=user.id)
    db.add(nova_chave)
    db.commit()
    return {"message": "Chave PIX criada", "chave": chave_final}

@router.delete("/chave/excluir")
def excluir_chave(chave: str, db: Session = Depends(get_db), user: models.Usuario = Depends(get_current_user)):
    chave_db = db.query(models.ChavePix).filter(models.ChavePix.chave == chave, models.ChavePix.usuario_id == user.id).first()
    
    if not chave_db:
        raise HTTPException(status_code=404, detail="Chave não encontrada ou não pertence a você")
    
    db.delete(chave_db)
    db.commit()
    return {"message": "Chave PIX excluída"}