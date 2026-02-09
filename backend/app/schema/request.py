from pydantic import BaseModel, EmailStr

class Usuario(BaseModel):
    nome: str
    sobrenome: str
    cpf: str
    email: EmailStr
    senha: str

class Login(BaseModel):
    cpf: str
    senha: str

class Money(BaseModel):
    valor: int

class TED(BaseModel):
    valor: int 
    agencia: str
    conta: str

class Pix(BaseModel):
    valor: int
    chave: str
    tipo_chave: str

class Confirmar(BaseModel):
    id_transferencia: str

class Chave(BaseModel):
    valor: str
    tipo: str

class ChaveExcluir(BaseModel):
    valor: str