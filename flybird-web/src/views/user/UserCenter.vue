<template>
    <div class="user-center">
      <HeadView />
      <div class="min-h-screen bg-gray-50 pt-16 sm:pt-20 lg:pb-0 mt-4">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 mt-4 lg:mt-0">
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8">
            <!-- 左侧导航 - 仅桌面端显示 -->
            <div class="hidden lg:block lg:col-span-3">
              <div class="bg-white rounded-lg shadow overflow-hidden sticky top-20">
                <nav class="space-y-1">
                    <button
                        v-for="tab in tabs"
                        :key="tab.key"
                        @click="handleTabChange(tab.key)" 
                        class="w-full flex items-center px-4 py-3 text-sm font-medium group"
                        :class="[
                        currentTab === tab.key
                            ? 'bg-gray-100 text-indigo-600'
                            : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                        ]"
                    >
                    <div class="flex items-center flex-1 min-w-0">
                      <component
                        :is="tab.icon"
                        :class="[
                          currentTab === tab.key ? 'text-indigo-600' : 'text-gray-400 group-hover:text-gray-500',
                          'h-5 w-5 flex-shrink-0'
                        ]"
                      />
                      <span class="ml-2 truncate">{{ tab.name }}</span>
                    </div>
                    <span 
                      v-if="getTabMetric(tab.key)"
                      :class="[
                        currentTab === tab.key ? 'bg-indigo-100 text-indigo-600' : 'bg-gray-100 text-gray-900',
                        'ml-3 inline-block py-0.5 px-2 text-xs rounded-full'
                      ]"
                    >
                      {{ getTabMetric(tab.key) }}
                    </span>
                  </button>
                </nav>
              </div>
            </div>
  
            <!-- 中间内容区 -->
            <div class="lg:col-span-6">
              <component :is="currentComponent" />
            </div>
  
            <!-- 右侧广告位 - 仅桌面端显示 -->
            <div class="hidden lg:block lg:col-span-3">
              <div class="bg-white rounded-lg shadow p-4 sticky top-20">
                <h3 class="text-lg font-medium text-gray-900 mb-4">推荐职位</h3>
                <div class="space-y-4">
                  <div v-for="job in recommendedJobs" :key="job.id" class="flex space-x-3">
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-medium text-gray-900 truncate">{{ job.title }}</p>
                      <p class="text-sm text-gray-500">{{ job.company }}</p>
                    </div>
                    <div class="flex-shrink-0">
                      <span class="text-sm font-medium text-indigo-600">{{ job.salary }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <MobileTabBar 
          :menu-groups="menuGroups"
          :unread-messages="unreadMessagesCount"
        />
      </div>
      <FootView />
    </div>
  </template>
<script setup>
import { ref, computed, watch, onMounted, defineAsyncComponent } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import profile from '@/api/profile'
import HeadView from '../../components/HeadView.vue'
import FootView from '../../components/FootView.vue'
import {
  UserIcon,
  DocumentTextIcon,
  PhotoIcon,
  DocumentIcon,
  StarIcon,
  EnvelopeIcon,
  GlobeAltIcon,
  Cog6ToothIcon,
  PlusCircleIcon,
  Bars3Icon,
  XMarkIcon,
  BookmarkIcon,
  HomeIcon,
  CogIcon
} from '@heroicons/vue/24/outline'
import MobileTabBar from '@/components/MobileTabBar.vue'

// 创建加载组件
const LoadingComponent = {
  name: 'LoadingComponent',
  template: `
    <div class="p-4 text-center">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
      <p class="mt-2 text-gray-600">加载中...</p>
    </div>
  `
}

// 异步组件
const MyProfile = defineAsyncComponent({
  loader: () => import('@/views/user/MyProfile/index.vue'),
  loadingComponent: LoadingComponent,
  timeout: 10000,  // 增加超时时间到10秒
  delay: 200,
  onError(error, retry, fail, attempts) {
    if (attempts <= 3) {
      // 重试3次
      retry()
    } else {
      fail()
    }
  }
})

const MyResumes = defineAsyncComponent({
  loader: () => import('@/views/user/MyResumes.vue'),
  loadingComponent: LoadingComponent,
  timeout: 10000
})

const MyPortfolio = defineAsyncComponent({
  loader: () => import('@/views/user/MyProfile/components/MyPortfolio.vue'),
  loadingComponent: LoadingComponent,
  timeout: 10000
})

const AccountSettings = defineAsyncComponent({
  loader: () => import('@/views/user/AccountSettings.vue'),
  loadingComponent: LoadingComponent,
  timeout: 10000
})

const MyCreations = defineAsyncComponent({
  loader: () => import('@/views/user/MyProfile/components/MyCreations.vue'),
  loadingComponent: LoadingComponent,
  timeout: 10000
})

const MyFavorites = defineAsyncComponent({
  loader: () => import('@/views/user/MyProfile/components/MyFavorites.vue'),
  loadingComponent: LoadingComponent,
  timeout: 10000
})

const MyMessages = defineAsyncComponent({
  loader: () => import('@/views/user/MyProfile/components/MyMessages.vue'),
  loadingComponent: LoadingComponent,
  timeout: 10000
})

const MyHomepage = defineAsyncComponent({
  loader: () => import('@/views/user/MyProfile/components/MyHomepage.vue'),
  loadingComponent: LoadingComponent,
  timeout: 10000
})

const route = useRoute()
const router = useRouter()

// 统一的 currentTab 声明，使用 URL 参数或 localStorage
const currentTab = ref(route.query.tab || localStorage.getItem('userCenterTab') || 'profile')

// 监听标签变化
watch(currentTab, (newTab) => {
  // 更新 localStorage
  localStorage.setItem('userCenterTab', newTab)
  // 更新 URL 参数
  router.replace({
    query: { ...route.query, tab: newTab }
  })
})

// 监听 URL 参数变化
watch(
  () => route.query.tab,
  (newTab) => {
    if (newTab && newTab !== currentTab.value) {
      currentTab.value = newTab
    }
  }
)

// 处理标签切换
const handleTabChange = (key) => {
  currentTab.value = key
}

// 将原有的tabs拆分为主要和次要标签
const tabs = [
  { 
    key: 'profile', 
    name: '个人档案',
    icon: UserIcon
  },
  { 
    key: 'resumes', 
    name: '我的简历',
    icon: DocumentIcon
  },
  { 
    key: 'creations', 
    name: '我的创作',
    icon: DocumentTextIcon
  },
  { 
    key: 'portfolio', 
    name: '作品集',
    icon: PhotoIcon
  },
  { 
    key: 'favorites', 
    name: '我的收藏',
    icon: StarIcon
  },
  { 
    key: 'messages', 
    name: '我的消息',
    icon: EnvelopeIcon
  },
  { 
    key: 'homepage', 
    name: '我的主页',
    icon: GlobeAltIcon
  },
  { 
    key: 'account', 
    name: '账户设置',
    icon: Cog6ToothIcon
  }
]

// 模拟数据
const portfolioCount = ref(4) // 假设有4个作品
const creationsCount = ref(5) // 假设有5个创作
const favoritesCount = ref(10) // 假设有10个收藏
const unreadMessagesCount = ref(3) // 假设有3条未读消息

const messageBadge = computed(() => unreadMessagesCount.value)

// 移动端底部导航按钮
const mobileActions = [
  {
    key: 'more',
    label: '更多',
    icon: Bars3Icon,
    handler: () => { 
      isMobileMenuOpen.value = true 
    }
  },
  {
    key: 'profile',
    label: '档案',
    icon: UserIcon,
    handler: () => handleTabChange('profile')
  },
  {
    key: 'resumes',
    label: '简历',
    icon: DocumentIcon,
    handler: () => handleTabChange('resumes')
  },
  {
    key: 'messages',
    label: '消息',
    icon: EnvelopeIcon,
    handler: () => handleTabChange('messages'),
    badge: messageBadge
  },
  {
    key: 'account',
    label: '设置',
    icon: Cog6ToothIcon,
    handler: () => handleTabChange('account')
  }
]

// 移动端菜单状态
const isMobileMenuOpen = ref(false)

// 处理移动端标签切换
const handleMobileTabChange = (key) => {
  currentTab.value = key
  isMobileMenuOpen.value = false
}

// 动态组件
const currentComponent = computed(() => {
  switch (currentTab.value) {
    case 'profile':
      return MyProfile
    case 'homepage':
      return MyHomepage
    case 'resumes':
      return MyResumes
    case 'creations':
      return MyCreations
    case 'portfolio':
      return MyPortfolio
    case 'favorites':
      return MyFavorites
    case 'messages':
      return MyMessages
    case 'account':
      return AccountSettings
    default:
      return MyProfile
  }
})

// 从 store 或者 API 获取完整度数据
const completionData = ref({
  total_score: 0
})

// 获取完整度数据
const fetchCompleteness = async () => {
  try {
    const response = await profile.getCompleteness()
    if (response.data?.code === 200 && response.data?.data) {
      completionData.value = response.data.data
    }
  } catch (error) {
    console.error('获取简历完整度失败:', error)
  }
}

// 获取标签指标
const getTabMetric = (key) => {
  switch (key) {
    case 'profile':
      const score = Math.round(completionData.value.total_score || 0)
      return score + '分'
    case 'resumes':
      return '2'
    case 'creations':
      return creationsCount.value
    case 'portfolio':
      return portfolioCount.value
    case 'favorites':
      return favoritesCount.value
    case 'messages':
      return unreadMessagesCount.value
    default:
      return ''
  }
}

// 在组件挂载时获取数据
onMounted(async () => {
  await fetchCompleteness()
})

// 监听路由变化，在进入个人资料页时刷新数据
watch(() => route.path, async (newPath) => {
  if (newPath.includes('/user/profile')) {
    await fetchCompleteness()
  }
})

// 推荐职位数据
const recommendedJobs = [
  {
    id: 1,
    title: '高级前端工程师',
    company: '字节跳动',
    salary: '25-35K'
  },
  {
    id: 2,
    title: '资深产品经理',
    company: '腾讯',
    salary: '30-45K'
  },
  {
    id: 3,
    title: 'UI设计师',
    company: '阿里巴巴',
    salary: '20-30K'
  }
]

// 判断标签是否激活
const isActiveTab = (key) => {
  if (key === 'more') {
    return false // "更多"按钮永远不会处于激活状态
  }
  return currentTab.value === key
}
 </script>
 
 <style scoped>
 .user-center {
   min-height: 100vh;
   display: flex;
   flex-direction: column;
 }

 /* 确保移动端底部导航不会遮挡内容 */
 @media (max-width: 1024px) {
   .user-center {
     padding-bottom: calc(env(safe-area-inset-bottom) + 56px); /* 56px 是底部导航栏的高度 */
   }
   
   .safe-area-inset-bottom {
     padding-bottom: env(safe-area-inset-bottom);
   }

   /* 防止水平滚动 */
   .overflow-x-auto {
     -webkit-overflow-scrolling: touch;
     scrollbar-width: none; /* Firefox */
     -ms-overflow-style: none; /* IE and Edge */
   }
   
   .overflow-x-auto::-webkit-scrollbar {
     display: none; /* Chrome, Safari and Opera */
   }
 }
 </style>