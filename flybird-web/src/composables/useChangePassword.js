import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'

export function useChangePassword() {
  const userStore = useUserStore()
  const state = ref({
    oldPassword: '',
    newPassword: '',
    confirmPassword: '',
    loading: false,
    error: '',
    strength: 0
  })

  const validatePassword = (password) => {
    if (!password) return 0
    
    let strength = 0
    
    // 基本要求：长度至少8位
    if (password.length >= 8) strength++
    
    // 包含字母
    if (/[a-zA-Z]/.test(password)) strength++
    
    // 包含数字
    if (/\d/.test(password)) strength++
    
    // 额外加分项（可选）
    // 包含大写字母
    if (/[A-Z]/.test(password)) strength++
    
    // 包含特殊字符
    if (/[!@#$%^&*]/.test(password)) strength++
    
    return strength
  }

  const checkPasswordStrength = (password) => {
    let score = 0
    
    if (password.length >= 8) score += 1
    if (password.length >= 12) score += 1
    
    if (/[a-z]/.test(password)) score += 1
    if (/[A-Z]/.test(password)) score += 1
    if (/\d/.test(password)) score += 1
    if (/[!@#$%^&*]/.test(password)) score += 1
    
    return score
  }

  const updatePasswordStrength = (password) => {
    state.value.strength = checkPasswordStrength(password)
  }

  const isPasswordValid = computed(() => {
    const password = state.value.newPassword
    return password &&
           password.length >= 8 &&
           /[A-Za-z]/.test(password) &&
           /\d/.test(password)
  })

  const strengthText = computed(() => {
    const strength = state.value.strength
    if (strength <= 1) return '弱'
    if (strength <= 3) return '中'
    if (strength <= 5) return '强'
    return '非常强'
  })

  const strengthTextClass = computed(() => {
    const strength = state.value.strength
    if (strength <= 1) return 'text-red-500'
    if (strength <= 3) return 'text-yellow-500'
    if (strength <= 5) return 'text-green-500'
    return 'text-green-600'
  })

  const strengthColorClass = computed(() => {
    const strength = state.value.strength
    if (strength <= 1) return 'bg-red-500'
    if (strength <= 3) return 'bg-yellow-500'
    if (strength <= 5) return 'bg-green-500'
    return 'bg-green-600'
  })

  return {
    state,
    validatePassword,
    updatePasswordStrength,
    isPasswordValid,
    strengthText,
    strengthTextClass,
    strengthColorClass,
    userStore
  }
} 