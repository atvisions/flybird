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
        old_password: data.old_password,
        new_password: data.new_password,
        confirm_password: data.confirm_password
      }
    })
  },

  // 更换手机号
  changePhone: (data) => {
    // 确保数据格式正确
    const requestData = {
      phone: data.phone.trim(),  // 去除可能的空格
      verify_code: data.code.trim(),  // 修改字段名为 verify_code
      old_phone: data.oldPhone?.trim() || null  // 添加原手机号字段
    }

    console.log('Sending change phone request:', {
      url: '/api/v1/users/account/phone/',
      data: requestData
    })

    return request({
      url: '/api/v1/users/account/phone/',
      method: 'post',
      data: requestData,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    })
  },

  // 绑定邮箱
  bindEmail: (data) => {
    return request.post('/api/v1/users/account/bind-email/', {
      email: data.email,
      code: data.code
    })
  },

  // 更换邮箱
  changeEmail: (data) => {
    return request.post('/api/v1/users/account/change-email/', {
      email: data.email,
      code: data.code,
      password: data.password
    })
  },

  // 解绑邮箱
  unbindEmail: (data) => {
    return request.post('/api/v1/users/account/unbind-email/', {
      password: data.password
    })
  },

  // 发送邮箱验证码
  sendEmailCode: (data) => {
    return request.post('/api/v1/users/account/send-email-code/', {
      email: data.email
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

  // 发送验证码 (用于更换手机号和邮箱)
  sendVerifyCode: (data) => {
    const requestData = {
      phone: data.phone.trim(),
      scene: data.scene,
      type: 'sms'
    }

    console.log('Sending verify code request:', {
      url: '/api/v1/users/auth/sms/send/',
      data: requestData
    })

    return request({
      url: '/api/v1/users/auth/sms/send/',
      method: 'post',
      data: requestData,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    })
  },
}

export default account 