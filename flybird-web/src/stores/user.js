import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(null)
  
  // 判断是否登录
  const isLoggedIn = computed(() => {
    return !!token.value
  })
  
  // 判断是否是会员
  const isPro = computed(() => {
    return userInfo.value?.is_pro || false
  })
  
  // 设置用户信息
  const setUserInfo = (info) => {
    userInfo.value = info
  }
  
  // 设置 token
  const setToken = (newToken) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }
  
  // 清除用户信息
  const clearUser = () => {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
  }
  
  return {
    token,
    userInfo,
    isLoggedIn,
    isPro,
    setUserInfo,
    setToken,
    clearUser
  }
}) 