<template>
  <div class="py-4 pb-24 lg:py-6 mt-[28px] md:mt-[72px]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 顶部横幅 -->
      <PageBanner theme="violet">
        <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">技术文章</h1>
        <p class="text-gray-600 text-lg max-w-2xl">分享技术经验，共同成长</p>
      </PageBanner>

      <!-- 移动端当前分类显示 -->
      <div class="flex items-center justify-between py-3 sm:hidden">
        <div class="flex items-center space-x-2">
          <span class="text-sm text-gray-500">当前：</span>
          <span class="text-sm font-medium text-gray-900">
            {{ currentCategoryName }}
          </span>
        </div>
        <button 
          class="text-sm text-gray-500 hover:text-gray-900 flex items-center"
          @click="showCategoryMenu = true"
        >
          切换分类
          <ChevronRightIcon class="w-4 h-4 ml-1" />
        </button>
      </div>

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
                  <span class="hidden sm:inline">发布内容</span>
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

      <!-- 文章列表和右侧内容 -->
      <div class="flex flex-col lg:flex-row gap-4 lg:gap-6 mt-4 lg:mt-6">
        <!-- 左侧文章列表 -->
        <div class="lg:flex-1 lg:max-w-[calc(100%-320px-24px)]">
          <!-- 文章列表 -->
          <div class="bg-white rounded-lg lg:rounded-xl border border-gray-100 p-4 lg:p-6">
            <div class="flex items-center justify-between mb-3 lg:mb-6">
              <h2 class="text-lg font-bold text-gray-900">全部文章</h2>
              
              共 {{ filteredArticles.length }} 篇文章
            </div>
            <div class="space-y-3 lg:space-y-5">
              <div v-for="(article, index) in articles" :key="article.id"
                class="group cursor-pointer rounded-lg lg:rounded-xl hover:bg-gray-50 transition-colors"
              >
                <!-- 使用flex-col在移动端垂直布局，lg:flex-row在大屏幕水平布局 -->
                <div class="flex flex-col lg:flex-row gap-3 lg:gap-4 p-3 lg:p-4">
                  <!-- 序号和内容容器 -->
                  <div class="flex flex-1 gap-4">
                    <!-- 文章信息 -->
                    <div class="flex-1 min-w-0">
                      <div class="flex items-center space-x-2 mb-3">
                        <span class="px-3 py-1 bg-blue-500/90 rounded-full text-xs font-medium text-white">
                          {{ article.category }}
                        </span>
                        <span class="text-xs text-gray-500">{{ article.createTime }}</span>
                      </div>
                      <h3 class="text-base font-medium text-gray-900 group-hover:text-blue-600 transition-colors line-clamp-1 mb-2">
                        {{ article.title }}
                      </h3>
                      <!-- 在移动端隐藏描述 -->
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
                          <span class="hidden sm:inline">{{ article.createTime }}</span>
                        </div>
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
          </div>

          <!-- 分页导航 -->
          <div class="mt-8 flex justify-center">
            <nav class="flex items-center gap-2">
              <button 
                class="w-10 h-10 rounded-lg border border-gray-200 flex items-center justify-center text-gray-500 hover:border-gray-300 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="currentPage === 1"
                @click="currentPage--"
              >
                <ChevronLeftIcon class="w-5 h-5" />
              </button>
              
              <div class="flex items-center gap-1">
                <button
                  v-for="page in totalPages"
                  :key="page"
                  @click="currentPage = page"
                  class="w-10 h-10 rounded-lg flex items-center justify-center text-sm font-medium transition-colors"
                  :class="[
                    currentPage === page
                      ? 'bg-gray-900 text-white'
                      : 'text-gray-600 hover:bg-gray-100'
                  ]"
                >
                  {{ page }}
                </button>
              </div>
              
              <button 
                class="w-10 h-10 rounded-lg border border-gray-200 flex items-center justify-center text-gray-500 hover:border-gray-300 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="currentPage === totalPages"
                @click="currentPage++"
              >
                <ChevronRightIcon class="w-5 h-5" />
              </button>
            </nav>
          </div>
        </div>

        <!-- 右侧内容 -->
        <div class="lg:w-[320px] space-y-6">
          <!-- 推荐文章 -->
          <div class="bg-white rounded-lg lg:rounded-xl border border-gray-100 p-4 lg:p-6">
            <h2 class="text-lg font-bold text-gray-900 mb-4 flex items-center justify-between">
              <span>推荐文章</span>
              <a href="#" class="text-sm font-medium text-gray-500 hover:text-gray-900">更多</a>
            </h2>
            <div class="space-y-4">
              <!-- 推荐文章列表 -->
              <div v-for="article in recommendedArticles" :key="article.id"
                class="group cursor-pointer rounded-lg lg:rounded-xl hover:bg-gray-50 transition-colors"
              >
                <div class="flex p-4 items-center space-x-4">
                  <div class="w-20 h-20 rounded-lg overflow-hidden flex-shrink-0">
                    <img :src="article.cover" class="w-full h-full object-cover" alt="">
                  </div>
                  <div class="flex-1 min-w-0">
                    <h3 class="text-sm font-medium text-gray-900 line-clamp-2 group-hover:text-blue-600 transition-colors">
                      {{ article.title }}
                    </h3>
                    <div class="mt-2 flex items-center text-xs text-gray-500">
                      <span class="flex items-center">
                        <EyeIcon class="w-3 h-3 mr-1" />{{ article.views }}
                      </span>
                      <span class="mx-2">·</span>
                      <span>{{ article.createTime }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 文章排行 -->
          <div class="bg-white rounded-lg lg:rounded-xl border border-gray-100 p-4 lg:p-6">
            <h2 class="text-lg font-bold text-gray-900 mb-4 flex items-center justify-between">
              <span>文章排行</span>
              <a href="#" class="text-sm font-medium text-gray-500 hover:text-gray-900">更多</a>
            </h2>
            <div class="space-y-4">
              <div v-for="(article, index) in topArticles" :key="article.id"
                class="group cursor-pointer rounded-lg lg:rounded-xl hover:bg-gray-50 transition-colors"
              >
                <div class="flex items-start space-x-4 p-4">
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
                  <div class="flex-1 min-w-0">
                    <h3 class="text-sm font-medium text-gray-900 line-clamp-2 group-hover:text-blue-600 transition-colors">
                      {{ article.title }}
                    </h3>
                    <div class="mt-2 flex items-center text-xs text-gray-500">
                      <span class="flex items-center">
                        <EyeIcon class="w-3 h-3 mr-1" />{{ article.views }}
                      </span>
                      <span class="mx-2">·</span>
                      <span class="flex items-center">
                        <ChatBubbleLeftIcon class="w-3 h-3 mr-1" />{{ article.comments }}
                      </span>
                    </div>
                  </div>
                </div>
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
  ChevronLeftIcon,
  HomeIcon,
  CodeBracketIcon,
  ServerIcon,
  DevicePhoneMobileIcon,
  SparklesIcon,
  CogIcon
} from '@heroicons/vue/24/outline'
import { useRouter, useRoute } from 'vue-router'
import { useStore } from 'vuex'
import PageBanner from '@/components/common/PageBanner.vue'
import CategoryMenu from '@/components/CategoryMenu.vue'
import MobileTabBar from '@/components/MobileTabBar.vue'
import { mainCategories, communityCategories } from '@/config/communityCategories'

