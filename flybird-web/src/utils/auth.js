import { auth } from '@/api/auth'
import { storage } from './storage'
import { STORAGE_KEYS } from '@/constants'

export const authManager = {
  // 检查是否已登录
  isAuthenticated() {
    const authData = storage.getAuth()
    if (!authData) return false
    
    // 修改为毫秒级比较，因为 storage.getAuth 已经返回毫秒级时间戳
    return authData.expiration > Date.now()
  },

  // 获取当前token
  getToken() {
    const authData = storage.getAuth()
    return authData?.access
  },

  // 获取刷新token
  getRefreshToken() {
    const authData = storage.getAuth()
    return authData?.refresh
  },

  // 处理登录
  async login(credentials, remember = false) {
    const response = await auth.loginWithPassword(credentials)
    
    if (response.data?.code === 200) {
      const { access, refresh } = response.data.data
      storage.saveAuth({ access, refresh }, remember)
      if (remember) {
        storage.savePhone(credentials.phone, true)
      }
    }
    
    return response
  },

  // 处理登出
  async logout() {
    try {
      await auth.logout()
    } finally {
      storage.clearAuth()
    }
  }
}

// 检查 token 是否过期
export const isTokenExpired = () => {
  const expiresAt = localStorage.getItem(STORAGE_KEYS.TOKEN_EXPIRES)
  if (!expiresAt) return true
  
  // 将存储的秒级时间戳转换为毫秒级进行比较
  const expirationTime = parseInt(expiresAt) * 1000
  return Date.now() >= expirationTime
}

// 格式化过期时间
export const formatExpireTime = (timestamp) => {
  // 将秒级时间戳转换为毫秒级再格式化
  return new Date(timestamp * 1000).toLocaleString()
}

// 获取当前时间戳（秒）
export const getCurrentTimestamp = () => {
  return Math.floor(Date.now() / 1000)
}

// 计算过期时间（秒）
export const calculateExpiration = (remember = false) => {
  // 添加调试信息
  console.log('Calculating expiration with remember:', remember)
  
  const now = getCurrentTimestamp()
  const expiresIn = remember ? 
    7 * 24 * 60 * 60 :  // 7天（秒）
    24 * 60 * 60        // 24小时（秒）
  
  const expiration = now + expiresIn
  console.log('Expiration calculation:', {
    remember,
    now,
    expiresIn,
    expiration,
    formattedExpiration: new Date(expiration * 1000).toLocaleString()
  })
  
  return expiration
}

// 添加一个辅助函数用于调试
export const getExpirationInfo = () => {
  const expiresAt = localStorage.getItem(STORAGE_KEYS.TOKEN_EXPIRES)
  if (!expiresAt) return null
  
  const expirationTime = parseInt(expiresAt) * 1000
  return {
    expiresAt,
    expirationTime,
    formattedTime: new Date(expirationTime).toLocaleString(),
    now: Date.now(),
    formattedNow: new Date().toLocaleString(),
    isExpired: Date.now() >= expirationTime
  }
} 