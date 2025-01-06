import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { auth } from '@/api/auth'
import { SMS_SCENE } from '@/constants'
import { showToast } from '@/components/ToastMessage'

export function useResetPassword() {
  const router = useRouter()
  
  const form = ref({
    phone: '',
    code: '',
    password: '',
    confirmPassword: ''
  })
  
  const loading = ref(false)
  const countdown = ref(0)
  const showPassword = ref(false)
  
  const isFormValid = computed(() => {
    return form.value.phone && 
           form.value.code && 
           form.value.password &&
           form.value.confirmPassword &&
           form.value.password === form.value.confirmPassword &&
           form.value.password.length >= 6 &&
           /^1[3-9]\d{9}$/.test(form.value.phone)
  })
  
  const validateForm = () => {
    const phoneRegex = /^1[3-9]\d{9}$/
    
    if (!form.value.phone) {
      showToast('请输入手机号', 'warning')
      return false
    }
    if (!phoneRegex.test(form.value.phone)) {
      showToast('请输入正确的手机号', 'warning')
      return false
    }
    if (!form.value.code) {
      showToast('请输入验证码', 'warning')
      return false
    }
    if (!form.value.password) {
      showToast('请输入新密码', 'warning')
      return false
    }
    if (form.value.password.length < 6) {
      showToast('密码长度不能少于6位', 'warning')
      return false
    }
    if (!form.value.confirmPassword) {
      showToast('请确认密码', 'warning')
      return false
    }
    if (form.value.confirmPassword !== form.value.password) {
      showToast('两次输入的密码不一致', 'warning')
      return false
    }
    return true
  }
  
  const startCountdown = () => {
    countdown.value = 60
    const timer = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        clearInterval(timer)
      }
    }, 1000)
  }
  
  const handleSendCode = async () => {
    if (!form.value.phone || !/^1[3-9]\d{9}$/.test(form.value.phone)) {
      showToast('请输入正确的手机号', 'warning')
      return
    }
    
    try {
      loading.value = true
      const response = await auth.sendVerifyCode({
        phone: form.value.phone,
        scene: SMS_SCENE.RESET_PASSWORD
      })

      if (response.data?.code === 200) {
        showToast('验证码已发送', 'success')
        startCountdown()
      } else {
        throw new Error(response.data?.message || '发送验证码失败')
      }
    } catch (error) {
      if (error.response?.data?.message?.includes('未注册')) {
        showToast('该手机号未注册，请先注册', 'warning')
        setTimeout(() => router.push('/register'), 1500)
        return
      }
      
      showToast(error.response?.data?.message || error.message || '发送验证码失败', 'error')
    } finally {
      loading.value = false
    }
  }
  
  const handleResetPassword = async () => {
    if (!validateForm()) return

    try {
      loading.value = true
      const response = await auth.resetPassword({
        phone: form.value.phone,
        code: form.value.code,
        new_password: form.value.password,
        confirm_password: form.value.confirmPassword
      })

      if (response.data?.code === 200) {
        showToast('密码重置成功', 'success')
        setTimeout(() => router.push('/login'), 1500)
      } else {
        throw new Error(response.data?.message || '重置密码失败')
      }
    } catch (error) {
      showToast(error.response?.data?.message || error.message || '重置密码失败', 'error')
    } finally {
      loading.value = false
    }
  }
  
  return {
    form,
    loading,
    countdown,
    showPassword,
    isFormValid,
    handleSendCode,
    handleResetPassword,
    togglePassword: () => showPassword.value = !showPassword.value
  }
} 