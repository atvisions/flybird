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

}

export const updateNickname = (nickname) => {
  return user.updateUsername({ username: nickname })
}

export default user