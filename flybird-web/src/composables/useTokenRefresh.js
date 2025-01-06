import { onMounted, onUnmounted } from 'vue'
import { useStore } from 'vuex'
import { isTokenExpired } from '@/utils/auth'

export function useTokenRefresh() {
  const store = useStore()
  let refreshTimer = null
  
  // 检查并刷新 token
  const checkAndRefreshToken = async () => {
    try {
      // 如果 token 即将过期（比如还有 30 分钟就过期）
      const expiresAt = localStorage.getItem('token_expires')
      if (!expiresAt) return
      
      const expirationTime = parseInt(expiresAt) * 1000
      const thirtyMinutes = 30 * 60 * 1000
      const shouldRefresh = expirationTime - Date.now() <= thirtyMinutes
      
      if (shouldRefresh) {
        await store.dispatch('refreshToken')
      }
    } catch (error) {
      console.error('Token refresh failed:', error)
    }
  }
  
  // 设置定时检查
  const startTokenRefresh = () => {
    // 每 15 分钟检查一次
    refreshTimer = setInterval(checkAndRefreshToken, 15 * 60 * 1000)
    // 立即执行一次检查
    checkAndRefreshToken()
  }
  
  // 清理定时器
  const stopTokenRefresh = () => {
    if (refreshTimer) {
      clearInterval(refreshTimer)
      refreshTimer = null
    }
  }
  
  // 在组件挂载时启动，卸载时清理
  onMounted(() => {
    startTokenRefresh()
  })
  
  onUnmounted(() => {
    stopTokenRefresh()
  })
  
  return {
    checkAndRefreshToken,
    startTokenRefresh,
    stopTokenRefresh
  }
} 