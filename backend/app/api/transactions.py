import uuid
from decimal import Decimal
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from api.auth import get_current_user
from models import models

router = APIRouter(prefix="/transaction", tags=["Transactions"])

@router.post("/sinalizar/dados")
def sinalizar_ted(valor: float, agencia: str, conta: str, db: Session = Depends(get_db), user: models.Usuario = Depends(get_current_user)):
    recebedor = db.query(models.Usuario).filter(
        models.Usuario.agencia == agencia, 
        models.Usuario.numero_conta == conta
    ).first()
    
    if not recebedor:
        raise HTTPException(status_code=404, detail="Conta destino não encontrada")

    id_transf = str(uuid.uuid4())

    nova_pendencia = models.TransferenciaPendente(
        id=id_transf,
        valor=Decimal(str(valor)),
        tipo_operacao="TRANSFERENCIA",
        remetente_id=user.id,
        recebedor_id=recebedor.id,
        data_expiracao=datetime.utcnow() + timedelta(minutes=5)
    )
    db.add(nova_pendencia)
    db.commit()

    return {
        "id_transferencia": id_transf,
        "recebedor": {"nome": recebedor.nome, "cpf": f"***.{recebedor.cpf[3:6]}.***-**"},
        "valor": valor
    }

@router.post("/sinalizar/pix")
def sinalizar_pix(valor: float, chave: str, tipo_chave: str, db: Session = Depends(get_db), user: models.Usuario = Depends(get_current_user)):
    chave_db = db.query(models.ChavePix).filter(
        models.ChavePix.chave == chave, 
        models.ChavePix.tipo == tipo_chave.upper()
    ).first()
    
    if not chave_db:
        raise HTTPException(status_code=404, detail="Chave PIX não encontrada")

    recebedor = chave_db.dono
    id_transf = str(uuid.uuid4())
    
    pendencia = models.TransferenciaPendente(
        id=id_transf,
        valor=Decimal(str(valor)),
        tipo_operacao="PIX",
        remetente_id=user.id,
        recebedor_id=recebedor.id,
        data_expiracao=datetime.utcnow() + timedelta(minutes=5)
    )
    db.add(pendencia)
    db.commit()

    return {
        "id_transferencia": id_transf,
        "recebedor": {"nome": recebedor.nome, "cpf": f"***.{recebedor.cpf[3:6]}.***-**"},
        "valor": valor
    }

@router.post("/confirmar")
def confirmar_transferencia(id_transferencia: str, db: Session = Depends(get_db), user: models.Usuario = Depends(get_current_user)):
    pendencia = db.query(models.TransferenciaPendente).filter(models.TransferenciaPendente.id == id_transferencia).first()
    
    if not pendencia:
        raise HTTPException(status_code=404, detail="Sinalização expirada ou inexistente")

    if user.saldo < pendencia.valor:
        db.delete(pendencia)
        db.commit()
        raise HTTPException(status_code=400, detail="Saldo insuficiente para completar a operação")

    recebedor = db.query(models.Usuario).get(pendencia.recebedor_id)

    user.saldo -= pendencia.valor
    recebedor.saldo += pendencia.valor

    tipo_base = pendencia.tipo_operacao

    extrato_saida = models.Transacao(
        valor=pendencia.valor, id_transferencia=id_transferencia,
        tipo=f"{tipo_base}_ENVIADO", usuario_id=user.id,
        remetente_nome=user.nome, remetente_cpf=user.cpf,
        recebedor_nome=recebedor.nome, recebedor_cpf=recebedor.cpf
    )

    extrato_entrada = models.Transacao(
        valor=pendencia.valor, id_transferencia=id_transferencia,
        tipo=f"{tipo_base}_RECEBIDO", usuario_id=recebedor.id,
        remetente_nome=user.nome, remetente_cpf=user.cpf,
        recebedor_nome=recebedor.nome, recebedor_cpf=recebedor.cpf
    )

    db.add_all([extrato_saida, extrato_entrada])
    db.delete(pendencia)
    db.commit()

    return {
        "status": "sucesso", "valor": pendencia.valor, "recebedor": recebedor.nome
    }


@router.post("/deposit")
def depositar(valor: float, db: Session = Depends(get_db), user: models.Usuario = Depends(get_current_user)):
    if valor <= 0:
        raise HTTPException(status_code=400, detail="O valor do depósito deve ser maior que zero")

    valor_decimal = Decimal(str(valor))

    user.saldo += valor_decimal

    nova_transacao = models.Transacao(
        valor=valor_decimal,
        id_transferencia=str(uuid.uuid4()),
        tipo="DEPOSITO",
        remetente_nome=None,
        remetente_cpf=None,
        recebedor_nome=user.nome,
        recebedor_cpf=user.cpf,
        usuario_id=user.id
    )

    db.add(nova_transacao)
    db.commit()
    db.refresh(user)

    return {
        "message": "Depósito realizado com sucesso",
        "novo_saldo": user.saldo,
        "id_transacao": nova_transacao.id_transferencia
    }

@router.post("/withdraw")
def sacar(valor: float, db: Session = Depends(get_db), user: models.Usuario = Depends(get_current_user)):
    valor_decimal = Decimal(str(valor))

    if valor_decimal <= 0:
        raise HTTPException(status_code=400, detail="O valor do saque deve ser maior que zero")

    if user.saldo < valor_decimal:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")

    user.saldo -= valor_decimal

    nova_transacao = models.Transacao(
        valor=valor_decimal,
        id_transferencia=str(uuid.uuid4()),
        tipo="SAQUE",
        remetente_nome=user.nome,
        remetente_cpf=user.cpf,
        recebedor_nome=None,
        recebedor_cpf=None,
        usuario_id=user.id
    )

    db.add(nova_transacao)
    db.commit()
    db.refresh(user)

    return {
        "message": "Saque realizado com sucesso",
        "novo_saldo": user.saldo,
        "id_transacao": nova_transacao.id_transferencia
    }