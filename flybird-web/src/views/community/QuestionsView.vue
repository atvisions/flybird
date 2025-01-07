<template>
  <div class="py-4 pb-24 lg:py-6 mt-[72px]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 顶部横幅 -->
      <PageBanner theme="violet">
        <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">问答社区</h1>
        <p class="text-gray-600 text-lg max-w-2xl">解答技术难题，分享解决方案</p>
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
                <button class="h-9 px-4 sm:px-5 bg-gradient-to-r from-violet-600 to-indigo-600 text-white rounded-full hover:shadow-lg hover:shadow-violet-500/20 transition-all duration-300 text-sm font-medium flex items-center group">
                  <PlusIcon class="w-4 h-4 mr-1.5 sm:mr-2 group-hover:scale-110 transition-transform" />
                  <span class="hidden sm:inline">发布问题</span>
                  <span class="sm:hidden">发布</span>
                </button>
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
                v-for="category in categories"
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

      <!-- 问答列表和右侧内容 -->
      <div class="flex flex-col lg:flex-row gap-4 lg:gap-6 mt-4 lg:mt-6">
        <!-- 左侧问答列表 -->
        <div class="lg:flex-1">
          <!-- 问答列表 -->
          <div class="bg-white rounded-lg lg:rounded-xl border border-gray-100 p-4 lg:p-6">
            <div class="flex items-center justify-between mb-3 lg:mb-6">
              <h2 class="text-lg font-bold text-gray-900">全部问答</h2>
              共 {{ filteredQuestions.length }} 个问题
            </div>
            <div class="space-y-3 lg:space-y-5">
              <div v-for="question in paginatedQuestions" :key="question.id"
                class="group cursor-pointer rounded-lg lg:rounded-xl hover:bg-gray-50 transition-colors"
              >
                <div class="p-4">
                  <!-- 问题标题和标签 -->
                  <div class="flex items-start gap-4">
                    <div class="flex-1 min-w-0">
                      <div class="flex items-center gap-2 mb-2">
                        <span 
                          class="px-2 py-1 text-xs font-medium rounded-full"
                          :class="{
                            'bg-orange-100 text-orange-600': question.status === 'unsolved',
                            'bg-green-100 text-green-600': question.status === 'solved',
                            'bg-purple-100 text-purple-600': question.status === 'featured',
                            'bg-blue-100 text-blue-600': question.status === 'reward'
                          }"
                        >
                          {{ getStatusText(question.status) }}
                        </span>
                        <span class="text-xs text-gray-500">{{ question.createTime }}</span>
                      </div>
                      <h3 class="text-base font-medium text-gray-900 group-hover:text-blue-600 transition-colors line-clamp-1 mb-2">
                        {{ question.title }}
                      </h3>
                      <p class="text-sm text-gray-500 line-clamp-2 mb-4">{{ question.description }}</p>
                      <div class="flex flex-wrap items-center gap-4">
                        <div class="flex items-center space-x-2">
                          <img :src="question.author.avatar" class="w-5 h-5 rounded-full">
                          <span class="text-sm text-gray-600">{{ question.author.name }}</span>
                        </div>
                        <div class="flex items-center text-xs text-gray-500 space-x-3">
                          <span class="flex items-center">
                            <EyeIcon class="w-3 h-3 mr-1" />{{ question.views }}
                          </span>
                          <span class="flex items-center">
                            <ChatBubbleLeftIcon class="w-3 h-3 mr-1" />{{ question.answers }}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 分页导航 -->
          <div class="mt-8 flex justify-center">
            <!-- ... 分页导航保持不变 ... -->
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
      :categories="categories"
      @category-change="handleCategoryChange"
    />
    <!-- 使用移动端底部导航栏 -->
    <MobileTabBar :menu-groups="menuGroups" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { 
  EyeIcon, 
  ChatBubbleLeftIcon,
  ArrowsUpDownIcon,
  ChevronDownIcon,
  FireIcon,
  ClockIcon,
  HandThumbUpIcon,
  PlusIcon,
  UserIcon,
  ChevronRightIcon,
  ChevronLeftIcon
} from '@heroicons/vue/24/outline'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import PageBanner from '@/components/common/PageBanner.vue'
import CategoryMenu from '@/components/CategoryMenu.vue'
import MobileTabBar from '@/components/MobileTabBar.vue'
import { mainCategories, communityCategories } from '@/config/communityCategories'

const router = useRouter()
const store = useStore()

// 使用 Vuex store 的 isAuthenticated 状态
const isAuthenticated = computed(() => store.state.isAuthenticated)

// 状态管理
const currentCategory = ref('all')
const showSortMenu = ref(false)
const currentSort = ref('popular')
const currentPage = ref(1)
const pageSize = 10

// 排序选项
const sortOptions = {
  popular: { label: '最受欢迎', icon: FireIcon },
  newest: { label: '最新发布', icon: ClockIcon },
  answers: { label: '最多回答', icon: ChatBubbleLeftIcon },
  views: { label: '最多浏览', icon: EyeIcon }
}

// 分页后的问题列表
const paginatedQuestions = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  const end = start + pageSize
  return filteredQuestions.value.slice(start, end)
})

// 总页数
const totalPages = computed(() => {
  return Math.ceil(filteredQuestions.value.length / pageSize)
})

// 处理排序
const handleSort = (value) => {
  currentSort.value = value
  showSortMenu.value = false
}

