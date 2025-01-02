import { calculateExpiration } from './auth'

// 存储键名常量
export const STORAGE_KEYS = {
  TOKEN: 'token',
  REFRESH_TOKEN: 'refresh_token',
  USER_INFO: 'user_info',
  TOKEN_EXPIRES: 'token_expires',
  REMEMBER_ME: 'remember_me',
  REMEMBERED_PHONE: 'remembered_phone',
  ACCOUNT: 'account'
}

export const storage = {
  // 保存认证信息
  saveAuth({ access, refresh }, remember = false) {
    // 添加调试信息
    console.log('Storage saveAuth called with remember:', remember)
    
    const expiration = calculateExpiration(remember)
    console.log('Calculated expiration:', {
      remember,
      expiration,
      formattedTime: new Date(expiration * 1000).toLocaleString()
    })
    
    // 保存到 localStorage
    localStorage.setItem(STORAGE_KEYS.TOKEN, access)
    localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, refresh)
    localStorage.setItem(STORAGE_KEYS.TOKEN_EXPIRES, expiration.toString())
    
    if (remember) {
      localStorage.setItem(STORAGE_KEYS.REMEMBER_ME, 'true')
    } else {
      localStorage.removeItem(STORAGE_KEYS.REMEMBER_ME)
    }
  },

  // 获取认证信息
  getAuth() {
    const access = localStorage.getItem(STORAGE_KEYS.TOKEN)
    const refresh = localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN)
    const expiration = localStorage.getItem(STORAGE_KEYS.TOKEN_EXPIRES)
    const remember = localStorage.getItem(STORAGE_KEYS.REMEMBER_ME) === 'true'
    
    if (!access || !refresh || !expiration) return null
    
    return {
      access,
      refresh,
      expiration: parseInt(expiration) * 1000,
      remember
    }
  },

  // 清除认证信息
  clearAuth() {
    localStorage.removeItem(STORAGE_KEYS.TOKEN)
    localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN)
    localStorage.removeItem(STORAGE_KEYS.TOKEN_EXPIRES)
    localStorage.removeItem(STORAGE_KEYS.REMEMBER_ME)
    localStorage.removeItem(STORAGE_KEYS.REMEMBERED_PHONE)
    localStorage.removeItem(STORAGE_KEYS.USER_INFO)
  },

  // 保存账号
  saveAccount(account, remember = false) {
    if (remember) {
      localStorage.setItem(STORAGE_KEYS.ACCOUNT, account)
    } else {
      localStorage.removeItem(STORAGE_KEYS.ACCOUNT)
    }
  },

  // 获取保存的账号
  getSavedAccount() {
    return localStorage.getItem(STORAGE_KEYS.ACCOUNT)
  },

  // 获取记住的手机号
  getRememberedPhone() {
    return localStorage.getItem(STORAGE_KEYS.REMEMBERED_PHONE)
  }
}

// 导出清除认证存储的函数
export const clearAuthStorage = () => storage.clearAuth() 