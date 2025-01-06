<template>
    <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto">
      <div class="flex min-h-screen items-center justify-center p-4">
        <!-- 背景遮罩 -->
        <div class="fixed inset-0 bg-black bg-opacity-25" @click="$emit('close')"></div>
        
        <!-- 弹窗内容 -->
        <div class="relative bg-white rounded-lg shadow-xl max-w-2xl w-full mx-auto">
          <!-- 标题栏 -->
          <div class="flex items-center justify-between p-4 border-b">
            <h3 class="text-lg font-medium">{{ title }}</h3>
            <button 
              @click="$emit('close')"
              class="p-1 hover:bg-gray-100 rounded-full"
            >
              <XMarkIcon class="w-5 h-5" />
            </button>
          </div>
          
          <!-- 表单内容 -->
          <div class="p-4">
            <slot></slot>
          </div>
  
          <!-- 底部按钮 -->
          <div class="flex justify-end gap-3 px-4 py-3 border-t">
            <button 
              @click="$emit('close')"
              class="px-4 py-2 border rounded-lg hover:bg-gray-50"
            >
              取消
            </button>
            <button 
              @click="$emit('submit')"
              class="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600"
            >
              确认
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { XMarkIcon } from '@heroicons/vue/24/outline'
  
  defineProps({
    show: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      required: true
    }
  })
  
  defineEmits(['close', 'submit'])
  </script>