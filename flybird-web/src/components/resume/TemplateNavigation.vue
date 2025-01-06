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
          <button class="h-9 px-4 sm:px-5 bg-gradient-to-r from-rose-600 to-pink-600 text-white rounded-full hover:shadow-lg hover:shadow-rose-500/20 transition-all duration-300 text-sm font-medium flex items-center group">
            <PlusIcon class="w-4 h-4 mr-1.5 sm:mr-2 group-hover:scale-110 transition-transform" />
            <span>创建简历</span>
          </button>
        </div>
      </div>

      <!-- 分隔线 -->
      <div class="h-px bg-gray-200"></div>
      
      <!-- 二级分类标签和排序 -->
      <div class="flex items-center justify-between h-10">
        <!-- 左侧分类标签 -->
        <div class="flex items-center -mx-1 overflow-x-auto no-scrollbar flex-1">
          <button
            v-for="category in currentCategories"
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

        <!-- 右侧功能区 -->
        <div class="flex items-center gap-4 flex-shrink-0">       
          <!-- 会员模板开关 -->
          <div class="flex items-center gap-2 border-l border-gray-200 pl-4">
            <span class="text-sm text-gray-600">会员模板</span>
            <Switch
              v-model="showProTemplates"
              class="relative inline-flex h-6 w-11 items-center rounded-full bg-gray-200"
              :class="[showProTemplates ? 'bg-rose-600' : 'bg-gray-200']"
            >
              <span class="sr-only">显示会员模板</span>
              <span
                class="inline-block h-4 w-4 transform rounded-full bg-white transition"
                :class="[showProTemplates ? 'translate-x-6' : 'translate-x-1']"
              />
            </Switch>
          </div>
           <!-- 排序按钮 -->
           <div class="relative">
            <button 
              @click="isShowSort = !isShowSort"
              class="h-10 flex items-center px-4 bg-white border border-gray-200 rounded-lg text-sm font-medium hover:border-gray-300"
            >
              <ArrowsUpDownIcon class="w-4 h-4 mr-2 text-gray-500" />
              {{ currentSort.label }}
              <ChevronDownIcon class="w-4 h-4 ml-2 text-gray-500" />
            </button>
            
            <div v-if="isShowSort"
              class="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg border border-gray-100 py-1 z-20"
            >
              <button
                v-for="sort in sortOptions"
                :key="sort.value"
                @click="handleSort(sort)"
                class="w-full px-4 py-2 text-left text-sm hover:bg-gray-50 flex items-center"
                :class="{ 'text-gray-900 font-medium': currentSort.value === sort.value, 'text-gray-600': currentSort.value !== sort.value }"
              >
                {{ sort.label }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Switch } from '@headlessui/vue'
import { 
  PlusIcon, 
  ArrowsUpDownIcon, 
  ChevronDownIcon,
  FireIcon,
  ClockIcon,
  HandThumbUpIcon,
  ChatBubbleLeftIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const route = useRoute()

// 当前选中的分类
const currentCategory = ref('all')

// 判断是否在首页
const isHomePage = computed(() => {
  return route.path === '/templates'
})

// 主导航数据
const mainNavs = [
  { name: '全部模板', path: '/templates' },
  { name: '简历模板', path: '/templates/resume' },
  { name: '求职信', path: '/templates/cover-letter' },
  { name: '个人简介', path: '/templates/bio' }
]

// 根据当前路由显示不同的分类选项
const currentCategories = computed(() => {
  const path = route.path
  if (path.includes('resume')) {
    return resumeCategories
  } else if (path.includes('cover-letter')) {
    return coverLetterCategories
  } else if (path.includes('bio')) {
    return bioCategories
  }
  return allCategories
})

// 处理分类变更
const handleCategoryChange = (categoryId) => {
  currentCategory.value = categoryId
}

// 分类数据
const allCategories = [
  { id: 'all', name: '全部' },
  { id: 'popular', name: '最热门' },
  { id: 'newest', name: '最新' },
  { id: 'recommended', name: '推荐' }
]

const resumeCategories = [
  { id: 'all', name: '全部' },
  { id: 'fresh', name: '应届生' },
  { id: 'intern', name: '实习生' },
  { id: 'tech', name: '技术类' },
  { id: 'design', name: '设计类' },
  { id: 'product', name: '产品类' },
  { id: 'operation', name: '运营类' }
]

const coverLetterCategories = [
  { id: 'all', name: '全部' },
  { id: 'job', name: '求职信' },
  { id: 'intern', name: '实习信' },
  { id: 'recommend', name: '推荐信' },
  { id: 'thank', name: '感谢信' }
]

const bioCategories = [
  { id: 'all', name: '全部' },
  { id: 'personal', name: '个人简介' },
  { id: 'project', name: '项目简介' },
  { id: 'team', name: '团队简介' },
  { id: 'company', name: '公司简介' }
]


// 会员模板开关状态
const showProTemplates = ref(false)

// 排序相关状态
const isShowSort = ref(false)
const currentSort = ref({ label: '默认排序', value: 'default' })
const sortOptions = [
  { label: '默认排序', value: 'default' },
  { label: '最新发布', value: 'newest' },
  { label: '最多使用', value: 'most-used' },
  { label: '最多收藏', value: 'most-liked' }
]

// 处理排序选择
const handleSort = (sort) => {
  currentSort.value = sort
  isShowSort.value = false
}

// 获取横幅描述
const getBannerDescription = computed(() => {
  const descriptions = {
    '/templates': '精选优质简历模板，助你打造完美简历',
    '/templates/resume': '为在校生和应届生量身定制的简历模板',
    '/templates/cover-letter': '专业的求职信模板，助力职业发展',
    '/templates/bio': '专业的个人简介模板，展现个人魅力'
  }
  return descriptions[route.path] || ''
})

// 向父组件暴露数据
defineExpose({
  currentCategory,
  showProTemplates,
  currentSort
})
</script> 