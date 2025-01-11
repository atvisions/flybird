import { createStore } from 'vuex'

export default createStore({
  state: {
    isAuthenticated: false,
    userInfo: null,
  },
  mutations: {
    SET_AUTH_STATUS(state, status) {
      state.isAuthenticated = status
    },
    SET_USER_INFO(state, info) {
      state.userInfo = info
    }
  },
  actions: {
    // 会员相关的 actions
    async createOrder({ commit }, orderData) {
      try {
        const response = await membership.createOrder(orderData)
        return response.data
      } catch (error) {
        throw error
      }
    }
  }
}) 