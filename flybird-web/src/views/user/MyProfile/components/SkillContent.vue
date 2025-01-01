<template>
  <div class="space-y-4">
    <!-- 技能列表 -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div 
        v-for="(skill, index) in data" 
        :key="index" 
        class="bg-gray-50 rounded-lg border border-gray-100 p-4 hover:shadow-sm transition-all"
      >
        <!-- 技能头部 -->
        <div class="flex items-start justify-between mb-3">
          <div class="flex-1 min-w-0">
            <h4 class="text-base font-medium text-gray-900 break-words">{{ skill.name }}</h4>
          </div>
          <div class="flex items-center space-x-2 ml-4">
            <button
              @click="$emit('edit', skill)"
              class="p-1 hover:bg-white rounded-full transition-colors"
            >
              <PencilSquareIcon class="w-4 h-4 text-gray-400" />
            </button>
            <button
              @click="$emit('delete', skill.id)"
              class="p-1 hover:bg-white rounded-full transition-colors"
            >
              <TrashIcon class="w-4 h-4 text-gray-400" />
            </button>
          </div>
        </div>

        <!-- 熟练度进度条 -->
        <div class="mb-3">
          <div class="flex items-center justify-between mb-1">
            <span class="text-sm text-gray-500">熟练度</span>
            <span class="text-sm font-medium text-blue-600">{{ getLevelLabel(skill.level) }}</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div 
              class="bg-blue-600 h-2 rounded-full transition-all"
              :style="{ width: getLevelPercentage(skill.level) }"
            ></div>
          </div>
        </div>

        <!-- 技能描述 -->
        <div class="text-sm text-gray-600 break-words whitespace-pre-wrap">
          {{ skill.description }}
        </div>
      </div>
    </div>

    <!-- 添加按钮 -->
    <button
      @click="$emit('add')"
      class="w-full flex items-center justify-center px-4 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-all"
    >
      <PlusIcon class="w-4 h-4 mr-2" />
      添加专业技能
    </button>
  </div>
</template>

<script setup>
import { PencilSquareIcon, TrashIcon, PlusIcon } from '@heroicons/vue/24/outline'

defineProps({
  data: {
    type: Array,
    required: true
  }
})

defineEmits(['edit', 'delete', 'add'])

// 获取熟练度标签
const getLevelLabel = (level) => {
  const levelMap = {
    'beginner': '入门',
    'intermediate': '熟练',
    'advanced': '精通',
    'expert': '专家'
  }
  return levelMap[level] || level
}

// 获取熟练度进度条百分比
const getLevelPercentage = (level) => {
  const percentageMap = {
    'beginner': '25%',
    'intermediate': '50%',
    'advanced': '75%',
    'expert': '100%'
  }
  return percentageMap[level] || '0%'
}
</script>

<style scoped>
/* 进度条动画 */
.bg-blue-600 {
  transition: width 0.3s ease-in-out;
}

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