// 问答数据
const questions = ref([
  {
    id: 1,
    title: '如何优雅地处理Vue3项目中的全局状态管理？',
    description: '在开发大型Vue3项目时，需要管理复杂的全局状态。目前正在考虑使用Pinia，但对于一些最佳实践还不太清楚，特别是在处理异步操作和模块拆分方面...',
    author: {
      name: '张小明',
      avatar: 'https://picsum.photos/32/32?random=1'
    },
    status: 'unsolved',
    answers: 12,
    views: 1234,
    createTime: '2小时前'
  },
  {
    id: 2,
    title: 'Vue3性能优化的最佳实践有哪些？',
    description: '最近在做一个Vue3项目的性能优化，主要涉及到大数据列表渲染、组件懒加载等方面。想请教下大家在实际项目中都采用了哪些优化手段？',
    author: {
      name: '李大山',
      avatar: 'https://picsum.photos/32/32?random=2'
    },
    status: 'solved',
    answers: 8,
    views: 892,
    createTime: '4小时前'
  },
  {
    id: 3,
    title: 'TypeScript 在大型项目中的实践经验分享',
    description: '团队正在将一个大型 JavaScript 项目迁移到 TypeScript，想了解下其他团队在类型定义、代码组织、工具链配置等方面的最佳实践。',
    author: {
      name: '王大力',
      avatar: 'https://picsum.photos/32/32?random=3'
    },
    status: 'featured',
    answers: 15,
    views: 1567,
    createTime: '6小时前'
  },
  {
    id: 4,
    title: '微前端架构下的性能优化策略',
    description: '在微前端架构中遇到了一些性能问题，主要是首屏加载速度和应用间通信的性能。希望能得到一些实践经验的分享。',
    author: {
      name: '赵明',
      avatar: 'https://picsum.photos/32/32?random=4'
    },
    status: 'reward',
    answers: 20,
    views: 2023,
    createTime: '8小时前'
  },
  {
    id: 5,
    title: 'Node.js 内存泄漏问题排查与解决',
    description: '生产环境的 Node.js 服务出现内存泄漏，导致需要频繁重启。想请教下如何有效地排查和解决此类问题。',
    author: {
      name: '陈小红',
      avatar: 'https://picsum.photos/32/32?random=5'
    },
    status: 'unsolved',
    answers: 6,
    views: 876,
    createTime: '12小时前'
  },
  {
    id: 6,
    title: 'React 18 新特性在实际项目中的应用',
    description: '想了解下大家在项目中是如何使用 React 18 的新特性的，特别是 Concurrent Mode 和 Suspense 的实践经验。',
    author: {
      name: '周建国',
      avatar: 'https://picsum.photos/32/32?random=6'
    },
    status: 'solved',
    answers: 18,
    views: 1432,
    createTime: '1天前'
  },
  {
    id: 7,
    title: 'GraphQL 在复杂业务场景下的优化',
    description: '在使用 GraphQL 处理复杂的业务查询时遇到了性能问题，特别是涉及到深层嵌套和多表关联的场景。',
    author: {
      name: '李云',
      avatar: 'https://picsum.photos/32/32?random=7'
    },
    status: 'featured',
    answers: 10,
    views: 945,
    createTime: '1天前'
  },
  {
    id: 8,
    title: '前端监控系统的设计与实现',
    description: '正在搭建一个前端监控系统，需要覆盖性能监控、错误监控、用户行为分析等功能。希望能得到一些架构设计的建议。',
    author: {
      name: '张监控',
      avatar: 'https://picsum.photos/32/32?random=8'
    },
    status: 'reward',
    answers: 25,
    views: 2890,
    createTime: '2天前'
  },
  {
    id: 9,
    title: 'WebAssembly 在图像处理中的应用',
    description: '想在浏览器端实现一些复杂的图像处理功能，考虑使用 WebAssembly。想了解下在实际项目中的应用案例。',
    author: {
      name: '王图像',
      avatar: 'https://picsum.photos/32/32?random=9'
    },
    status: 'unsolved',
    answers: 8,
    views: 1234,
    createTime: '2天前'
  },
  {
    id: 10,
    title: 'CSS 架构设计：如何管理大型项目的样式代码',
    description: '在维护一个大型项目的 CSS 代码时遇到了一些问题，想了解下大家是如何组织和管理样式代码的，包括命名规范、模块化方案等。',
    author: {
      name: '刘样式',
      avatar: 'https://picsum.photos/32/32?random=10'
    },
    status: 'solved',
    answers: 16,
    views: 1678,
    createTime: '3天前'
  }
])

// 筛选问题
const filteredQuestions = computed(() => {
  let result = [...questions.value]
  
  // 应用分类筛选
  if (currentCategory.value !== 'all') {
    result = result.filter(question => question.category === currentCategory.value)
  }
  
  // 应用排序
  switch (currentSort.value) {
    case 'popular':
      result.sort((a, b) => b.views - a.views)
      break
    case 'newest':
      result.sort((a, b) => new Date(b.createTime) - new Date(a.createTime))
      break
    case 'answers':
      result.sort((a, b) => b.answers - a.answers)
      break
    case 'views':
      result.sort((a, b) => b.views - a.views)
      break
  }
  
  return result
})

// 热门问题
const hotQuestions = computed(() => 
  [...questions.value]
    .sort((a, b) => b.answers - a.answers)
    .slice(0, 5)
)

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

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    unsolved: '待解决',
    solved: '已解决',
    featured: '精选',
    reward: '悬赏'
  }
  return statusMap[status] || status
}

// 使用问答页面的配置
const categoryConfig = communityCategories.questions
const categories = computed(() => categoryConfig.categories)
</script> 