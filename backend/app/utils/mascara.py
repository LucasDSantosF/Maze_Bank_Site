def mascarar_cpf(cpf: str):
    if not cpf: return None
    return f"***.{cpf[3:6]}.{cpf[6:9]}-**"