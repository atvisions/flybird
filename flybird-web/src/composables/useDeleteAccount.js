import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { account } from '@/api/account'
import { showToast } from '@/components/ToastMessage'

export function useDeleteAccount() {
  const router = useRouter()
  const store = useStore()
  const loading = ref(false)

  const handleDeleteAccount = async (password) => {
    try {
      loading.value = true
      const response = await account.deleteAccount({ password })
      
      if (response.data?.code === 200) {
        showToast('账号注销成功', 'success')
        
        // 清理本地存储和状态
        await store.dispatch('logout')
        
        // 等待一下再跳转
        setTimeout(() => {
          router.push('/login')
        }, 1500)
      }
    } catch (error) {
      console.error('注销账号失败:', error)
      showToast(error.response?.data?.message || '注销账号失败', 'error')
      throw error // 向上传递错误，让调用者也能处理
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    handleDeleteAccount
  }
} 