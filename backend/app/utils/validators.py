import re
from fastapi import HTTPException, status

def validar_senha_forte(senha: str):
    if len(senha) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "A senha deve ter no mínimo 8 caracteres.", "error_code": "BAD_REQUEST"}
        )

    if not re.search(r"[A-Z]", senha):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "A senha deve conter pelo menos uma letra maiúscula.", "error_code": "BAD_REQUEST"}
        )

    if not re.search(r"[a-z]", senha):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "A senha deve conter pelo menos uma letra minúscula.", "error_code": "BAD_REQUEST"}
        )

    if not re.search(r"\d", senha):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "A senha deve conter pelo menos um número.", "error_code": "BAD_REQUEST"}
        )

    especial_regex = r"[!@#$%^&*(),.?\":{}|<>_\-+=\[\]\\\/;`~]"
    if not re.search(especial_regex, senha):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "A senha deve conter pelo menos um caractere especial (!@#$%^&*...).", "error_code": "BAD_REQUEST"}
        )
    
    return True