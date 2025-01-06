<template>
  <div class="flex flex-col min-h-screen">
    <HeadView />
    <main class="flex-1 pt-14 relative z-[1] bg-gray-50">
      <!-- Logo 部分 -->
      <div class="sm:mx-auto sm:w-full sm:max-w-md pt-8">
        <h2 class="mt-6 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">登录账号</h2>
      </div>

      <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-[480px]">
        <div class="bg-white px-6 py-12 shadow sm:rounded-lg sm:px-12">
          <form class="space-y-6" @submit.prevent="handleLogin">
            <!-- 手机号输入 -->
            <div>
              <label for="account" class="block text-sm font-medium leading-6 text-gray-900">账号</label>
              <div class="mt-2">
                <input 
                  type="text" 
                  id="account" 
                  v-model="loginManager.form.value.account"
                  @input="handleAccountInput"
                  required
                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6 px-3"
                  :class="{'ring-red-300': loginManager.state.accountError}"
                  placeholder="请输入手机号/邮箱/UID"
                >
                <div v-if="loginManager.state.accountError" class="mt-1 text-sm text-red-600">{{ loginManager.state.accountError }}</div>
              </div>
            </div>

            <!-- 密码输入 -->
            <div>
              <label for="password" class="block text-sm font-medium text-gray-700">密码</label>
              <div class="mt-2 relative">
                <input 
                  :type="loginManager.state.showPassword ? 'text' : 'password'"
                  id="password"
                  v-model="loginManager.form.value.password"
                  @input="handlePasswordInput"
                  required
                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6 px-3 pr-10"
                  :class="{'ring-red-300': loginManager.state.passwordError}"
                >
                <button 
                  type="button"
                  @click="togglePassword"
                  class="absolute inset-y-0 right-0 flex items-center pr-3"
                >
                  <!-- 密码显示/隐藏图标 -->
                  <svg v-if="loginManager.state.showPassword" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  <svg v-else class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                  </svg>
                </button>
              </div>
              <div v-if="loginManager.state.passwordError" class="mt-1 text-sm text-red-600">{{ loginManager.state.passwordError }}</div>
            </div>

            <!-- 记住我和忘记密码 -->
            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <input
                  id="remember-me"
                  v-model="loginManager.form.value.rememberMe"
                  type="checkbox"
                  class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                />
                <label for="remember-me" class="ml-2 block text-sm text-gray-900">
                  记住我
                </label>
              </div>

              <div class="text-sm">
                <router-link to="/reset-password" class="font-medium text-primary-600 hover:text-primary-500">
                  忘记密码？
                </router-link>
              </div>
            </div>

            <!-- 登录按钮 -->
            <div>
              <button 
                type="submit"
                :disabled="!isFormValid"
                class="flex w-full justify-center rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <svg v-if="loginManager.state.loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ loginManager.state.loading ? '登录中...' : '登录' }}
              </button>
            </div>
          </form>

          <!-- 其他登录方式 -->
          <div class="mt-6">
            <div class="relative">
              <div class="absolute inset-0 flex items-center">
                <div class="w-full border-t border-gray-300"></div>
              </div>
              <div class="relative flex justify-center text-sm">
                <span class="bg-white px-2 text-gray-500">其他登录方式</span>
              </div>
            </div>

            <div class="mt-6 grid grid-cols-3 gap-3">
              <div>
                <button
                  @click="handleWeChatClick" 
                  class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                >
                  <span class="sr-only">微信登录</span>
                  <svg class="w-5 h-5 text-green-600" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M8.667 15.273c-.328 0-.593-.265-.593-.593v-1.778a.592.592 0 0 1 1.186 0v1.778c0 .328-.265.593-.593.593zm6.666 0c-.328 0-.593-.265-.593-.593v-1.778a.592.592 0 0 1 1.186 0v1.778c0 .328-.265.593-.593.593z"/>
                    <path d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm5.918 12.08c-.533 2.923-3.982 5.012-7.918 4.37-2.718-.444-4.963-2.165-5.735-4.37-.844-2.413.437-4.693 2.735-5.912.842-.446 1.777-.724 2.735-.832.437-.049.877-.073 1.318-.073 1.683 0 3.23.446 4.503 1.208 1.41.841 2.333 2.083 2.432 3.49.05.706-.095 1.406-.432 2.032-.535.99-1.563 1.756-2.9 2.165-1.096.336-2.245.361-3.368.073-.89-.227-1.683-.631-2.333-1.208-.437-.384-.706-.841-.816-1.333-.073-.336.024-.681.267-.927.242-.242.583-.339.915-.266.339.073.63.291.78.582.145.29.436.532.824.678.63.242 1.37.266 2.023.073.824-.242 1.37-.752 1.37-1.284 0-.532-.533-1.018-1.37-1.26-.63-.193-1.37-.169-2.023.073-.388.146-.679.388-.824.679-.145.29-.436.508-.78.581-.332.073-.673-.024-.915-.266-.243-.242-.34-.587-.267-.923.11-.492.379-.95.816-1.333.65-.577 1.443-.981 2.333-1.208 1.123-.288 2.272-.263 3.368.073 1.337.409 2.365 1.175 2.9 2.165.337.626.482 1.326.432 2.032-.099 1.407-1.022 2.649-2.432 3.49-1.273.762-2.82 1.208-4.503 1.208-.441 0-.881-.024-1.318-.073-.958-.108-1.893-.386-2.735-.832-2.298-1.219-3.579-3.499-2.735-5.912.772-2.205 3.017-3.926 5.735-4.37 3.936-.642 7.385 1.447 7.918 4.37z"/>
                  </svg>
                </button>
              </div>

              <div>
                <a href="#" class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                  <span class="sr-only">QQ登录</span>
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12.003 2c-2.265 0-6.29 1.364-6.29 7.325v1.195S3.55 14.96 3.55 17.474c0 .665.17 1.025.281 1.025.114 0 .902-.484 1.748-2.072 0 0-.18 2.197 1.904 3.967 0 0-1.77.495-1.77 1.182 0 .686 4.078.43 6.29.43 2.213 0 6.29.256 6.29-.43 0-.687-1.77-1.182-1.77-1.182s2.085-1.77 1.905-3.967c.846 1.588 1.634 2.072 1.746 2.072.111 0 .283-.36.283-1.025 0-2.514-2.166-6.954-2.166-6.954V9.325C18.29 3.364 14.268 2 12.003 2z"/>
                  </svg>
                </a>
              </div>

              <div>
                <a href="#" class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                  <span class="sr-only">微博登录</span>
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M10.098 20.323c-3.977.391-7.414-1.406-7.672-4.02-.259-2.609 2.759-5.047 6.74-5.441 3.979-.394 7.413 1.404 7.672 4.018.259 2.6-2.759 5.049-6.74 5.443z"/>
                  </svg>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import HeadView from '@/components/HeadView.vue'
