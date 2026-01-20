export const validarSenha = (senha) => {
    if (senha.length < 8) {
        return { 
            valido: false, 
            mensagem: 'A senha deve ter no mínimo 8 caracteres.' 
        };
    }

    if (!/[A-Z]/.test(senha)) {
        return { 
            valido: false, 
            mensagem: 'A senha deve conter pelo menos uma letra maiúscula.' 
        };
    }

    if (!/[a-z]/.test(senha)) {
        return { 
            valido: false, 
            mensagem: 'A senha deve conter pelo menos uma letra minúscula.' 
        };
    }

    if (!/\d/.test(senha)) {
        return { 
            valido: false, 
            mensagem: 'A senha deve conter pelo menos um número.' 
        };
    }

    const especialRegex = /[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/;`~]/;
    if (!especialRegex.test(senha)) {
        return { 
            valido: false, 
            mensagem: 'A senha deve conter pelo menos um caractere especial (!@#$%^&*...).' 
        };
    }

    return { valido: true, mensagem: '' };
}