from fastapi import APIRouter, Depends

from models import models
from api.auth import get_current_user
from schema.response import BaseResponse, UsuarioSchema, ErrorResponseSchema

router = APIRouter(prefix="/user", tags=["User Profile"])

@router.get(
    "/me",
    response_model=BaseResponse[UsuarioSchema],
    responses={401: {"model": ErrorResponseSchema}}
)
def obter_meu_perfil(usuario_atual: models.Usuario = Depends(get_current_user)):
    data = {
        "nome": usuario_atual.nome,
        "sobrenome": usuario_atual.sobrenome,
        "email": usuario_atual.email,
        "cpf": usuario_atual.cpf,
        "detalhes_bancarios": {
            "agencia": usuario_atual.agencia,
            "conta": usuario_atual.numero_conta,
            "saldo": usuario_atual.saldo
        },
        "membro_desde": usuario_atual.data_criacao
    }

    return {
        "success": True,
        "message": "Perfil carregado com sucesso",
        "data": data
    }