import { defineStore } from 'pinia'
import profile from '@/api/profile'
import { MEDIA_URL } from '@/config/index'

export const useProfileStore = defineStore({
  id: 'profile',
  state: () => ({
    basicInfo: null,
    avatarUpdateTime: null
  }),

  getters: {
    // 获取职业头像的完整 URL
    profileAvatarUrl: (state) => {
      const avatar = state.basicInfo?.avatar
      if (!avatar) return null
      // 如果已经是完整的 URL，直接返回
      if (avatar.startsWith('http')) return avatar
      // 如果是相对路径，需要去掉开头的 /media/
      const cleanPath = avatar.replace(/^\/media\//, '')
      return `${MEDIA_URL}/${cleanPath}`
    }
  },

  actions: {
    // 更新头像
    async updateAvatar(file) {
      try {
        const response = await profile.uploadAvatar(file)
        if (response?.data?.code === 200) {
          const avatarUrl = response.data.data.avatar
          
          // 更新 store 状态
          if (!this.basicInfo) {
            this.basicInfo = {}
          }
          this.basicInfo.avatar = avatarUrl
          this.avatarUpdateTime = Date.now()
          
          console.log('Store updated:', {
            avatar: this.basicInfo.avatar,
            updateTime: this.avatarUpdateTime
          })
          
          return response
        }
        throw new Error(response?.data?.message || '上传失败')
      } catch (error) {
        console.error('职业头像上传失败:', error)
        throw error
      }
    }
  }
}) 