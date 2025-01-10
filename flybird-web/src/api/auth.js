import request from '@/utils/request'

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
      
      if (error.response) {
        
        // 直接抛出服务器返回的错误信息
        throw new Error(error.response.data.message || '登录失败，请稍后重试')
      }
      throw error
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
    // 验证必要参数
    if (!data.phone || !data.scene) {
      throw new Error('手机号和场景参数不能为空')
    }
    
    // 验证场景是否有效
    const validScenes = ['register', 'login', 'reset_password', 'change_phone']
    if (!validScenes.includes(data.scene)) {
      throw new Error('无效的场景类型')
    }
    
    return request({
      url: '/api/v1/users/auth/sms/send/',
      method: 'post',
      data: {
        phone: data.phone,
        scene: data.scene
      }
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
    try {
      const response = await request.post('/api/v1/users/auth/register/', {
        phone: data.phone,
        code: data.code,
        password: data.password,
        confirm_password: data.confirmPassword
      })
      
      // 如果注册成功，直接返回登录所需的 token 信息
      if (response?.data?.code === 200) {
        const userData = response.data.data
        // 直接返回响应，让 store 处理 token 和用户信息
        return response
      }
      throw new Error(response?.data?.message || '注册失败')
    } catch (error) {
      console.error('Registration failed:', error)
      throw error
    }
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
    console.error('Login response error:', response?.data)
    throw new Error(response?.data?.message || '登录失败')
  }
}

export default auth 