<template>
  <div class="py-4 lg:py-6 mt-[72px] ">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 顶部横幅 -->
      <PageBanner theme="violet">
        <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">热门话题</h1>
        <p class="text-gray-600 text-lg max-w-2xl">参与技术讨论，表达你的观点</p>
      </PageBanner>

      <!-- 使用导航组件 -->
      <CommunityNavigation v-model:currentCategory="currentCategory" />



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
                class="group cursor-pointer bg-white rounded-lg lg:rounded-xl border border-gray-100 p-6"
              >
                <!-- 标题和作者信息 -->
                <div class="flex items-center justify-between mb-6">
                  <h3 class="text-lg font-bold text-gray-900">{{ topic.title }}</h3>
                  <div class="flex items-center gap-3">
                    <div class="text-right">
                      <div class="text-sm font-medium text-gray-900">{{ topic.author.name }}</div>
                      <div class="text-xs text-gray-500">{{ topic.createTime }}</div>
                    </div>
                    <img :src="topic.author.avatar" class="w-10 h-10 rounded-full ring-2 ring-gray-50">
                  </div>
                </div>

                <!-- VS选项对比区域 -->
                <div class="relative mb-6">
                  <!-- 进度条背景 -->
                  <div class="absolute inset-0 flex">
                    <!-- 左侧进度 -->
                    <div 
                      class="h-full bg-gradient-to-r from-blue-50 to-blue-100 rounded-l-lg"
                      :style="{ width: `${(topic.votesA / (topic.votesA + topic.votesB)) * 100}%` }"
                    ></div>
                    <!-- 右侧进度 -->
                    <div 
                      class="h-full bg-gradient-to-l from-purple-50 to-purple-100 rounded-r-lg"
                      :style="{ width: `${(topic.votesB / (topic.votesA + topic.votesB)) * 100}%` }"
                    ></div>
                  </div>

                  <!-- 选项内容 -->
                  <div class="relative flex items-center min-h-[80px]">
                    <!-- 选项A -->
                    <div class="flex-1 p-4">
                      <div class="text-center">
                        <!-- 百分比指示器 -->
                        <div class="absolute -top-3 left-[25%] -translate-x-1/2 px-3 py-1 bg-blue-600 rounded-full text-white text-xs font-medium">
                          {{ Math.round((topic.votesA / (topic.votesA + topic.votesB)) * 100) }}%
                        </div>
                        <div class="font-medium text-blue-600 mb-1">{{ topic.optionA }}</div>
                        <div class="text-sm text-gray-500 mb-4">{{ topic.votesA }} 票</div>
                        <!-- 投票按钮 -->
                        <button 
                          class="w-20 h-10 rounded-full border-2 border-blue-200 bg-white hover:bg-blue-50 transition-colors mx-auto flex items-center justify-center cursor-pointer"
                        >
                          <HandThumbUpIcon class="w-4 h-4 text-blue-600" />
                          <span class="ml-2 text-sm font-medium text-blue-600">投票</span>
                        </button>
                      </div>
                    </div>

                    <!-- VS标志 -->
                    <div class="w-12 h-12 rounded-full bg-white shadow-md border border-gray-100 flex items-center justify-center z-10">
                      <span class="text-sm font-bold bg-gradient-to-r from-blue-600 to-purple-600 text-transparent bg-clip-text">VS</span>
                    </div>

                    <!-- 选项B -->
                    <div class="flex-1 p-4">
                      <div class="text-center">
                        <!-- 百分比指示器 -->
                        <div class="absolute -top-3 right-[25%] translate-x-1/2 px-3 py-1 bg-purple-600 rounded-full text-white text-xs font-medium">
                          {{ Math.round((topic.votesB / (topic.votesA + topic.votesB)) * 100) }}%
                        </div>
                        <div class="font-medium text-purple-600 mb-1">{{ topic.optionB }}</div>
                        <div class="text-sm text-gray-500 mb-4">{{ topic.votesB }} 票</div>
                        <!-- 投票按钮 -->
                        <button 
                          class="cursor-pointer w-20 h-10 rounded-full border-2 border-purple-200 bg-white hover:bg-purple-50 transition-colors mx-auto flex items-center justify-center"
                        >
                          <HandThumbUpIcon class="w-4 h-4 text-purple-600" />
                          <span class="ml-2 text-sm font-medium text-purple-600">投票</span>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 底部信息 -->
                <div class="flex items-center justify-between pt-4 border-t border-gray-100">
                  <!-- 参与者头像组 -->
                  <div class="flex items-center">
                    <!-- 当没有人参与时 -->
                    <div v-if="topic.votesA + topic.votesB === 0" 
                      class="text-sm text-gray-400"
                    >
                      暂无人参与
                    </div>
                    <!-- 当只有1人参与时 -->
                    <div v-else-if="topic.votesA + topic.votesB === 1" 
                      class="flex items-center gap-2"
                    >
                      <img :src="`https://picsum.photos/32/32?random=${topic.id}`"
                        class="w-8 h-8 rounded-full border-2 border-white"
                      >
                      <span class="text-sm text-gray-500">第一个参与者</span>
                    </div>
                    <!-- 当有多人参与时 -->
                    <div v-else class="flex items-center gap-2">
                      <div class="flex -space-x-2">
                        <img v-for="i in Math.min(5, Math.floor((topic.votesA + topic.votesB) / 10))" :key="i"
                          :src="`https://picsum.photos/32/32?random=${topic.id * 10 + i}`"
                          class="w-8 h-8 rounded-full border-2 border-white hover:scale-110 transition-transform duration-300"
                        >
                        <div v-if="topic.votesA + topic.votesB > 50" 
                          class="w-8 h-8 rounded-full border-2 border-white bg-gray-50 flex items-center justify-center hover:bg-gray-100 transition-colors"
                        >
                          <span class="text-xs text-gray-500">+{{ topic.votesA + topic.votesB - 50 }}</span>
                        </div>
                      </div>
                      <span class="text-sm text-gray-500">{{ topic.votesA + topic.votesB }} 人参与</span>
                    </div>
                  </div>
                  <div class="flex items-center space-x-3 text-sm text-gray-500">
                    <span class="flex items-center">
                      <ChatBubbleLeftIcon class="w-4 h-4 mr-1" />{{ topic.comments }}
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
  ChevronRightIcon
} from '@heroicons/vue/24/outline'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import PageBanner from '@/components/common/PageBanner.vue'
import CommunityNavigation from '@/components/community/CommunityNavigation.vue'

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
    category: 'framework',
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
    category: 'framework',
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
    category: 'language',
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
    category: 'database',
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
    category: 'devops',
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
    category: 'frontend',
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
    category: 'backend',
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
    category: 'testing',
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

// 筛选话题
const filteredTopics = computed(() => {
  let result = [...topics.value]
  
  // 应用分类筛选
  if (currentCategory.value !== 'all') {
    result = result.filter(topic => topic.category === currentCategory.value)
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