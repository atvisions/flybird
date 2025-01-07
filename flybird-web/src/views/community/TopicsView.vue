<template>
  <div class="py-4 pb-24 lg:py-6 mt-[72px] ">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 顶部横幅 -->
      <PageBanner theme="violet">
        <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">热门话题</h1>
        <p class="text-gray-600 text-lg max-w-2xl">参与技术讨论，表达你的观点</p>
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
                  <span class="hidden sm:inline">发起话题</span>
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

      <!-- 话题列表和右侧内容 -->
      <div class="flex flex-col lg:flex-row gap-4 lg:gap-6 mt-4 lg:mt-6">
        <!-- 左侧话题列表 -->
        <div class="lg:flex-1 lg:max-w-[calc(100%-320px-24px)]">

          <!-- 话题列表 -->
          <div class="bg-white rounded-lg lg:rounded-xl border border-gray-100 p-4 lg:p-6">
            <div class="flex items-center justify-between mb-3 lg:mb-6">
              <h2 class="text-lg font-bold text-gray-900">全部话题</h2>
              共 {{ filteredTopics.length }} 个话题
            </div>
            <div class="space-y-3 lg:space-y-5">
              <div v-for="topic in paginatedTopics" :key="topic.id"
                class="group cursor-pointer"
              >
                <!-- 话题标题 -->
                <h3 class="text-xl font-bold text-gray-900 mb-6">{{ topic.title }}</h3>
                
                <!-- 作者信息 -->
                <div class="flex items-center space-x-3 mb-6">
                  <img :src="topic.author.avatar" class="w-8 h-8 rounded-full">
                  <div class="flex items-center gap-3">
                    <span class="text-sm font-medium text-gray-900">{{ topic.author.name }}</span>
                    <span class="text-xs text-gray-500">{{ topic.createTime }}</span>
                  </div>
                </div>

                <!-- VS选项对比区域 -->
                <div class="relative mb-8">
                  <!-- 进度条背景 -->
                  <div class="absolute inset-0 flex rounded-xl overflow-hidden">
                    <!-- 左侧进度 -->
                    <div 
                      class="h-full bg-gradient-to-r from-blue-50 to-blue-100"
                      :style="{ width: `${(topic.votesA / (topic.votesA + topic.votesB)) * 100}%` }"
                    ></div>
                    <!-- 右侧进度 -->
                    <div 
                      class="h-full bg-gradient-to-l from-purple-50 to-purple-100"
                      :style="{ width: `${(topic.votesB / (topic.votesA + topic.votesB)) * 100}%` }"
                    ></div>
                  </div>

                  <!-- 选项内容 -->
                  <div class="relative flex items-center min-h-[100px]">
                    <!-- 选项A -->
                    <div class="flex-1 p-6">
                      <div class="text-center">
                        <!-- 百分比指示器 -->
                        <div class="absolute -top-3 left-[25%] -translate-x-1/2 px-3 py-1 bg-blue-600 rounded-full text-white text-xs font-medium">
                          {{ Math.round((topic.votesA / (topic.votesA + topic.votesB)) * 100) }}%
                        </div>
                        <div class="text-lg font-medium text-blue-600 mb-2">{{ topic.optionA }}</div>
                        <div class="text-sm text-gray-500 mb-4">{{ topic.votesA }} 票</div>
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
                          {{ Math.round((topic.votesB / (topic.votesA + topic.votesB)) * 100) }}%
                        </div>
                        <div class="text-lg font-medium text-purple-600 mb-2">{{ topic.optionB }}</div>
                        <div class="text-sm text-gray-500 mb-4">{{ topic.votesB }} 票</div>
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
                      <img v-for="i in Math.min(3, Math.floor((topic.votesA + topic.votesB) / 10))" :key="i"
                        :src="`https://picsum.photos/32/32?random=${topic.id * 10 + i}`"
                        class="w-6 h-6 rounded-full ring-2 ring-white"
                      >
                    </div>
                    <span class="text-xs text-gray-500">{{ topic.votesA + topic.votesB }} 人参与</span>
                  </div>
                  <div class="flex items-center space-x-3">
                    <span class="flex items-center text-xs text-gray-500">
                      <ChatBubbleLeftIcon class="w-3 h-3 mr-1" />{{ topic.comments }}
                    </span>
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
          <!-- 热门话题 -->
          <div class="bg-white rounded-xl border border-gray-100 p-6">
            <h2 class="text-lg font-bold text-gray-900 mb-4">热门话题</h2>
            <div class="space-y-4">
              <div v-for="(topic, index) in hotTopics" :key="topic.id"
                class="group cursor-pointer "
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
                      {{ topic.title }}
                    </h3>
                    <div class="flex items-center text-xs text-gray-500">
                      <span class="flex items-center">
                        <ChatBubbleLeftIcon class="w-3 h-3 mr-1" />
                        <span class="text-blue-600 font-medium">{{ topic.comments }}</span>
                        <span class="ml-1">评论</span>
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
  HomeIcon,
  BoltIcon,
  BriefcaseIcon,
  WrenchScrewdriverIcon
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
  votes: { label: '最多投票', icon: HandThumbUpIcon },
  comments: { label: '最多评论', icon: ChatBubbleLeftIcon }
}

// 处理排序
const handleSort = (value) => {
  currentSort.value = value
  showSortMenu.value = false
}

