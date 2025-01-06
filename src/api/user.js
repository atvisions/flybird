import request from '@/utils/request'

// 获取用户资料
export const getProfile = () => {
  return request({
    url: '/api/v1/users/profile/',
    method: 'get'
  })
}

// 更新用户资料
export const updateProfile = (data) => {
  return request({
    url: '/api/v1/users/profile/',
    method: 'put',
    data
  })
}

// 更新头像
export const updateAvatar = (file) => {
  const formData = new FormData()
  formData.append('avatar', file)
  return request({
    url: '/api/v1/users/profile/avatar/',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 发送短信验证码
export const sendSmsCode = (data) => {
  return request({
    url: '/api/v1/users/auth/sms/send/',
    method: 'post',
    data
  })
}

// 重置密码
export const resetPassword = (data) => {
  return request({
    url: '/api/v1/users/auth/password/reset/',
    method: 'post',
    data
  })
}

// 修改手机号
export const changePhone = (data) => {
  return request({
    url: '/api/v1/users/account/phone/',
    method: 'post',
    data
  })
}

// 修改密码
export const changePassword = (data) => {
  return request({
    url: '/api/v1/users/account/password/',
    method: 'post',
    data
  })
}

// 删除账号
export const deleteAccount = (data) => {
  return request({
    url: '/api/v1/users/account/delete/',
    method: 'post',
    data
  })
} 