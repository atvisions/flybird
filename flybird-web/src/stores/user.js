import { defineStore } from 'pinia'
import request from '@/utils/request'
import { showToast } from '@/components/ToastMessage'

export const useUserStore = defineStore('user', {
  state: () => ({
    userInfo: null,
    loading: false,
    error: null
  }),

  getters: {
    userBasicInfo: (state) => state.userInfo,
    username: (state) => state.userInfo?.username,
    avatar: (state) => state.userInfo?.avatar,
    isLoading: (state) => state.loading,
    hasError: (state) => state.error !== null
  },

  actions: {
    async getUserInfo() {
      try {
        this.loading = true
        this.error = null
        
        const response = await request.get('/api/v1/users/userInfo/')
        
        if (response?.data?.code === 200) {
          this.userInfo = response.data.data
          return this.userInfo
        }
        
        throw new Error(response?.data?.message || '获取用户信息失败')
      } catch (error) {
        console.error('获取用户信息失败:', error)
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    clearUserInfo() {
      this.userInfo = null
      this.loading = false
      this.error = null
    },

    setUserInfo(info) {
      this.userInfo = info
    }
  }
}) 