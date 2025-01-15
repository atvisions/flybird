import { defineStore } from 'pinia'

export const useSubscriptionStore = defineStore({
  id: 'subscription',
  state: () => ({
    subscriptionStatus: null,
    subscriptionEndDate: null,
    loading: false
  }),

  getters: {
    isSubscribed: (state) => {
      if (!state.subscriptionStatus) return false
      if (!state.subscriptionEndDate) return false
      return new Date(state.subscriptionEndDate) > new Date()
    }
  },

  actions: {
    async fetchSubscriptionStatus() {
      try {
        this.loading = true
        // TODO: 调用后端 API 获取会员状态
        // const response = await api.subscription.getStatus()
        // this.subscriptionStatus = response.data.status
        // this.subscriptionEndDate = response.data.endDate
      } catch (error) {
        console.error('获取会员状态失败:', error)
      } finally {
        this.loading = false
      }
    }
  }
}) 