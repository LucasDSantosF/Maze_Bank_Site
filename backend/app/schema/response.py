from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import TypeVar, Generic, Optional, Any

T = TypeVar("T")

class BaseResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None
    error_code: Optional[str] = None


# Usuario
class DetalhesBancariosSchema(BaseModel):
    agencia: str
    conta: str
    saldo: float


class UsuarioSchema(BaseModel):
    nome: str
    sobrenome: str
    email: EmailStr
    cpf: str
    detalhes_bancarios: DetalhesBancariosSchema
    membro_desde: datetime

    class Config:
        from_attributes = True

# Extrato
class TransacaoSchema(BaseModel):
    id: int
    tipo: str
    valor: float
    data: datetime
    id_transferencia: str
    remetente_nome: Optional[str] = None
    recebedor_nome: Optional[str] = None
    remetente_cpf: Optional[str] = None
    recebedor_cpf: Optional[str] = None

    class Config:
        from_attributes = True

# Contatos
class DadosBancariosContatoSchema(BaseModel):
    agencia: str
    conta: str
    cpf: str

class BaseChavePix(BaseModel):
    chave: Optional[str] = None
    tipo: Optional[str] = None

class ContatoSchema(BaseModel):
    nome: str
    dados: DadosBancariosContatoSchema
    chave: BaseChavePix

    class Config:
        from_attributes = True

# Chave
class ChavePixSchema(BaseModel):
    chave: str
    tipo: str

    class Config:
        from_attributes = True

#Transferencia
class ConfirmacaoPagamentoSchema(BaseModel):
    valor: float
    recebedor: str
    contato_salvo: bool

#Sinalização
class Remetente(BaseModel):
    nome: str
    cpf: str
    agencia: Optional[str] = None
    conta: Optional[str] = None

class Recebedor(BaseModel):
    nome: str
    cpf: str
    agencia: Optional[str] = None
    conta: Optional[str] = None

class ComprovanteTransferenciaSchema(BaseModel):
    id_transferencia: str
    remetente: Remetente
    recebedor: Recebedor
    valor: float

class ComprovantePixSchema(BaseModel):
    id_transferencia: str
    remetente: Remetente
    recebedor: Recebedor
    chave: BaseChavePix
    valor: float


class ErrorResponseSchema(BaseModel):
    success: bool = False
    message: str
    data: Optional[Any] = None
    error_code: Optional[str] = "GENERIC_ERROR"

    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "message": "Saldo insuficiente para realizar a transação.",
                "data": None,
                "error_code": "INSUFFICIENT_FUNDS"
            }
        }