import { showToast } from '@/components/ToastMessage'
import { auth } from '@/api/auth'
import { STORAGE_KEYS } from '@/utils/storage'
import { ElMessage } from 'element-plus'
import { authService } from '@/services/authService'
import { useLogin } from '@/composables/useLogin'

const router = useRouter()
const store = useStore()

// 使用 useLogin composable
const loginManager = useLogin()  // 创建一个实例

// 修改表单验证状态
const isFormValid = computed(() => {
  return loginManager.form.value.account && 
         loginManager.form.value.password && 
         !loginManager.state.loading && 
         !loginManager.state.accountError && 
         !loginManager.state.passwordError
})

// 修改手机号验证
const validateAccount = () => {
  loginManager.state.accountError = ''
  if (!loginManager.form.value.account) {
    loginManager.state.accountError = '请输入账号'
    return false
  }
  // 验证账号格式：手机号/邮箱/UID
  const phoneRegex = /^1[3-9]\d{9}$/
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  const uidRegex = /^\d+$/
  
  if (!phoneRegex.test(loginManager.form.value.account) && 
      !emailRegex.test(loginManager.form.value.account) && 
      !uidRegex.test(loginManager.form.value.account)) {
    loginManager.state.accountError = '请输入正确的手机号/邮箱/UID'
    return false
  }
  return true
}

