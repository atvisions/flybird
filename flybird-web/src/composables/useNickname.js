import { reactive } from 'vue'
import { useStore } from 'vuex'
import { user } from '@/api/user'
import { showToast } from '@/components/ToastMessage'

export function useNickname() {
  const store = useStore()
  const state = reactive({
    value: '',
    loading: false,
    error: ''
  })

  // 昵称验证规则
  const validateNickname = (nickname) => {
    if (!nickname || !nickname.trim()) {
      return '昵称不能为空'
    }
    // 长度检查：4-8个字符
    if (nickname.length < 4 || nickname.length > 8) {
      return '昵称长度需要在4-8个字符之间'
    }
    
    // 字符类型检查：只允许中文、数字、英文字母
    if (!/^[\u4e00-\u9fa5a-zA-Z0-9]+$/.test(nickname)) {
      return '昵称只能包含中文、数字、英文字母'
    }
    
    return ''
  }

  const handleUpdate = async () => {
    // 验证昵称
    const error = validateNickname(state.value)
    if (error) {
      state.error = error
      showToast(error, 'error')
      return false
    }

    state.loading = true
    state.error = ''
    
    try {
      await user.updateUsername({ username: state.value })
      await store.dispatch('fetchUserInfo')
      showToast('昵称修改成功', 'success')
      return true
    } catch (error) {
      const errorMsg = error.response?.data?.message || '修改失败'
      state.error = errorMsg
      showToast(errorMsg, 'error')
      return false
    } finally {
      state.loading = false
    }
  }

  return {
    state,
    handleUpdate,
    validateNickname
  }
} 