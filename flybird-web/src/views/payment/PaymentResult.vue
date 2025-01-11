<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-white py-16">
    <HeadView />
    
    <div class="max-w-3xl mx-auto px-4 py-16 sm:py-24">
      <!-- 等待状态 -->
      <div v-if="status === 'pending'" class="text-center">
        <div class="mb-8">
          <div class="relative mx-auto h-24 w-24">
            <svg class="absolute inset-0 h-full w-full text-blue-100 animate-spin-slow" viewBox="0 0 100 100">
              <circle cx="50" cy="50" r="45" stroke="currentColor" stroke-width="8" fill="none" />
            </svg>
            <svg class="absolute inset-0 h-full w-full text-blue-500 animate-spin" viewBox="0 0 100 100">
              <circle 
                cx="50" cy="50" r="45" 
                stroke="currentColor" 
                stroke-width="8" 
                fill="none"
                stroke-dasharray="180 300"
              />
            </svg>
          </div>
        </div>
        <h2 class="text-2xl font-bold text-gray-900 mb-4">正在处理支付结果</h2>
        <p class="text-gray-500">请稍候，正在验证支付状态...</p>
      </div>

      <!-- 成功状态 -->
      <div v-else-if="status === 'success'" class="text-center">
        <div class="mb-12">
          <div class="relative mx-auto h-24 w-24">
            <!-- 成功动画背景 -->
            <div class="absolute inset-0 rounded-full bg-green-100 animate-ping-slow"></div>
            <!-- 成功图标 -->
            <div class="relative flex items-center justify-center h-full w-full">
              <svg class="h-16 w-16 text-green-500 animate-success" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path 
                  stroke-linecap="round" 
                  stroke-linejoin="round" 
                  stroke-width="2" 
                  d="M5 13l4 4L19 7"
                />
              </svg>
            </div>
          </div>
        </div>
        
        <h2 class="text-3xl font-bold text-gray-900 mb-4">支付成功</h2>
        <p class="text-lg text-gray-600 mb-12">您的会员已经开通，立即开始享受会员权益吧！</p>
        
        <div class="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-6">
          <router-link 
            to="/user?tab=membership" 
            class="w-full sm:w-auto inline-flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-lg shadow-sm text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 transition-all duration-200"
          >
            <svg class="w-5 h-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 2a8 8 0 100 16 8 8 0 000-16zm0 14a6 6 0 100-12 6 6 0 000 12zm1-7a1 1 0 10-2 0v3a1 1 0 102 0V9z" clip-rule="evenodd" />
            </svg>
            查看会员信息
          </router-link>
          
          <router-link 
            to="/" 
            class="w-full sm:w-auto inline-flex items-center justify-center px-8 py-3 border border-gray-300 text-base font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 transition-all duration-200"
          >
            <svg class="w-5 h-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" clip-rule="evenodd" />
            </svg>
            返回首页
          </router-link>
        </div>
      </div>

      <!-- 失败状态 -->
      <div v-else class="text-center">
        <div class="mb-12">
          <div class="relative mx-auto h-24 w-24">
            <!-- 失败动画背景 -->
            <div class="absolute inset-0 rounded-full bg-red-100 animate-pulse"></div>
            <!-- 失败图标 -->
            <div class="relative flex items-center justify-center h-full w-full">
              <svg class="h-16 w-16 text-red-500 animate-error" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path 
                  stroke-linecap="round" 
                  stroke-linejoin="round" 
                  stroke-width="2" 
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </div>
          </div>
        </div>
        
        <h2 class="text-3xl font-bold text-gray-900 mb-4">支付失败</h2>
        <p class="text-lg text-gray-600 mb-3">抱歉，支付过程中出现了问题</p>
        <p class="text-base text-gray-500 mb-12">{{ errorMessage }}</p>
        
        <div class="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-6">
          <router-link 
            to="/pro" 
            class="w-full sm:w-auto inline-flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-lg shadow-sm text-white bg-gradient-to-r from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700 transition-all duration-200"
          >
            <svg class="w-5 h-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" />
            </svg>
            重新支付
          </router-link>
          
          <router-link 
            to="/" 
            class="w-full sm:w-auto inline-flex items-center justify-center px-8 py-3 border border-gray-300 text-base font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 transition-all duration-200"
          >
            <svg class="w-5 h-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" clip-rule="evenodd" />
            </svg>
            返回首页
          </router-link>
        </div>
      </div>
    </div>

    <FootView />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import HeadView from '@/components/HeadView.vue'
import FootView from '@/components/FootView.vue'
import { membership } from '@/api/membership'
import { showToast } from '@/components/ToastMessage'
import { useAccountStore } from '@/stores/account'

const accountStore = useAccountStore()
const route = useRoute()
const status = ref('pending')
const errorMessage = ref('')
const maxRetries = 5
const retryInterval = 2000
let retryCount = 0

const errorMessages = {
  'order_not_found': '订单不存在',
  'verify_failed': '支付验证失败',
  'system_error': '系统错误',
  'unknown': '未知错误'
}

const verifyPayment = async (orderNo) => {
  try {
    status.value = 'pending'
    const response = await membership.verifyPayment(orderNo)
    
    if (response?.data?.code === 200) {
      await accountStore.fetchUserInfo()
      
      status.value = 'success'
      showToast('支付成功', 'success')
      
      window.dispatchEvent(new Event('payment-success'))
      return true
    } else if (response?.data?.code === 400) {
      if (retryCount < maxRetries) {
        retryCount++
        console.log(`支付验证重试 ${retryCount}/${maxRetries}`)
        await new Promise(resolve => setTimeout(resolve, retryInterval))
        return await verifyPayment(orderNo)
      }
      status.value = 'fail'
      errorMessage.value = response?.data?.message || '支付验证失败'
      showToast(errorMessage.value, 'error')
      return false
    }
    status.value = 'fail'
    errorMessage.value = response?.data?.message || '支付验证失败'
    showToast(errorMessage.value, 'error')
    return false
  } catch (error) {
    console.error('支付验证失败:', error)
    status.value = 'fail'
    errorMessage.value = error?.response?.data?.message || '系统错误'
    showToast('支付验证失败', 'error')
    return false
  }
}

onMounted(async () => {
  // 从URL参数中获取支付状态
  const reason = route.query.reason
  if (reason) {
    status.value = 'fail'
    errorMessage.value = errorMessages[reason] || '支付失败，请重试'
  } else {
    // 处理支付宝回调
    const orderNo = route.query.out_trade_no
    if (orderNo) {
      status.value = 'pending'
      await verifyPayment(orderNo)
    }
  }
})
</script> 

<style scoped>
.animate-ping-slow {
  animation: ping 2s cubic-bezier(0, 0, 0.2, 1) infinite;
}

.animate-spin-slow {
  animation: spin 3s linear infinite;
}

.animate-success {
  animation: success 0.5s ease-out forwards;
}

.animate-error {
  animation: error 0.5s ease-out forwards;
}

@keyframes success {
  0% {
    transform: scale(0.5);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes error {
  0% {
    transform: scale(0.5) rotate(-45deg);
    opacity: 0;
  }
  100% {
    transform: scale(1) rotate(0);
    opacity: 1;
  }
}
</style> 