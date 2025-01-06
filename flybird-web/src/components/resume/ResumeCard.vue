<template>
  <div class="group bg-white rounded-lg lg:rounded-xl border border-gray-100 overflow-hidden hover:shadow-lg transition-all duration-300">
    <!-- 封面图 -->
    <div class="relative aspect-w-3 aspect-h-4 bg-gray-100 overflow-hidden">
      <img 
        :src="template.cover" 
        :alt="template.title"
        class="w-full h-full object-cover transform group-hover:scale-105 transition-all duration-500"
      />
      <!-- 悬浮操作按钮 -->
      <div class="absolute inset-0 flex items-center justify-center opacity-0 bg-black/40 group-hover:opacity-100 transition-all duration-500">
        <button class="bg-white text-gray-900 px-4 py-2 rounded-full text-sm font-medium hover:bg-gray-50">
          使用模板
        </button>
      </div>
      <!-- 收藏按钮 -->
      <button 
        class="absolute top-3 right-3 w-8 h-8 rounded-full bg-white/90 backdrop-blur-sm flex items-center justify-center hover:bg-white transition-colors z-10"
        :class="{ 'text-rose-600': template.isLiked, 'text-gray-600': !template.isLiked }"
        @click.stop="$emit('like')"
      >
        <HeartIcon v-if="template.isLiked" class="w-5 h-5 fill-current" />
        <HeartIcon v-else class="w-5 h-5" />
      </button>
      <!-- 会员标识 -->
      <div 
        v-if="template.isPro"
        class="absolute top-3 left-3 w-8 h-8 bg-gradient-to-r from-yellow-500 to-amber-500 rounded-full flex items-center justify-center z-10"
      >
      <svg class="w-4 h-4 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M5 16L3 5L8.5 10L12 4L15.5 10L21 5L19 16H5Z" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round" />
          </svg>
      </div>
      <!-- 分类标签 -->
      <div class="absolute bottom-3 left-3 z-10">
        <span class="px-2.5 py-1 bg-white/90 backdrop-blur-sm rounded-full text-xs font-medium text-gray-700">
          {{ template.category }}
        </span>
      </div>
    </div>

    <!-- 模板信息 -->
    <div class="p-3 lg:p-4">
      <h3 class="text-sm font-medium text-gray-900 group-hover:text-blue-600 transition-colors line-clamp-1 mb-2">
        {{ template.title }}
      </h3>
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3 text-sm text-gray-500">
          <span class="flex items-center">
            <DocumentDuplicateIcon class="w-4 h-4 mr-1" />{{ formatNumber(template.useCount) }}
          </span>
          <span class="flex items-center">
            <EyeIcon class="w-4 h-4 mr-1" />{{ formatNumber(template.viewCount) }}
          </span>
        </div>
        <!-- 会员价格标识 -->
        <div 
          v-if="template.isPro"
          class="flex items-center"
        >
          <span class="text-xs font-medium text-amber-600">会员免费</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { DocumentDuplicateIcon, EyeIcon, HeartIcon } from '@heroicons/vue/24/outline'
import { CrownIcon } from '@heroicons/vue/24/solid'

const props = defineProps({
  template: {
    type: Object,
    required: true,
    validator: (obj) => {
      console.log('Template props:', obj)
      return obj.title && 
             typeof obj.isPro === 'boolean' && 
             typeof obj.useCount === 'number' &&
             typeof obj.viewCount === 'number' &&
             typeof obj.isLiked === 'boolean' &&
             typeof obj.category === 'string'
    }
  }
})

defineEmits(['like'])

// 格式化数字，超过1000显示为k
const formatNumber = (num) => {
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'k'
  }
  return num
}
</script> 