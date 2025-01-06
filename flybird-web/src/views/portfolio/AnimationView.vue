<template>
  <div class="py-4 lg:py-6 mt-[72px]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 顶部横幅 -->
      <PageBanner theme="blue">
        <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">动画作品</h1>
        <p class="text-gray-600 text-lg max-w-2xl">分享你的动画创作，发现优秀作品</p>
      </PageBanner>

      <!-- 使用导航组件 -->
      <PortfolioNavigation v-model:currentCategory="currentCategory" />

            <!-- 移动端分类显示 -->
            <div class="md:hidden mb-6">
        <div class="flex items-center justify-between">
          <h1 class="text-xl font-bold text-gray-900">摄影作品</h1>
          <span class="text-sm text-gray-500">{{ works.length }}个作品</span>
        </div>
      </div>
    <!-- 作品列表 -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6 mt-6">
        <div v-for="work in filteredWorks" :key="work.id"
          class="group bg-white rounded-xl border border-gray-100 overflow-hidden hover:shadow-lg transition-all duration-300"
        >
          <!-- 作品封面 -->
          <div class="relative aspect-w-1 aspect-h-1 overflow-hidden">
            <img 
              :src="work.cover" 
              class="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-500"
              alt=""
            >
            <!-- 播放按钮 -->
            <div class="absolute inset-0 flex items-center justify-center">
              <div class="w-10 h-10 rounded-full bg-black/50 backdrop-blur-sm flex items-center justify-center text-white transform group-hover:scale-110 transition-transform">
                <PlayIcon class="w-5 h-5" />
              </div>
            </div>
            <!-- 类型标签 -->
            <div class="absolute top-4 left-4">
              <span class="px-3 py-1 bg-white/90 backdrop-blur-sm rounded-full text-xs font-medium text-gray-900">
                {{ work.type }}
              </span>
            </div>
          </div>

          <!-- 作品信息 -->
          <div class="p-3 lg:p-4">
            <h3 class="text-sm font-medium text-gray-900 mb-2 line-clamp-1">{{ work.title }}</h3>
            
            <!-- 作者信息和统计 -->
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <img :src="work.author.avatar" class="w-5 h-5 rounded-full">
                <span class="text-sm text-gray-600">{{ work.author.name }}</span>
              </div>
              <div class="flex items-center space-x-3 text-sm text-gray-500">
                <span class="flex items-center">
                  <EyeIcon class="w-4 h-4 mr-1" />{{ work.views }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import PageBanner from '@/components/common/PageBanner.vue'
import PortfolioNavigation from '@/components/portfolio/PortfolioNavigation.vue'
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRoute } from 'vue-router'
import { 
  EyeIcon, 
  HeartIcon,
  PlusIcon,
  UserIcon,
  PlayIcon
} from '@heroicons/vue/24/outline'

const store = useStore()
const route = useRoute()

// 使用 Vuex store 的 isAuthenticated 状态
const isAuthenticated = computed(() => store.state.isAuthenticated)

// 主导航数据
const mainNavs = [
  { name: '发现', path: '/portfolio' },
  { name: '设计', path: '/portfolio/design' },
  { name: '视频', path: '/portfolio/video' },
  { name: '动画', path: '/portfolio/animation' },
  { name: '摄影', path: '/portfolio/photo' }
]

const currentCategory = ref('all')
const animationCategories = [
  { id: 'all', name: '全部' },
  { id: '2d', name: '2D动画' },
  { id: '3d', name: '3D动画' },
  { id: 'motion', name: '动态图形' },
  { id: 'character', name: '角色动画' },
  { id: 'game', name: '游戏动画' },
  { id: 'other', name: '其他' }
]

// 模拟作品数据
const works = ref([
  {
    id: 1,
    title: '游戏角色动画',
    type: '角色动画',
    description: '为MOBA游戏设计的英雄角色动画，包含基础动作和技能特效...',
    cover: 'https://picsum.photos/600/400?random=20',
    author: {
      name: '张三',
      avatar: 'https://picsum.photos/32/32?random=20',
      title: '游戏动画师'
    },
    views: 3456,
    likes: 234
  },
  {
    id: 2,
    title: '品牌动态Logo',
    type: '动态图形',
    description: '科技公司品牌Logo的动态演绎，展现品牌活力与创新精神...',
    cover: 'https://picsum.photos/600/400?random=21',
    author: {
      name: '李四',
      avatar: 'https://picsum.photos/32/32?random=21',
      title: '动效设计师'
    },
    views: 2789,
    likes: 167
  }
])

// 根据分类过滤作品
const filteredWorks = computed(() => {
  if (currentCategory.value === 'all') {
    return works.value
  }
  return works.value.filter(work => work.type === currentCategory.value)
})
</script> 