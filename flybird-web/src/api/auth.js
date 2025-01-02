import request from '@/utils/request'

export const auth = {
  // 密码登录
  loginWithPassword: async (data) => {
    try {
      const response = await request.post('/api/v1/users/auth/login/password/', data)
      if (response.data?.code === 200) {
        // 立即设置 token
        const token = response.data.data.access
        if (token) {
          request.defaults.headers.common['Authorization'] = `Bearer ${token}`
        }
      }
      return response
    } catch (error) {
      console.error('Login request failed:', error)
      throw error
    }
  },
  
  // 获取用户信息
  getUserInfo() {
    return request.get('/api/v1/users/profile/data/')
      .then(response => {
        // 重新组织数据结构
        const processedData = {
          code: response.data.code,
          message: response.data.message,
          data: response.data.data
        }
        return processedData
      })
  },
  
  // 退出登录
  logout: async () => {
    const refreshToken = localStorage.getItem('refresh_token')
    if (!refreshToken) return
    try {
      await request.post('/api/v1/users/auth/logout/', { refresh: refreshToken })
    } finally {
      // 无论请求是否成功，都清除本地存储
      localStorage.clear()
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
  
  // 更新密码
  updatePassword: (data) => {
    return request({
      url: '/api/v1/users/account/password/',
      method: 'post',
      data
    })
  },
  
  // 发送验证码
  sendVerifyCode: (data) => {
    return request({
      url: '/api/v1/users/auth/sms/send/',
      method: 'post',
      data: {
        phone: data.phone,
        scene: data.scene
      }
    })
  },
  
  // 更换手机号
  changePhone: (data) => {
    return request.post('/api/v1/users/account/phone/', data)
  },
  
  // 删除账户
  deleteAccount: (data) => {
    return request({
      url: '/api/v1/users/account/delete/',
      method: 'POST',
      data,
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
  },
  
  // 发送重置密码验证码
  sendResetCode: (phone) => {
    return request.post('/api/v1/users/auth/sms/send/', {
      phone,
      scene: 'reset_password'
    })
  },
  
  // 重置密码
  resetPassword: async (data) => {
    return request.post('/api/v1/users/auth/password/reset/', {
      phone: data.phone,
      code: data.code,
      new_password: data.new_password,
      confirm_password: data.confirm_password
    })
  },
  
  // 注册
  register: async (data) => {
    return request.post('/api/v1/users/auth/register/', {
      phone: data.phone,
      code: data.code,
      password: data.password,
      confirm_password: data.confirm_password
    })
  },
  
  // 密码登录
  passwordLogin(data) {
    return request({
      url: '/api/v1/users/auth/login/password/',
      method: 'post',
      data: {
        account: data.account,
        password: data.password
      }
    })
  }
}

export default auth 