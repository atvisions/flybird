import request from '@/utils/request'

// 发送验证码
export const sendSmsCode = (data) => {
  return request({
    url: '/api/v1/users/auth/sms/send/',
    method: 'post',
    data
  })
}

// 注册
export const register = (data) => {
  return request({
    url: '/api/v1/users/auth/register/',
    method: 'post',
    data
  })
}

// 登录
export const login = (data) => {
  return request({
    url: '/api/v1/users/auth/login/password/',
    method: 'post',
    data
  })
}

// 登出
export const logout = () => {
  return request({
    url: '/api/v1/users/auth/logout/',
    method: 'post'
  })
} 