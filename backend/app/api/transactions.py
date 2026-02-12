import uuid
from decimal import Decimal
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from api.auth import get_current_user
from models import models
from utils.mascara import mascarar_cpf
from schema.request import Money, TED, Pix, Confirmar
from schema.response import BaseResponse, ConfirmacaoPagamentoSchema, ComprovanteTransferenciaSchema, ComprovantePixSchema, ErrorResponseSchema

router = APIRouter(prefix="/transaction", tags=["Transactions"])

@router.post(
    "/sinalizar/dados", 
    response_model=BaseResponse[ComprovanteTransferenciaSchema],
    responses={401: {"model": ErrorResponseSchema}}
)
def sinalizar_ted(request: TED, db: Session = Depends(get_db), user: models.Usuario = Depends(get_current_user)):
    recebedor = db.query(models.Usuario).filter(
        models.Usuario.agencia == request.agencia, 
        models.Usuario.numero_conta == request.conta
    ).first()
    
    if not recebedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Conta destino não encontrada", "error_code": "NOT_FOUND"}
        )

    id_transf = str(uuid.uuid4())

    nova_pendencia = models.TransferenciaPendente(
        id=id_transf,
        valor=Decimal(str(request.valor)),
        tipo_operacao="TRANSFERENCIA",
        remetente_id=user.id,
        recebedor_id=recebedor.id,
        data_expiracao=datetime.utcnow() + timedelta(minutes=5)
    )
    db.add(nova_pendencia)
    db.commit()

    data = {
        "id_transferencia": id_transf,
        "remetente": {
            "nome": f"{user.nome} {user.sobrenome}",
            "cpf": mascarar_cpf(user.cpf),
            "agencia": user.agencia,
            "conta": user.numero_conta
        },
        "recebedor": {
            "nome": f"{recebedor.nome} {recebedor.sobrenome}", 
            "cpf": mascarar_cpf(recebedor.cpf),
            "agencia": recebedor.agencia,
            "conta": recebedor.numero_conta
        },
        "valor": request.valor
    }

    return {
        "success": True,
        "message": "Transferência realizada com sucesso!",
        "data": data
    }

@router.post(
    "/sinalizar/pix",
    response_model=BaseResponse[ComprovantePixSchema],
    responses={401: {"model": ErrorResponseSchema}}
)
def sinalizar_pix(request: Pix, db: Session = Depends(get_db), user: models.Usuario = Depends(get_current_user)):
    chave_db = db.query(models.ChavePix).filter(
        models.ChavePix.chave == request.chave, 
        models.ChavePix.tipo == request.tipo_chave.upper()
    ).first()
    
    if not chave_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail={"message": "Chave PIX não encontrada", "error_code": "NOT_FOUND"}
        )

    recebedor = chave_db.dono
    id_transf = str(uuid.uuid4())
    
    pendencia = models.TransferenciaPendente(
        id=id_transf,
        valor=Decimal(str(request.valor)),
        tipo_operacao="PIX",
        remetente_id=user.id,
        recebedor_id=recebedor.id,
        chave_pix_id=chave_db.id,
        data_expiracao=datetime.utcnow() + timedelta(minutes=5)
    )
    db.add(pendencia)
    db.commit()

    data = {
        "id_transferencia": id_transf,
        "remetente": {
            "nome": f"{user.nome} {user.sobrenome}",
            "cpf": mascarar_cpf(user.cpf)
        },
        "recebedor": {
            "nome": f"{recebedor.nome} {recebedor.sobrenome}", 
            "cpf": mascarar_cpf(recebedor.cpf)
        },
        "chave": {
            "chave": chave_db.chave, 
            "tipo": chave_db.tipo
        },
        "valor": request.valor
    }

    return {
        "success": True,
        "message": "Pix realizada com sucesso!",
        "data": data
    }

