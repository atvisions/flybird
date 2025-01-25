<template>
  <div 
    class="fixed inset-0 bg-white z-50 flex flex-col items-center justify-center"
    :class="{ 'opacity-0 pointer-events-none': !show }"
  >
    <div class="flex flex-col items-center">
      <div class="w-16 h-16 mb-4">
        <svg class="animate-spin" viewBox="0 0 24 24">
          <circle 
            class="opacity-25" 
            cx="12" 
            cy="12" 
            r="10" 
            stroke="currentColor" 
            stroke-width="4"
            fill="none"
          />
          <path 
            class="opacity-75" 
            fill="currentColor" 
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
      </div>
      <p class="text-gray-600 text-lg">{{ message || '加载中...' }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  loading: {
    type: Boolean,
    required: true
  },
  message: {
    type: String,
    default: ''
  },
  minLoadingTime: {
    type: Number,
    default: 2000 // 最小加载时间（2秒）
  }
})

const emit = defineEmits(['loading-complete'])

const show = ref(true)
const startTime = ref(0)
let loadingCompleteTimeout = null
const loadingFinished = ref(false)
const minTimeReached = ref(false)

// 检查是否可以完成加载
const checkComplete = () => {
  if (loadingFinished.value && minTimeReached.value) {
    show.value = false
    emit('loading-complete')
  }
}

// 监听 loading 状态变化
watch(() => props.loading, (newLoading) => {
  if (newLoading) {
    // 重置状态
    loadingFinished.value = false
    minTimeReached.value = false
    if (loadingCompleteTimeout) {
      clearTimeout(loadingCompleteTimeout)
      loadingCompleteTimeout = null
    }
    // 开始加载时记录时间
    startTime.value = Date.now()
    show.value = true
    
    // 设置最小加载时间定时器
    loadingCompleteTimeout = setTimeout(() => {
      minTimeReached.value = true
      checkComplete()
    }, props.minLoadingTime)
  } else {
    // 标记加载完成
    loadingFinished.value = true
    checkComplete()
  }
}, { immediate: true })

// 组件挂载时记录开始时间
onMounted(() => {
  startTime.value = Date.now()
  // 设置最小加载时间定时器
  loadingCompleteTimeout = setTimeout(() => {
    minTimeReached.value = true
    checkComplete()
  }, props.minLoadingTime)
})

// 组件卸载时清理定时器
onUnmounted(() => {
  if (loadingCompleteTimeout) {
    clearTimeout(loadingCompleteTimeout)
    loadingCompleteTimeout = null
  }
})
</script>

<style scoped>
.opacity-0 {
  opacity: 0;
}

.pointer-events-none {
  pointer-events: none;
}

svg {
  color: #1890ff;
}

/* 添加过渡效果 */
.fixed {
  transition: opacity 0.3s ease-in-out;
}
</style> 