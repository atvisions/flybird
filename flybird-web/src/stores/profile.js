import { defineStore } from 'pinia'
import profile from '@/api/profile'
import config from '@/config'

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
        console.log('Profile API Response:', response.data)
        
        if (response.data.code === 200) {
          const data = response.data.data
          console.log('Original avatar URL:', data.basic_info?.avatar)
          console.log('Config mediaURL:', config.mediaURL)
          
          if (data.basic_info?.avatar) {
            // 如果是完整URL，替换端口号
            if (data.basic_info.avatar.startsWith('http')) {
              console.log('处理完整URL')
              // 使用正则表达式替换所有出现的8080端口
              data.basic_info.avatar = data.basic_info.avatar.replace(/:8080\//g, ':8000/')
              console.log('替换端口后的URL:', data.basic_info.avatar)
            } else {
              console.log('处理相对路径')
              // 清理路径中的media前缀
              const cleanPath = data.basic_info.avatar.replace(/^\/?(media\/)?/, '')
              data.basic_info.avatar = `${config.mediaURL}/${cleanPath}`
              console.log('构建的完整URL:', data.basic_info.avatar)
            }
          }
          
          this.profileData = data
          console.log('Final profileData:', this.profileData)
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