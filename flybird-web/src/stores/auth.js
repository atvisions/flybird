import { defineStore } from 'pinia'
import { auth } from '@/api/auth'
import request from '@/utils/request'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/account'
import { useUserStore } from '@/stores/user'
import { showToast } from '@/components/ToastMessage'
import { STORAGE_KEYS } from '@/utils/storage'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLoggedIn: false,
    rememberMe: false,
    token: localStorage.getItem('token') || null,
    refreshToken: null,
    tokenExpiresAt: null
  }),

  getters: {
    // 添加 getter，替代直接访问 isLoggedIn
    isAuthenticated: (state) => {
      const isValid = state.isLoggedIn && !!state.token && !state.isTokenExpired()
      return isValid
    },
    
    // 获取记住的账号
    rememberedAccount: () => localStorage.getItem('remembered_account'),
    
    // 获取当前 token
    currentToken: (state) => state.token,
    
    // 检查是否需要刷新 token
    needsTokenRefresh: (state) => {
      if (!state.tokenExpiresAt) return false
      // 如果 token 将在 5 分钟内过期，就需要刷新
      const fiveMinutes = 5 * 60 * 1000
      return new Date().getTime() + fiveMinutes > state.tokenExpiresAt
    }
  },

  actions: {
    async login(credentials, rememberMe = false) {
      try {
        console.log('Login attempt with:', { account: credentials.account, rememberMe })
        const response = await auth.loginWithPassword(credentials)
        console.log('Login response:', response)
        
        if (response) {
          // 保存 token
          this.token = response.token
          this.refreshToken = response.refresh
          localStorage.setItem('token', response.token)
          localStorage.setItem('refresh_token', response.refresh)
          
          // 设置请求头
          request.defaults.headers.common['Authorization'] = `Bearer ${response.token}`
          
          // 设置登录状态
          this.isLoggedIn = true
          
          // 登录成功后立即获取用户信息并存储
          const accountStore = useAccountStore()
          console.log('Fetching user info after login...')
          await accountStore.fetchUserInfo()
          
          console.log('User info fetched:', accountStore.userInfo)
          
          // 记住账号功能
          if (rememberMe) {
            localStorage.setItem('remember_me', 'true')
            localStorage.setItem('remembered_account', credentials.account)
          }
          
          // 显示登录成功提示
          showToast('登录成功', 'success')
          
          // 获取重定向地址
          const urlParams = new URLSearchParams(window.location.search)
          const redirect = urlParams.get('redirect')
          
          // 如果有重定向地址，则跳转到重定向地址，否则跳转到用户中心
          window.location.href = redirect || '/user?tab=home'
          
          return true
        }
        return false
      } catch (error) {
        console.error('Login failed:', error)
        
        // 更详细的错误处理
        if (error.response?.status === 401) {
          throw new Error('账号或密码错误')
        } else if (error.response?.status === 429) {
          throw new Error('登录尝试次数过多，请稍后再试')
        } else if (error.response?.data?.message) {
          throw new Error(error.response.data.message)
        } else {
          throw new Error('登录失败，请稍后重试')
        }
      }
    },

    async logout() {
      try {
        // 清除所有 localStorage - 移到最前面
        localStorage.clear()
        
        if (this.refreshToken) {
          try {
            await auth.logout()
          } catch (error) {
            console.error('Logout API error:', error)
            // 即使 API 调用失败，继续清理本地状态
          }
        }
        
        // 清除 store 状态
        this.clearAuth()
        const accountStore = useAccountStore()
        const userStore = useUserStore()
        accountStore.clearUserInfo()
        userStore.clearUserInfo()
        
        // 清除请求头中的 token
        delete request.defaults.headers.common['Authorization']
        
        // 使用 window.location 强制跳转
        window.location.href = '/login'
        
        showToast('已退出登录', 'success')
      } catch (error) {
        console.error('Logout failed:', error)
        showToast('退出登录失败，请重试', 'error')
      }
    },

    clearAuth() {
      // 清除请求头
      delete request.defaults.headers.common['Authorization']
      
      // 重置状态
      this.isLoggedIn = false
      this.token = null
      this.refreshToken = null
      this.tokenExpiresAt = null
      this.rememberMe = false
      
      // 确保清除所有认证相关的本地存储
      Object.values(STORAGE_KEYS).forEach(key => {
        localStorage.removeItem(key)
      })
    },

    // 检查 token 是否过期
    isTokenExpired() {
      // 如果没有设置过期时间，默认认为 token 有效
      if (!this.tokenExpiresAt) return false
      const now = new Date().getTime()
      const isExpired = now > this.tokenExpiresAt
      console.log('Token expiry check:', {
        now,
        expiresAt: this.tokenExpiresAt,
        isExpired
      })
      return isExpired
    },

    // 从 localStorage 恢复认证状态
    restoreAuth() {
      const token = localStorage.getItem('token')
      const refreshToken = localStorage.getItem('refresh_token')
      const tokenExpiresAt = localStorage.getItem('token_expires_at')
      const rememberMe = localStorage.getItem('remember_me') === 'true'


      if (token && refreshToken) {
        this.token = token
        this.refreshToken = refreshToken
        this.tokenExpiresAt = tokenExpiresAt ? parseInt(tokenExpiresAt) : null
        this.rememberMe = rememberMe
        this.isLoggedIn = true
        
        // 设置请求头
        request.defaults.headers.common['Authorization'] = `Bearer ${token}`
        return true
      } else {
        console.log('Auth restore failed: No token found')
        return false
      }
    },

    async register(data) {
      try {
        const response = await auth.register(data)
        
        if (response?.data?.code === 200) {
          const userData = response.data.data
          // 保存 token
          this.token = userData.access
          this.refreshToken = userData.refresh
          localStorage.setItem('token', userData.access)
          localStorage.setItem('refresh_token', userData.refresh)
          localStorage.setItem('isLoggedIn', 'true')
          
          // 设置请求头
          request.defaults.headers.common['Authorization'] = `Bearer ${userData.access}`
          
          // 设置登录状态
          this.isLoggedIn = true
          
          // 初始化用户数据
          const accountStore = useAccountStore()
          accountStore.userInfo = {
            id: userData.id,
            uid: userData.uid,
            username: userData.username || `FB${userData.uid}`,
            phone: userData.phone,
            email: null,
            avatar: null,
            position: null,
            bio: null,
            is_vip: false,
            is_staff: false,
            background_image: null
          }
          
          // 保存到本地存储
          localStorage.setItem('userInfo', JSON.stringify(accountStore.userInfo))
          
          showToast('注册成功', 'success')
          
          // 跳转到用户中心
          window.location.replace('/user?tab=home')
          
          return true
        }
        return false
      } catch (error) {
        console.error('Registration failed:', error)
        this.clearAuth()
        const accountStore = useAccountStore()
        accountStore.clearUserInfo()
        showToast(error.message || '注册失败，请稍后重试', 'error')
        throw error
      }
    },

    async refreshAuthToken() {
      try {
        if (!this.refreshToken) {
          throw new Error('No refresh token available')
        }

        const response = await auth.refreshToken(this.refreshToken)
        
        if (response?.token) {
          this.token = response.token
          localStorage.setItem('token', response.token)
          request.defaults.headers.common['Authorization'] = `Bearer ${response.token}`
          
          // 更新过期时间
          if (response.expires_in) {
            this.tokenExpiresAt = new Date().getTime() + (response.expires_in * 1000)
            localStorage.setItem('token_expires_at', this.tokenExpiresAt.toString())
          }
          
          return true
        }
        return false
      } catch (error) {
        console.error('Token refresh failed:', error)
        // 如果刷新失败，清除认证状态并重定向到登录页
        this.clearAuth()
        window.location.href = `/login?redirect=${encodeURIComponent(window.location.pathname)}`
        throw error
      }
    },

    async initialize() {
      const restored = this.restoreAuth()
      
      if (restored) {
        // 如果已登录，获取用户信息
        try {
          const accountStore = useAccountStore()
          await accountStore.fetchUserInfo()
        } catch (error) {
          console.error('Failed to fetch user info during initialization:', error)
          // 如果获取用户信息失败，可能是 token 已失效
          this.clearAuth()
        }
      }

    }
  }
}) 