const router = useRouter()
const route = useRoute()
const store = useStore()

const currentCategory = ref('all')
const showSortMenu = ref(false)
const currentSort = ref('popular')

// 排序选项
const sortOptions = {
  popular: { label: '最受欢迎', icon: FireIcon },
  newest: { label: '最新发布', icon: ClockIcon },
  comments: { label: '最多评论', icon: ChatBubbleLeftIcon },
  likes: { label: '最多点赞', icon: HandThumbUpIcon }
}

// 处理排序
const handleSort = (value) => {
  currentSort.value = value
  showSortMenu.value = false
}

// 文章数据
const articles = ref([
  {
    id: 1,
    type: 'article',
    category: 'frontend',
    title: '2024年前端开发趋势展望',
    description: '探讨新的前端框架、工具和最佳实践，帮助开发者在新的一年保持技术领先。包括AI辅助开发、WebAssembly应用、微前端架构等热门话题。',
    cover: 'https://picsum.photos/600/300?random=1',
    author: {
      name: '张小明',
      avatar: 'https://picsum.photos/32/32?random=1'
    },
    createTime: '2小时前',
    views: 1234,
    comments: 56
  },
  {
    id: 2,
    type: 'article',
    category: 'backend',
    title: 'Spring Boot 3.0 新特性详解',
    description: '深入解析Spring Boot 3.0的重要更新，包括原生支持GraalVM、HTTP接口声明式客户端、改进的AOT支持等特性。',
    cover: 'https://picsum.photos/600/300?random=2',
    author: {
      name: '李大山',
      avatar: 'https://picsum.photos/32/32?random=2'
    },
    createTime: '3小时前',
    views: 892,
    comments: 45
  },
  {
    id: 3,
    type: 'article',
    category: 'architecture',
    title: '微服务架构实践：从单体到微服务的演进之路',
    description: '分享一个大型企业级应用从单体架构迁移到微服务的实践经验，包括服务拆分策略、数据一致性处理、服务治理等核心话题。',
    cover: 'https://picsum.photos/600/300?random=3',
    author: {
      name: '王大力',
      avatar: 'https://picsum.photos/32/32?random=3'
    },
    createTime: '5小时前',
    views: 1567,
    comments: 89
  },
  {
    id: 4,
    type: 'article',
    category: 'mobile',
    title: 'Flutter vs React Native：2024移动开发框架对比',
    description: '详细对比两大主流跨平台开发框架的优劣，从性能、生态、开发效率等多个维度进行分析，帮助开发者做出技术选型。',
    cover: 'https://picsum.photos/600/300?random=4',
    author: {
      name: '赵明',
      avatar: 'https://picsum.photos/32/32?random=4'
    },
    createTime: '6小时前',
    views: 2023,
    comments: 134
  },
  {
    id: 5,
    type: 'article',
    category: 'ai',
    title: 'AI 驱动的代码生成：提升开发效率的新方向',
    description: '探讨AI在软件开发中的应用，特别是代码生成、代码补全、代码审查等场景，以及如何有效利用AI工具提升开发效率。',
    cover: 'https://picsum.photos/600/300?random=5',
    author: {
      name: '陈小红',
      avatar: 'https://picsum.photos/32/32?random=5'
    },
    createTime: '8小时前',
    views: 3102,
    comments: 167
  },
  {
    id: 6,
    type: 'article',
    category: 'devops',
    title: 'Docker 和 Kubernetes 最佳实践指南',
    description: '详细介绍容器化和编排技术的实践经验，包括镜像优化、集群管理、服务发现、负载均衡等核心概念的实战应用。',
    cover: 'https://picsum.photos/600/300?random=6',
    author: {
      name: '周建国',
      avatar: 'https://picsum.photos/32/32?random=6'
    },
    createTime: '12小时前',
    views: 1876,
    comments: 98
  },
  {
    id: 7,
    type: 'article',
    category: 'database',
    title: 'MongoDB 性能优化实战',
    description: '深入探讨 MongoDB 在大规模应用场景下的性能优化策略，包括索引设计、查询优化、分片策略等实用技巧。',
    cover: 'https://picsum.photos/600/300?random=7',
    author: {
      name: '李云',
      avatar: 'https://picsum.photos/32/32?random=7'
    },
    createTime: '15小时前',
    views: 1543,
    comments: 76
  },
  {
    id: 8,
    type: 'article',
    category: 'algorithm',
    title: '算法之美：图算法在社交网络中的应用',
    description: '通过实际案例讲解图算法在社交网络分析中的应用，包括最短路径、社区发现、影响力分析等经典算法的实现。',
    cover: 'https://picsum.photos/600/300?random=8',
    author: {
      name: '张算法',
      avatar: 'https://picsum.photos/32/32?random=8'
    },
    createTime: '18小时前',
    views: 2234,
    comments: 145
  },
  {
    id: 9,
    type: 'article',
    category: 'frontend',
    title: 'Next.js 13 服务端组件实战',
    description: '探索 Next.js 13 中服务端组件的最佳实践，包括数据获取、状态管理、性能优化等关键主题的深入讲解。',
    cover: 'https://picsum.photos/600/300?random=9',
    author: {
      name: '王前端',
      avatar: 'https://picsum.photos/32/32?random=9'
    },
    createTime: '1天前',
    views: 1987,
    comments: 112
  },
  {
    id: 10,
    type: 'article',
    category: 'backend',
    title: 'Go 微服务框架选型对比',
    description: '对比主流的 Go 微服务框架，从性能、易用性、生态等多个维度进行分析，帮助开发者选择适合的技术栈。',
    cover: 'https://picsum.photos/600/300?random=10',
    author: {
      name: '刘后端',
      avatar: 'https://picsum.photos/32/32?random=10'
    },
    createTime: '1天前',
    views: 2456,
    comments: 167
  }
])

