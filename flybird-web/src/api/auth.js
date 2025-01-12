import request from '@/utils/request'
import { API_URL } from '@/config/index'

export const auth = {
  // 密码登录
  loginWithPassword: async function(data) {
    try {
      // 打印请求数据
      console.log('Login request data:', {
        account: data.account,
        password: '***'  // 不打印实际密码
      })
      const response = await request.post('/api/v1/users/auth/login/password/', {
        account: data.account,
        password: data.password
      })
      return this.handleLoginResponse(response)
    } catch (error) {
      // 打印错误详情
      console.error('Login error:', {
        status: error.response?.status,
        data: error.response?.data
      })
      
      if (error.response) {
        // 直接抛出服务器返回的错误信息，不要再包装一层
        throw error
      }
      throw new Error('网络连接失败，请稍后重试')
    }
  },
  
  // 退出登录
  logout: async () => {
    const refreshToken = localStorage.getItem('refresh_token')
    if (!refreshToken) return
    try {
      await request.post('/api/v1/users/auth/logout/', { refresh: refreshToken })
    } finally {
      // 清除所有相关的本地存储数据
      localStorage.removeItem('token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('token_expires_at')
      // 清除用户相关数据
      localStorage.removeItem('remember_me')
      localStorage.removeItem('remembered_account')
      localStorage.removeItem('userInfo')
      // 清除其他可能存在的数据
      localStorage.removeItem('isLoggedIn')
      // 清除请求头中的 token
      delete request.defaults.headers.common['Authorization']
    }
  },
  
  // 刷新 token
  refreshToken: (data) => {
    return request.post('/api/v1/users/auth/token/refresh/', data)
  },
  
  // 更新用户名（昵称）
  updateUsername: (data) => {
    return request.post('/api/v1/users/account/username/', data)
  },
  
  // 发送验证码
  sendVerifyCode: (data) => {
    return request({
      url: '/api/v1/users/auth/sms/send/',
      method: 'post',
      data: {
        phone: data.phone,
        scene: data.scene,
        type: 'sms'
      }
    })
  },
  
  // 重置密码
  resetPassword: (data) => {
    // 打印请求数据以便调试
    console.log('Reset password request data:', {
      phone: data.phone,
      code: data.code,
      new_password: '***',
      confirm_password: '***'
    })

    return request({
      url: '/api/v1/users/auth/password/reset/',
      method: 'post',
      data: {
        phone: data.phone,
        code: data.code,
        new_password: data.new_password,
        confirm_password: data.confirm_password
      }
    }).then(response => {
      console.log('Reset password success response:', response.data)
      return response
    }).catch(error => {
      console.log('Reset password error response:', error.response?.data)
      // 处理错误响应
      const errorData = error.response?.data
      if (errorData) {
        // 如果错误信息在 code 字段中
        if (errorData.code && Array.isArray(errorData.code)) {
          throw new Error(errorData.code[0])
        }
        // 如果错误信息在其他字段中
        for (const key in errorData) {
          if (Array.isArray(errorData[key])) {
            throw new Error(errorData[key][0])
          }
        }
        // 如果有直接的错误消息
        if (errorData.message) {
          throw new Error(errorData.message)
        }
      }
      throw error
    })
  },
  
  // 注册
  register: (data) => {
    return request({
      url: '/api/v1/users/auth/register/',
      method: 'post',
      data: {
        phone: data.phone,
        code: data.code,
        password: data.password,
        confirm_password: data.confirmPassword
      }
    })
  },
  
  handleLoginResponse(response) {
    if (response?.data?.code === 200) {
      const userData = response.data.data
      // 设置请求头的 Authorization
      const token = userData.access
      if (token) {
        request.defaults.headers.common['Authorization'] = `Bearer ${token}`
      }
      
      return {
        token: token,
        refresh: userData.refresh,
        userInfo: {
          id: userData.id,
          uid: userData.uid,
          username: userData.username,
          avatar: userData.avatar
        }
      }
    }
    // 如果不是成功响应，抛出错误
    throw new Error(response?.data?.message || '登录失败')
  }
}

export default auth 