import axios from 'axios'
import router from '../router'

const api = axios.create({
    baseURL: 'http://localhost:8000',
    withCredentials: true,
    headers: {
      'Content-Type': 'application/json'
    },
    timeout: 60000,
})

// Estado para gerenciar refresh
let isRefreshing = false
let failedQueue = []

// Função para processar fila de requisições pendentes
const processQueue = (error) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve()
    }
  })
  failedQueue = []
}

// Rotas que não devem tentar refresh
const AUTH_ROUTES = ['/auth/login', '/auth/refresh', '/auth/logout', '/auth/register']

const isAuthRoute = (url) => {
  return AUTH_ROUTES.some(route => url?.includes(route))
}

// Interceptor de REQUISIÇÃO
api.interceptors.request.use(
  (config) => {
    // Garante que withCredentials está sempre true
    config.withCredentials = true
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor de RESPOSTA
api.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config

    // Ignora erros que não são 401
    if (error.response?.status !== 401) {
      return Promise.reject(error)
    }

    // Se for 401 em rotas de autenticação, redireciona direto
    if (isAuthRoute(originalRequest.url)) {  
      // Limpa estado de refresh para evitar loop
      isRefreshing = false
      processQueue(error)
      
      router.push('/login')
      return Promise.reject(error)
    }

    // Se já tentou fazer retry, não tenta novamente
    if (originalRequest._retry) {
      // Limpa estado de refresh para evitar loop
      isRefreshing = false
      processQueue(error)
      
      router.push('/login')
      return Promise.reject(error)
    }

    // Se já está renovando, adiciona à fila de espera
    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        failedQueue.push({ resolve, reject })
      })
        .then(() => {
          return api(originalRequest)
        })
        .catch((err) => {
          return Promise.reject(err)
        })
    }

    // Inicia processo de refresh
    originalRequest._retry = true // Marca APENAS a requisição original
    isRefreshing = true

    try {
      // Tenta renovar o token (usando rota correta do seu backend)
      await api.post('/auth/refresh')
      
      // Processa todas as requisições que estavam esperando
      processQueue(null)
      
      // Reseta flag
      isRefreshing = false
      
      // Retenta a requisição original
      return api(originalRequest)
      
    } catch (refreshError) {
      // CRÍTICO: Limpa tudo antes de redirecionar
      processQueue(refreshError)
      isRefreshing = false
      
      // Redireciona para login
      router.push('/login')
      
      return Promise.reject(refreshError)
    }
  }
)

export default api