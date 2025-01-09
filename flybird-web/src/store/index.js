import { createStore } from 'vuex'
import { STORAGE_KEYS } from '@/utils/storage'
import profile from '@/api/profile'
import { auth } from '@/api/auth'
import request from '@/utils/request'
import router from '../router'
import { storage } from '@/utils/storage'
import { getExpirationInfo } from '@/utils/auth'
import defaultAvatar from '@/assets/images/default-avatar.png'
import user from '@/api/user'

export default createStore({
  state: {
    isAuthenticated: false,
    userInfo: null,
    basicInfo: null,
    completeness: null,
    token: null,
    refreshToken: null,
    isLoadingUserInfo: false,
    lastUserInfoFetch: null
  },

  mutations: {
    SET_AUTH(state, isAuthenticated) {
      state.isAuthenticated = isAuthenticated
    },

    SET_USER_INFO(state, userInfo) {
      // 深度合并更新
      if (state.userInfo) {
        state.userInfo = {
          ...state.userInfo,
          code: userInfo.code,
          message: userInfo.message,
          data: {
            ...state.userInfo.data,
            user: {
              ...state.userInfo.data?.user,
              ...userInfo.data?.user
            },
            ...userInfo.data
          }
        }
      } else {
        state.userInfo = userInfo
      }
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
    },

    UPDATE_BASIC_INFO(state, basicInfo) {
      if (state.userInfo?.data) {
        state.userInfo.data.basic_info = {
          ...state.userInfo.data.basic_info,
          ...basicInfo
        }
      }
    },

    UPDATE_AVATAR(state, avatarUrl) {
      if (state.userInfo?.data?.basic_info) {
        state.userInfo.data.basic_info.avatar = avatarUrl
      }
    },

    UPDATE_BACKGROUND(state, backgroundUrl) {
      if (state.userInfo?.data?.basic_info) {
        state.userInfo.data.basic_info.background = backgroundUrl
      }
    },

    SET_LOADING_USER_INFO(state, isLoading) {
      state.isLoadingUserInfo = isLoading
    },

    SET_LAST_USER_INFO_FETCH(state, timestamp) {
      state.lastUserInfoFetch = timestamp
    }
  },

  getters: {
    userAvatar: state => {
      return state.userInfo?.data?.basic_info?.avatar || defaultAvatar
    },

    userName: state => {
      return state.userInfo?.data?.basic_info?.nickname || '未设置昵称'
    },

    userNickname: state => {
      return state.userInfo?.data?.basic_info?.nickname || '未设置昵称'
    },

    userPhone: state => {
      return state.userInfo?.data?.basic_info?.phone
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

    async fetchUserInfo({ commit, state }) {
      // 如果正在加载，返回
      if (state.isLoadingUserInfo) {
        return
      }
      
      // 如果数据已经存在且在5分钟内获取过，直接返回
      const now = Date.now()
      if (state.userInfo && state.lastUserInfoFetch && 
          (now - state.lastUserInfoFetch) < 5 * 60 * 1000) {
        return state.userInfo
      }

      try {
        commit('SET_LOADING_USER_INFO', true)
        const response = await auth.getUserInfo()
        
        if (response.code === 200) {
          commit('SET_USER_INFO', response)
          commit('SET_LAST_USER_INFO_FETCH', now)
          return response.data
        }
      } catch (error) {
        console.error('获取用户信息失败:', error)
        throw error
      } finally {
        commit('SET_LOADING_USER_INFO', false)
      }
    },

    async updateBasicInfo({ commit }, { type, data }) {
      try {
        let response
        if (type === 'avatar') {
          response = await profile.uploadAvatar(data)
        } else if (type === 'background') {
          response = await profile.uploadBackground(data)
        } else if (type === 'basic') {
          response = await profile.updateModule('basic_info', data)
        } else {
          throw new Error('未知的更新类型')
        }

        if (response?.data?.code === 200) {
          if (type === 'avatar' || type === 'background') {
            commit('SET_AVATAR_UPDATE_TIME', Date.now())
          }
          if (type === 'basic') {
            commit('UPDATE_BASIC_INFO', response.data.data)
          } else {
            const { user, basic_info } = response.data.data
            if (user) {
              commit('SET_USER_INFO', user)
            }
            if (basic_info) {
              commit('SET_BASIC_INFO', basic_info)
            }
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
          commit('SET_COMPLETENESS', response.data)
          return response.data
        }
      } catch (error) {
        console.error('获取完整度失败:', error)
      }
    },

    async login({ commit }, { access, refresh, rememberMe = false }) {
      try {
        // 使用 storage 服务保存认证信息，它会处理过期时间
        storage.saveAuth({ access, refresh }, rememberMe)
        
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
    },

    async updateAvatar({ commit }, formData) {
      try {
        const response = await profile.uploadAvatar(formData)
        if (response.data?.code === 200) {
          const avatarUrl = response.data.data.avatar
          commit('UPDATE_AVATAR', avatarUrl)
          return avatarUrl
        }
        throw new Error(response.data?.message || '更新头像失败')
      } catch (error) {
        console.error('Failed to update avatar:', error)
        throw error
      }
    },

    async updateBackground({ commit }, formData) {
      try {
        const response = await profile.uploadBackground(formData)
        if (response.data?.code === 200) {
          const backgroundUrl = response.data.data.background
          commit('UPDATE_BACKGROUND', backgroundUrl)
          return backgroundUrl
        }
        throw new Error(response.data?.message || '更新背景图失败')
      } catch (error) {
        console.error('Failed to update background:', error)
        throw error
      }
    },

    async getUserInfo({ commit }) {
      try {
        const response = await user.getUserInfo()
        if (response.data?.code === 200) {
          commit('SET_USER_INFO', response.data)
        }
        return response
      } catch (error) {
        console.error('获取用户信息失败:', error)
        throw error
      }
    }
  }
})