// 根据分类和排序筛选文章
const filteredArticles = computed(() => {
  let result = [...articles.value]
  
  // 应用分类筛选
  if (currentCategory.value !== 'all') {
    result = result.filter(article => article.category === currentCategory.value)
  }
  
  // 应用排序
  switch (currentSort.value) {
    case 'popular':
      result.sort((a, b) => b.views - a.views)
      break
    case 'newest':
      result.sort((a, b) => new Date(b.createTime) - new Date(a.createTime))
      break
    case 'comments':
      result.sort((a, b) => b.comments - a.comments)
      break
  }
  
  return result
})

// 推荐文章（浏览量最高的前3篇）
const recommendedArticles = computed(() => 
  [...articles.value]
    .sort((a, b) => b.views - a.views)
    .slice(0, 3)
)

// 文章排行（最近一周最热门的文章）
const topArticles = computed(() => 
  [...articles.value]
    .sort((a, b) => b.views + b.comments * 2 - (a.views + a.comments * 2))
    .slice(0, 5)
)

// 使用 Vuex store 的 isAuthenticated 状态
const isAuthenticated = computed(() => store.state.isAuthenticated)

// 分页相关
const currentPage = ref(1)
const pageSize = 10

// 分页后的文章列表
const paginatedArticles = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  const end = start + pageSize
  return filteredArticles.value.slice(start, end)
})

// 总页数
const totalPages = computed(() => {
  return Math.ceil(filteredArticles.value.length / pageSize)
})

// 分类相关状态
const showCategoryMenu = ref(false)
const currentLevel = ref('main')
const currentMainCategory = ref('all')
const currentSubCategory = ref('')
const currentThirdCategory = ref('')

// 使用 communityCategories 配置
const categoryConfig = communityCategories.articles
const categories = computed(() => categoryConfig.categories)

// 获取当前分类名称
const currentCategoryName = computed(() => {
  if (currentMainCategory.value === 'all') return '全部'
  const category = categories.value.find(c => c.id === currentMainCategory.value)
  return category?.name || ''
})

// 处理分类切换
const handleCategoryChange = (categoryId, level = 'main') => {
  if (level === 'main') {
    currentMainCategory.value = categoryId
    currentSubCategory.value = ''
    currentThirdCategory.value = ''
    showCategoryMenu.value = false
  }
}
</script> 