import axios from 'axios'
import { STORAGE_KEYS } from '@/utils/storage'

const request = axios.create({
  baseURL: 'http://192.168.3.16:8000',
  timeout: 5000,
  withCredentials: true
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem(STORAGE_KEYS.TOKEN)
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem(STORAGE_KEYS.TOKEN)
      delete request.defaults.headers.common['Authorization']
    }
    return Promise.reject(error)
  }
)

export default request