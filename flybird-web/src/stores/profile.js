import { defineStore } from 'pinia'
import profile from '@/api/profile'

export const useProfileStore = defineStore('profile', {
  state: () => ({
    profileData: null,
    loading: false,
    error: null
  }),

  actions: {
    // 获取档案数据
    async loadProfileData() {
      try {
        this.loading = true
        const response = await profile.getData()
        if (response.data.code === 200) {
          this.profileData = response.data.data
        } else {
          throw new Error(response.data.message || '获取档案数据失败')
        }
      } catch (error) {
        console.error('获取档案数据失败:', error)
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    // 清除状态
    clearState() {
      this.profileData = null
      this.loading = false
      this.error = null
    }
  }
}) 