<template>
    <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto">
      <div class="flex min-h-screen items-center justify-center p-4">
        <!-- 背景遮罩 -->
        <div class="fixed inset-0 bg-black bg-opacity-25" @click="$emit('close')"></div>
        
        <!-- 弹窗内容 -->
        <div class="relative bg-white rounded-lg shadow-xl max-w-2xl w-full mx-auto">
          <!-- 标题栏 -->
          <div class="flex items-center justify-between p-4 border-b">
            <h3 class="text-lg font-medium">AI 优化建议</h3>
            <button 
              @click="$emit('close')"
              class="p-1 hover:bg-gray-100 rounded-full"
            >
              <XMarkIcon class="w-5 h-5" />
            </button>
          </div>
          
          <!-- 建议列表 -->
          <div class="p-4">
            <div class="space-y-4">
              <div v-for="(suggestion, index) in suggestions" 
                   :key="index"
                   class="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                <SparklesIcon class="w-5 h-5 text-primary-500 flex-shrink-0 mt-0.5" />
                <div class="flex-1">
                  <p class="text-sm text-gray-700">{{ suggestion.content }}</p>
                  <button 
                    v-if="suggestion.action"
                    @click="handleAction(suggestion)"
                    class="mt-2 text-sm text-primary-600 hover:text-primary-700"
                  >
                    立即优化
                  </button>
                </div>
              </div>
            </div>
          </div>
  
          <!-- 底部按钮 -->
          <div class="flex justify-end px-4 py-3 border-t">
            <button 
              @click="$emit('close')"
              class="px-4 py-2 border rounded-lg hover:bg-gray-50"
            >
              关闭
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { XMarkIcon, SparklesIcon } from '@heroicons/vue/24/outline'
  
  defineProps({
    show: {
      type: Boolean,
      default: false
    },
    suggestions: {
      type: Array,
      default: () => []
    }
  })
  
  const emit = defineEmits(['close', 'action'])
  
  const handleAction = (suggestion) => {
    if (suggestion.action) {
      emit('action', suggestion)
      emit('close')
    }
  }
  </script>