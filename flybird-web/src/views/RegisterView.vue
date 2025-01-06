<template>
  <div class="flex flex-col min-h-screen">
  <HeadView />
  <main class="flex-1 pt-14 relative z-[1] bg-gray-50">
    <div class="sm:mx-auto sm:w-full sm:max-w-md pt-8">
      <h2 class="mt-6 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">注册账号</h2>
    </div>
    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-[480px]">
      <div class="bg-white px-6 py-12 shadow sm:rounded-lg sm:px-12">
        <form class="space-y-6" @submit.prevent="handleRegister">
          <!-- 手机号输入 -->
          <div>
            <label for="phone" class="block text-sm font-medium leading-6 text-gray-900">手机号</label>
            <div class="mt-2">
              <input 
                id="phone" 
                v-model="form.phone" 
                type="text" 
                required
                placeholder="请输入手机号"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" 
              />
            </div>
          </div>

          <!-- 验证码输入 -->
          <div>
            <label for="code" class="block text-sm font-medium leading-6 text-gray-900">验证码</label>
            <div class="mt-2 flex">
              <div class="flex-grow">
                <input 
                  id="code" 
                  v-model="form.code" 
                  type="text" 
                  required
                  placeholder="请输入验证码"
                  class="block w-full rounded-l-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" 
                />
              </div>
              <button 
                type="button"
                @click="handleSendCode"
                :disabled="form.countdown > 0 || sendingCode"
                class="relative -ml-px whitespace-nowrap inline-flex items-center rounded-r-md px-6 py-2 text-sm font-semibold ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-10 w-[140px]"
                :class="form.countdown > 0 || sendingCode ? 'text-gray-400 bg-gray-50' : 'text-indigo-600'"
              >
                <svg v-if="sendingCode" class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span class="w-full text-center">
                  {{ sendingCode ? '发送中...' : form.countdown > 0 ? `${form.countdown}s` : '获取验证码' }}
                </span>
              </button>
            </div>
          </div>

          <!-- 密码输入 -->
          <div>
            <label for="password" class="block text-sm font-medium leading-6 text-gray-900">密码</label>
            <div class="mt-2 relative">
              <input 
                id="password" 
                v-model="form.password" 
                :type="showPassword ? 'text' : 'password'" 
                required
                placeholder="请输入密码"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" 
              />
              <button 
                type="button" 
                @click="togglePassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                <svg v-if="showPassword" class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                <svg v-else class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                </svg>
              </button>
            </div>
          </div>

          <!-- 确认密码输入 -->
          <div>
            <label for="confirmPassword" class="block text-sm font-medium leading-6 text-gray-900">确认密码</label>
            <div class="mt-2 relative">
              <input 
                id="confirmPassword" 
                v-model="form.confirmPassword"
                :type="showPassword ? 'text' : 'password'"
                required
                placeholder="请确认密码"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" 
              />
              <button 
                type="button" 
                @click="togglePassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                <svg v-if="showPassword" class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                <svg v-else class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                </svg>
              </button>
            </div>
          </div>

          <!-- 服务条款 -->
          <div class="flex items-center">
            <input 
              id="agree-terms" 
              v-model="agreed" 
              type="checkbox" 
              required
              class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600" 
            />
            <label for="agree-terms" class="ml-3 block text-sm leading-6 text-gray-900">
              我已阅读并同意
              <a href="#" class="font-semibold text-indigo-600 hover:text-indigo-500">服务条款</a>
              和
              <a href="#" class="font-semibold text-indigo-600 hover:text-indigo-500">隐私政策</a>
            </label>
          </div>

          <!-- 注册按钮 -->
          <div>
            <button 
              type="submit" 
              :disabled="!isFormValid || loading"
              class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ loading ? '注册中...' : '注册' }}
            </button>
          </div>
        </form>

        <!-- 登录链接 -->
        <div>
          <div class="relative mt-10">
            <div class="absolute inset-0 flex items-center" aria-hidden="true">
              <div class="w-full border-t border-gray-200"></div>
            </div>
            <div class="relative flex justify-center text-sm font-medium leading-6">
              <span class="bg-white px-6 text-gray-900">已有账号?</span>
            </div>
          </div>

          <div class="mt-6">
            <router-link 
              to="/login"
              class="flex w-full justify-center rounded-md bg-white px-3 py-1.5 text-sm font-semibold leading-6 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            >
              登录
            </router-link>
          </div>
        </div>
      </div>
    </div>

</main>
</div>
</template>

<script setup>
import { computed } from 'vue'
import HeadView from '@/components/HeadView.vue'
import { useRegister } from '@/composables/useRegister'

const {
  form,
  loading,
  sendingCode,
  agreed,
  showPassword,
  handleSendCode,
  handleRegister
} = useRegister()

// 表单是否有效
const isFormValid = computed(() => {
  return form.value.phone && 
         form.value.code && 
         form.value.password && 
         form.value.confirmPassword && 
         agreed.value
})

// 切换密码显示状态
const togglePassword = () => {
  showPassword.value = !showPassword.value
}
</script>