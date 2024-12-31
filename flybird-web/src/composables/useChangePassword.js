import { reactive } from 'vue'
import { useStore } from 'vuex'
import { user } from '@/api/user'
import { showToast } from '@/components/ToastMessage'

export function useChangePassword() {
  const store = useStore()
  const state = reactive({
    oldPassword: '',
    newPassword: '',
    confirmPassword: '',
    loading: false
  })

  const handleUpdate = async () => {
    if (!state.oldPassword || !state.newPassword || !state.confirmPassword) {
      showToast('请填写完整信息', 'error')
      return false
    }

    if (state.newPassword !== state.confirmPassword) {
      showToast('两次输入的密码不一致', 'error')
      return false
    }

    state.loading = true
    try {
      await user.updatePassword({
        old_password: state.oldPassword,
        new_password: state.newPassword,
        confirm_password: state.confirmPassword
      })
      showToast('密码修改成功', 'success')
      return true
    } catch (error) {
      showToast(error.response?.data?.message || '修改失败', 'error')
      return false
    } finally {
      state.loading = false
    }
  }

  return {
    state,
    handleUpdate
  }
} 