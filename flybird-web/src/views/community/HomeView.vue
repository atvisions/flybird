<template>
  <div class="min-h-screen py-4 pb-24 lg:py-6 mt-[72px]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 顶部横幅 -->
      <PageBanner theme="violet">
        <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">社区广场</h1>
        <p class="text-gray-600 text-lg max-w-2xl">分享技术经验，共同成长</p>
      </PageBanner>

      <!-- PC端导航 -->
      <div class="mt-6 bg-white rounded-xl border border-gray-100 p-4 hidden md:block mb-6">
        <div class="flex flex-col gap-4">
          <!-- 左侧主导航和右侧按钮 -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <!-- 左侧主导航 -->
            <div class="flex items-center -mx-1">
              <router-link
                v-for="nav in mainCategories"
                :key="nav.path"
                :to="nav.path"
                class="px-4 sm:px-6 py-3 mx-1 text-sm font-medium transition-colors group whitespace-nowrap flex items-center"
                :class="[
                  $route.path === nav.path
                    ? 'text-gray-900'
                    : 'text-gray-500 hover:text-gray-700'
                ]"
              >
                <component :is="nav.icon" class="w-4 h-4 mr-2 flex-shrink-0" />
                <span class="relative">
                  {{ nav.name }}
                  <span 
                    class="absolute left-1/2 -translate-x-1/2 -bottom-3 w-1.5 h-1.5 rounded-full transition-colors"
                    :class="$route.path === nav.path ? 'bg-gray-900' : 'bg-transparent group-hover:bg-gray-200'"
                  ></span>
                </span>
              </router-link>
            </div>

            <!-- 右侧操作按钮 -->
            <div class="flex items-center gap-2 sm:gap-3">
              <template v-if="isAuthenticated">
                <!-- 发布按钮 -->
                <router-link 
                  to="/community/create?type=article"
                  class="h-9 px-4 sm:px-5 bg-gradient-to-r from-violet-600 to-indigo-600 text-white rounded-full hover:shadow-lg hover:shadow-violet-500/20 transition-all duration-300 text-sm font-medium flex items-center group"
                >
                  <PlusIcon class="w-4 h-4 mr-1.5 sm:mr-2 group-hover:scale-110 transition-transform" />
                  <span class="hidden sm:inline">发布内容</span>
                  <span class="sm:hidden">发布</span>
                </router-link>
              </template>
              <template v-else>
                <!-- 登录按钮 -->
                <router-link 
                  :to="`/login?redirect=${encodeURIComponent($route.fullPath)}`"
                  class="h-9 px-4 sm:px-5 bg-gradient-to-r from-violet-600 to-indigo-600 text-white rounded-full hover:shadow-lg hover:shadow-violet-500/20 transition-all duration-300 text-sm font-medium flex items-center group"
                >
                  <UserIcon class="w-4 h-4 mr-1.5 sm:mr-2 group-hover:scale-110 transition-transform" />
                  <span>登录</span>
                </router-link>
              </template>
            </div>
          </div>

          <!-- 分隔线 -->
          <div class="h-px bg-gray-200"></div>

          <!-- 分类标签 -->
          <div class="flex items-center h-10 justify-between">
            <!-- 左侧分类标签 -->
            <div class="flex items-center -mx-1 overflow-x-auto no-scrollbar">
              <button
                v-for="category in homeCategories"
                :key="category.id"
                @click="handleCategoryChange(category.id)"
                class="h-10 px-4 mx-1 rounded-full text-sm font-medium transition-colors whitespace-nowrap inline-flex items-center"
                :class="[
                  currentMainCategory === category.id
                    ? 'bg-gray-900 text-white'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                ]"
              >
                <component :is="category.icon" class="w-4 h-4 mr-2 flex-shrink-0" />
                {{ category.name }}
              </button>
            </div>

            <!-- 右侧排序按钮 -->
            <div class="relative flex-shrink-0 ml-4">
              <button 
                @click="showSortMenu = !showSortMenu"
                class="h-10 inline-flex items-center px-4 bg-white border border-gray-200 rounded-lg text-sm font-medium hover:border-gray-300"
              >
                <ArrowsUpDownIcon class="w-4 h-4 mr-2 text-gray-500 flex-shrink-0" />
                {{ sortOptions[currentSort]?.label || '排序' }}
                <ChevronDownIcon class="w-4 h-4 ml-2 text-gray-500 flex-shrink-0" />
              </button>
              
              <div v-if="showSortMenu"
                class="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg border border-gray-100 py-1 z-20"
              >
                <button
                  v-for="(option, key) in sortOptions"
                  :key="key"
                  @click="handleSort(key)"
                  class="w-full px-4 py-2 text-left text-sm hover:bg-gray-50 inline-flex items-center"
                  :class="{ 'text-gray-900 font-medium': currentSort === key, 'text-gray-600': currentSort !== key }"
                >
                  <component 
                    :is="option.icon" 
                    class="w-4 h-4 mr-2 flex-shrink-0"
                    :class="currentSort === key ? 'text-gray-900' : 'text-gray-400'"
                  />
                  {{ option.label }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 内容列表和右侧内容 -->
      <div class="flex flex-col lg:flex-row gap-4 lg:gap-6 mt-4 lg:mt-6">
        <!-- 左侧内容列表 -->
        <div class="lg:flex-1 lg:max-w-[calc(100%-320px-24px)]">
          <!-- 置顶话题 -->
          <div class="bg-white rounded-lg lg:rounded-xl border border-gray-100 p-4 lg:p-6 mb-4 lg:mb-6">
            <!-- 话题标题 -->
            <div class="flex items-center space-x-2 mb-6">
              <div class="flex items-center space-x-2">
                <span class="px-2 py-1 bg-rose-500 rounded-full text-xs font-medium text-white">置顶</span>
                <h3 class="text-xl font-bold text-gray-900">每周技术分享：前端框架之争</h3>
              </div>
            </div>

            <!-- 作者信息 -->
            <div class="flex items-center space-x-3 mb-6">
              <div class="flex items-center space-x-2">
                <img src="https://picsum.photos/32/32?random=1" class="w-6 h-6 rounded-full">
                <span class="text-sm text-gray-600">技术社区</span>
              </div>
              <span class="text-xs text-gray-500">2小时前</span>
            </div>

            <!-- VS选项对比区域 -->
            <div class="relative mb-8">
              <!-- 进度条背景 -->
              <div class="absolute inset-0 flex rounded-xl overflow-hidden">
                <!-- 左侧进度 -->
                <div 
                  class="h-full bg-gradient-to-r from-blue-50 to-blue-100"
                  style="width: 60%"
                ></div>
                <!-- 右侧进度 -->
                <div 
                  class="h-full bg-gradient-to-l from-purple-50 to-purple-100"
                  style="width: 40%"
                ></div>
              </div>

              <!-- 选项内容 -->
              <div class="relative flex items-center min-h-[100px]">
                <!-- 选项A -->
                <div class="flex-1 p-6">
                  <div class="text-center">
                    <!-- 百分比指示器 -->
                    <div class="absolute -top-3 left-[25%] -translate-x-1/2 px-3 py-1 bg-blue-600 rounded-full text-white text-xs font-medium">
                      60%
                    </div>
                    <div class="text-lg font-medium text-blue-600 mb-2">Vue 3</div>
                    <div class="text-sm text-gray-500 mb-4">234 票</div>
                    <!-- 投票按钮 -->
                    <button 
                      class="px-6 h-10 rounded-full bg-blue-50 hover:bg-blue-100 transition-colors mx-auto flex items-center justify-center cursor-pointer"
                    >
                      <span class="text-sm font-medium text-blue-600">投票</span>
                    </button>
                  </div>
                </div>

                <!-- VS标志 -->
                <div class="w-10 h-10 rounded-full bg-white shadow-sm flex items-center justify-center z-10">
                  <span class="text-xs font-bold text-gray-400">VS</span>
                </div>

                <!-- 选项B -->
                <div class="flex-1 p-6">
                  <div class="text-center">
                    <!-- 百分比指示器 -->
                    <div class="absolute -top-3 right-[25%] translate-x-1/2 px-3 py-1 bg-purple-600 rounded-full text-white text-xs font-medium">
                      40%
                    </div>
                    <div class="text-lg font-medium text-purple-600 mb-2">React</div>
                    <div class="text-sm text-gray-500 mb-4">156 票</div>
                    <!-- 投票按钮 -->
                    <button 
                      class="px-6 h-10 rounded-full bg-purple-50 hover:bg-purple-100 transition-colors mx-auto flex items-center justify-center cursor-pointer"
                    >
                      <span class="text-sm font-medium text-purple-600">投票</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- 底部信息 -->
            <div class="flex items-center justify-between">
              <!-- 参与者头像组 -->
              <div class="flex items-center gap-2">
                <div class="flex -space-x-2">
                  <img v-for="i in 3" :key="i"
                    :src="`https://picsum.photos/32/32?random=${i}`"
                    class="w-6 h-6 rounded-full ring-2 ring-white"
                  >
                </div>
                <span class="text-xs text-gray-500">390 人参与</span>
              </div>
              <div class="flex items-center space-x-3">
                <span class="flex items-center text-xs text-gray-500">
                  <ChatBubbleLeftIcon class="w-3 h-3 mr-1" />89
                </span>
              </div>
            </div>
          </div>

          <!-- 文章列表 -->
          <div class="bg-white rounded-lg lg:rounded-xl border border-gray-100 p-4 lg:p-6">
            <!-- 内容过滤器 -->
            <div class="flex items-center justify-between mb-3 lg:mb-6">
              <div class="flex items-center space-x-4">
                <h2 class="text-lg font-medium text-gray-900">最新文章</h2>
                <span class="text-sm text-gray-500">共 {{ totalItems }} 条内容</span>
              </div>
            </div>

            <!-- 文章列表 -->
            <div class="space-y-3 lg:space-y-5">
              <div v-for="article in filteredContent" :key="article.id"
                class="group cursor-pointer rounded-lg lg:rounded-xl hover:bg-gray-50 transition-colors"
              >
                <div class="flex flex-col lg:flex-row gap-3 lg:gap-4 p-3 lg:p-4">
                  <!-- 文章信息 -->
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center space-x-2 mb-3">
                      <span class="px-3 py-1 bg-blue-500/90 rounded-full text-xs font-medium text-white">
                        {{ article.category }}
                      </span>
                      <span class="text-xs text-gray-500">{{ article.date }}</span>
                    </div>
                    <h3 class="text-base font-medium text-gray-900 group-hover:text-blue-600 transition-colors line-clamp-1 mb-2">
                      {{ article.title }}
                    </h3>
                    <p class="text-sm text-gray-500 line-clamp-1 mb-3 hidden lg:block">{{ article.description }}</p>
                    <div class="flex flex-wrap items-center gap-4">
                      <div class="flex items-center space-x-2">
                        <img :src="article.author.avatar" class="w-5 h-5 rounded-full">
                        <span class="text-sm text-gray-600">{{ article.author.name }}</span>
                      </div>
                      <div class="flex items-center text-xs text-gray-500 space-x-3">
                        <span class="flex items-center">
                          <EyeIcon class="w-3 h-3 mr-1" />{{ article.views }}
                        </span>
                        <span class="flex items-center">
                          <ChatBubbleLeftIcon class="w-3 h-3 mr-1" />{{ article.comments }}
                        </span>
                      </div>
                    </div>
                  </div>

                  <!-- 文章封面图 -->
                  <div class="flex-shrink-0 w-full lg:w-24 h-32 lg:h-24 rounded-lg overflow-hidden order-first lg:order-last">
                    <img 
                      :src="article.cover" 
                      class="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-500"
                      alt=""
                    >
                  </div>
                </div>
              </div>
            </div>

            <!-- 加载更多 -->
            <div v-if="hasMore" class="mt-8 text-center">
              <button
                class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                :disabled="loading"
                @click="loadMore"
              >
                <template v-if="!loading">加载更多</template>
                <template v-else>
                  <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-gray-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  加载中...
                </template>
              </button>
            </div>
          </div>
        </div>

        <!-- 右侧内容 -->
        <div class="lg:w-[320px] space-y-6">
          <!-- 热门问题 -->
          <div class="bg-white rounded-xl border border-gray-100 p-6">
            <h2 class="text-lg font-bold text-gray-900 mb-4">热门问题</h2>
            <div class="space-y-4">
              <div v-for="(question, index) in hotQuestions" :key="question.id"
                class="group cursor-pointer"
              >
                <div class="flex items-start space-x-3">
                  <div class="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center"
                    :class="{
                      'bg-orange-100 text-orange-600': index === 0,
                      'bg-blue-100 text-blue-600': index === 1,
                      'bg-purple-100 text-purple-600': index === 2,
                      'bg-gray-100 text-gray-600': index > 2
                    }"
                  >
                    <span class="text-sm font-medium">{{ index + 1 }}</span>
                  </div>
                  <div class="flex-1">
                    <h3 class="text-sm font-medium text-gray-900 group-hover:text-blue-600 transition-colors line-clamp-2 mb-2">
                      {{ question.title }}
                    </h3>
                    <div class="flex items-center text-xs text-gray-500">
                      <span class="flex items-center">
                        <ChatBubbleLeftIcon class="w-3 h-3 mr-1" />
                        <span class="text-blue-600 font-medium">{{ question.answers }}</span>
                        <span class="ml-1">回答</span>
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 活跃用户 -->
          <div class="bg-white rounded-xl border border-gray-100 p-6">
            <h2 class="text-lg font-bold text-gray-900 mb-4">活跃用户</h2>
            <div class="grid grid-cols-4 gap-4">
              <div v-for="user in activeUsers" :key="user.id"
                class="flex flex-col items-center"
              >
                <img :src="user.avatar" class="w-12 h-12 rounded-full mb-2">
                <span class="text-xs text-gray-600 text-center">{{ user.name }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 分类切换菜单 -->
    <CategoryMenu v-if="showCategoryMenu" 
      v-model:show="showCategoryMenu"
      v-model:currentLevel="currentLevel"
      v-model:currentMainCategory="currentMainCategory"
      v-model:currentSubCategory="currentSubCategory"
      v-model:currentThirdCategory="currentThirdCategory"
      :categories="homeCategories"
      @category-change="handleCategoryChange"
    />

    <!-- 使用移动端底部导航栏 -->
    <MobileTabBar :menu-groups="menuGroups" />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { mainCategories } from '@/config/communityCategories'
import MobileTabBar from '@/components/MobileTabBar.vue'
import { PlusIcon, UserIcon, ArrowsUpDownIcon, ChevronDownIcon } from '@heroicons/vue/24/outline'
import ContentCard from '@/components/community/ContentCard.vue'
import PageBanner from '@/components/common/PageBanner.vue'
import CategoryMenu from '@/components/CategoryMenu.vue'
import { useCommunityData } from '@/composables/useCommunityData'
import {
  ChatBubbleLeftIcon,
  UserGroupIcon,
  EyeIcon,
  ChevronRightIcon,
  HomeIcon,
  SparklesIcon,
  ClockIcon,
  DocumentTextIcon,
  QuestionMarkCircleIcon,
  HashtagIcon,
  CodeBracketIcon,
  ServerIcon,
  FireIcon
} from '@heroicons/vue/24/outline'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
const store = useStore()

// 分类相关状态
const currentMainCategory = ref('all')
const currentSort = ref('popular')

// 移动端分类相关状态
const showCategoryMenu = ref(false)
const currentLevel = ref('main')
const currentSubCategory = ref('')
const currentThirdCategory = ref('')
// 使用 Vuex store 的 isAuthenticated 状态
const isAuthenticated = computed(() => store.state.isAuthenticated)
// 监听父组件传递的分类变化
const props = defineProps({
  currentCategory: {
    type: String,
    default: 'all'
  }
})

// 当父组件的分类变化时，更新本地分类
watch(() => props.currentCategory, (newValue) => {
  currentMainCategory.value = newValue
})

// 内容数据相关
const { 
  content,
  totalItems,
  loading,
  hasMore,
  loadMore
} = useCommunityData()

// 根据分类和排序过滤内容
const filteredContent = computed(() => {
  let result = [...content.value]
  
  // 应用分类过滤
  if (currentMainCategory.value !== 'all') {
    result = result.filter(item => item.category === currentMainCategory.value)
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

// 处理点赞
const handleLike = (contentId) => {
  // TODO: 实现点赞逻辑
  console.log('Like content:', contentId)
}

// 处理收藏
const handleCollect = (contentId) => {
  // TODO: 实现收藏逻辑
  console.log('Collect content:', contentId)
}

// 热门问题数据
const hotQuestions = ref([
  {
    id: 1,
    title: '如何优化 Vue 3 项目的性能？分享一些实践经验',
    answers: 56
  },
  {
    id: 2,
    title: 'TypeScript 在大型项目中的最佳实践是什么？',
    answers: 43
  },
  {
    id: 3,
    title: '微服务架构下如何处理分布式事务？',
    answers: 38
  },
  {
    id: 4,
    title: '前端项目如何做好错误监控和性能监控？',
    answers: 32
  },
  {
    id: 5,
    title: '如何设计一个高可用的消息队列系统？',
    answers: 29
  }
])

// 活跃用户数据
const activeUsers = ref([
  {
    id: 1,
    name: '张小明',
    avatar: 'https://picsum.photos/32/32?random=1'
  },
  {
    id: 2,
    name: '李大山',
    avatar: 'https://picsum.photos/32/32?random=2'
  },
  {
    id: 3,
    name: '王大力',
    avatar: 'https://picsum.photos/32/32?random=3'
  },
  {
    id: 4,
    name: '赵明',
    avatar: 'https://picsum.photos/32/32?random=4'
  },
  {
    id: 5,
    name: '陈小红',
    avatar: 'https://picsum.photos/32/32?random=5'
  },
  {
    id: 6,
    name: '周建国',
    avatar: 'https://picsum.photos/32/32?random=6'
  },
  {
    id: 7,
    name: '李云',
    avatar: 'https://picsum.photos/32/32?random=7'
  },
  {
    id: 8,
    name: '张算法',
    avatar: 'https://picsum.photos/32/32?random=8'
  }
])

// 首页分类
const homeCategories = [
  { id: 'all', name: '全部', icon: HomeIcon },
  { id: 'recommend', name: '推荐', icon: SparklesIcon },
  { id: 'following', name: '关注', icon: UserGroupIcon },
  { id: 'latest', name: '最新', icon: ClockIcon }
]

// 排序选项
const sortOptions = {
  popular: { label: '最受欢迎', icon: FireIcon },
  newest: { label: '最新发布', icon: ClockIcon },
  views: { label: '最多浏览', icon: EyeIcon }
}

// 获取当前分类名称
const currentCategoryName = computed(() => {
  if (currentMainCategory.value === 'all') return '全部'
  const category = homeCategories.value.find(c => c.id === currentMainCategory.value)
  return category?.name || ''
})

// 处理分类切换
const handleCategoryChange = (categoryId, level = 'main') => {
  if (level === 'main') {
    currentMainCategory.value = categoryId
    currentSubCategory.value = ''
    currentThirdCategory.value = ''
    // 根据分类ID跳转到对应页面
    switch (categoryId) {
      case 'home':
        router.push('/community')
        break
      case 'articles':
        router.push('/community/articles')
        break
      case 'topics':
        router.push('/community/topics')
        break
      case 'questions':
        router.push('/community/questions')
        break
      default:
        showCategoryMenu.value = false
    }
  } else if (level === 'sub') {
    currentSubCategory.value = categoryId
    currentThirdCategory.value = ''
    showCategoryMenu.value = false
  } else if (level === 'third') {
    currentThirdCategory.value = categoryId
    showCategoryMenu.value = false
  }
}

// 移动端底部导航菜单
const menuGroups = [
  {
    title: '社区',
    items: [
      { 
        name: '文章', 
        path: '/community/articles', 
        icon: DocumentTextIcon 
      },
      { 
        name: '问答', 
        path: '/community/questions', 
        icon: QuestionMarkCircleIcon 
      },
      { 
        name: '话题', 
        path: '/community/topics', 
        icon: HashtagIcon 
      }
    ]
  }
]

const router = useRouter()
</script> 