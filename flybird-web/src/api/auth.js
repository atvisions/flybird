import request from '@/utils/request'
import { SMS_SCENE } from '@/store'

export const auth = {
  // 密码登录
  login: async (data) => {
    try {
      const response = await request({
        url: '/api/v1/users/auth/login/password/',
        method: 'post',
        data: {
          phone: data.phone.trim(),
          password: data.password
        }
      })

      if (!response.data || response.data.code !== 200) {
        throw new Error(response.data?.message || '登录失败')
      }

      // 只返回必要的认证信息
      const { access, refresh } = response.data.data
      if (!access) {
        throw new Error('登录失败：未获取到 token')
      }

      return {
        data: {
          access,
          refresh
        }
      }
    } catch (error) {
      throw error
    }
  },
  
  // 退出登录
  logout: () => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      return Promise.resolve()
    }

    return request({
      url: '/api/v1/users/auth/logout/',
      method: 'post',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    }).catch(error => {
      if (error.response?.status === 401) {
        return Promise.resolve()
      }
      throw error
    })
  },
  
  // 刷新 token
  refreshToken: (data) => {
    return request({
      url: '/api/v1/users/auth/token/refresh/',
      method: 'post',
      data
    })
  },

  // 注册
  register: async (data) => {
    try {
      const response = await request({
        url: '/api/v1/users/auth/register/',
        method: 'post',
        data: {
          phone: data.phone.trim(),
          code: data.code,
          password: data.password
        }
      })

      console.log('Register response:', response)

      // 验证响应数据
      if (!response.data || response.data.code !== 200) {
        throw new Error(response.data?.message || '注册失败')
      }

      // 验证必要的数据字段
      const { access, refresh, user } = response.data.data || {}
      if (!access || !refresh || !user) {
        console.error('Incomplete response data:', response.data)
        throw new Error('注册响应数据不完整')
      }

      return response
    } catch (error) {
      console.error('Register error details:', {
        status: error.response?.status,
        data: error.response?.data,
        message: error.message,
        stack: error.stack
      })

      // 处理错误
      if (error.response?.data?.errors) {
        const errors = error.response.data.errors
        if (errors.code) {
          throw new Error(errors.code[0])
        }
        if (errors.phone) {
          throw new Error(errors.phone[0])
        }
        if (errors.password) {
          throw new Error(errors.password[0])
        }
      }

      throw new Error(error.response?.data?.message || error.message || '注册失败，请稍后重试')
    }
  },

  // 发送验证码
  sendVerifyCode: async (data) => {
    try {
      // 打印完整的请求数据
      console.log('Sending verify code request:', {
        url: '/api/v1/users/auth/sms/send/',
        method: 'post',
        data: {
          phone: data.phone.trim(),
          scene: data.scene
        }
      })

      const response = await request({
        url: '/api/v1/users/auth/sms/send/',
        method: 'post',
        headers: {
          'Content-Type': 'application/json'
        },
        data: {
          phone: data.phone.trim(),
          scene: data.scene
        }
      })
      
      // 检查响应格式
      if (!response.data || response.data.code !== 200) {
        throw new Error(response.data?.message || '发送验证码失败')
      }

      console.log('Send verify code response:', response)
      return response
    } catch (error) {
      // 打印详细的错误信息
      console.error('Send verify code error details:', {
        status: error.response?.status,
        data: error.response?.data,
        message: error.message,
        requestData: {
          phone: data.phone.trim(),
          scene: data.scene
        }
      })

      // 处理错误
      if (error.response?.data) {
        throw new Error(error.response.data.message || '发送验证码失败')
      }
      
      throw new Error(error.message || '发送验证码失败，请稍后重试')
    }
  },

  // 重置密码
  resetPassword: (data) => {
    return request({
      url: '/api/v1/users/auth/password/reset/',
      method: 'post',
      data: {
        phone: data.phone.trim(),
        code: data.code,
        new_password: data.new_password,
        confirm_password: data.confirm_password
      }
    })
  },

  // 更换手机号
  changePhone: async (data) => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      throw new Error('未登录或登录已过期')
    }

    try {
      const response = await request({
        url: '/api/v1/users/account/phone/',
        method: 'post',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        data: {
          phone: data.phone,
          code: data.code
        }
      })

      console.log('Change phone response:', response)
      return response
    } catch (error) {
      console.error('Change phone error details:', {
        status: error.response?.status,
        data: error.response?.data,
        message: error.message,
        raw: error
      })

      // 处理错误
      if (error.response) {
        const errorData = error.response.data
        
        // 处理错误信息
        if (errorData.errors) {
          const errorMessages = []
          if (errorData.errors.phone) {
            errorMessages.push(errorData.errors.phone[0])
          }
          if (errorData.errors.code) {
            errorMessages.push(errorData.errors.code[0])
          }
          if (errorMessages.length > 0) {
            throw new Error(errorMessages.join('; '))
          }
        }

        if (errorData.message) {
          throw new Error(errorData.message)
        }
      }

      throw new Error(error.message || '手机号修改失败，请稍后重试')
    }
  },

  // 更新个人资料
  updateProfile: (data) => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      throw new Error('未登录或登录已过期')
    }

    return request({
      url: '/api/v1/users/auth/profile/',
      method: 'patch',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      data: {
        username: data.username
      }
    })
  },

  // 获取用户信息
  getUserInfo: async () => {
    try {
      const token = localStorage.getItem('access_token')
      if (!token) {
        throw new Error('未找到访问令牌')
      }

      const response = await request({
        url: '/api/v1/users/profile/basic/',
        method: 'get',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (!response.data || response.data.code !== 200) {
        throw new Error(response.data?.message || '获取用户信息失败')
      }

      return response
    } catch (error) {
      throw error
    }
  },

  // 上传头像
  uploadAvatar: async (formData) => {
    try {
      const response = await request({
        url: '/api/v1/users/profile/avatar/upload/',
        method: 'post',
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        data: formData
      })

      return response
    } catch (error) {
      throw error
    }
  },

  // 更新用户名
  updateUsername: async (data) => {
    try {
      const response = await request({
        url: '/api/v1/users/account/username/',
        method: 'post',
        data: {
          username: data.username
        }
      })

      return response
    } catch (error) {
      throw error
    }
  },

  // 更新基本信息
  updateBasicInfo: async (data) => {
    try {
      const response = await request({
        url: '/api/v1/users/profile/basic/',
        method: 'post',
        data: {
          basic_info: {
            ...data
          }
        }
      })

      return response
    } catch (error) {
      throw error
    }
  }
} 