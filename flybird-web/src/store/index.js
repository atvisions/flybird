import { createStore } from 'vuex'
import { authService } from '@/services/authService'
import { STORAGE_KEYS } from '@/utils/storage'
import profile from '@/api/profile'
import { auth } from '@/api/auth'
import request from '@/utils/request'
import router from '../router'
import { storage } from '@/utils/storage'
import { getExpirationInfo } from '@/utils/auth'
import defaultAvatar from '@/assets/images/default-avatar.png'

export default createStore({
  state: {
    isAuthenticated: false,
    userInfo: null,
    basicInfo: null,
    completeness: null,
    token: null,
    refreshToken: null
  },

  mutations: {
    SET_AUTH(state, isAuthenticated) {
      state.isAuthenticated = isAuthenticated
    },

    SET_USER_INFO(state, userInfo) {
      state.userInfo = userInfo
    },

    SET_BASIC_INFO(state, basicInfo) {
      state.basicInfo = {
        ...state.basicInfo,
        ...basicInfo
      }
    },

    SET_COMPLETENESS(state, completeness) {
      state.completeness = completeness
    },

    SET_AVATAR_UPDATE_TIME(state, timestamp) {
      state.avatarUpdateTime = timestamp
    },

    SET_TOKEN(state, token) {
      state.token = token
      state.isAuthenticated = !!token
    },

    SET_REFRESH_TOKEN(state, refreshToken) {
      state.refreshToken = refreshToken
    },

    SET_USER(state, user) {
      state.userInfo = user
    },

    SET_LOGGED_IN(state, status) {
      state.isAuthenticated = status
    },

    SET_AUTHENTICATED(state, isAuthenticated) {
      state.isAuthenticated = isAuthenticated
    },

    CLEAR_USER_INFO(state) {
      state.userInfo = null
    },

    CLEAR_BASIC_INFO(state) {
      state.basicInfo = null
    }
  },

  getters: {
    userAvatar: state => {
      return state.basicInfo?.avatar || defaultAvatar
    },

    userName: state => {
      return state.basicInfo?.name || state.userInfo?.username || '未设置昵称'
    },

    userNickname: state => {
      return state.userInfo?.username || '未设置昵称'
    },

    userPhone: state => {
      return state.basicInfo?.phone || state.userInfo?.phone
    },

    profileCompleteness: state => {
      return state.completeness || 0
    }
  },

  actions: {
    async checkAuth({ commit, dispatch }) {
      try {
        const token = localStorage.getItem(STORAGE_KEYS.TOKEN)
        if (!token) {
          return false
        }

        // 设置请求头
        request.defaults.headers.common['Authorization'] = `Bearer ${token}`
        
        // 尝试获取用户信息来验证 token 是否有效
        try {
          await dispatch('fetchUserInfo')
          commit('SET_LOGGED_IN', true)
          return true
        } catch (error) {
          if (error.response?.status === 401) {
            // token 无效，尝试刷新
            const refreshSuccess = await dispatch('refreshToken')
            if (refreshSuccess) {
              await dispatch('fetchUserInfo')
              commit('SET_LOGGED_IN', true)
              return true
            }
          }
          return false
        }
      } catch (error) {
        console.error('Auth check failed:', error)
        return false
      }
    },

    async fetchUserInfo({ commit }) {
      try {
        const response = await auth.getUserInfo()
        console.log('User info response:', response)
        
        if (response.data?.code === 200) {
          const { user, basic_info } = response.data.data
          if (user) {
            commit('SET_USER_INFO', {
              uid: user.uid,
              username: user.username,
              phone: user.phone
            })
          }
          if (basic_info) {
            commit('SET_BASIC_INFO', basic_info)
          }
          return response.data.data
        }
      } catch (error) {
        console.error('Failed to get user info:', error.response || error)
        throw error
      }
    },

    async updateBasicInfo({ commit }, { type, data }) {
      try {
        let response
        if (type === 'avatar') {
          response = await profile.uploadAvatar(data)
        } else if (type === 'basic') {
          response = await profile.updateBasicInfo(data)
        } else {
          throw new Error('未知的更新类型')
        }

        if (response?.data?.code === 200) {
          if (type === 'avatar') {
            commit('SET_AVATAR_UPDATE_TIME', Date.now())
          }
          const { user, basic_info } = response.data.data
          if (user) {
            commit('SET_USER_INFO', user)
          }
          if (basic_info) {
            commit('SET_BASIC_INFO', basic_info)
          }
          return response
        }
        throw new Error(response?.data?.message || '更新失败')
      } catch (error) {
        console.error('Failed to update basic info:', error)
        throw error
      }
    },

    async logout({ commit }) {
      try {
        await auth.logout()
      } catch (error) {
        console.error('Logout failed:', error)
      } finally {
        // 清理状态
        commit('SET_TOKEN', null)
        commit('SET_REFRESH_TOKEN', null)
        commit('SET_USER', null)
        commit('SET_LOGGED_IN', false)
        commit('CLEAR_USER_INFO')
        commit('CLEAR_BASIC_INFO')
        
        // 使用 storage 服务清除认证信息
        storage.clearAuth()
        
        // 清除请求头
        delete request.defaults.headers.common['Authorization']
        
        // 跳转到登录页
        router.push('/login')
      }
    },

    async fetchCompleteness({ commit }) {
      try {
        const response = await profile.getCompleteness()
        if (response.data?.code === 200) {
          commit('SET_COMPLETENESS', response.data.data)
        }
      } catch (error) {
        console.error('Failed to get completeness:', error)
      }
    },

    async login({ commit }, { access, refresh, rememberMe = false }) {
      try {
        // 添加调试信息
        console.log('Store login action called with rememberMe:', rememberMe)
        
        // 使用 storage 服务保存认证信息，它会处理过期时间
        storage.saveAuth({ access, refresh }, rememberMe)
        
        // 添加调试信息
        console.log('After storage.saveAuth:', {
          rememberMe,
          tokenInfo: getExpirationInfo(),
          savedRememberMe: localStorage.getItem(STORAGE_KEYS.REMEMBER_ME)
        })
        
        // 设置请求头
        request.defaults.headers.common['Authorization'] = `Bearer ${access}`
        
        // 更新 store 状态
        commit('SET_TOKEN', access)
        commit('SET_REFRESH_TOKEN', refresh)
        commit('SET_LOGGED_IN', true)

        // 获取用户信息
        try {
          const userInfoResponse = await this.dispatch('fetchUserInfo')
          if (userInfoResponse?.data?.user && rememberMe) {
            storage.savePhone(userInfoResponse.data.user.phone, true)
          }
        } catch (error) {
          console.warn('获取用户信息失败，但不影响登录状态:', error)
        }
      } catch (error) {
        console.error('登录失败:', error)
        throw error
      }
    },

    async refreshToken({ commit, state }) {
      try {
        const refreshToken = localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN)
        if (!refreshToken) {
          throw new Error('No refresh token')
        }

        const response = await auth.refreshToken({ refresh: refreshToken })
        
        if (response.data?.code === 200) {
          const { access } = response.data.data
          
          // 使用 storage 服务保存认证信息
          // 保持原有的记住我状态
          const rememberMe = localStorage.getItem(STORAGE_KEYS.REMEMBER_ME) === 'true'
          storage.saveAuth({ 
            access, 
            refresh: refreshToken  // 保持原有的 refresh token
          }, rememberMe)
          
          // 更新 store 状态
          commit('SET_TOKEN', access)
          
          return true
        }
        return false
      } catch (error) {
        console.error('Token refresh failed:', error)
        // 清除所有认证状态
        commit('SET_TOKEN', null)
        commit('SET_REFRESH_TOKEN', null)
        commit('SET_USER', null)
        commit('SET_LOGGED_IN', false)
        
        // 使用 storage 服务清除认证信息
        storage.clearAuth()
        
        return false
      }
    }
  }
})