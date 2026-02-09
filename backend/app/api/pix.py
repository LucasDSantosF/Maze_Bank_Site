import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from models import models
from api.auth import  get_current_user
from schema.request import Chave, ChaveExcluir
from schema.response import BaseResponse, ChavePixSchema, ErrorResponseSchema

router = APIRouter(prefix="/pix", tags=["PIX"])

@router.get(
    "/chaves",
    response_model=BaseResponse[list[ChavePixSchema]],
    responses={401: {"model": ErrorResponseSchema}}
)
def listar_chaves(user: models.Usuario = Depends(get_current_user)):
    return {
        "success": True,
        "message": "Suas chaves PIX foram recuperadas",
        "data": user.minhas_chaves
    }

@router.post(
    "/chave",
    responses={401: {"model": ErrorResponseSchema}}
)
def criar_chave(request: Chave, db: Session = Depends(get_db), user: models.Usuario = Depends(get_current_user)):
    if len(user.minhas_chaves) >= 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Limite de 5 chaves atingido", "error_code": "BAD_REQUEST"}
        )
    
    chave_final = request.valor
    if request.tipo.upper() == "ALEATORIA":
        chave_final = str(uuid.uuid4())
    elif not request.valor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Valor da chave é obrigatório para este tipo", "error_code": "BAD_REQUEST"}
        )

    if db.query(models.ChavePix).filter(models.ChavePix.chave == chave_final).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail={"message": "Esta chave PIX já pertence a alguém", "error_code": "BAD_REQUEST"}
        )

    nova_chave = models.ChavePix(chave=chave_final, tipo=request.tipo.upper(), usuario_id=user.id)
    db.add(nova_chave)
    db.commit()

    return {
        "success": True,
        "message": "Chave PIX criada",
    }

@router.delete(
    "/chave/excluir",
    responses={401: {"model": ErrorResponseSchema}}
)
def excluir_chave(request: ChaveExcluir, db: Session = Depends(get_db), user: models.Usuario = Depends(get_current_user)):
    chave_db = db.query(models.ChavePix).filter(models.ChavePix.chave == request.valor, models.ChavePix.usuario_id == user.id).first()
    
    if not chave_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail={"message": "Chave não encontrada ou não pertence a você", "error_code": "NOT_FOUND"}
            )
    
    db.delete(chave_db)
    db.commit()
    
    return {
        "success": True,
        "message": "Chave PIX excluída",
    }
