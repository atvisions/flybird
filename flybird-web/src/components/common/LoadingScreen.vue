<template>
  <div class="fixed inset-0 bg-gradient-to-br from-gray-900 to-gray-800 flex items-center justify-center z-50">
    <div class="text-center">
      <!-- 加载动画 -->
      <div class="relative w-24 h-24 mx-auto mb-8">
        <!-- 外圈旋转光环 -->
        <div class="absolute inset-0 border-4 border-rose-500/30 rounded-full animate-[spin_3s_linear_infinite]"></div>
        <div class="absolute inset-0 border-4 border-transparent border-t-rose-500 rounded-full animate-[spin_2s_linear_infinite]"></div>
        
        <!-- 内圈脉冲 -->
        <div class="absolute inset-4 bg-rose-500 rounded-full animate-[pulse_2s_ease-in-out_infinite]">
          <div class="w-full h-full bg-gradient-to-tr from-rose-600 to-rose-400 rounded-full"></div>
        </div>
        
        <!-- 光点环绕 -->
        <div class="absolute w-2 h-2 bg-rose-400 rounded-full top-0 left-1/2 -translate-x-1/2 animate-[bounce_1s_ease-in-out_infinite]"></div>
      </div>
      
      <!-- 加载文字 -->
      <h2 class="text-2xl font-bold text-white mb-4">正在准备编辑器</h2>
      <p class="text-rose-400 text-lg">{{ loadingText }}</p>
      
      <!-- 错误重试按钮 -->
      <template v-if="error">
        <p class="text-red-400 mt-4">{{ error }}</p>
        <button 
          @click="initialize"
          class="mt-4 px-6 py-2 bg-rose-500 text-white rounded-lg hover:bg-rose-600 transition-colors"
        >
          重试
        </button>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAccountStore } from '@/stores/account'
import { useRoute, useRouter } from 'vue-router'
import { templateApi } from '@/api/template'
import { ElMessage } from 'element-plus'

const props = defineProps({
  templateId: {
    type: [String, Number],
    required: true
  },
  mode: {
    type: String,
    required: true,
    validator: (value) => ['edit', 'use'].includes(value)
  }
})

const emit = defineEmits(['load-complete'])

const loadingText = ref('正在加载...')
const error = ref('')
const accountStore = useAccountStore()
const router = useRouter()

// 加载用户信息
const loadUserInfo = async () => {
  loadingText.value = '正在获取用户信息...'
  try {
    await accountStore.fetchUserInfo()
    if (!accountStore.userInfo?.id) {
      throw new Error('无法获取用户信息')
    }
    console.log('用户信息加载完成:', accountStore.userInfo.id)
  } catch (error) {
    console.error('加载用户信息失败:', error)
    throw new Error('无法获取用户信息')
  }
}

// 加载模板数据
const loadTemplateData = async () => {
  loadingText.value = '正在加载模板数据...'
  
  // 检查模板ID
  if (!props.templateId) {
    console.error('模板ID未定义')
    throw new Error('模板ID不能为空')
  }
  
  try {
    const response = await templateApi.getDetail(props.templateId)
    console.log('获取到模板数据:', response)

    const templateData = response.data
    
    // 仅在编辑模式下检查权限
    if (props.mode === 'edit') {
      const creator = templateData.creator
      if (Number(creator) !== Number(accountStore.userInfo?.id)) {
        console.log('权限检查:', { creator, userId: accountStore.userInfo?.id })
        throw new Error('没有权限编辑此模板')
      }
    }

    return templateData
  } catch (error) {
    if (error.response?.status === 404) {
      throw new Error('模板不存在')
    }
    throw error
  }
}

const initialize = async () => {
  error.value = '' // 清除之前的错误
  try {
    // 1. 先加载用户信息
    await loadUserInfo()
    
    // 2. 再加载模板数据
    const templateData = await loadTemplateData()
    
    // 3. 加载完成,发送数据
    loadingText.value = '初始化编辑器...'
    emit('load-complete', { success: true, templateData })

  } catch (error) {
    console.error('初始化失败:', error)
    error.value = error.message || '加载失败'
    emit('load-complete', { success: false, error: error.message })
  }
}

onMounted(() => {
  initialize()
})
</script>

<style scoped>
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(0.8);
    opacity: 0.8;
  }
  50% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes bounce {
  0%, 100% {
    transform: translateX(-50%) translateY(0);
  }
  50% {
    transform: translateX(-50%) translateY(-20px);
  }
}
</style> 