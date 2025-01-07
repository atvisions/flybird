<template>
  <div class="py-4 lg:py-6 mt-[72px]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 顶部横幅 -->
      <PageBanner :theme="theme">
        <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">{{ title }}</h1>
        <p class="text-gray-600 text-lg max-w-2xl">{{ description }}</p>
      </PageBanner>



      <!-- PC端导航 -->
      <PortfolioNavigation 
        v-model:currentCategory="currentMainCategory"
        v-model:currentSort="currentSort"
        :type="type"
        :categories="currentTypeCategories"
        class="hidden md:block"
      />

      <!-- 作品列表 -->
      <div class="max-w-7xl mx-auto mt-6">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
          <div v-for="work in filteredWorks" :key="work.id"
            class="bg-white rounded-lg lg:rounded-xl border border-gray-100 overflow-hidden hover:shadow-lg transition-all duration-300"
          >
            <!-- 作品封面 -->
            <div class="aspect-w-16 aspect-h-9 sm:aspect-w-1 sm:aspect-h-1 bg-gray-100 relative group overflow-hidden">
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
                <span class="text-white font-medium mb-2">{{ getWorkTypeName(work.type) }}</span>
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
            <div class="p-4 lg:p-4">
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

    <!-- 分类切换菜单 -->
    <CategoryMenu v-if="showCategoryMenu" 
      v-model:show="showCategoryMenu"
      v-model:currentLevel="currentLevel"
      v-model:currentMainCategory="currentMainCategory"
      v-model:currentSubCategory="currentSubCategory"
      v-model:currentThirdCategory="currentThirdCategory"
      :type="type"
      :categories="currentTypeCategories"
      @category-change="handleCategoryChange"
    />

    <!-- 使用移动端底部导航栏 -->
    <MobileTabBar :menu-groups="menuGroups" />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import MobileTabBar from '@/components/MobileTabBar.vue'
import PageBanner from '@/components/common/PageBanner.vue'
import CategoryMenu from '@/components/portfolio/CategoryMenu.vue'
import PortfolioNavigation from '@/components/portfolio/PortfolioNavigation.vue'
import {
  ChevronRightIcon,
  PlayIcon,
  EyeIcon,
  HeartIcon
} from '@heroicons/vue/24/outline'
import { portfolioCategories } from '@/config/portfolioCategories'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  theme: {
    type: String,
    default: 'blue'
  },
  type: {
    type: String,
    required: true
  },
  menuGroups: {
    type: Array,
    required: true
  },
  works: {
    type: Array,
    required: true
  }
})

const route = useRoute()

// 分类相关状态
const currentMainCategory = ref('all')
const currentSubCategory = ref('')
const currentThirdCategory = ref('')
const currentLevel = ref('main')
const showCategoryMenu = ref(false)

// 排序相关状态
const showSortMenu = ref(false)
const currentSort = ref('popular')

// 获取当前类型的分类数据
const currentTypeCategories = computed(() => {
  const categoryConfig = portfolioCategories[props.type] || {}
  return categoryConfig.categories || []
})

// 计算当前显示的分类名称
const currentCategoryName = computed(() => {
  if (currentMainCategory.value === 'all') return '全部'
  const mainCategory = currentTypeCategories.value.find(c => c.id === currentMainCategory.value)
  if (!currentSubCategory.value) return mainCategory?.name
  const subCategory = mainCategory?.children?.find(c => c.id === currentSubCategory.value)
  return subCategory?.name
})

// 获取当前分类的子分类
const currentSubCategories = computed(() => {
  if (currentMainCategory.value === 'all') return []
  const mainCategory = currentTypeCategories.value.find(c => c.id === currentMainCategory.value)
  return mainCategory?.children || []
})

// 处理分类切换
const handleCategoryChange = (categoryId, level = 'main') => {
  if (level === 'main') {
    currentMainCategory.value = categoryId
    currentSubCategory.value = ''
    currentThirdCategory.value = ''
    if (categoryId !== 'all') {
      currentLevel.value = 'sub'
    } else {
      showCategoryMenu.value = false  // 选择"全部"时关闭菜单
    }
  } else if (level === 'sub') {
    currentSubCategory.value = categoryId
    currentThirdCategory.value = ''
    showCategoryMenu.value = false
  }
}

// 监听路由参数变化
watch(() => route.query.category, (newCategory) => {
  if (newCategory) {
    currentMainCategory.value = newCategory
  }
}, { immediate: true })

// 过滤作品列表
const filteredWorks = computed(() => {
  let result = [...props.works]
  
  // 应用分类过滤
  if (currentMainCategory.value !== 'all') {
    if (currentSubCategory.value) {
      result = result.filter(work => work.subCategory === currentSubCategory.value)
    } else {
      result = result.filter(work => work.type === currentMainCategory.value)
    }
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

// 判断是否在首页
const isHomePage = computed(() => {
  return route.path === '/portfolio'
})

// 获取作品类型名称
const getWorkTypeName = (type) => {
  const category = currentTypeCategories.value.find(c => c.id === type)
  return category?.name || type
}
</script>

<style scoped>
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
</style> 