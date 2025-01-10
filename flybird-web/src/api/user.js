import request from '@/utils/request'

export const user = {
  // 获取用户信息
  getUserInfo: () => {
    return request.get('/api/v1/users/userInfo/')
  },

  // 更新用户头像
  updateAvatar: (data) => {
    const formData = new FormData()
    formData.append('avatar', data)
    return request.post('/api/v1/users/userInfo/avatar/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 更新用户背景图
  updateBackground: (data) => {
    const formData = new FormData()
    formData.append('background', data)
    return request.post('/api/v1/users/userInfo/background/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 更新用户基本信息
  updateUserInfo: (data) => {
    const formData = new FormData()
    Object.keys(data).forEach(key => {
      if (data[key] !== null && data[key] !== undefined) {
        formData.append(key, data[key])
      }
    })
    
    return request({
      url: '/api/v1/users/userInfo/',
      method: 'put',
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }
}

export default user