import { reactive } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { user } from '@/api/user'
import { showToast } from '@/components/ToastMessage'

export function useDeleteAccount() {
  const store = useStore()
  const router = useRouter()
  const state = reactive({
    password: '',
    loading: false
  })

  const handleDelete = async () => {
    if (!state.password) {
      showToast('请输入密码', 'error')
      return false
    }

    state.loading = true
    try {
      await user.deleteAccount({ password: state.password })
      showToast('账户已注销', 'success')
      await store.dispatch('logout')
      router.push('/login')
      return true
    } catch (error) {
      showToast(error.response?.data?.message || '注销失败', 'error')
      return false
    } finally {
      state.loading = false
    }
  }

  return {
    state,
    handleDelete
  }
} 