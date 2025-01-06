import { storage } from '@/utils/storage'
import { authManager } from '@/utils/auth'

export default {
  state: {
    isAuthenticated: false,
    userInfo: null
  },

  mutations: {
    SET_AUTH(state, isAuthenticated) {
      state.isAuthenticated = isAuthenticated
    },

    SET_USER_INFO(state, userInfo) {
      state.userInfo = userInfo
    }
  },

  actions: {
    async checkAuth({ commit }) {
      const isAuthenticated = authManager.isAuthenticated()
      commit('SET_AUTH', isAuthenticated)
      return isAuthenticated
    },

    async logout({ commit }) {
      try {
        // 先清除本地存储的认证信息
        commit('SET_TOKEN', null)
        commit('SET_USER', null)
        localStorage.removeItem('token')
        localStorage.removeItem('user')

        // 然后尝试发送退出请求，但不等待响应
        try {
          await api.post('/users/auth/logout/')
        } catch (error) {
          // 忽略退出请求的错误，因为用户已经退出
          console.log('Logout request failed, but user is already logged out locally')
        }

        // 返回成功
        return Promise.resolve()
      } catch (error) {
        return Promise.reject(error)
      }
    }
  }
} 