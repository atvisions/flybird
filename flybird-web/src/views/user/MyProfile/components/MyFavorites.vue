<template>
  <div class="space-y-6">
    <!-- 标签切换 -->
    <div class="bg-white rounded-lg shadow">
      <div class="px-4 py-5 sm:p-6">
        <div class="border-b border-gray-200">
          <nav class="-mb-px flex space-x-8">
            <button
              v-for="tab in tabs"
              :key="tab.key"
              @click="currentTab = tab.key"
              class="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm"
              :class="[
                currentTab === tab.key
                  ? 'border-indigo-500 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              {{ tab.label }}
            </button>
          </nav>
        </div>

        <!-- 收藏内容列表 -->
        <div class="mt-6 space-y-4">
          <div v-for="item in currentItems" :key="item.id" class="flex items-start space-x-4 p-4 hover:bg-gray-50 rounded-lg">
            <div class="flex-1">
              <h3 class="text-base font-medium text-gray-900">{{ item.title }}</h3>
              <p class="mt-1 text-sm text-gray-500">{{ item.description }}</p>
              <div class="mt-2 flex items-center text-xs text-gray-500 space-x-4">
                <span>{{ item.author }}</span>
                <span>{{ item.createTime }}</span>
                <span class="flex items-center">
                  <EyeIcon class="w-4 h-4 mr-1" />{{ item.views }}
                </span>
              </div>
            </div>
            <button 
              @click="handleUnfavorite(item)"
              class="p-1.5 text-gray-400 hover:text-red-600 rounded-lg hover:bg-red-50"
            >
              <StarIcon class="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { EyeIcon, StarIcon } from '@heroicons/vue/24/outline'
import { showToast } from '@/components/ToastMessage'

const tabs = [
  { key: 'articles', label: '文章' },
  { key: 'questions', label: '问答' },
  { key: 'topics', label: '话题' }
]

const currentTab = ref('articles')

// 模拟数据
const favorites = ref({
  articles: [
    {
      id: 1,
      title: '2024年前端开发趋势展望',
      description: '探讨新的前端框架、工具和最佳实践...',
      author: '张小明',
      createTime: '2小时前',
      views: 1234
    }
  ],
  questions: [
    {
      id: 1,
      title: 'Vue3性能优化的最佳实践有哪些？',
      description: '最近在做一个Vue3项目的性能优化...',
      author: '李大山',
      createTime: '4小时前',
      views: 892
    }
  ],
  topics: [
    {
      id: 1,
      title: '开发移动应用选择哪个方案？',
      description: 'Flutter vs React Native 的选择...',
      author: '王大力',
      createTime: '1天前',
      views: 2341
    }
  ]
})

const currentItems = computed(() => favorites.value[currentTab.value] || [])

const handleUnfavorite = async (item) => {
  try {
    // TODO: 调用取消收藏 API
    showToast('已取消收藏', 'success')
    // 从列表中移除
    favorites.value[currentTab.value] = favorites.value[currentTab.value].filter(i => i.id !== item.id)
  } catch (error) {
    showToast('操作失败', 'error')
  }
}
</script> 