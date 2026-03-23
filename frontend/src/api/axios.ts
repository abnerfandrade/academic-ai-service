import axios from 'axios'
import { toast } from 'sonner'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status
    if (status === 500) {
      toast.error('Erro inesperado. Tente novamente.')
    } else if (status === 400) {
      toast.error(error.response?.data?.detail || 'Requisição inválida')
    } else if (status === 404) {
      window.history.back()
    }
    return Promise.reject(error)
  }
)

export default api
