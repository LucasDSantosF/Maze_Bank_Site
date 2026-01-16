export const validarSenha = (senha) => {
    // 1. Validar Comprimento Mínimo
    if (senha.length < 8) {
        return { 
            valido: false, 
            mensagem: 'A senha deve ter no mínimo 8 caracteres.' 
        };
    }

    // 2. Validar Letra Maiúscula
    // Procuramos por qualquer caractere entre A e Z
    if (!/[A-Z]/.test(senha)) {
        return { 
            valido: false, 
            mensagem: 'A senha deve conter pelo menos uma letra maiúscula.' 
        };
    }

    // 3. Validar Letra Minúscula
    // Procuramos por qualquer caractere entre a e z
    if (!/[a-z]/.test(senha)) {
        return { 
            valido: false, 
            mensagem: 'A senha deve conter pelo menos uma letra minúscula.' 
        };
    }

    // 4. Validar Números
    // \d é o atalho para dígitos (0-9)
    if (!/\d/.test(senha)) {
        return { 
            valido: false, 
            mensagem: 'A senha deve conter pelo menos um número.' 
        };
    }

    // 5. Validar Caracteres Especiais
    // Usamos a lista exata que você definiu no seu código Python
    // Nota: Escapamos caracteres que podem quebrar a string no JS (\ e /)
    const especialRegex = /[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/;`~]/;
    if (!especialRegex.test(senha)) {
        return { 
            valido: false, 
            mensagem: 'A senha deve conter pelo menos um caractere especial (!@#$%^&*...).' 
        };
    }

    // Se passou por todos os IFs, a senha é válida
    return { valido: true, mensagem: '' };
}