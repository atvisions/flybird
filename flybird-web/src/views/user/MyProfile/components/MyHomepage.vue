<template>
  <div class="bg-white rounded-lg shadow">
    <div class="px-6 py-4 border-b border-gray-200">
      <h3 class="text-lg font-medium text-gray-900">我的主页</h3>
    </div>
    <div class="p-6">
      <!-- 主页预览卡片 -->
      <div class="mb-6 p-4 bg-gray-50 rounded-lg overflow-hidden">
        <div class="flex items-center mb-4">
          <img 
            :src="userInfo.avatar || 'https://picsum.photos/200/200'" 
            class="w-16 h-16 rounded-full"
            alt="头像"
          >
          <div class="ml-4">
            <h4 class="text-lg font-medium text-gray-900">{{ userInfo.name }}</h4>
            <p class="text-sm text-gray-500">{{ userInfo.title }}</p>
          </div>
        </div>
        <p class="text-gray-600">{{ userInfo.bio }}</p>
      </div>

      <!-- 主页链接 -->
      <div class="space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center gap-4 p-4 bg-gray-50 rounded-lg">
          <div class="flex-1 mr-4">
            <p class="text-sm text-gray-500 mb-1">我的主页链接</p>
            <div class="flex items-center">
              <span class="text-gray-900 truncate text-sm">{{ pageUrl }}</span>
            </div>
          </div>
          <div class="flex items-center space-x-2 w-full sm:w-auto justify-end">
            <button 
              @click="copyLink"
              class="flex-1 sm:flex-none inline-flex items-center justify-center px-3 py-1.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
            >
              <DocumentDuplicateIcon class="w-4 h-4 mr-1" />
              复制链接
            </button>
            <a 
              :href="pageUrl"
              target="_blank"
              class="flex-1 sm:flex-none inline-flex items-center justify-center px-3 py-1.5 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700"
            >
              <ArrowTopRightOnSquareIcon class="w-4 h-4 mr-1" />
              访问主页
            </a>
          </div>
        </div>

        <!-- 二维码分享 -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between p-4 bg-gray-50 rounded-lg">
          <div>
            <p class="text-sm text-gray-500 mb-1">主页二维码</p>
            <p class="text-xs text-gray-400">扫描二维码，在手机上查看</p>
          </div>
          <div class="w-24 h-24 bg-white p-2 rounded-lg mt-4 sm:mt-0 mx-auto sm:mx-0">
            <!-- 这里需要集成二维码生成库 -->
            <img 
              :src="qrCodeUrl" 
              class="w-full h-full"
              alt="二维码"
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { 
  DocumentDuplicateIcon, 
  ArrowTopRightOnSquareIcon 
} from '@heroicons/vue/24/outline'
import { showToast } from '@/components/ToastMessage'

// 模拟用户数据
const userInfo = ref({
  name: '张三',
  title: '高级前端工程师',
  avatar: 'https://picsum.photos/200/200',
  bio: '热爱技术，专注于前端开发和用户体验设计。5年+开发经验，擅长Vue.js和React技术栈。'
})

// 生成页面URL
const pageUrl = computed(() => {
  return `${window.location.origin}/u/${userInfo.value.name}`
})

// 生成二维码URL（这里需要集成二维码生成库）
const qrCodeUrl = computed(() => {
  // 临时使用示例图片
  return 'https://picsum.photos/200/200'
})

// 复制链接
const copyLink = async () => {
  try {
    await navigator.clipboard.writeText(pageUrl.value)
    showToast('链接已复制到剪贴板', 'success')
  } catch (error) {
    showToast('复制失败，请手动复制', 'error')
  }
}
</script> 