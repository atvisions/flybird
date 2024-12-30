import request from '@/utils/request'
import { SMS_SCENE } from '@/store'

export const user = {
  // 获取用户信息
  getUserInfo: () => {
    return request({
      url: '/api/v1/users/info/',
      method: 'get'
    })
  },

  // 修改密码
  changePassword: (data) => {
    return request({
      url: '/api/v1/users/account/password/',
      method: 'post',
      data: {
        old_password: data.old_password,
        new_password: data.new_password,
        confirm_password: data.confirm_password
      }
    })
  },

  // 更换手机号
  changePhone: (data) => {
    const token = localStorage.getItem('access_token')
    return request({
      url: '/api/v1/users/account/phone/',
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : undefined
      },
      data: {
        new_phone: data.phone,
        code: data.code
      }
    })
  },

  // 删除账号
  deleteAccount: async (data) => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      throw new Error('未登录或登录已过期')
    }

    try {
      const response = await request({
        url: '/api/v1/users/account/delete/',
        method: 'post',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        data: {
          password: data.password
        }
      })

      return response
    } catch (error) {
      console.error('Delete account error details:', {
        status: error.response?.status,
        data: error.response?.data,
        message: error.message
      })

      throw new Error(error.response?.data?.message || '注销账号失败，请稍后重试')
    }
  }
}

// 导出需要的方法
export const { getUserInfo, changePassword, changePhone, deleteAccount } = user

// 发送短信验证码
export const sendSmsCode = (data) => {
  // 只有更换手机号场景需要 token
  const needToken = data.scene === SMS_SCENE.CHANGE_PHONE
  const token = needToken ? localStorage.getItem('access_token') : undefined
  
  if (needToken && !token) {
    console.error('Token required but not found')
    throw new Error('登录已过期，请重新登录')
  }
  
  console.log('Sending SMS code with data:', {
    phone: data.phone,
    scene: data.scene,
    needToken,
    hasToken: !!token,
    token: token ? `${token.substring(0, 10)}...` : undefined,
    fullConfig: {
      url: '/api/v1/users/auth/sms/send/',
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        ...(needToken ? { 'Authorization': `Bearer ${token}` } : {})
      },
      data: {
        phone: data.phone.trim(),
        scene: data.scene || SMS_SCENE.CHANGE_PHONE
      }
    }
  })
  
  const headers = {
    'Content-Type': 'application/json'
  }

  if (needToken && token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  return request({
    url: '/api/v1/users/auth/sms/send/',
    method: 'post',
    headers,
    data: {
      phone: data.phone.trim(),
      scene: data.scene || SMS_SCENE.CHANGE_PHONE
    }
  }).catch(error => {
    // 如果是 401 错误，说明 token 过期
    if (error.response?.status === 401) {
      throw new Error('登录已过期，请重新登录')
    }
    
    console.error('SMS code error details:', {
      status: error.response?.status,
      data: error.response?.data,
      config: error.config,
      headers: error.response?.headers,
      originalError: error.message,
      stack: error.stack
    })
    throw error
  })
}