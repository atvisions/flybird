import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { auth } from '@/api/auth'
import { showToast } from '@/components/ToastMessage'

export function useLogout() {
  const store = useStore()
  const router = useRouter()

  const handleLogout = async () => {
    try {
      // 调用后端登出接口
      await auth.logout()
      
      // 清理本地状态
      await store.dispatch('logout')
      
      // 显示成功提示
      showToast('已安全退出', 'success')
      
      // 跳转到登录页
      router.push('/login')
    } catch (error) {
      console.error('登出失败:', error)
      showToast('退出失败，请重试', 'error')
      
      // 即使后端登出失败，也要清理本地状态
      await store.dispatch('logout')
      router.push('/login')
    }
  }

  return {
    handleLogout
  }
} 