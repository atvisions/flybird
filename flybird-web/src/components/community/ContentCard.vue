<template>
  <div class="bg-white rounded-lg border border-gray-100 overflow-hidden hover:shadow-lg transition-all duration-300">
    <!-- 封面图 -->
    <div v-if="content.cover" class="aspect-w-16 aspect-h-9 bg-gray-100 relative">
      <img 
        :src="content.cover" 
        :alt="content.title"
        class="w-full h-full object-cover"
      />
    </div>

    <!-- 内容信息 -->
    <div class="p-4">
      <!-- 标题和标签 -->
      <div class="mb-3">
        <h3 class="text-base font-medium text-gray-900 hover:text-blue-600 transition-colors line-clamp-2 mb-2">
          {{ content.title }}
        </h3>
        <div class="flex items-center space-x-2">
          <span class="px-2 py-1 bg-gray-100 rounded-full text-xs font-medium text-gray-600">
            {{ content.category }}
          </span>
        </div>
      </div>

      <!-- 作者信息 -->
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <img :src="content.author.avatar" class="w-6 h-6 rounded-full">
          <span class="text-sm text-gray-600">{{ content.author.name }}</span>
        </div>
        <div class="flex items-center space-x-4">
          <button 
            class="text-gray-400 hover:text-gray-500"
            @click="$emit('like', content.id)"
          >
            <HeartIcon class="w-5 h-5" :class="{ 'text-rose-500 fill-current': content.isLiked }" />
          </button>
          <button 
            class="text-gray-400 hover:text-gray-500"
            @click="$emit('collect', content.id)"
          >
            <BookmarkIcon class="w-5 h-5" :class="{ 'text-blue-500 fill-current': content.isCollected }" />
          </button>
        </div>
      </div>

      <!-- 统计信息 -->
      <div class="mt-3 flex items-center space-x-4 text-sm text-gray-500">
        <span class="flex items-center">
          <EyeIcon class="w-4 h-4 mr-1" />{{ content.views }}
        </span>
        <span class="flex items-center">
          <HeartIcon class="w-4 h-4 mr-1" />{{ content.likes }}
        </span>
        <span class="flex items-center">
          <ChatBubbleLeftIcon class="w-4 h-4 mr-1" />{{ content.comments }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { 
  HeartIcon, 
  BookmarkIcon, 
  EyeIcon,
  ChatBubbleLeftIcon
} from '@heroicons/vue/24/outline'

defineProps({
  content: {
    type: Object,
    required: true,
    validator: (obj) => {
      return obj.id && 
             obj.title && 
             obj.author &&
             typeof obj.views === 'number' &&
             typeof obj.likes === 'number' &&
             typeof obj.comments === 'number'
    }
  }
})

defineEmits(['like', 'collect'])
</script> 