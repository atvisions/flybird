import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { auth } from '@/api/auth'
import { SMS_SCENE } from '@/constants'
import { showToast } from '@/components/ToastMessage'
import { STORAGE_KEYS } from '@/utils/storage'
import { getExpirationInfo } from '@/utils/auth'

export function useLogin() {
  const store = useStore()
  const router = useRouter()
  
  // 表单数据
  const form = ref({
    phone: localStorage.getItem(STORAGE_KEYS.REMEMBERED_PHONE) || '',
    password: '',
    code: '',
    rememberMe: localStorage.getItem(STORAGE_KEYS.REMEMBER_ME) === 'true',
    countdown: 0
  })
  
  // 状态
  const loading = ref(false)
  const sendingCode = ref(false)
  const showPassword = ref(false)
  const phoneError = ref('')
  const passwordError = ref('')

  // 处理密码登录
  const handlePasswordLogin = async () => {
    try {
      loading.value = true
      console.log('Login with remember me:', form.value.rememberMe)
      
      const response = await auth.loginWithPassword({
        phone: form.value.phone,
        password: form.value.password
      })

      if (response.data?.code === 200) {
        const { access, refresh } = response.data.data
        await store.dispatch('login', {
          access,
          refresh,
          rememberMe: form.value.rememberMe
        })
        
        console.log('Login successful:', {
          rememberMe: form.value.rememberMe,
          tokenInfo: getExpirationInfo(),
          savedPhone: localStorage.getItem(STORAGE_KEYS.REMEMBERED_PHONE),
          savedRememberMe: localStorage.getItem(STORAGE_KEYS.REMEMBER_ME)
        })
        
        showToast('登录成功', 'success')
        router.push('/user')
      }
    } catch (error) {
      handleLoginError(error)
    } finally {
      loading.value = false
    }
  }

  // 处理验证码登录
  const handleCodeLogin = async () => {
    try {
      loading.value = true
      const response = await auth.loginWithCode({
        phone: form.value.phone,
        code: form.value.code
      })

      if (response.data?.code === 200) {
        const { access, refresh } = response.data.data
        await store.dispatch('login', {
          access,
          refresh,
          rememberMe: form.value.rememberMe  // 传递记住我状态
        })
        
        showToast('登录成功', 'success')
        router.push('/user')
      }
    } catch (error) {
      handleError(error)
    } finally {
      loading.value = false
    }
  }

  // 其他代码保持不变...

  return {
    form,
    loading,
    sendingCode,
    showPassword,
    phoneError,
    passwordError,
    handlePasswordLogin,
    handleCodeLogin,
    // ...其他返回值
  }
} 