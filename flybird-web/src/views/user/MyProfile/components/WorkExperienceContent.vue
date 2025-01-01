<template>
  <div class="space-y-4">
    <div v-for="item in data" :key="item.id" class="bg-gray-50 rounded-lg p-4">
      <!-- 标题栏 -->
      <div class="flex items-center justify-between mb-3">
        <div class="flex-1 min-w-0">
          <h4 class="text-base font-medium text-gray-900 break-words">{{ item.company }}</h4>
        </div>
        <div class="flex items-center space-x-2">
          <!-- 编辑按钮 -->
          <button
            @click="$emit('edit', item)"
            class="p-1 rounded-full hover:bg-gray-100 transition-colors duration-200"
            title="编辑"
          >
            <PencilSquareIcon class="w-5 h-5 text-gray-900 hover:text-gray-700" />
          </button>
          <!-- 删除按钮 -->
          <button
            @click="$emit('remove', item.id)"
            class="p-1 rounded-full hover:bg-gray-100 transition-colors duration-200"
            title="删除"
          >
            <TrashIcon class="w-5 h-5 text-gray-900 hover:text-red-600" />
          </button>
        </div>
      </div>

      <!-- 其他内容保持不变 -->
      <div class="flex items-center space-x-2">
        <span class="text-gray-600">{{ item.position }}</span>
        <span class="text-gray-500">·</span>
        <span class="text-sm text-gray-500 mt-1">
          {{ formatDateRange(item.start_date, item.end_date, item.is_current) }}
          <span v-if="item.duration" class="ml-1">({{ item.duration }})</span>
        </span>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="!data || data.length === 0" class="text-gray-400 text-center py-4">
      暂无工作经历，点击上方添加按钮新增
    </div>
  </div>
</template>

<script setup>
import { watch, computed } from 'vue'
import { 
  PencilSquareIcon, 
  TrashIcon 
} from '@heroicons/vue/24/outline'

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  }
})

defineEmits(['edit', 'remove'])

// 格式化日期范围
const formatDateRange = (startDate, endDate, isCurrent) => {
  if (!startDate) return ''
  
  const start = new Date(startDate).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'numeric'
  })
  
  if (isCurrent) {
    return `${start} - 至今`
  }
  
  if (endDate) {
    const end = new Date(endDate).toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'numeric'
    })
    return `${start} - ${end}`
  }
  
  return start
}

// 添加计算工作时长的函数
const calculateDuration = (startDate, endDate, isCurrent) => {
  if (!startDate) return ''
  
  const start = new Date(startDate)
  const end = isCurrent ? new Date() : (endDate ? new Date(endDate) : null)
  
  if (!end) return ''
  
  const years = end.getFullYear() - start.getFullYear()
  const months = end.getMonth() - start.getMonth()
  
  let totalMonths = years * 12 + months
  if (end.getDate() < start.getDate()) {
    totalMonths--
  }
  
  const finalYears = Math.floor(totalMonths / 12)
  const finalMonths = totalMonths % 12
  
  let duration = ''
  if (finalYears > 0) {
    duration += `${finalYears}年`
  }
  if (finalMonths > 0) {
    duration += `${finalMonths}个月`
  }
  
  return duration
}

// 添加计算属性处理工作经历数据
const workExperiences = computed(() => {
  return props.data?.map(item => ({
    ...item,
    duration: calculateDuration(item.start_date, item.end_date, item.is_current)
  })) || []
})

// 监听数据变化
watch(() => props.data, (newVal) => {
  // 移除所有 console.log
}, { immediate: true })
</script>

<style scoped>
.work-experience-content {
  @apply space-y-4;
}

/* 移动端适配 */
@media (max-width: 640px) {
  .work-experience-content {
    @apply space-y-3;
  }
}
</style> 