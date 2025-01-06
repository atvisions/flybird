<template>
  <div class="group bg-white rounded-xl border border-gray-100 overflow-hidden hover:shadow-lg transition-all duration-300">
    <!-- 模板预览图 -->
    <div class="relative aspect-[3/4] overflow-hidden">
      <img 
        :src="template.cover" 
        class="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-500"
        alt=""
      >
      <!-- 悬浮操作按钮 -->
      <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-4">
        <button class="px-4 py-2 bg-white/90 hover:bg-white text-gray-900 rounded-full text-sm font-medium transition-colors">
          预览模板
        </button>
        <button class="px-4 py-2 bg-rose-500 hover:bg-rose-600 text-white rounded-full text-sm font-medium transition-colors">
          使用模板
        </button>
      </div>
    </div>

    <!-- 模板信息 -->
    <div class="p-4">
      <h3 class="text-lg font-medium text-gray-900 mb-1">{{ template.title }}</h3>
      <p class="text-sm text-gray-500 mb-3 line-clamp-2">{{ template.description }}</p>
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <img :src="template.author.avatar" class="w-6 h-6 rounded-full">
          <span class="text-sm text-gray-600">{{ template.author.name }}</span>
        </div>
        <div class="flex items-center space-x-4 text-sm text-gray-500">
          <span class="flex items-center">
            <EyeIcon class="w-4 h-4 mr-1" />
            {{ template.views }}
          </span>
          <span class="flex items-center">
            <HeartIcon class="w-4 h-4 mr-1" />
            {{ template.likes }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { EyeIcon, HeartIcon } from '@heroicons/vue/24/outline'

defineProps({
  template: {
    type: Object,
    required: true
  }
})
</script> 