// 修改密码验证
const validatePassword = () => {
  loginManager.state.passwordError = ''
  if (!loginManager.form.value.password) {
    loginManager.state.passwordError = '请输入密码'
    return false
  }
  if (loginManager.form.value.password.length < 6) {
    loginManager.state.passwordError = '密码长度不能少于6位'
    return false
  }
  return true
}

// 表单验证
const validateForm = () => {
  const isAccountValid = validateAccount()
  const isPasswordValid = validatePassword()
  return isAccountValid && isPasswordValid
}

// 处理登录错误
const handleLoginError = (error) => {
  console.error('登录失败:', error)
  
  // 处理特定错误
  if (error.response?.data?.detail) {
    if (error.response.data.detail.includes('不存在')) {
      showToast('账号不存在，请先注册', 'warning')
      setTimeout(() => {
        router.push('/register')
      }, 1500)
      return
    }
    if (error.response.data.detail.includes('密码错误')) {
      showToast('密码错误，请重试或找回密码', 'error')
      return
    }
  }
  
  // 处理其他错误
  const errorMessage = error.response?.data?.detail || 
                      error.response?.data?.message || 
                      error.message || 
                      '登录失败，请重试'
  showToast(errorMessage, 'error')
}

// 处理登录
const handleLogin = async () => {
  if (!validateAccount() || !validatePassword()) return
  
  try {
    loginManager.state.loading = true
    const success = await loginManager.handlePasswordLogin()
    
    if (success) {
      // 等待用户信息加载完成
      await store.dispatch('fetchUserInfo')
      showToast('登录成功', 'success')
      
      // 获取 redirect 参数，如果没有则默认跳转到首页
      const redirect = router.currentRoute.value.query.redirect || '/'
      router.push(redirect)
    }
  } catch (error) {
    console.error('登录失败:', error)
    handleLoginError(error)
  } finally {
    loginManager.state.loading = false
  }
}

// 切换密码显示
const togglePassword = () => {
  loginManager.state.showPassword = !loginManager.state.showPassword
}

// 输入事件处理
const handleAccountInput = () => {
  if (loginManager.state.accountError) {
    loginManager.validateAccount()
  }
}

const handlePasswordInput = () => {
  if (loginManager.state.passwordError) {
    loginManager.validatePassword()
  }
}

// 检查登录状态
onMounted(async () => {
  const isAuthenticated = await store.dispatch('checkAuth')
  if (isAuthenticated) {
    const redirect = router.currentRoute.value.query.redirect || '/'
    router.push(redirect)
  }
})

// 在组件挂载时恢复记住我状态
onMounted(() => {
  const savedRememberMe = localStorage.getItem(STORAGE_KEYS.REMEMBER_ME)
  if (savedRememberMe !== null) {
    loginManager.form.value.rememberMe = savedRememberMe === 'true'  // 更新 form 中的 rememberMe
  }
})

// 添加 watch 监听 rememberMe 的变化
watch(() => loginManager.form.value.rememberMe, (newValue) => {  // 监听 form 中的 rememberMe
  if (!newValue) {
    localStorage.removeItem(STORAGE_KEYS.REMEMBERED_PHONE)
    localStorage.removeItem(STORAGE_KEYS.REMEMBER_ME)
    localStorage.removeItem(STORAGE_KEYS.TOKEN)
    localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN)
    localStorage.removeItem(STORAGE_KEYS.TOKEN_EXPIRES)
  }
  localStorage.setItem(STORAGE_KEYS.REMEMBER_ME, newValue.toString())
})

// 在组件卸载时，如果没有选择记住我，清除相关信息
onUnmounted(() => {
  if (!loginManager.form.value.rememberMe) {  // 使用 form 中的 rememberMe
    localStorage.removeItem(STORAGE_KEYS.REMEMBERED_PHONE)
    localStorage.removeItem(STORAGE_KEYS.REMEMBER_ME)
  }
})
</script>