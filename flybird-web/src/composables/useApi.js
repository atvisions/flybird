import axios from 'axios'

export function useApi() {
  const api = axios.create({
    baseURL: process.env.VUE_APP_API_URL || '/api',
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json'
    }
  })

  // 请求拦截器
  api.interceptors.request.use(
    config => {
      const token = localStorage.getItem('token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    },
    error => {
      return Promise.reject(error)
    }
  )

  // 响应拦截器
  api.interceptors.response.use(
    response => response,
    error => {
      if (error.response?.status === 401) {
        // 处理未授权错误
        localStorage.removeItem('token')
        window.location.href = '/login'
      }
      return Promise.reject(error)
    }
  )

  return api
} 