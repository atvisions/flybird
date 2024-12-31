import request from '@/utils/request'

export const user = {
  // 更新用户名
  updateUsername: (data) => {
    return request.post('/api/v1/users/account/username/', {
      username: data.username
    })
  },

  // 更换手机号
  changePhone: (data) => {
    return request.post('/api/v1/users/account/phone/', {
      phone: data.phone,
      code: data.code
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

  // 删除账户
  deleteAccount: (data) => {
    return request.post('/api/v1/users/account/delete/', {
      password: data.password
    })
  },

  // 获取个人资料布局
  getProfileLayout() {
    return request({
      url: '/api/v1/users/profile/layout/',
      method: 'get'
    })
  },

  // 更新个人资料布局
  updateProfileLayout(data) {
    console.log('发送布局更新请求:', data.data.layout)
    return request({
      url: '/api/v1/users/profile/layout/',
      method: 'put',
      data: data.data.layout
    })
  },

  // 获取个人资料数据
  getProfileData: () => {
    return request.get('/api/v1/users/profile/data/')
  },

  // 更新个人资料数据
  updateProfileData: (data) => {
    return request.post('/api/v1/users/profile/data/', data)
  }
}

export const updateNickname = (nickname) => {
  return user.updateUsername({ username: nickname })
}

export default user