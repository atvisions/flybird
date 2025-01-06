import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  // 从 localStorage 获取初始登录状态
  const isLoggedIn = ref(localStorage.getItem('isLoggedIn') === 'true')
  const userInfo = ref(JSON.parse(localStorage.getItem('userInfo')) || null)

  // 登录
  const login = (user) => {
    isLoggedIn.value = true
    userInfo.value = user
    // 保存到 localStorage
    localStorage.setItem('isLoggedIn', 'true')
    localStorage.setItem('userInfo', JSON.stringify(user))
  }

  // 登出
  const logout = () => {
    isLoggedIn.value = false
    userInfo.value = null
    // 清除 localStorage
    localStorage.removeItem('isLoggedIn')
    localStorage.removeItem('userInfo')
  }

  return {
    isLoggedIn,
    userInfo,
    login,
    logout
  }
}, {
  persist: true // 启用状态持久化
}) 