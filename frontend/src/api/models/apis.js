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