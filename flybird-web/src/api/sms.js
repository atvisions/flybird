import request from '@/utils/request'

export const sms = {
  // 发送验证码
  sendVerifyCode: (data) => {
    return request.post('/api/v1/users/auth/sms/send/', data)
  }
}

export default sms 