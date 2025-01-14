import { defineStore } from 'pinia'
import request from '@/utils/request'
import { user } from '@/api/user'
import defaultAvatar from '@/assets/images/default-avatar.png'
import { showToast } from '@/components/ToastMessage'
import { useAuthStore } from '@/stores/auth'
import config from '@/config'

export const useAccountStore = defineStore('account', {
  state: () => ({
    userInfo: JSON.parse(localStorage.getItem('userInfo')) || null,
    avatarUpdateTime: null,
    background_image: localStorage.getItem('background_image') || null
  }),

  getters: {
    avatar: (state) => {
      const avatar = state.userInfo?.avatar
      if (!avatar || avatar === 'null' || avatar === 'undefined' || typeof avatar === 'undefined' || avatar === null) {
        return defaultAvatar
      }
      if (avatar.startsWith('http') || avatar.startsWith('data:image')) {
        return avatar
      }
      return avatar.startsWith('/media') 
        ? `${config.API_URL}${avatar}`
        : `${config.API_URL}/media/${avatar}`
    },
    username: (state) => state.userInfo?.username || '未设置用户名',
    uid: (state) => state.userInfo?.uid,
    background: (state) => state.userInfo?.background_image || state.background_image,
    phone: (state) => state.userInfo?.phone,
    email: (state) => state.userInfo?.email,
    position: (state) => state.userInfo?.position,
    bio: (state) => state.userInfo?.bio,
    isVip: (state) => state.userInfo?.is_vip || false,
    isStaff: (state) => state.userInfo?.is_staff || false
  },

  actions: {
    async fetchUserInfo() {
      try {
        const response = await user.getUserInfo()
        if (response?.data?.code === 200) {
          const userData = response.data.data
          
          this.userInfo = {
            ...userData,
            id: userData.id,
            uid: userData.uid,
            username: userData.username,
            phone: userData.phone || null,
            email: userData.email || null,
            avatar: userData.avatar || null,
            position: userData.position || null,
            bio: userData.bio || null,
            is_vip: userData.is_vip || false,
            vip_type: userData.vip_type || 'none',
            vip_expire_time: userData.vip_expire_time || null,
            vip_status: userData.vip_status || '普通用户',
            is_staff: userData.is_staff || false,
            background_image: userData.background_image || null
          }
          
          localStorage.setItem('userInfo', JSON.stringify(this.userInfo))
          return this.userInfo
        }
        return null
      } catch (error) {
        console.error('获取用户信息失败:', error)
        throw error
      }
    },

    async updateAvatar(formData) {
      try {
        const file = formData.get('avatar')
        const response = await request.post('/api/v1/users/userInfo/avatar/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        if (response?.data?.code === 200) {
          this.avatarUpdateTime = Date.now()
          this.userInfo = {
            ...this.userInfo,
            avatar: response.data.data.avatar
          }
          localStorage.setItem('userInfo', JSON.stringify(this.userInfo))
          return response
        }
        throw new Error(response?.data?.message || '更新头像失败')
      } catch (error) {
        console.error('Failed to update avatar:', error)
        throw error
      }
    },

    async updateBackground(formData) {
      try {
        const file = formData.get('background')
        const response = await user.updateBackground(file)
        if (response?.data?.code === 200) {
          this.background_image = response.data.data.background
          this.userInfo = {
            ...this.userInfo,
            background_image: response.data.data.background
          }
          
          localStorage.setItem('userInfo', JSON.stringify(this.userInfo))
          localStorage.setItem('background_image', this.background_image)
          return response
        }
        throw new Error(response?.data?.message || '更新背景图失败')
      } catch (error) {
        console.error('Failed to update background:', error)
        throw error
      }
    },

    async updateUserInfo(data) {
      try {
        const response = await user.updateUserInfo(data)
       
        if (response?.data?.code === 200) {
          const userData = response.data.data
          
          if (data.avatar) {
            this.avatarUpdateTime = Date.now()
          }
          
          this.userInfo = {
            ...this.userInfo,
            avatar: userData.avatar,
            id: userData.id,
            uid: userData.uid,
            username: userData.username,
            phone: userData.phone || null,
            email: userData.email || null,
            position: userData.position || null,
            bio: userData.bio || null,
            is_vip: userData.is_vip || false,
            is_staff: userData.is_staff || false
          }
          
          localStorage.setItem('userInfo', JSON.stringify(this.userInfo))
          
          return response
        }
        throw new Error(response?.data?.message || '更新用户信息失败')
      } catch (error) {
        console.error('Failed to update user info:', error)
        throw error
      }
    },

    clearUserInfo() {
      this.userInfo = null
      this.avatarUpdateTime = null
      this.background_image = null
    },

    async deleteAccount(data) {
      try {
        const response = await user.deleteAccount(data)
        if (response?.data?.code === 200) {
          const authStore = useAuthStore()
          authStore.clearAuth()
          this.clearUserInfo()
          localStorage.clear()
          
          showToast('账号已注销', 'success')
          return true
        }
        return false
      } catch (error) {
        if (error.response?.status === 401) {
          const authStore = useAuthStore()
          authStore.clearAuth()
          this.clearUserInfo()
          localStorage.clear()
          
          showToast('账号已注销', 'success')
          return true
        }
        console.error('Failed to delete account:', error)
        throw error
      }
    },

    async changePhone(data) {
      try {
        console.log('Starting phone change process:', {
          phone: data.phone,
          oldPhone: this.userInfo?.phone,
          hasCode: !!data.code
        })

        // 验证手机号格式
        const phoneRegex = /^1[3-9]\d{9}$/
        if (!phoneRegex.test(data.phone)) {
          throw new Error('请输入正确的手机号格式')
        }

        // 验证验证码格式
        if (data.code && !/^\d{6}$/.test(data.code)) {
          throw new Error('请输入6位数字验证码')
        }

        // 如果没有验证码，先发送验证码
        if (!data.code) {
          console.log('No code provided, sending verification code')
          await account.sendVerifyCode({
            phone: data.phone,
            scene: 'change_phone',
            type: 'sms'
          })
          showToast('验证码已发送', 'success')
          return true
        }

        console.log('Attempting to change phone with code')
        const response = await account.changePhone({
          phone: data.phone,
          code: data.code,
          oldPhone: this.userInfo?.phone
        })
        console.log('Change phone response:', response)
        
        if (response?.data?.code === 200) {
          // 更新本地用户信息
          this.userInfo = {
            ...this.userInfo,
            phone: data.phone
          }
          localStorage.setItem('userInfo', JSON.stringify(this.userInfo))
          
          showToast('手机号更新成功', 'success')
          return true
        }
        return false
      } catch (error) {
        console.error('手机号更新失败:', error)
        if (error.response) {
          console.error('Error response:', {
            status: error.response.status,
            data: error.response.data,
            headers: error.response.headers,
            message: error.response.data?.message || error.response.data?.detail
          })
        }
        
        // 提供更友好的错误信息
        let errorMessage
        if (error.isPhoneDisabled) {
          errorMessage = error.friendlyMessage
        } else {
          errorMessage = error.response?.data?.message 
            || error.response?.data?.detail
            || error.response?.data?.error 
            || error.message 
            || '手机号更新失败，请稍后重试'
        }

        // 如果是发送验证码时的错误，添加更多提示信息
        if (error.response?.data?.code === 'sms_limit_exceeded') {
          errorMessage = '该手机号发送验证码次数过多，请24小时后再试'
        } else if (error.response?.data?.code === 'phone_blacklisted') {
          errorMessage = '该手机号已被限制使用，请更换其他手机号'
        }

        showToast(errorMessage, 'error')
        throw error
      }
    },

    // 发送验证码
    async sendVerifyCode(phone, scene) {
      try {
        const response = await account.sendVerifyCode({
          phone,
          scene,
          type: 'sms'
        })
        if (response?.data?.code === 200) {
          showToast('验证码已发送', 'success')
          return true
        }
        return false
      } catch (error) {
        console.error('发送验证码失败:', error)
        let errorMessage
        if (error.response?.data?.code === 'sms_limit_exceeded') {
          errorMessage = '该手机号发送验证码次数过多，请24小时后再试'
        } else if (error.response?.data?.code === 'phone_blacklisted') {
          errorMessage = '该手机号已被限制使用，请更换其他手机号'
        } else {
          errorMessage = error.response?.data?.message || '发送验证码失败，请稍后重试'
        }
        showToast(errorMessage, 'error')
        throw error
      }
    }
  }
}) 