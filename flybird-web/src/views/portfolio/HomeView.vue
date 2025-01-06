<template>
  <div class="py-4 lg:py-6 mt-[72px]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 顶部横幅 -->
      <PageBanner theme="blue">
        <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">设计作品集</h1>
        <p class="text-gray-600 text-lg max-w-2xl">发现优秀设计灵感，分享你的创意作品</p>
      </PageBanner>

      <!-- 使用导航组件 -->
      <PortfolioNavigation v-model:currentCategory="currentCategory" />

      <!-- 作品列表 -->
      <div class="max-w-7xl mx-auto mt-6">
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
          <div v-for="work in filteredWorks" :key="work.id"
            class="bg-white rounded-lg lg:rounded-xl border border-gray-100 overflow-hidden hover:shadow-lg transition-all duration-300"
          >
            <!-- 作品封面 -->
            <div class="aspect-w-1 aspect-h-1 bg-gray-100 relative group overflow-hidden">
              <img 
                :src="work.cover" 
                class="w-full h-full object-cover transform group-hover:scale-110 transition-all duration-500"
                alt=""
              >
              <!-- 视频时长标记 -->
              <div v-if="work.isVideo" 
                class="absolute bottom-2 right-2 px-2 py-1 bg-black/70 rounded-md text-white text-xs flex items-center"
              >
                <PlayIcon class="w-3 h-3 mr-1" />
                {{ work.duration }}
              </div>
              <!-- 悬浮遮罩 -->
              <div class="absolute inset-0 bg-black/60 invisible group-hover:visible opacity-0 group-hover:opacity-100 transition-all duration-300 flex flex-col items-center justify-center transform group-hover:scale-110">
                <span class="text-white font-medium mb-2">{{ portfolioCategories.find(c => c.id === work.type)?.name }}</span>
                <div class="flex items-center gap-3">
                  <span class="flex items-center text-gray-300 text-sm">
                    <EyeIcon class="w-4 h-4 mr-1" />{{ work.views }}
                  </span>
                  <span class="flex items-center text-gray-300 text-sm">
                    <HeartIcon class="w-4 h-4 mr-1" />{{ work.likes }}
                  </span>
                </div>
              </div>
            </div>

            <!-- 作品信息 -->
            <div class="p-3 lg:p-4">
              <h3 class="text-sm font-medium text-gray-900 hover:text-blue-600 transition-colors line-clamp-1 mb-2">
                {{ work.title }}
              </h3>
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <img :src="work.author.avatar" class="w-5 h-5 rounded-full">
                  <span class="text-sm text-gray-600">{{ work.author.name }}</span>
                </div>
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
  RectangleStackIcon,
  UserGroupIcon,
  SparklesIcon,
  ShareIcon,
  HeartIcon,
  ArrowsUpDownIcon,
  ChevronDownIcon,
  FireIcon,
  ClockIcon,
  CalendarIcon,
  PlusIcon,
  UserIcon,
  ChevronRightIcon,
  PlayIcon
} from '@heroicons/vue/24/outline'
import PageBanner from '@/components/common/PageBanner.vue'
import PortfolioNavigation from '@/components/portfolio/PortfolioNavigation.vue'

const store = useStore()
const route = useRoute()

// 使用 Vuex store 的 isAuthenticated 状态
const isAuthenticated = computed(() => store.state.isAuthenticated)

// 当前选中的分类
const currentCategory = ref('all')

// 作品分类数据
const portfolioCategories = [
  { id: 'all', name: '全部' },
  { id: 'ui', name: 'UI设计' },
  { id: 'graphic', name: '平面设计' },
  { id: 'web', name: 'Web设计' },
  { id: 'video', name: '视频制作' },
  { id: 'animation', name: '动画' },
  { id: 'illustration', name: '插画' }
]

const showSortMenu = ref(false)
const currentSort = ref('popular')

// 排序选项
const sortOptions = {
  popular: { label: '最受欢迎', icon: FireIcon },
  newest: { label: '最新发布', icon: CalendarIcon },
  views: { label: '最多浏览', icon: ShareIcon },
  likes: { label: '最多点赞', icon: HeartIcon }
}

// 模拟作品数据
const works = ref([
  {
    id: 1,
    title: '智能家居App UI设计',
    type: 'ui',
    cover: 'https://picsum.photos/600/400?random=1',
    author: {
      name: '张小明',
      avatar: 'https://picsum.photos/32/32?random=1'
    },
    views: 1234,
    likes: 89,
    isVideo: false
  },
  {
    id: 2,
    title: '2024科技峰会品牌设计',
    type: 'graphic',
    cover: 'https://picsum.photos/600/400?random=2',
    author: {
      name: '李晓华',
      avatar: 'https://picsum.photos/32/32?random=2'
    },
    views: 856,
    likes: 67,
    isVideo: false
  },
  {
    id: 3,
    title: '产品宣传创意视频',
    type: 'video',
    cover: 'https://picsum.photos/600/400?random=3',
    author: {
      name: '王大力',
      avatar: 'https://picsum.photos/32/32?random=3'
    },
    views: 2341,
    likes: 178,
    isVideo: true,
    duration: '2:35'
  },
  {
    id: 4,
    title: '企业品牌动画',
    type: 'animation',
    cover: 'https://picsum.photos/600/400?random=4',
    author: {
      name: '赵明',
      avatar: 'https://picsum.photos/32/32?random=4'
    },
    views: 1567,
    likes: 92,
    isVideo: true,
    duration: '1:45'
  },
  {
    id: 5,
    title: '电商网站设计',
    type: 'web',
    cover: 'https://picsum.photos/600/400?random=5',
    author: {
      name: '陈小红',
      avatar: 'https://picsum.photos/32/32?random=5'
    },
    views: 987,
    likes: 45,
    isVideo: false
  },
  {
    id: 6,
    title: '旅行类App界面设计',
    type: 'ui',
    cover: 'https://picsum.photos/600/400?random=6',
    author: {
      name: '刘艺',
      avatar: 'https://picsum.photos/32/32?random=6'
    },
    views: 765,
    likes: 34,
    isVideo: false
  },
  {
    id: 7,
    title: '音乐节创意海报',
    type: 'graphic',
    cover: 'https://picsum.photos/600/400?random=7',
    author: {
      name: '周设计',
      avatar: 'https://picsum.photos/32/32?random=7'
    },
    views: 543,
    likes: 28,
    isVideo: false
  },
  {
    id: 8,
    title: '游戏角色原画设计',
    type: 'illustration',
    cover: 'https://picsum.photos/600/400?random=8',
    author: {
      name: '林画师',
      avatar: 'https://picsum.photos/32/32?random=8'
    },
    views: 876,
    likes: 56,
    isVideo: false
  }
])

// 根据分类和排序过滤作品
const filteredWorks = computed(() => {
  let result = [...works.value]
  
  // 应用分类过滤
  if (currentCategory.value !== 'all') {
    result = result.filter(work => work.type === currentCategory.value)
  }
  
  // 应用排序
  switch (currentSort.value) {
    case 'popular':
      result.sort((a, b) => (b.views + b.likes) - (a.views + a.likes))
      break
    case 'newest':
      result.sort((a, b) => new Date(b.date) - new Date(a.date))
      break
    case 'views':
      result.sort((a, b) => b.views - a.views)
      break
    case 'likes':
      result.sort((a, b) => b.likes - a.likes)
      break
  }
  
  return result
})

// 处理排序
const handleSort = (value) => {
  currentSort.value = value
  showSortMenu.value = false
}
</script> 