@router.post(
    "/confirmar",
    response_model=BaseResponse[ConfirmacaoPagamentoSchema],
    responses={401: {"model": ErrorResponseSchema}}
)
def confirmar_transferencia(request: Confirmar, db: Session = Depends(get_db), user: models.Usuario = Depends(get_current_user)):
    pendencia = db.query(models.TransferenciaPendente).filter(models.TransferenciaPendente.id == request.id_transferencia).first()
    
    if not pendencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail={"message": "Sinalização expirada ou inexistente", "error_code": "NOT_FOUND"}
        )

    if user.saldo < pendencia.valor:
        db.delete(pendencia)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Saldo insuficiente para completar a operação", "error_code": "BAD_REQUEST"}
        )

    recebedor = db.query(models.Usuario).get(pendencia.recebedor_id)

    user.saldo -= pendencia.valor
    recebedor.saldo += pendencia.valor

    tipo_base = pendencia.tipo_operacao

    tipo_saida = f"{tipo_base}_ENVIADO" if tipo_base == "PIX" else f"{tipo_base}_ENVIADA"
    tipo_entrada = f"{tipo_base}_RECEBIDO" if tipo_base == "PIX" else f"{tipo_base}_RECEBIDA"

    extrato_saida = models.Transacao(
        valor=pendencia.valor, id_transferencia=request.id_transferencia,
        tipo=tipo_saida, usuario_id=user.id,
        remetente_nome=f"{user.nome} {user.sobrenome}", remetente_cpf=user.cpf,
        recebedor_nome=f"{recebedor.nome} {recebedor.sobrenome}", recebedor_cpf=recebedor.cpf
    )

    extrato_entrada = models.Transacao(
        valor=pendencia.valor, id_transferencia=request.id_transferencia,
        tipo=tipo_entrada, usuario_id=recebedor.id,
        remetente_nome=f"{user.nome} {user.sobrenome}", remetente_cpf=user.cpf,
        recebedor_nome=f"{recebedor.nome} {recebedor.sobrenome}", recebedor_cpf=recebedor.cpf
    )

    contato_existente = db.query(models.Contato).filter(
        models.Contato.usuario_id == user.id,
        models.Contato.cpf == recebedor.cpf
    ).first()

    chave_db = db.query(models.ChavePix).filter(
        models.ChavePix.id == pendencia.chave_pix_id
    ).first()

    valor_chave = getattr(chave_db , 'chave', None)
    valor_tipo = getattr(chave_db , 'tipo', None)

    if not contato_existente:
        novo_contato = models.Contato(
            nome=f"{recebedor.nome} {recebedor.sobrenome}",
            cpf=recebedor.cpf,
            agencia=recebedor.agencia,
            conta=recebedor.numero_conta,
            chave_pix=valor_chave,
            tipo_chave_pix=valor_tipo,
            usuario_id=user.id
        )
        db.add(novo_contato)
    else:
        if pendencia.tipo_operacao == "PIX" and not contato_existente.chave_pix:
            contato_existente.chave_pix = valor_chave
            contato_existente.tipo_chave_pix = valor_tipo

    db.add_all([extrato_saida, extrato_entrada])
    db.delete(pendencia)
    db.commit()

    dados_confirmacao = {
        "valor": pendencia.valor, 
        "recebedor": recebedor.nome,
        "contato_salvo": not contato_existente
    }

    return {
        "success": True,
        "message": "Pagamento processado com sucesso",
        "data": dados_confirmacao
    }

@router.post(
    "/deposit",
    responses={401: {"model": ErrorResponseSchema}}
)
def depositar(money: Money, db: Session = Depends(get_db), user: models.Usuario = Depends(get_current_user)):
    if money.valor <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "O valor do depósito deve ser maior que zero", "error_code": "BAD_REQUEST"}
        )

    valor_decimal = Decimal(str(money.valor))

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
        "success": True,
        "message": "Depósito realizado com sucesso",
    }

@router.post(
    "/withdraw",
    responses={401: {"model": ErrorResponseSchema}}
)
def sacar(money: Money, db: Session = Depends(get_db), user: models.Usuario = Depends(get_current_user)):
    valor_decimal = Decimal(str(money.valor))

    if valor_decimal <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "O valor do saque deve ser maior que zero", "error_code": "BAD_REQUEST"}
        )

    if user.saldo < valor_decimal:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail={"message": "Saldo insuficiente", "error_code": "BAD_REQUEST"}
        )

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
        "success": True,
        "message": "Saque realizado com sucesso",
    }