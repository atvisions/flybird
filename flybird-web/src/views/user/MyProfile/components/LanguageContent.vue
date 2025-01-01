<template>
  <div class="space-y-4">
    <!-- 语言列表 -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div 
        v-for="(lang, index) in data" 
        :key="index" 
        class="bg-gray-50 rounded-lg border border-gray-100 p-4 hover:shadow-sm transition-all"
      >
        <!-- 语言头部 -->
        <div class="flex items-start justify-between mb-3">
          <div class="flex-1 min-w-0">
            <h4 class="text-base font-medium text-gray-900 break-words">{{ lang.name }}</h4>
          </div>
          <div class="flex items-center space-x-2 ml-4">
            <button
              @click="$emit('edit', lang)"
              class="p-1 hover:bg-white rounded-full transition-colors"
            >
              <PencilSquareIcon class="w-4 h-4 text-gray-400" />
            </button>
            <button
              @click="$emit('delete', lang.id)"
              class="p-1 hover:bg-white rounded-full transition-colors"
            >
              <TrashIcon class="w-4 h-4 text-gray-400" />
            </button>
          </div>
        </div>

        <!-- 语言等级 -->
        <div class="mb-3">
          <div class="flex items-center justify-between mb-1">
            <span class="text-sm text-gray-500">掌握程度</span>
            <span class="text-sm font-medium text-blue-600">{{ lang.proficiency_display }}</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div 
              class="bg-blue-600 h-2 rounded-full transition-all"
              :style="{ width: getProficiencyPercentage(lang.proficiency) }"
            ></div>
          </div>
        </div>

        <!-- 证书和分数信息 -->
        <div v-if="lang.certification || lang.score" class="mt-2 space-y-1">
          <div v-if="lang.certification" class="text-sm text-gray-600">
            证书：{{ lang.certification }}
          </div>
          <div v-if="lang.score" class="text-sm text-gray-600">
            分数：{{ lang.score }}
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
      添加语言能力
    </button>
  </div>
</template>

<script setup>
import { PencilSquareIcon, TrashIcon, PlusIcon } from '@heroicons/vue/24/outline'
import { watch } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    required: true
  }
})

defineEmits(['edit', 'delete', 'add'])

// 获取等级进度条百分比
const getProficiencyPercentage = (proficiency) => {
  const percentageMap = {
    'elementary': '25%',
    'intermediate': '50%',
    'advanced': '75%',
    'native': '100%'
  }
  return percentageMap[proficiency] || '0%'
}

// 添加数据监听
watch(() => props.data, (newData) => {

}, { immediate: true, deep: true })
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