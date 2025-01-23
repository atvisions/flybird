import request from '@/utils/request'

export const account = {
  // 获取用户信息
  getUserInfo: () => {
    return request.get('/api/v1/users/userInfo/')
  },

  // 更新密码
  updatePassword: (data) => {
    return request({
      url: '/api/v1/users/account/password/',
      method: 'post',
      data: {
        old_password: data.oldPassword,
        new_password: data.newPassword,
        confirm_password: data.confirmPassword
      }
    })
  },

  // 更换手机号
  changePhone: (data) => {
    return request({
      url: '/api/v1/users/account/phone/',
      method: 'post',
      data: {
        phone: data.phone.trim(),
        code: data.code.trim()
      }
    })
  },

  // 绑定邮箱
  bindEmail: (data) => {
    return request({
      url: '/api/v1/users/account/bind-email/',
      method: 'post',
      data: {
        email: data.email,
        code: data.code,
        password: data.password
      }
    })
  },

  // 更换邮箱
  changeEmail: (data) => {
    return request.post('/api/v1/users/account/change-email/', data)
  },

  // 解绑邮箱
  unbindEmail: (data) => {
    return request.post('/api/v1/users/account/unbind-email/', {
      password: data.password
    })
  },

  // 发送邮箱验证码
  sendEmailCode: (data) => {
    return request({
      url: '/api/v1/users/account/send-email-code/',
      method: 'post',
      data: {
        email: data.email,
        password: data.password
      }
    })
  },

  // 注销账号
  deleteAccount: (data) => {
    return request({
      url: '/api/v1/users/account/delete/',
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
        phone: data.phone.trim(),
        scene: data.scene,
        type: 'sms',
        is_test: process.env.NODE_ENV === 'development'
      }
    })
  },

  // 获取指定用户的公开信息
  getUserPublicInfo: (userId) => {
    return request.get(`/api/v1/users/users/${userId}/`)
  },
}

export default account 