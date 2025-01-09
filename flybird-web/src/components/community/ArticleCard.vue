<template>
  <div class="bg-white rounded-lg border border-gray-100 p-4 lg:p-6 hover:shadow-lg transition-shadow">
    <!-- 头部信息 -->
    <div class="flex items-start justify-between">
      <div class="flex items-center">
        <!-- 作者头像 -->
        <img 
          :src="article.author.avatar" 
          class="w-10 h-10 rounded-full object-cover"
          @error="handleImageError"
        >
        <div class="ml-3">
          <!-- 作者名称 -->
          <div class="text-sm font-medium text-gray-900">{{ article.author.name }}</div>
          <!-- 发布时间 -->
          <div class="text-xs text-gray-500">{{ formatTime(article.createTime) }}</div>
        </div>
      </div>
      <!-- 分类标签 -->
      <div class="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm">
        {{ article.category }}
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="mt-4">
      <!-- 标题 -->
      <h3 class="text-lg font-medium text-gray-900 hover:text-violet-600 transition-colors">
        <router-link :to="`/community/articles/${article.id}`">
          {{ article.title }}
        </router-link>
      </h3>
      <!-- 内容预览 -->
      <p class="mt-2 text-gray-600 text-sm line-clamp-3">
        {{ article.content }}
      </p>
    </div>

    <!-- 底部信息 -->
    <div class="mt-4 flex items-center justify-between">
      <!-- 标签 -->
      <div class="flex gap-2">
        <span 
          v-for="tag in article.tags" 
          :key="tag"
          class="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm"
        >
          {{ tag }}
        </span>
      </div>
      <!-- 统计信息 -->
      <div class="flex items-center gap-4 text-sm text-gray-500">
        <div class="flex items-center">
          <EyeIcon class="w-4 h-4 mr-1" />
          {{ article.views }}
        </div>
        <div class="flex items-center">
          <ChatBubbleLeftIcon class="w-4 h-4 mr-1" />
          {{ article.comments }}
        </div>
        <div class="flex items-center">
          <HeartIcon class="w-4 h-4 mr-1" />
          {{ article.likes }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { EyeIcon, ChatBubbleLeftIcon, HeartIcon } from '@heroicons/vue/24/outline'
import defaultAvatar from '@/assets/images/default-avatar.png'

const props = defineProps({
  article: {
    type: Object,
    required: true
  }
})

// 处理图片加载错误
const handleImageError = (e) => {
  e.target.src = defaultAvatar
}

// 格式化时间
const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  const now = new Date()
  const diff = now - date

  if (diff < 60000) { // 小于1分钟
    return '刚刚'
  } else if (diff < 3600000) { // 小于1小时
    return `${Math.floor(diff / 60000)}分钟前`
  } else if (diff < 86400000) { // 小于24小时
    return `${Math.floor(diff / 3600000)}小时前`
  } else if (diff < 604800000) { // 小于7天
    return `${Math.floor(diff / 86400000)}天前`
  } else {
    return date.toLocaleDateString()
  }
}
</script> 