<template>
  <div class="group relative bg-white rounded-2xl overflow-hidden border border-gray-100 hover:border-gray-200 hover:shadow-lg transition-all duration-300">
    <!-- 推荐标记 -->
    <div v-if="template.is_recommended" 
      class="absolute top-3 right-3 z-10 bg-gradient-to-r from-amber-500 to-amber-600 text-white text-xs px-2 py-1 rounded-full font-medium flex items-center">
      <SparklesIcon class="w-3 h-3 mr-1" />
      飞鸟推荐
    </div>

    <!-- 操作按钮遮罩层 -->
    <div class="absolute inset-0 bg-black/60 invisible group-hover:visible flex items-center justify-center transition-all duration-300 z-20">
      <button 
        @click="handleUseTemplate(template)"
        class="px-6 py-2.5 bg-white hover:bg-gray-50 text-gray-900 rounded-full text-sm font-medium transition-colors scale-90 group-hover:scale-100"
      >
        使用该模版
      </button>
    </div>

    <!-- 缩略图 -->
    <div class="relative aspect-w-16 aspect-h-9 rounded-lg overflow-hidden bg-gray-100 z-10">
      <img 
        v-if="template.thumbnail" 
        :src="template.thumbnail" 
        :alt="template.name"
        class="w-full h-full object-cover"
      />
      <div v-else class="w-full h-full flex items-center justify-center text-gray-400">
        <DocumentIcon class="w-12 h-12" />
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="p-4">
      <!-- 标题和标签 -->
      <div class="mb-2">
        <h3 class="text-base font-medium text-gray-900 mb-1">{{ template.name }}</h3>
        <div class="flex items-center gap-2">
          <span class="px-2 py-0.5 bg-gray-100 text-gray-600 rounded text-xs">{{ template.category }}</span>
          <span v-if="template.isPro" class="px-2 py-0.5 bg-amber-100 text-amber-600 rounded text-xs">Pro</span>
        </div>
      </div>

      <!-- 简介 -->
      <p v-if="template.description" class="text-sm text-gray-500 mb-3 line-clamp-2">{{ template.description }}</p>

      <!-- 底部信息 -->
      <div class="flex items-center justify-between">
        <!-- 创作者信息 -->
        <div class="flex items-center gap-2">
          <div class="relative">
            <img 
              v-if="template.creator_avatar" 
              :src="template.creator_avatar" 
              :alt="template.creator_name"
              class="w-6 h-6 rounded-full object-cover"
            />
            <div v-else class="w-6 h-6 rounded-full bg-gray-200 flex items-center justify-center">
              <UserIcon class="w-4 h-4 text-gray-400" />
            </div>
            <!-- VIP 标识 -->
            <div 
              v-if="template.creator_is_vip" 
              class="absolute -bottom-1 -right-1 w-3 h-3 bg-gradient-to-r from-amber-500 to-yellow-500 rounded-full flex items-center justify-center"
            >
              <CrownIcon class="w-2 h-2 text-white" />
            </div>
          </div>
          <div class="flex flex-col">
            <span class="text-sm text-gray-900">{{ template.creator_name }}</span>
            <span v-if="template.creator_position" class="text-xs text-gray-500">{{ template.creator_position }}</span>
          </div>
        </div>

        <!-- 统计信息 -->
        <div class="flex items-center gap-3 relative z-30">
          <div class="flex items-center text-gray-400 text-sm">
            <EyeIcon class="w-4 h-4 mr-1" />
            {{ template.viewCount }}
          </div>
          <button 
            @click="$emit('like', template)"
            class="flex items-center text-gray-400 hover:text-rose-600 text-sm transition-colors"
            :class="{ 'text-rose-600': template.isLiked }"
          >
            <component 
              :is="template.isLiked ? HeartSolidIcon : HeartOutlineIcon" 
              class="w-4 h-4 mr-1"
            />
            {{ template.likes || 0 }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { 
  DocumentIcon, 
  UserIcon, 
  EyeIcon, 
  HeartIcon as HeartOutlineIcon,
  PlusIcon,
  CrownIcon,
  SparklesIcon
} from '@heroicons/vue/24/outline'
import { HeartIcon as HeartSolidIcon } from '@heroicons/vue/24/solid'
import { useRouter } from 'vue-router'

const emit = defineEmits(['like', 'use'])

const router = useRouter()

const handleUseTemplate = (template) => {
  router.push(`/editor/resume/new/${template.id}`)
}

const props = defineProps({
  template: {
    type: Object,
    required: true,
    default: () => ({
      id: '',
      name: '',
      description: '',
      thumbnail: '',
      category: '',
      creator_name: '',
      creator_avatar: '',
      creator_is_vip: false,
      creator_position: '',
      useCount: 0,
      viewCount: 0,
      isPro: false,
      is_recommended: false
    })
  }
})
</script> 