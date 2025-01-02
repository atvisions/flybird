import { ref, reactive } from 'vue'
import { auth } from '@/api/auth'
import { storage } from '@/utils/storage'
import { useStore } from 'vuex'
import request from '@/utils/request'

export function useLogin() {
  const store = useStore()
  const form = ref({
    account: '',
    password: '',
    code: '',
    rememberMe: false
  })

  const state = reactive({
    loading: false,
    sendingCode: false,
    showPassword: false,
    accountError: '',
    passwordError: ''
  })

  // 验证账号
  const validateAccount = () => {
    state.accountError = ''
    if (!form.value.account) {
      state.accountError = '请输入账号'
      return false
    }
    // 验证账号格式：手机号/邮箱/UID
    const phoneRegex = /^1[3-9]\d{9}$/
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    const uidRegex = /^\d+$/
    
    if (!phoneRegex.test(form.value.account) && 
        !emailRegex.test(form.value.account) && 
        !uidRegex.test(form.value.account)) {
      state.accountError = '请输入正确的手机号/邮箱/UID'
      return false
    }
    return true
  }

  // 验证密码
  const validatePassword = () => {
    state.passwordError = ''
    if (!form.value.password) {
      state.passwordError = '请输入密码'
      return false
    }
    if (form.value.password.length < 6) {
      state.passwordError = '密码长度不能少于6位'
      return false
    }
    return true
  }

  // 密码登录
  const handlePasswordLogin = async () => {
    if (!validateAccount() || !validatePassword()) {
      return false
    }

    try {
      state.loading = true
      const response = await auth.passwordLogin({
        account: form.value.account,
        password: form.value.password
      })

      if (response.data?.code === 200) {
        const { access, refresh } = response.data.data
        
        // 保存认证信息
        storage.saveAuth({
          access,
          refresh
        }, form.value.rememberMe)

        // 设置请求头的 token
        request.defaults.headers.common['Authorization'] = `Bearer ${access}`
        
        // 更新 store 中的登录状态
        await store.dispatch('fetchUserInfo')
        store.commit('SET_TOKEN', access)
        store.commit('SET_REFRESH_TOKEN', refresh)
        store.commit('SET_LOGGED_IN', true)

        // 如果选择记住我，保存账号
        if (form.value.rememberMe) {
          storage.saveAccount(form.value.account)
        }

        return true
      }
      return false
    } finally {
      state.loading = false
    }
  }

  // 验证码登录
  const handleCodeLogin = async () => {
    // ... 验证码登录逻辑 ...
  }

  return {
    form,
    state,
    handlePasswordLogin,
    validateAccount,
    validatePassword
  }
} 