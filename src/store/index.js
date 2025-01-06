import { createStore } from 'vuex'
import request from '@/utils/request'

const store = createStore({
  state: {
    user: null,
    profile: null,
  },
  getters: {
    getUserAvatar: (state) => {
      const defaultAvatar = '/images/default-avatar.png'
      const baseUrl = process.env.VUE_APP_API_URL || ''

      try {
        // 获取头像数据
        const basicInfo = state.profile?.basic_info
        if (!basicInfo) {
          return defaultAvatar
        }

        // 获取头像值
        let avatarUrl = ''

        // 处理不同类型的头像数据
        switch (typeof basicInfo.avatar) {
          case 'string':
            avatarUrl = basicInfo.avatar
            break
          case 'object':
            if (basicInfo.avatar && basicInfo.avatar.url) {
              avatarUrl = basicInfo.avatar.url
            }
            break
          default:
            return defaultAvatar
        }

        // 如果没有头像，返回默认头像
        if (!avatarUrl) {
          return defaultAvatar
        }

        // 检查是否是完整URL
        const isFullUrl = /^https?:\/\//i.test(avatarUrl)
        return isFullUrl ? avatarUrl : `${baseUrl}${avatarUrl}`

      } catch (error) {
        return defaultAvatar
      }
    }
  },
  mutations: {
    setUser(state, user) {
      state.user = user
    },
    setProfile(state, profile) {
      state.profile = profile
    },
    updateAvatar(state, avatar) {
      if (state.profile?.basic_info) {
        state.profile.basic_info.avatar = avatar
      }
    }
  },
  actions: {
    async uploadAvatar({ commit }, file) {
      try {
        console.log('开始上传头像:', {
          fileName: file.name,
          fileSize: file.size,
          fileType: file.type
        })

        const formData = new FormData()
        formData.append('avatar', file)
        
        const response = await request({
          url: '/api/v1/users/profile/avatar/upload/',
          method: 'post',
          data: formData,
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        
        console.log('头像上传响应:', {
          code: response.data.code,
          message: response.data.message,
          avatar: response.data.data?.avatar
        })

        if (response.data.code === 200) {
          commit('updateAvatar', response.data.data.avatar)
          return response.data.data.avatar
        }
        throw new Error(response.data.message)
      } catch (error) {
        console.error('头像上传失败:', error.message)
        throw error
      }
    }
  }
})

export default store 