import axios from 'axios'
import router from '@/router'
import { STORAGE_KEYS } from '@/utils/storage'

const request = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL,
  timeout: 10000,
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem(STORAGE_KEYS.TOKEN)
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    // 如果是 FormData，让浏览器自动处理 Content-Type
    if (config.data instanceof FormData) {
      config.headers['Content-Type'] = undefined
      // 添加额外的 FormData 处理
      config.headers['Accept'] = 'application/json'
      // 防止 axios 处理 FormData
      if (!config.transformRequest) {
        config.transformRequest = [(data) => data]
      }
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
  response => {
    return response
  },
  async error => {
    console.error('Response error:', error)
    if (error.response) {
      console.error('Error details:', {
        status: error.response.status,
        data: error.response.data,
        config: {
          url: error.config.url,
          method: error.config.method,
          data: error.config.data instanceof FormData 
            ? '(FormData)' 
            : typeof error.config.data === 'string' 
              ? JSON.parse(error.config.data || '{}')
              : error.config.data || {},
          headers: error.config.headers
        }
      })
      console.error('Full response:', error.response)

      // 处理特定的错误情况
      if (error.response.status === 400) {
        // 检查是否是手机号被停用的错误
        const errorData = error.response.data
        if (errorData.code === 'phone_disabled' || 
            errorData.message?.includes('停用') || 
            errorData.message?.includes('限制')) {
          error.isPhoneDisabled = true
          error.friendlyMessage = '该手机号已被限制使用，请更换其他手机号'
        }
      }
    }

    if (error.response?.status === 401) {
      // 清除本地存储的认证信息
      localStorage.removeItem(STORAGE_KEYS.TOKEN)
      localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN)
      
      // 如果不是登录页面，则重定向到登录页
      if (!window.location.pathname.includes('/login')) {
        router.push('/login')
      }
    }
    return Promise.reject(error)
  }
)

export default request