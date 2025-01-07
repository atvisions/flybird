<template>
  <div class="py-4 pb-24 lg:py-6 mt-[72px]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 顶部横幅 -->
      <PageBanner theme="rose">
        <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">求职信模板</h1>
        <p class="text-gray-600 text-lg max-w-2xl">专业的求职信模板，助力职业发展</p>
      </PageBanner>

      <!-- PC端导航 -->
      <ResumeNavigation 
        v-model:currentCategory="currentMainCategory"
        v-model:currentSort="currentSort"
        class="hidden md:block"
      />

      <!-- 模板列表 -->
      <div class="max-w-7xl mx-auto mt-6">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
          <ResumeCard
            v-for="template in filteredTemplates"
            :key="template.id"
            :template="{
              ...template,
              category: getTemplateCategoryName(template.category),
              useCount: template.downloads || 0,
              viewCount: template.views || 0,
              isLiked: false,
              isPro: template.isPro || false
            }"
            @like="handleLike(template)"
          />
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
import { useRoute } from 'vue-router'
import MobileTabBar from '@/components/MobileTabBar.vue'
import PageBanner from '@/components/common/PageBanner.vue'
import CategoryMenu from '@/components/CategoryMenu.vue'
import ResumeNavigation from '@/components/resume/ResumeNavigation.vue'
import ResumeCard from '@/components/resume/ResumeCard.vue'
import { useCoverLetterData } from '@/composables/useCoverLetterData'
import {
  ChevronRightIcon,
  EyeIcon,
  HeartIcon,
  HomeIcon,
  DocumentTextIcon,
  BriefcaseIcon,
  AcademicCapIcon,
  SparklesIcon
} from '@heroicons/vue/24/outline'

const route = useRoute()

// 分类相关状态
const currentMainCategory = ref('all')
const currentSubCategory = ref('')
const currentThirdCategory = ref('')
const currentLevel = ref('main')
const showCategoryMenu = ref(false)

// 排序相关状态
const currentSort = ref('popular')

// 分类数据
const categories = computed(() => [
  { id: 'all', name: '全部', icon: HomeIcon },
  { id: 'general', name: '通用型', icon: DocumentTextIcon },
  { id: 'career', name: '职业型', icon: BriefcaseIcon },
  { id: 'academic', name: '学术型', icon: AcademicCapIcon },
  { id: 'creative', name: '创意型', icon: SparklesIcon }
])

// 获取模板数据
const { templates } = useCoverLetterData()

// 过滤模板列表
const filteredTemplates = computed(() => {
  let result = [...templates.value]
  
  // 应用分类过滤
  if (currentMainCategory.value !== 'all') {
    result = result.filter(template => template.category === currentMainCategory.value)
  }
  
  // 应用排序
  switch (currentSort.value) {
    case 'popular':
      result.sort((a, b) => (b.views + b.likes) - (a.views + a.likes))
      break
    case 'newest':
      result.sort((a, b) => new Date(b.date) - new Date(a.date))
      break
    case 'downloads':
      result.sort((a, b) => b.downloads - a.downloads)
      break
    case 'likes':
      result.sort((a, b) => b.likes - a.likes)
      break
  }
  
  return result
})

// 获取当前分类名称
const currentCategoryName = computed(() => {
  if (currentMainCategory.value === 'all') return '全部'
  const category = categories.value.find(c => c.id === currentMainCategory.value)
  return category?.name || ''
})

// 获取模板分类名称
const getTemplateCategoryName = (categoryId) => {
  const category = categories.value.find(c => c.id === categoryId)
  return category?.name || categoryId
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

// 处理模板点赞
const handleLike = (template) => {
  // TODO: 实现点赞逻辑
  console.log('Like template:', template.id)
}
</script> 