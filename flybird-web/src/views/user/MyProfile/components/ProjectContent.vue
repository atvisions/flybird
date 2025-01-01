<template>
  <div class="relative space-y-0">
    <!-- 时间线 -->
    <div class="absolute left-[0.5625rem] top-3 bottom-3 w-px bg-gray-200"></div>

    <!-- 项目经历列表 -->
    <div 
      v-for="(project, index) in data" 
      :key="index" 
      class="relative pl-12 pb-6"
    >
      <!-- 时间节点 -->
      <div class="absolute left-[0.5625rem] -translate-x-1/2 top-2 w-3 h-3 rounded-full bg-white border-2 border-blue-500"></div>
      
      <!-- 内容卡片 -->
      <div class="bg-gray-50 rounded-lg border border-gray-100 p-4 hover:shadow-sm transition-shadow">
        <!-- 头部信息 -->
        <div class="flex flex-col space-y-2">
          <!-- 项目名称和操作按钮 -->
          <div class="flex items-start justify-between">
            <div>
              <h4 class="text-base font-medium text-gray-900">{{ project.name }}</h4>
              <div class="text-sm text-gray-500 mt-1">
                {{ formatDate(project.start_date) }} - {{ project.is_current ? '至今' : formatDate(project.end_date) }}
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <button
                @click="$emit('edit', project)"
                class="p-1 hover:bg-white rounded-full transition-colors"
              >
                <PencilSquareIcon class="w-4 h-4 text-gray-400" />
              </button>
              <button
                @click="$emit('delete', project.id)"
                class="p-1 hover:bg-white rounded-full transition-colors"
              >
                <TrashIcon class="w-4 h-4 text-gray-400" />
              </button>
            </div>
          </div>

          <!-- 角色 -->
          <div class="text-sm font-medium text-blue-600">
            {{ project.role }}
          </div>

          <!-- 项目描述 -->
          <div class="mt-3 space-y-2">
            <div class="flex items-center space-x-2">
              <DocumentTextIcon class="w-4 h-4 text-gray-400" />
              <span class="text-sm text-gray-500">项目描述</span>
            </div>
            <div class="text-sm leading-relaxed text-gray-600 pl-6">
              {{ project.description }}
            </div>
          </div>

          <!-- 项目成就 -->
          <div v-if="project.achievement" class="mt-3 space-y-2">
            <div class="flex items-center space-x-2">
              <TrophyIcon class="w-4 h-4 text-yellow-500" />
              <span class="text-sm text-gray-500">项目成就</span>
            </div>
            <div class="text-sm leading-relaxed text-gray-600 pl-6">
              {{ project.achievement }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加按钮 -->
    <div class="relative pl-12">
      <div class="absolute left-[0.5625rem] -translate-x-1/2 top-2 w-3 h-3 rounded-full bg-white border-2 border-gray-300"></div>
      <button
        @click="$emit('add')"
        class="w-full flex items-center justify-center px-4 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-all"
      >
        <PlusIcon class="w-4 h-4 mr-2" />
        添加项目经历
      </button>
    </div>
  </div>
</template>

<script setup>
import { PencilSquareIcon, TrashIcon, PlusIcon, DocumentTextIcon, TrophyIcon } from '@heroicons/vue/24/outline'

defineProps({
  data: {
    type: Array,
    required: true
  }
})

defineEmits(['edit', 'delete', 'add'])

// 格式化日期显示
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}`
}
</script> 