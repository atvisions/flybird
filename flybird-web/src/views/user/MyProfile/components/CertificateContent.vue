<template>
  <div class="space-y-4">
    <!-- 证书列表 -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div 
        v-for="(cert, index) in data" 
        :key="index" 
        class="bg-gray-50 rounded-lg border border-gray-100 p-4 hover:shadow-sm transition-all"
      >
        <!-- 证书头部 -->
        <div class="flex items-start justify-between mb-3">
          <div class="flex-1 min-w-0">
            <h4 class="text-base font-medium text-gray-900 break-words">{{ cert.name }}</h4>
            <div class="text-sm text-gray-500 mt-1">
              {{ cert.issuing_authority }}
            </div>
          </div>
          <div class="flex items-center space-x-2 ml-4">
            <button
              @click="$emit('edit', cert)"
              class="p-1 hover:bg-white rounded-full transition-colors"
            >
              <PencilSquareIcon class="w-4 h-4 text-gray-400" />
            </button>
            <button
              @click="$emit('delete', cert.id)"
              class="p-1 hover:bg-white rounded-full transition-colors"
            >
              <TrashIcon class="w-4 h-4 text-gray-400" />
            </button>
          </div>
        </div>

        <!-- 证书信息 -->
        <div class="space-y-2">
          <!-- 日期信息 -->
          <div class="flex items-center text-sm text-gray-500">
            <CalendarIcon class="w-4 h-4 mr-1.5 text-gray-400" />
            <span>颁发日期：{{ formatDate(cert.issue_date) }}</span>
            <span v-if="cert.expiry_date" class="ml-2">
              到期日期：{{ formatDate(cert.expiry_date) }}
            </span>
          </div>

          <!-- 证书编号 -->
          <div v-if="cert.credential_id" class="flex items-center text-sm text-gray-500">
            <IdentificationIcon class="w-4 h-4 mr-1.5 text-gray-400" />
            <span>证书编号：{{ cert.credential_id }}</span>
          </div>

          <!-- 证书描述 -->
          <div v-if="cert.description" class="mt-2 text-sm text-gray-600 break-words whitespace-pre-wrap">
            {{ cert.description }}
          </div>
        </div>
      </div>
    </div>

    <!-- 添加按钮 -->
    <button
      @click="$emit('add')"
      class="w-full flex items-center justify-center px-4 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-all"
    >
      <PlusIcon class="w-4 h-4 mr-2" />
      添加证书奖项
    </button>
  </div>
</template>

<script setup>
import { PencilSquareIcon, TrashIcon, PlusIcon, CalendarIcon, IdentificationIcon } from '@heroicons/vue/24/outline'

defineProps({
  data: {
    type: Array,
    required: true
  }
})

defineEmits(['edit', 'delete', 'add'])

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}`
}

// 处理删除
const handleDelete = async (id) => {
  // 直接触发删除事件，让父组件处理确认弹窗
  emit('delete', id)
}
</script>

<style scoped>
/* 卡片悬停效果 */
.hover\:shadow-sm:hover {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transform: translateY(-1px);
}

/* 响应式布局优化 */
@media (max-width: 640px) {
  .grid-cols-2 {
    grid-template-columns: 1fr;
  }
}
</style> 