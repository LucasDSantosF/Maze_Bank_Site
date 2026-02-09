import api from '../axios'
import router from '../../router'


export const auth = {

     login: async (credentials) => {
        try {
            const response = await api.post('/auth/login', credentials)
            return response
        } catch (error) {
            throw error
        };
    },

    registrar: async (credentials) => {
        try {
            const response = await api.post('/auth/register', credentials)
            return response
        } catch (error) {
            throw error
        }
    },

    usuario: async () => {
        try {
            const response = await api.get('/user/me');
            return response.data
        } catch (error) {
            throw error
        }
    },

    logout: async () => {
        try {
            await api.post('/auth/logout')
        } finally {
            router.push('/login')
        }
    },

    checkAuth: async () => {
        try {
            const response = await api.get('/user/me');
            if (response.status === 204) {
                return false
            } else {
                return true
            }
        } catch (error) {
            return false
        }
    }
}

export const pix = {

    resumo: async () => {
        try {
            const response = await api.get('/extrato/resumo/pix')
            return response.data
        } catch (error) {
            throw error
        };
    },

    chaves: async () => {
        try {
            const response = await api.get('/pix/chaves')
            return response.data
        } catch (error) {
            throw error
        };
    },

    chave: async (payload) => {
        try {
            const response = await api.post('/pix/chave', payload)
            return response.data
        } catch (error) {
            throw error
        };
    },

    excluir: async (payload) => {
        try {
            const response = await api.delete('/pix/chave/excluir', { data: payload })
            return response.data
        } catch (error) {
            throw error
        };
    },
}

export const transactions = {
    deposito: async (payload) => {
        try {
            const response = await api.post('/transaction/deposit', payload)
            return response.data
        } catch (error) {
            throw error
        };
    },

    saque: async (payload) => {
        try {
            const response = await api.post('/transaction/withdraw', payload)
            return response.data
        } catch (error) {
            throw error
        };
    },

    ted: async (payload) => {
        try {
            const response = await api.post('/transaction/sinalizar/dados', payload)
            return response.data
        } catch (error) {
            throw error
        };
    },

    pix: async (payload) => {
        try {
            const response = await api.post('/transaction/sinalizar/pix', payload)
            return response.data
        } catch (error) {
            throw error
        };
    },

    confirmar: async (payload) => {
        try {
            const response = await api.post('/transaction/confirmar', payload)
            return response.data
        } catch (error) {
            throw error
        };
    },


    contatos: async () => {
        try {
            const response = await api.get('/contatos/')
            return response.data
        } catch (error) {
            throw error
        };
    },

    extrato: async (filtros = {}) => {
        try {
            const response = await api.get('/extrato', { params: filtros  });
            return response.data
        } catch (error) {
            throw error
        };
    },

    resumo: async () => {
        try {
            const response = await api.get('/extrato/resumo')
            return response.data
        } catch (error) {
            throw error
        };
    },
}