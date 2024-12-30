import axios from 'axios'

// 创建 axios 实例
const request = axios.create({
  baseURL: process.env.VUE_APP_API_URL,
  timeout: 15000,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    // 如果有 token，添加到 headers 中
    const token = localStorage.getItem('access_token')
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
request.interceptors.response.use(
  response => {
    return response
  },
  async error => {
    return Promise.reject(error)
  }
)

export default request