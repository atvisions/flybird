import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

// API 路径常量
export const API_PATHS = {
  UPLOAD_AVATAR: '/api/v1/users/profile/avatar/upload/',
  PROFILE: '/api/v1/users/profile/',
  AUTH: {
    LOGIN: '/api/v1/users/auth/login/',
    REGISTER: '/api/v1/users/auth/register/',
    LOGOUT: '/api/v1/users/auth/logout/',
    REFRESH: '/api/v1/users/auth/token/refresh/',
    SMS: '/api/v1/users/auth/sms/send/'
  },
  ACCOUNT: {
    PASSWORD: '/api/v1/users/account/password/',
    PHONE: '/api/v1/users/account/phone/',
    DELETE: '/api/v1/users/account/delete/'
  }
}

// 创建 axios 实例
const request = axios.create({
  baseURL: process.env.VUE_APP_API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      router.push('/login')
    }
    ElMessage.error(error.response?.data?.message || '请求失败')
    return Promise.reject(error)
  }
)

export default request 