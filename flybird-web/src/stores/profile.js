import { defineStore } from 'pinia'
import profile from '@/api/profile'
import { eventBus } from '@/utils/eventBus'

export const useProfileStore = defineStore({
  id: 'profile',
  state: () => ({
    basicInfo: null,
    avatarUpdateTime: null
  }),

  getters: {
    profileAvatar: (state) => {
      const url = state.basicInfo?.avatar
      return url ? `${import.meta.env.VITE_API_URL}${url}` : null
    }
  },

  actions: {
    // 清理 store 数据
    clearStore() {
      this.basicInfo = null
      this.avatarUpdateTime = null
      localStorage.removeItem('profile')  // 清除持久化数据
    },

    // 获取档案基本信息
    async fetchBasicInfo() {
      try {
        // 先清理旧数据
        this.clearStore()
        const response = await profile.getData()
        if (response?.data?.code === 200 && response?.data?.data?.basic_info) {
          console.log('Fetched basicInfo:', response.data.data.basic_info)
          this.basicInfo = response.data.data.basic_info
          this.avatarUpdateTime = Date.now()
          console.log('Store state after fetch:', {
            basicInfo: this.basicInfo,
            avatarUpdateTime: this.avatarUpdateTime
          })
          return this.basicInfo
        }
        return null
      } catch (error) {
        console.error('获取档案基本信息失败:', error)
        throw error
      }
    },

    // 更新头像
    async updateAvatar(formData) {
      try {
        const response = await profile.uploadAvatar(formData)
        if (response?.data?.code === 200) {
          // 直接更新头像
          if (this.basicInfo) {
            console.log('Updating avatar:', response.data.data.avatar)
            this.basicInfo.avatar = response.data.data.avatar
            this.avatarUpdateTime = Date.now()
            // 触发头像更新事件
            eventBus.emit('avatar-updated', response.data.data.avatar)
            console.log('Store state after update:', {
              basicInfo: this.basicInfo,
              avatarUpdateTime: this.avatarUpdateTime
            })
          }
          return response
        }
        throw new Error('上传失败')
      } catch (error) {
        throw error
      }
    }
  },

  persist: {
    enabled: true,
    strategies: [
      {
        key: 'profile',
        storage: localStorage,
        paths: ['basicInfo', 'avatarUpdateTime']
      }
    ]
  }
}) 