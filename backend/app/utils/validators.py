import re
from fastapi import HTTPException

def validar_senha_forte(senha: str):
    # 1. Validar Comprimento Mínimo
    if len(senha) < 8:
        raise HTTPException(
            status_code=400, 
            detail="A senha deve ter no mínimo 8 caracteres."
        )

    # 2. Validar Letra Maiúscula
    if not re.search(r"[A-Z]", senha):
        raise HTTPException(
            status_code=400, 
            detail="A senha deve conter pelo menos uma letra maiúscula."
        )

    # 3. Validar Letra Minúscula
    if not re.search(r"[a-z]", senha):
        raise HTTPException(
            status_code=400, 
            detail="A senha deve conter pelo menos uma letra minúscula."
        )

    # 4. Validar Números
    if not re.search(r"\d", senha):
        raise HTTPException(
            status_code=400, 
            detail="A senha deve conter pelo menos um número."
        )

    # 5. Validar Caracteres Especiais
    # Esta regex cobre os mesmos caracteres da sua função JS
    especial_regex = r"[!@#$%^&*(),.?\":{}|<>_\-+=\[\]\\\/;`~]"
    if not re.search(especial_regex, senha):
        raise HTTPException(
            status_code=400, 
            detail="A senha deve conter pelo menos um caractere especial (!@#$%^&*...)."
        )
    
    return True