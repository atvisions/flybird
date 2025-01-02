import { reactive, computed } from 'vue'
import { useStore } from 'vuex'
import { user } from '@/api/user'
import { showToast } from '@/components/ToastMessage'
import { ElMessage } from 'element-plus'

export function useChangePassword() {
  const store = useStore()
  const state = reactive({
    oldPassword: '',
    newPassword: '',
    confirmPassword: '',
    loading: false,
    error: '',
    strength: 0
  })

  const checkPasswordStrength = (password) => {
    let score = 0
    
    // 基础长度检查 (最多1分)
    if (password.length >= 8) score += 0.5
    if (password.length >= 12) score += 0.5
    
    // 字符类型检查
    if (/\d/.test(password)) score += 1  // 数字
    if (/[A-Za-z]/.test(password)) score += 1  // 字母
    if (/[!@#$%^&*]/.test(password)) score += 1  // 特殊字符（可选）
    
    // 额外加分项（可选）
    if (/[A-Z]/.test(password) && /[a-z]/.test(password)) score += 0.5  // 同时包含大小写
    
    return Math.floor(score)
  }

  const validatePassword = (password) => {
    if (!password) {
      return '密码不能为空'
    }
    if (password.length < 8 || password.length > 20) {
      return '密码长度必须在8-20个字符之间'
    }
    if (!/[A-Za-z]/.test(password)) {
      return '密码必须包含字母'
    }
    if (!/\d/.test(password)) {
      return '密码必须包含数字'
    }
    if (password === state.oldPassword) {
      return '新密码不能与当前密码相同'
    }
    return ''
  }

  const updatePasswordStrength = (password) => {
    state.strength = checkPasswordStrength(password)
  }

  const handleUpdate = async () => {
    try {
      state.loading = true
      state.error = ''

      if (!state.oldPassword) {
        state.error = '请输入原密码'
        return false
      }

      const newPasswordError = validatePassword(state.newPassword)
      if (newPasswordError) {
        state.error = newPasswordError
        return false
      }

      if (state.newPassword !== state.confirmPassword) {
        state.error = '两次输入的密码不一致'
        return false
      }

      if (state.newPassword === state.oldPassword) {
        state.error = '新密码不能与当前密码相同'
        return false
      }

      // 添加详细的错误日志
      try {
        await user.updatePassword({
          old_password: state.oldPassword,
          new_password: state.newPassword,
          confirm_password: state.confirmPassword
        })
        ElMessage.success('密码修改成功')
        return true
      } catch (error) {
        console.log('密码修改失败，详细错误：', {
          status: error.response?.status,
          data: error.response?.data,
          message: error.response?.data?.message || error.message
        })
        state.error = error.response?.data?.message || '密码修改失败'
        return false
      }
    } finally {
      state.loading = false
    }
  }

  const strengthText = computed(() => {
    const strength = state.strength
    if (strength < 2) return '弱'      // 基础要求：字母+数字
    if (strength < 3) return '中'      // 添加了长度或特殊字符
    if (strength < 4) return '强'      // 添加了更多增强项
    return '非常强'                    // 包含全部增强项
  })

  const strengthTextClass = computed(() => {
    const strength = state.strength
    if (strength < 2) return 'text-red-500'
    if (strength < 3) return 'text-yellow-500'
    if (strength < 4) return 'text-green-500'
    return 'text-green-600'
  })

  const strengthColorClass = computed(() => {
    const strength = state.strength
    if (strength < 2) return 'bg-red-500'
    if (strength < 3) return 'bg-yellow-500'
    if (strength < 4) return 'bg-green-500'
    return 'bg-green-600'
  })

  return {
    state,
    handleUpdate,
    validatePassword,
    updatePasswordStrength,
    strengthText,
    strengthTextClass,
    strengthColorClass
  }
} 