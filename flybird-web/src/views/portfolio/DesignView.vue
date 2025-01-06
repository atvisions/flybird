<template>
  <div class="py-4 lg:py-6 mt-[72px]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 顶部横幅 -->
      <PageBanner theme="blue">
        <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">设计作品</h1>
        <p class="text-gray-600 text-lg max-w-2xl">分享你的设计灵感，探索创意无限</p>
      </PageBanner>

      <!-- 使用导航组件 -->
      <PortfolioNavigation v-model:currentCategory="currentCategory" v-model:currentSort="currentSort" />
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

// 当前选中的分类
const currentCategory = ref('all')
const currentSort = ref('popular')

// 设计分类数据
const designCategories = [
  { id: 'all', name: '全部' },
  { id: 'ui', name: 'UI设计' },
  { id: 'graphic', name: '平面设计' },
  { id: 'brand', name: '品牌设计' },
  { id: 'web', name: '网页设计' },
  { id: 'illustration', name: '插画' },
  { id: 'icon', name: '图标设计' }
]

// 模拟作品数据
const works = ref([
  {
    id: 1,
    title: '电商App设计',
    type: 'UI设计',
    description: '一个现代简约风格的电商App设计，包含完整的用户流程和交互设计方案...',
    cover: 'https://picsum.photos/600/400?random=1',
    author: {
      name: '张小明',
      avatar: 'https://picsum.photos/32/32?random=1',
      title: '高级UI设计师'
    },
    views: 1234,
    likes: 89
  },
  {
    id: 2,
    title: '品牌VI设计',
    type: '品牌设计',
    description: '科技公司品牌视觉识别系统设计，包含logo、色彩、字体等规范...',
    cover: 'https://picsum.photos/600/400?random=2',
    author: {
      name: '李小红',
      avatar: 'https://picsum.photos/32/32?random=2',
      title: '品牌设计师'
    },
    views: 856,
    likes: 67
  },
  // 可以添加更多作品数据...
])

// 根据分类过滤作品
const filteredWorks = computed(() => {
  if (currentCategory.value === 'all') {
    return works.value
  }
  return works.value.filter(work => work.type === currentCategory.value)
})
</script> 