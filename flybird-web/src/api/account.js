import request from '@/utils/request'

// 账号管理相关功能
export const account = {
  // 注册账号
  register: (data) => {
    return request.post('/api/v1/users/auth/register/', {
      phone: data.phone,
      code: data.code,
      password: data.password,
      confirm_password: data.confirm_password
    })
  },

  // 重置密码
  resetPassword: (data) => {
    return request.post('/api/v1/users/auth/password/reset/', {
      phone: data.phone,
      code: data.code,
      new_password: data.password,
      confirm_password: data.confirmPassword
    })
  },

  // 修改密码
  updatePassword: (data) => {
    return request.post('/api/v1/users/account/password/', {
      old_password: data.old_password,
      new_password: data.new_password,
      confirm_password: data.confirm_password
    })
  },

  // 更换手机号
  changePhone: (data) => {
    return request.post('/api/v1/users/account/phone/', {
      phone: data.phone,
      code: data.code
    })
  },

  // 注销账号
  deleteAccount(data) {
    return request({
      url: '/api/v1/users/account/delete/',
      method: 'post',
      data: {
        password: data.password
      }
    })
  }
} 