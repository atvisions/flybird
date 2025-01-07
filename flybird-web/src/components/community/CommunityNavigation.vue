<template>
  <div class="mt-6 bg-white rounded-xl border border-gray-100 p-4 hidden md:block mb-6">
    <div class="flex flex-col gap-4">
      <!-- 左侧主导航和右侧按钮 -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <!-- 左侧主导航 -->
        <div class="flex items-center -mx-1">
          <router-link
            v-for="nav in mainNavs"
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
            <button class="h-9 px-4 sm:px-5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-full hover:shadow-lg hover:shadow-blue-500/20 transition-all duration-300 text-sm font-medium flex items-center group">
              <PlusIcon class="w-4 h-4 mr-1.5 sm:mr-2 group-hover:scale-110 transition-transform" />
              <span class="hidden sm:inline">发布内容</span>
              <span class="sm:hidden">发布</span>
            </button>
          </template>
          <template v-else>
            <!-- 登录按钮 -->
            <router-link 
              :to="`/login?redirect=${encodeURIComponent($route.fullPath)}`"
              class="h-9 px-4 sm:px-5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-full hover:shadow-lg hover:shadow-blue-500/20 transition-all duration-300 text-sm font-medium flex items-center group"
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
              currentCategory === category.id
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
    <!-- 添加一个遮罩层来处理排序菜单的点击外部关闭 -->
    <div v-if="showSortMenu" 
      class="fixed inset-0 z-10" 
      @click="showSortMenu = false"
    ></div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useStore } from 'vuex'
import { 
  PlusIcon, 
  UserIcon, 
  ArrowsUpDownIcon, 
  ChevronDownIcon, 
  FireIcon, 
  ClockIcon, 
  HandThumbUpIcon, 
  EyeIcon,
  HomeIcon,
  NewspaperIcon,
  QuestionMarkCircleIcon,
  HashtagIcon,
  DeviceMobileIcon,
  SparklesIcon,
  CogIcon,
  ServerIcon,
  CubeTransparentIcon,
  CheckCircleIcon,
  StarIcon,
  GiftIcon,
  BoltIcon,
  BriefcaseIcon,
  WrenchIcon,
  UserGroupIcon,
  CodeBracketIcon,
  DevicePhoneMobileIcon,
  WrenchScrewdriverIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  currentCategory: {
    type: String,
    required: true
  },
  currentSort: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update:currentCategory', 'update:currentSort'])

const router = useRouter()
const route = useRoute()
const store = useStore()

// 使用 Vuex store 的 isAuthenticated 状态
const isAuthenticated = computed(() => store.state.isAuthenticated)

// 主导航数据
const mainNavs = [
  { name: '首页', path: '/community', icon: HomeIcon },
  { name: '文章', path: '/community/articles', icon: NewspaperIcon },
  { name: '问答', path: '/community/questions', icon: QuestionMarkCircleIcon },
  { name: '话题', path: '/community/topics', icon: HashtagIcon }
]

// 根据当前路由显示不同的分类选项
const categories = computed(() => {
  const path = route.path
  if (path.includes('articles')) {
    return [
      { id: 'all', name: '全部', icon: HomeIcon },
      { id: 'frontend', name: '前端开发', icon: CodeBracketIcon },
      { id: 'backend', name: '后端开发', icon: ServerIcon },
      { id: 'mobile', name: '移动开发', icon: DevicePhoneMobileIcon },
      { id: 'ai', name: '人工智能', icon: SparklesIcon },
      { id: 'devops', name: 'DevOps', icon: CogIcon }
    ]
  } else if (path.includes('questions')) {
    return [
      { id: 'all', name: '全部', icon: HomeIcon },
      { id: 'unsolved', name: '待解决', icon: QuestionMarkCircleIcon },
      { id: 'solved', name: '已解决', icon: CheckCircleIcon },
      { id: 'featured', name: '精选问答', icon: StarIcon },
      { id: 'reward', name: '悬赏问答', icon: GiftIcon }
    ]
  } else if (path.includes('topics')) {
    return [
      { id: 'all', name: '全部', icon: HomeIcon },
      { id: 'hot', name: '热门话题', icon: FireIcon },
      { id: 'tech', name: '技术之争', icon: BoltIcon },
      { id: 'career', name: '职业发展', icon: BriefcaseIcon },
      { id: 'tools', name: '工具推荐', icon: WrenchScrewdriverIcon }
    ]
  }
  // 首页分类
  return [
    { id: 'all', name: '全部', icon: HomeIcon },
    { id: 'recommend', name: '推荐', icon: SparklesIcon },
    { id: 'following', name: '关注', icon: UserGroupIcon },
    { id: 'latest', name: '最新', icon: ClockIcon }
  ]
})

// 排序菜单状态
const showSortMenu = ref(false)

// 排序选项
const sortOptions = {
  popular: { label: '最受欢迎', icon: FireIcon },
  newest: { label: '最新发布', icon: ClockIcon },
  views: { label: '最多浏览', icon: EyeIcon },
  likes: { label: '最多点赞', icon: HandThumbUpIcon }
}

// 处理排序
const handleSort = (value) => {
  emit('update:currentSort', value)
  showSortMenu.value = false
}

// 处理分类变更
const handleCategoryChange = (categoryId) => {
  emit('update:currentCategory', categoryId)
}
</script> 