<template>
  <!-- 主导航区域 -->
  <div class="mt-6 bg-white rounded-xl border border-gray-100 p-4 hidden md:block mb-6">
    <div class="flex flex-col gap-4">
      <!-- 左侧主导航和右侧按钮 -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <!-- 左侧主导航 -->
        <div class="flex items-center -mx-1 overflow-x-auto no-scrollbar">
          <router-link
            v-for="nav in mainNavs"
            :key="nav.path"
            :to="nav.path"
            class="px-4 sm:px-8 py-3 mx-1 text-sm font-medium transition-colors relative group whitespace-nowrap"
            :class="[
              $route.path === nav.path
                ? 'text-gray-900'
                : 'text-gray-500 hover:text-gray-700'
            ]"
          >
            {{ nav.name }}
            <!-- 活跃状态指示器 -->
            <div 
              class="absolute left-1/2 -translate-x-1/2 bottom-4.5 w-1.5 h-1.5 rounded-full transition-colors"
              :class="$route.path === nav.path ? 'bg-gray-900' : 'bg-transparent group-hover:bg-gray-200'"
            ></div>
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
      
      <!-- 作品分类标签 -->
      <div class="flex items-center h-10" :class="{ 'justify-between': !isHomePage }">
        <!-- 左侧分类标签 -->
        <div class="flex items-center -mx-1 overflow-x-auto no-scrollbar" :class="{ 'flex-1': isHomePage }">
          <button
            v-for="category in portfolioCategories"
            :key="category.id"
            @click="handleCategoryChange(category.id)"
            class="h-10 px-4 mx-1 rounded-full text-sm font-medium transition-colors whitespace-nowrap flex items-center"
            :class="[
              currentCategory === category.id
                ? 'bg-gray-900 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            ]"
          >
            {{ category.name }}
          </button>
        </div>

        <!-- 右侧排序按钮 - 不在首页显示 -->
        <div v-if="!isHomePage" class="relative flex-shrink-0 ml-4">
          <button 
            @click="showSortMenu = !showSortMenu"
            class="h-10 flex items-center px-4 bg-white border border-gray-200 rounded-lg text-sm font-medium hover:border-gray-300"
          >
            <ArrowsUpDownIcon class="w-4 h-4 mr-2 text-gray-500" />
            {{ sortOptions[props.currentSort]?.label || '排序' }}
            <ChevronDownIcon class="w-4 h-4 ml-2 text-gray-500" />
          </button>
          
          <div v-if="showSortMenu"
            class="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg border border-gray-100 py-1 z-20"
          >
            <button
              v-for="(option, key) in sortOptions"
              :key="key"
              @click="handleSort(key)"
              class="w-full px-4 py-2 text-left text-sm hover:bg-gray-50 flex items-center"
              :class="{ 'text-gray-900 font-medium': props.currentSort === key, 'text-gray-600': props.currentSort !== key }"
            >
              <component 
                :is="option.icon" 
                class="w-4 h-4 mr-2"
                :class="props.currentSort === key ? 'text-gray-900' : 'text-gray-400'"
              />
              {{ option.label }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useStore } from 'vuex'
import { PlusIcon, UserIcon, ArrowsUpDownIcon, ChevronDownIcon, FireIcon, ClockIcon, HandThumbUpIcon, EyeIcon } from '@heroicons/vue/24/outline'

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

// 判断是否在首页
const isHomePage = computed(() => {
  return route.path === '/portfolio'
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

// 主导航数据
const mainNavs = [
  { name: '发现', path: '/portfolio' },
  { name: '设计', path: '/portfolio/design' },
  { name: '视频', path: '/portfolio/video' },
  { name: '动画', path: '/portfolio/animation' },
  { name: '摄影', path: '/portfolio/photo' }
]

// 作品分类
const portfolioCategories = [
  { id: 'all', name: '全部' },
  { id: 'ui', name: 'UI设计' },
  { id: 'graphic', name: '平面设计' },
  { id: 'web', name: 'Web开发' },
  { id: 'mobile', name: '移动开发' },
  { id: 'video', name: '视频制作' },
  { id: 'photo', name: '摄影作品' },
  { id: 'animation', name: '动画' },
  { id: 'illustration', name: '插画' },
  { id: 'game', name: '游戏设计' },
  { id: 'other', name: '其他' }
]

// 处理分类变更
const handleCategoryChange = (categoryId) => {
  emit('update:currentCategory', categoryId)
}
</script> 