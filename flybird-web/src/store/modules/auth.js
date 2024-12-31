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
        await authManager.logout()
      } finally {
        storage.clearAuth()
        commit('SET_AUTH', false)
        commit('SET_USER_INFO', null)
      }
    }
  }
} 