// 话题数据
const topics = ref([
  {
    id: 1,
    title: '开发移动应用选择哪个方案？',
    category: 'tech',
    optionA: 'Flutter',
    optionB: 'React Native',
    votesA: 234,
    votesB: 187,
    author: {
      name: '王大力',
      avatar: 'https://picsum.photos/32/32?random=1'
    },
    comments: 45,
    views: 1234,
    createTime: '2小时前'
  },
  {
    id: 2,
    title: '前端状态管理选型？',
    category: 'tech',
    optionA: 'Pinia',
    optionB: 'Redux',
    votesA: 1,
    votesB: 0,
    author: {
      name: '李小明',
      avatar: 'https://picsum.photos/32/32?random=2'
    },
    comments: 67,
    views: 2345,
    createTime: '4小时前'
  },
  {
    id: 3,
    title: '选择哪个UI组件库？',
    category: 'tools',
    optionA: 'Element Plus',
    optionB: 'Ant Design Vue',
    votesA: 567,
    votesB: 432,
    author: {
      name: '张前端',
      avatar: 'https://picsum.photos/32/32?random=3'
    },
    comments: 89,
    views: 3456,
    createTime: '6小时前'
  },
  {
    id: 4,
    title: '后端开发语言之争',
    category: 'tech',
    optionA: 'Java',
    optionB: 'Go',
    votesA: 789,
    votesB: 654,
    author: {
      name: '赵后端',
      avatar: 'https://picsum.photos/32/32?random=4'
    },
    comments: 123,
    views: 4567,
    createTime: '8小时前'
  },
  {
    id: 5,
    title: '数据库选型：MySQL vs PostgreSQL',
    category: 'tech',
    optionA: 'MySQL',
    optionB: 'PostgreSQL',
    votesA: 678,
    votesB: 543,
    author: {
      name: '陈数据',
      avatar: 'https://picsum.photos/32/32?random=5'
    },
    comments: 78,
    views: 2890,
    createTime: '10小时前'
  },
  {
    id: 6,
    title: '前端构建工具之争',
    category: 'tools',
    optionA: 'Vite',
    optionB: 'Webpack',
    votesA: 890,
    votesB: 456,
    author: {
      name: '周工具',
      avatar: 'https://picsum.photos/32/32?random=6'
    },
    comments: 92,
    views: 3456,
    createTime: '12小时前'
  },
  {
    id: 7,
    title: '容器编排平台选择',
    category: 'tech',
    optionA: 'Kubernetes',
    optionB: 'Docker Swarm',
    votesA: 567,
    votesB: 234,
    author: {
      name: '李运维',
      avatar: 'https://picsum.photos/32/32?random=7'
    },
    comments: 56,
    views: 1789,
    createTime: '15小时前'
  },
  {
    id: 8,
    title: 'CSS 预处理器选择',
    category: 'tech',
    optionA: 'Sass',
    optionB: 'Less',
    votesA: 456,
    votesB: 345,
    author: {
      name: '张样式',
      avatar: 'https://picsum.photos/32/32?random=8'
    },
    comments: 67,
    views: 2345,
    createTime: '18小时前'
  },
  {
    id: 9,
    title: 'Node.js Web 框架之争',
    category: 'tech',
    optionA: 'Express',
    optionB: 'Nest.js',
    votesA: 789,
    votesB: 567,
    author: {
      name: '王后端',
      avatar: 'https://picsum.photos/32/32?random=9'
    },
    comments: 88,
    views: 3123,
    createTime: '1天前'
  },
  {
    id: 10,
    title: '前端测试框架选择',
    category: 'tech',
    optionA: 'Jest',
    optionB: 'Vitest',
    votesA: 345,
    votesB: 234,
    author: {
      name: '刘测试',
      avatar: 'https://picsum.photos/32/32?random=10'
    },
    comments: 45,
    views: 1567,
    createTime: '1天前'
  }
])

// 分类相关状态
const showCategoryMenu = ref(false)
const currentLevel = ref('main')
const currentMainCategory = ref('all')
const currentSubCategory = ref('')
const currentThirdCategory = ref('')

// 使用话题页面的配置
const categoryConfig = communityCategories.topics
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

// 筛选话题
const filteredTopics = computed(() => {
  let result = [...topics.value]
  
  // 应用分类筛选
  if (currentMainCategory.value !== 'all') {
    result = result.filter(topic => topic.category === currentMainCategory.value)
  }
  
  // 应用排序
  switch (currentSort.value) {
    case 'popular':
      result.sort((a, b) => b.views - a.views)
      break
    case 'newest':
      result.sort((a, b) => new Date(b.createTime) - new Date(a.createTime))
      break
    case 'votes':
      result.sort((a, b) => (b.votesA + b.votesB) - (a.votesA + a.votesB))
      break
    case 'comments':
      result.sort((a, b) => b.comments - a.comments)
      break
  }
  
  return result
})

// 分页后的话题列表
const paginatedTopics = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  const end = start + pageSize
  return filteredTopics.value.slice(start, end)
})

// 总页数
const totalPages = computed(() => {
  return Math.ceil(filteredTopics.value.length / pageSize)
})

// 热门话题
const hotTopics = computed(() => 
  [...topics.value]
    .sort((a, b) => (b.votesA + b.votesB) - (a.votesA + a.votesB))
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
</script> 