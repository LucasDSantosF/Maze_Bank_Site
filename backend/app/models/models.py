from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from decimal import Decimal
from db.database import Base

class Contato(Base):
    __tablename__ = "contatos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    cpf = Column(String)
    chave_pix = Column(String, nullable=True)
    tipo_chave_pix = Column(String, nullable=True)
    agencia = Column(String, nullable=True)
    conta = Column(String, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    dono = relationship("Usuario", back_populates="contatos")

class TransferenciaPendente(Base):
    __tablename__ = "transferencias_pendentes"
    
    id = Column(String, primary_key=True)
    valor = Column(Numeric(10, 2))
    tipo_operacao = Column(String)
    remetente_id = Column(Integer)
    recebedor_id = Column(Integer)
    data_expiracao = Column(DateTime)

class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Numeric(precision=10, scale=2))
    id_transferencia = Column(String)
    tipo = Column(String)
    data = Column(DateTime(timezone=True), server_default=func.now())
    remetente_nome = Column(String, nullable=True)
    remetente_cpf = Column(String, nullable=True)
    recebedor_nome = Column(String, nullable=True)
    recebedor_cpf = Column(String, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    dono = relationship("Usuario", back_populates="transacoes")

class ChavePix(Base):
    __tablename__ = "chaves_pix"

    id = Column(Integer, primary_key=True, index=True)
    chave = Column(String, unique=True, index=True)
    tipo = Column(String)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    dono = relationship("Usuario", back_populates="minhas_chaves")

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    sobrenome = Column(String)
    email = Column(String, unique=True, index=True)
    cpf = Column(String, unique=True, index=True)
    senha_hash = Column(String)
    agencia = Column(String, default="0001")
    numero_conta = Column(String, unique=True, index=True)
    saldo = Column(Numeric(precision=10, scale=2), default=Decimal("0.00"))
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    minhas_chaves = relationship("ChavePix", back_populates="dono")
    transacoes = relationship("Transacao", back_populates="dono")
    refresh_token = Column(String, nullable=True)