<template>
  <div class="min-h-screen py-4 pb-24 lg:py-6 mt-[72px]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 顶部横幅 -->
      <PageBanner theme="blue">
        <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">{{ categoryConfig.title }}</h1>
        <p class="text-gray-600 text-lg max-w-2xl">{{ categoryConfig.description }}</p>
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
          <div v-for="work in works" :key="work.id"
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
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import MobileTabBar from '@/components/MobileTabBar.vue'
import PageBanner from '@/components/common/PageBanner.vue'
import CategoryMenu from '@/components/portfolio/CategoryMenu.vue'
import PortfolioNavigation from '@/components/portfolio/PortfolioNavigation.vue'
import { portfolioCategories, generateMenuGroups } from '@/config/portfolioCategories'
import { usePortfolioData } from '@/composables/usePortfolioData'
import {
  PlayIcon,
  EyeIcon,
  HeartIcon,
  ChevronRightIcon
} from '@heroicons/vue/24/outline'

const route = useRoute()
const type = 'discover'

// 使用统一的分类配置
const categoryConfig = portfolioCategories[type]
const menuGroups = generateMenuGroups(type)
const { works } = usePortfolioData(type)

// 分类相关状态
const currentMainCategory = ref('all')
const currentSubCategory = ref('')
const currentThirdCategory = ref('')
const currentLevel = ref('main')
const showCategoryMenu = ref(false)

// 排序相关状态
const currentSort = ref('popular')

// 获取当前类型的分类数据
const currentTypeCategories = computed(() => {
  return categoryConfig.categories || []
})

// 获取作品类型名称
const getWorkTypeName = (type) => {
  const category = currentTypeCategories.value.find(c => c.id === type)
  return category?.name || type
}

// 处理分类切换
const handleCategoryChange = (categoryId, level = 'main') => {
  if (level === 'main') {
    currentMainCategory.value = categoryId
    currentSubCategory.value = ''
    currentThirdCategory.value = ''
    if (categoryId !== 'all') {
      currentLevel.value = 'sub'
    } else {
      showCategoryMenu.value = false
    }
  } else if (level === 'sub') {
    currentSubCategory.value = categoryId
    currentThirdCategory.value = ''
    showCategoryMenu.value = false
  }
}
</script> 