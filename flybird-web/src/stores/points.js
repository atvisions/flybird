import { defineStore } from 'pinia'
import { useAuthStore } from '@/stores/auth'

export const usePointsStore = defineStore('points', {
  state: () => ({
    points: 0,
    lastCheckInTime: null,
    // ... 其他状态
  }),

  actions: {
    async getPointsInfo() {
      // 检查认证状态
      const authStore = useAuthStore()
      if (!authStore.isAuthenticated) {
        return null
      }

      try {
        const response = await points.getPointsInfo()
        if (response?.data?.code === 200) {
          this.points = response.data.data.points
          this.lastCheckInTime = response.data.data.last_check_in_time
          return response.data.data
        }
        return null
      } catch (error) {
        console.warn('获取积分信息失败:', error)
        // 非致命错误，返回 null
        return null
      }
    },

    // ... 其他 actions
  }
}) 