<template>
  <div class="py-4 lg:py-6 mt-[72px]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 顶部横幅 -->
      <PageBanner theme="blue">
        <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">视频作品</h1>
        <p class="text-gray-600 text-lg max-w-2xl">分享你的视频创作，展现影像魅力</p>
      </PageBanner>

      <!-- 使用导航组件 -->
      <PortfolioNavigation v-model:currentCategory="currentCategory" />

      <!-- 移动端分类显示 -->
      <div class="md:hidden mb-6">
        <div class="flex items-center justify-between">
          <h1 class="text-xl font-bold text-gray-900">视频作品</h1>
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
import PageBanner from '@/components/common/PageBanner.vue'
import PortfolioNavigation from '@/components/portfolio/PortfolioNavigation.vue'

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
const videoCategories = [
  { id: 'all', name: '全部' },
  { id: 'short', name: '短视频' },
  { id: 'vlog', name: 'Vlog' },
  { id: 'commercial', name: '商业广告' },
  { id: 'film', name: '影视作品' },
  { id: 'mv', name: '音乐MV' },
  { id: 'tutorial', name: '教程' }
]

// 模拟作品数据
const works = ref([
  {
    id: 1,
    title: '品牌宣传片',
    type: '商业广告',
    description: '科技公司品牌形象宣传片，展现企业创新精神和科技实力...',
    cover: 'https://picsum.photos/600/400?random=10',
    author: {
      name: '王小明',
      avatar: 'https://picsum.photos/32/32?random=10',
      title: '视频导演'
    },
    views: 2345,
    likes: 156
  },
  {
    id: 2,
    title: '旅行Vlog',
    type: 'Vlog',
    description: '记录在日本京都的传统文化探索之旅，展现当地独特的人文风景...',
    cover: 'https://picsum.photos/600/400?random=11',
    author: {
      name: '李小红',
      avatar: 'https://picsum.photos/32/32?random=11',
      title: 'Vlogger'
    },
    views: 1567,
    likes: 98
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