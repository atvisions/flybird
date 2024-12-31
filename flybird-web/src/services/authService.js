import { auth } from '@/api/auth'
import { storage } from '@/utils/storage'
import store from '@/store'

export const authService = {
  // 登录服务
  async login({ phone, password, rememberMe = false }) {
    try {
      const response = await auth.loginWithPassword({
        phone,
        password
      })

      if (response.data?.code === 200) {
        const { access, refresh } = response.data.data
        
        // 使用 storage 服务保存认证信息
        storage.saveAuth({ access, refresh }, rememberMe)
        
        // 如果记住我，保存手机号
        if (rememberMe) {
          storage.savePhone(phone, true)
        }
        
        // 更新 store 状态
        await store.dispatch('login', {
          access,
          refresh,
          rememberMe
        })
        
        return true
      }
      return false
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    }
  },

  // 添加登出服务
  async logout() {
    try {
      // 调用后端登出接口
      await auth.logout()
      // 清理本地状态
      await store.dispatch('logout')
      return true
    } catch (error) {
      console.error('Logout failed:', error)
      // 即使后端登出失败，也要清理本地状态
      await store.dispatch('logout')
      throw error
    }
  },

  // 检查认证状态
  async checkAuth() {
    return store.dispatch('checkAuth')
  }
}

export default authService 