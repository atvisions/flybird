import { createStore } from 'vuex'
import { getUserInfo } from '@/api/user' 
import { publicRequest } from '@/utils/request'
import router from '@/router'
import { showToast } from '@/components/ToastMessage'
import request from '@/utils/request'
import { auth } from '@/api/auth'

// Token 相关常量
const TOKEN_CONFIG = {
  // 有效期配置
  NORMAL_EXPIRATION_TIME: 2 * 60 * 60 * 1000,  // 普通登录时token有效期2小时
  REMEMBER_EXPIRATION_TIME: 7 * 24 * 60 * 60 * 1000,  // 记住我时token有效期7天
  REFRESH_INTERVAL: 20 * 60 * 1000,  // 刷新间隔20分钟
  REFRESH_THRESHOLD: 30 * 60 * 1000,  // 刷新阈值30分钟
  
  // 存储键名配置
  STORAGE_KEYS: {
    ACCESS_TOKEN: 'access_token',
    REFRESH_TOKEN: 'refresh_token',
    EXPIRATION: 'token_expiration',
    REMEMBER_ME: 'remember_me'
  }
}

let refreshInterval = null
let isRefreshingToken = false
let refreshSubscribers = []

// Token 刷新订阅机制
const addRefreshSubscriber = (callback) => {
  refreshSubscribers.push(callback)
}

const onTokenRefreshed = (token) => {
  refreshSubscribers.forEach(callback => callback(token))
  refreshSubscribers = []
}

/**
 * 短信验证码场
 * @enum {string}
 */
export const SMS_SCENE = {
  REGISTER: 'register',
  LOGIN: 'login',
  RESET_PASSWORD: 'reset_password',
  CHANGE_PHONE: 'change_phone',
  BIND_PHONE: 'bind_phone'
}

/**
 * Vuex Store 配置
 * @type {import('vuex').StoreOptions}
 */
export default createStore({
  state: {
    isAuthenticated: false,
    accessToken: null,
    refreshToken: null,
    tokenExpiration: null,
    userInfo: null  // 存储完整的用户信息响应
  },

  getters: {
    // 从统一的数据结构中获取信息
    getUserInfo: state => {
      return state.userInfo?.data?.data?.user || {}
    },
    getBasicInfo: state => {
      return state.userInfo?.data?.data?.basic_info || {}
    },
    getUserAvatar: state => {
      const avatar = state.userInfo?.data?.data?.basic_info?.avatar
      if (!avatar) return require('@/assets/images/default-avatar.png')
      return avatar.startsWith('http') ? avatar : `${process.env.VUE_APP_API_URL}${avatar}`
    },
    getUserPhone: state => state.userInfo?.data?.data?.user?.phone,
    getUserId: state => state.userInfo?.data?.data?.user?.uid
  },

  mutations: {
    SET_AUTH_DATA(state, { tokens, expiration }) {
      if (tokens) {
        state.accessToken = tokens.access
        state.refreshToken = tokens.refresh
        state.tokenExpiration = expiration
        state.isAuthenticated = true

        localStorage.setItem('access_token', tokens.access)
        localStorage.setItem('refresh_token', tokens.refresh)
        localStorage.setItem('token_expiration', expiration.toString())
      }
    },

    SET_USER_INFO(state, response) {
      try {
        // 直接保存完整的响应数据
        state.userInfo = response
      } catch (error) {
      }
    },

    CLEAR_AUTH(state) {
      state.isAuthenticated = false
      state.accessToken = null
      state.refreshToken = null
      state.tokenExpiration = null
      state.userInfo = null

      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('token_expiration')
    }
  },
  actions: {
    // 检查认证状态
    async checkAuth({ dispatch, commit }) {
      try {
        const token = localStorage.getItem('access_token')
        const refreshToken = localStorage.getItem('refresh_token')
        const expiration = localStorage.getItem('token_expiration')

        if (!token || !refreshToken || !expiration) {
          commit('CLEAR_AUTH')
          return false
        }

        const now = Date.now()
        const expirationTime = parseInt(expiration)
        const timeToExpire = expirationTime - now

        if (timeToExpire > TOKEN_CONFIG.REFRESH_THRESHOLD) {
          // 恢复认证状态
          commit('SET_AUTH_DATA', {
            tokens: { access: token, refresh: refreshToken },
            expiration: expirationTime
          })

          // 获取最新用户信息
          try {
            const response = await auth.getUserInfo()
            if (response.data?.code === 200) {
              commit('SET_USER_INFO', response)
            }
          } catch (error) {
          }

          return true
        }

        // token 即将过期，尝试刷新
        try {
          const newToken = await dispatch('refreshToken')
          if (newToken) {
            const response = await auth.getUserInfo()
            if (response.data?.code === 200) {
              commit('SET_USER_INFO', response)
            }
            return true
          }
        } catch (error) {
        }

        commit('CLEAR_AUTH')
        return false
      } catch (error) {
        commit('CLEAR_AUTH')
        return false
      }
    },

    // 登录
    async login({ commit }, { token, user }) {
      try {
        commit('SET_AUTH_DATA', {
          tokens: { 
            access: token.access,
            refresh: token.refresh 
          },
          expiration: new Date().getTime() + TOKEN_CONFIG.NORMAL_EXPIRATION_TIME
        })

        const response = await auth.getUserInfo()
        if (response.data?.code === 200) {
          commit('SET_USER_INFO', response)
        }

        return true
      } catch (error) {
        commit('CLEAR_AUTH')
        throw error
      }
    },

    // 登出
    async logout({ commit }) {
      try {
        await auth.logout()
      } finally {
        commit('CLEAR_AUTH')
        router.push('/login')
      }
    },

    // 获取用户信息
    async fetchUserInfo({ commit }) {
      try {
        const response = await auth.getUserInfo()
        if (response.data?.code === 200) {
          commit('SET_USER_INFO', response)
          return response.data.data
        }
      } catch (error) {
        throw error
      }
    }
  }
})