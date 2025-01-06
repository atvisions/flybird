import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { auth } from '@/api/auth'
import { SMS_SCENE } from '@/constants'
import { showToast } from '@/components/ToastMessage'

export function useRegister() {
  const router = useRouter()
  const store = useStore()
  
  // 表单数据
  const form = ref({
    phone: '',
    code: '',
    password: '',
    confirmPassword: '',
    countdown: 0
  })
  
  // 状态
  const loading = ref(false)
  const sendingCode = ref(false)
  const agreed = ref(false)
  const showPassword = ref(false)

  // 表单验证
  const validateForm = () => {
    if (!form.value.phone || !form.value.code || !form.value.password || !form.value.confirmPassword) {
      showToast('请填写完整信息', 'warning')
      return false
    }

    // 验证两次密码是否一致
    if (form.value.password !== form.value.confirmPassword) {
      showToast('两次输入的密码不一致', 'warning')
      return false
    }

    return true
  }


  // 处理错误
  const handleError = (error, { type, onRegistered }) => {
    // 处理限速错误
    if (error.isRateLimit) {
      const minutes = Math.ceil(error.retryAfter / 60)
      showToast(`操作过于频繁，请在 ${minutes} 分钟后重试`, 'warning')
      return
    }

    const errorData = error.response?.data
    
    // 处理已注册错误
    if (errorData?.errors?.phone?.[0]?.includes('已注册')) {
      showToast('手机号已注册', 'warning')
      onRegistered?.()
      return
    }
    
    // 处理验证码错误
    if (errorData?.errors?.code?.[0]?.includes('验证码')) {
      showToast('验证码错误或已过期，请重新获取', 'error')
      return
    }
    
    // 处理其他业务错误
    if (errorData?.message) {
      showToast(errorData.message, 'error')
      return
    }
    
    // 处理默认错误
    const defaultMessages = {
      sendCode: '发送验证码失败，请稍后重试',
      register: '注册失败，请稍后重试'
    }
    showToast(defaultMessages[type], 'error')
  }

  // 添加 startCountdown 函数
  const startCountdown = () => {
    form.value.countdown = 60
    const timer = setInterval(() => {
      form.value.countdown--
      if (form.value.countdown <= 0) {
        clearInterval(timer)
      }
    }, 1000)
  }

  const handleSendCode = async () => {
    // 先检查手机号是否为空
    if (!form.value.phone) {
      showToast('请输入手机号', 'warning')
      return
    }
    
    // 再检查手机号格式是否正确
    if (!/^1[3-9]\d{9}$/.test(form.value.phone)) {
      showToast('请输入正确的手机号', 'warning')
      return
    }
    
    try {
      sendingCode.value = true
      const response = await auth.sendVerifyCode({
        phone: form.value.phone,
        scene: SMS_SCENE.REGISTER
      })

      if (response.data?.code === 200) {
        showToast('验证码已发送', 'success')
        startCountdown()
      } else {
        throw new Error(response.data?.message || '发送验证码失败')
      }
    } catch (error) {
      // 直接使用错误信息显示
      showToast(error.response?.data?.message || error.message || '发送验证码失败', 'error')
    } finally {
      sendingCode.value = false
    }
  }

  // 注册处理
  const handleRegister = async () => {
    if (!validateForm()) return
    
    try {
      loading.value = true
      
      // 1. 注册 - 修改请求数据结构
      const registerResponse = await auth.register({
        phone: form.value.phone.trim(),
        code: form.value.code,
        password: form.value.password,
        confirm_password: form.value.password
      })

      if (!registerResponse.data || registerResponse.data.code !== 200) {
        throw new Error(registerResponse.data?.message || '注册失败')
      }

      // 2. 从响应中获取 tokens
      const { access, refresh } = registerResponse.data.data

      // 3. 更新 store 状态
      await store.dispatch('login', {
        access,
        refresh,
        rememberMe: false
      })

      showToast('注册成功', 'success')

      // 4. 等待一下再跳转
      await new Promise(resolve => setTimeout(resolve, 300))
      router.push('/user')
    } catch (error) {
      console.error('注册失败:', error)
      handleError(error, {
        type: 'register',
        onRegistered: () => router.push('/login')
      })
    } finally {
      loading.value = false
    }
  }

  return {
    form,
    loading,
    sendingCode,
    agreed,
    showPassword,
    handleRegister,
    handleSendCode
  }
} 