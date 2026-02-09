from fastapi import APIRouter, Depends

from api.auth import get_current_user
from models import models
from schema.response import BaseResponse, ContatoSchema, ErrorResponseSchema

router = APIRouter(prefix="/contatos", tags=["Agenda de Contatos"])

@router.get(
    "/",
    response_model=BaseResponse[list[ContatoSchema]],
    responses={401: {"model": ErrorResponseSchema}}
)
def listar_contatos(user: models.Usuario = Depends(get_current_user)):
    contatos_formatados = [
        {
            "nome": c.nome,
            "dados": {
                "agencia": c.agencia,
                "conta": c.conta,
                "cpf": f"***.{c.cpf[3:6]}.***-**"
            },
            "chave": {
                "chave": c.chave_pix, 
                "tipo": c.tipo_chave_pix

            },
        }
        for c in user.contatos
    ]

    return {
        "success": True,
        "message": "Contatos recuperados com sucesso",
        "data": contatos_formatados
    }