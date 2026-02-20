/**
 * Formata uma string ou número para o padrão de CPF (###.###.###-##)
 * @param {string|number} cpf 
 * @returns {string} CPF formatado
 */
export const formatarCPF = (cpf) => {
  if (!cpf) return ''
  
  // Remove qualquer caractere que não seja número
  const apenasNumeros = cpf.toString().replace(/\D/g, '')

  // Aplica a máscara usando regex
  return apenasNumeros
    .replace(/(\d{3})(\d)/, '$1.$2')       // Ponto após o terceiro dígito
    .replace(/(\d{3})(\d)/, '$1.$2')       // Ponto após o sexto dígito
    .replace(/(\d{3})(\d{1,2})$/, '$1-$2') // Traço após o nono dígito
}