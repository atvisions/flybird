import { account } from '@/api/account'
import { sms, SMS_SCENE } from '@/api/sms'

// 账号服务
export const accountService = {
  // 发送验证码
  async sendVerifyCode(phone, scene) {
    return sms.send({ phone, scene })
  },

  // 注册
  async register(data) {
    return account.register({
      phone: data.phone,
      code: data.code,
      password: data.password,
      confirm_password: data.confirm_password
    })
  },

  // 重置密码
  async resetPassword(data) {
    return account.resetPassword({
      phone: data.phone,
      code: data.code,
      new_password: data.password,
      confirm_password: data.confirmPassword
    })
  },

  // 更换手机号
  async changePhone(data) {
    return account.changePhone({
      phone: data.phone,
      code: data.code
    })
  },

  // 修改密码
  async updatePassword(data) {
    return account.updatePassword({
      old_password: data.oldPassword,
      new_password: data.newPassword,
      confirm_password: data.confirmPassword
    })
  },

  // 删除账号
  async deleteAccount(password) {
    return account.deleteAccount({ password })
  }
} 