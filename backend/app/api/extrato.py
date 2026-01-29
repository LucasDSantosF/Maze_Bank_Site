from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from datetime import datetime
from db.database import get_db
from api.auth import get_current_user
from models import models

router = APIRouter(prefix="/extrato", tags=["Extrato Bancário"])

def mascarar_cpf(cpf: str):
    if not cpf: return None
    return f"{cpf[:3]}.***.***-{cpf[-2:]}"

@router.get("/")
def listar_extrato(
    tipo: str = None, 
    data_inicio: datetime = None, 
    data_fim: datetime = None,
    user: models.Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(models.Transacao).filter(models.Transacao.usuario_id == user.id)

    if tipo:
        if tipo == "entrada":
            query = query.filter(models.Transacao.tipo.in_(["PIX_RECEBIDO", "DEPOSITO", "TRANSFERENCIA_RECEBIDA"]))
        elif tipo == "saida":
            query = query.filter(models.Transacao.tipo.in_(["PIX_ENVIADO", "SAQUE", "TRANSFERENCIA_ENVIADA"]))
        elif tipo == "pix":
            query = query.filter(models.Transacao.tipo.like("PIX_%"))
        else:
            query = query.filter(models.Transacao.tipo == tipo.upper())

    if data_inicio:
        query = query.filter(models.Transacao.data >= data_inicio)
    if data_fim:
        query = query.filter(models.Transacao.data <= data_fim)

    transacoes = query.order_by(models.Transacao.data.desc()).all()

    for t in transacoes:
        if "RECEBIDO" in t.tipo or "RECEBIDA" in t.tipo:
            t.remetente_cpf = mascarar_cpf(t.remetente_cpf)
        elif "ENVIADO" in t.tipo or "ENVIADA" in t.tipo:
            t.recebedor_cpf = mascarar_cpf(t.recebedor_cpf)

    return transacoes

@router.get("/resumo")
def resumo_geral(user: models.Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Transacao).filter(
        models.Transacao.usuario_id == user.id
    ).order_by(models.Transacao.data.desc()).limit(5).all()

@router.get("/resumo/pix")
def resumo_pix(user: models.Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Transacao).filter(
        and_(
            models.Transacao.usuario_id == user.id,
            models.Transacao.tipo.like("PIX_%")
        )
    ).order_by(models.Transacao.data.desc()).limit(5).all()