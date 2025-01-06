<template>
  <div class="space-y-6">
    <!-- 存储空间使用情况 -->
    <div class="bg-slate-50/70 rounded-lg p-4">
      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center space-x-2">
          <svg class="w-5 h-5 text-gray-400" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
          </svg>
          <span class="text-sm font-medium text-gray-700">存储空间</span>
        </div>
        <span class="text-sm text-gray-500" v-if="storageInfo">
          {{ formatStorage(storageInfo.usedSpace) }}/{{ formatStorage(storageInfo.totalSpace) }}
        </span>
      </div>
      <div class="w-full h-1.5 bg-gray-100 rounded-full overflow-hidden">
        <div class="h-full bg-gradient-to-r from-indigo-500 to-violet-500 transition-all duration-1000 ease-out"
          :style="{ width: `${spaceUsagePercentage}%` }">
        </div>
      </div>
    </div>

    <!-- 作品集列表 -->
    <div v-if="storageInfo?.portfolios" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="portfolio in storageInfo.portfolios" :key="portfolio.id"
        class="group relative bg-white rounded-xl shadow-sm hover:shadow-md transition-all duration-300">
        <!-- 作品集封面 -->
        <div class="aspect-[4/3] rounded-t-xl overflow-hidden">
          <img :src="portfolio.cover" :alt="portfolio.name"
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
        </div>
        
        <!-- 作品集信息 -->
        <div class="p-4">
          <div class="flex items-start justify-between">
            <div>
              <h3 class="text-base font-medium text-gray-900 group-hover:text-indigo-600 transition-colors">
                {{ portfolio.name }}
              </h3>
              <p class="mt-1 text-sm text-gray-500">{{ portfolio.description }}</p>
            </div>
            <!-- 更多操作按钮 -->
            <button class="p-1 text-gray-400 hover:text-gray-600 transition-colors">
              <svg class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
              </svg>
            </button>
          </div>
          
          <!-- 作品集统计 -->
          <div class="mt-3 flex items-center space-x-4 text-sm text-gray-500">
            <span class="flex items-center">
              <svg class="w-4 h-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" />
              </svg>
              {{ portfolio.imageCount }} 张图片
            </span>
            <span class="flex items-center">
              <svg class="w-4 h-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
              </svg>
              {{ formatDate(portfolio.updatedAt) }}
            </span>
          </div>
        </div>
      </div>

      <!-- 创建新作品集按钮 -->
      <button @click="handleCreatePortfolio"
        class="group relative flex flex-col items-center justify-center h-full min-h-[200px] rounded-xl border-2 border-dashed border-gray-200 hover:border-indigo-200 bg-slate-50/50 hover:bg-white transition-all duration-300">
        <div class="p-2 rounded-lg bg-indigo-50 group-hover:bg-indigo-100 transition-colors">
          <svg class="w-6 h-6 text-indigo-500" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4v16m8-8H4" />
          </svg>
        </div>
        <span class="mt-3 text-sm font-medium text-gray-900">创建新作品集</span>
        <span class="mt-1 text-sm text-gray-500">上传并整理您的作品</span>
      </button>
    </div>

    <!-- 加载状态 -->
    <div v-else class="py-12 text-center">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-gray-200 border-t-indigo-500"></div>
      <p class="mt-4 text-sm text-gray-500">加载中...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// 模拟的存储空间信息
const storageInfo = ref({
  usedSpace: 256 * 1024 * 1024, // 256MB
  totalSpace: 1024 * 1024 * 1024, // 1GB
  portfolios: [
    {
      id: 1,
      name: '产品设计作品',
      description: '包含个人完成的产品设计案例',
      cover: 'https://images.unsplash.com/photo-1561070791-2526d30994b5?q=80&w=800',
      imageCount: 12,
      updatedAt: new Date('2024-01-15')
    },
    {
      id: 2,
      name: 'UI 设计作品',
      description: '移动端与网页端界面设计',
      cover: 'https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?q=80&w=800',
      imageCount: 8,
      updatedAt: new Date('2024-02-01')
    },
    {
      id: 3,
      name: '平面设计作品',
      description: '品牌视觉与海报设计',
      cover: 'https://images.unsplash.com/photo-1626785774573-4b799315345d?q=80&w=800',
      imageCount: 6,
      updatedAt: new Date('2024-02-20')
    }
  ]
})

// 计算存储空间使用百分比
const spaceUsagePercentage = computed(() => {
  if (!storageInfo.value) return 0
  return Math.round((storageInfo.value.usedSpace / storageInfo.value.totalSpace) * 100)
})

// 格式化存储空间
const formatStorage = (bytes) => {
  const units = ['B', 'KB', 'MB', 'GB']
  let size = bytes
  let unitIndex = 0
  
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024
    unitIndex++
  }
  
  return `${size.toFixed(1)}${units[unitIndex]}`
}

// 格式化日期
const formatDate = (date) => {
  const d = new Date(date)
  return `${d.getMonth() + 1}月${d.getDate()}日`
}

// 创建新作品集 - 暂时只是添加到本地数据
const handleCreatePortfolio = () => {
  const newPortfolio = {
    id: storageInfo.value.portfolios.length + 1,
    name: '新作品集',
    description: '请添加作品集描述',
    cover: 'https://images.unsplash.com/photo-1626785774625-ddcddc3445e9?q=80&w=800',
    imageCount: 0,
    updatedAt: new Date()
  }
  storageInfo.value.portfolios.push(newPortfolio)
}
</script>