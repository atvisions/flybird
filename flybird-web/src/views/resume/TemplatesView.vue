<template>
  <div class="py-4 pb-24 lg:py-6 mt-[72px]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 顶部横幅 -->
      <PageBanner theme="rose">
        <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">精选简历模板</h1>
        <p class="text-gray-600 text-lg max-w-2xl">精选优质简历模板，助你打造完美简历</p>
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
              isPro: template.isPro || false
            }"
            @like="handleLike(template)"
            @use="handleUseTemplate"
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import PageBanner from '@/components/common/PageBanner.vue'
import CategoryMenu from '@/components/CategoryMenu.vue'
import ResumeNavigation from '@/components/resume/ResumeNavigation.vue'
import ResumeCard from '@/components/resume/ResumeCard.vue'
import { categoryApi } from '@/api/category'
import { templateApi } from '@/api/template'
import account from '@/api/account'
import config from '@/config'
import {
  ChevronRightIcon,
  EyeIcon,
  HeartIcon,
  HomeIcon,
  AcademicCapIcon,
  BriefcaseIcon,
  UserGroupIcon,
  SparklesIcon,
  LanguageIcon
} from '@heroicons/vue/24/outline'

const route = useRoute()
const router = useRouter()

// 分类相关状态
const currentMainCategory = ref('all')
const currentSubCategory = ref('')
const currentThirdCategory = ref('')
const currentLevel = ref('main')
const showCategoryMenu = ref(false)

// 排序相关状态
const currentSort = ref('newest')

// 分类数据
const categoryList = ref([])

// 加载分类数据
const loadCategories = async () => {
  try {
    const res = await categoryApi.getList()
    categoryList.value = Array.isArray(res) ? res : []
  } catch (error) {
    console.error('获取分类列表失败:', error)
    categoryList.value = []
  }
}

const categories = computed(() => {
  const allOption = { id: 'all', name: '全部', icon: HomeIcon }
  const formattedCategories = categoryList.value.map(category => ({
    id: category.id,
    name: category.name,
    icon: getIconForCategory(category.id)
  }))
  return [allOption, ...formattedCategories]
})

// 获取分类对应的图标
const getIconForCategory = (categoryId) => {
  const iconMap = {
    'fresh': AcademicCapIcon,
    'experienced': BriefcaseIcon,
    'manager': UserGroupIcon,
    'creative': SparklesIcon,
    'international': LanguageIcon
  }
  return iconMap[categoryId] || HomeIcon
}

// 模板数据
const templates = ref([])
const loading = ref(false)

// 加载模板数据
const loadTemplates = async () => {
  loading.value = true
  try {
    const params = {
      status: 1, // 1: 已发布
      is_public: true // 只显示公开的模板
    }
    
    if (currentMainCategory.value !== 'all') {
      params.category = currentMainCategory.value
    }
    
    const res = await templateApi.getTemplates(params)
    console.log('获取到的原始模板列表:', res)
    
    let templateList = []
    if (res.data?.results) {
      templateList = res.data.results
    } else if (Array.isArray(res.data)) {
      templateList = res.data
    } else if (Array.isArray(res)) {
      templateList = res
    }

    // 获取所有模板创建者的用户信息
    const creatorIds = [...new Set(templateList.map(t => t.creator))].filter(Boolean)
    const creatorInfoMap = new Map()
    
    for (const creatorId of creatorIds) {
      try {
        const userRes = await account.getUserPublicInfo(creatorId)
        console.log('获取到的用户信息:', userRes)
        if (userRes?.data?.data) {
          creatorInfoMap.set(creatorId, {
            name: userRes.data.data.username,
            avatar: userRes.data.data.avatar,
            is_vip: userRes.data.data.is_vip,
            position: userRes.data.data.position
          })
        }
      } catch (error) {
        console.error(`获取用户 ${creatorId} 信息失败:`, error)
      }
    }

    // 处理模板数据，确保所有必要的字段都存在
    templates.value = templateList.map(template => {
      const creatorInfo = creatorInfoMap.get(template.creator)
      console.log('模板创建者信息:', creatorInfo)
      
      // 如果有缩略图，确保使用完整的URL
      const thumbnail = template.thumbnail || template.cover
      const thumbnailUrl = thumbnail ? (
        thumbnail.startsWith('http') ? thumbnail : `${config.mediaURL}/${thumbnail.replace(/^\/?(media\/)?/, '')}`
      ) : null

      return {
        ...template,
        creator_name: creatorInfo?.name || template.creator_name || '匿名用户',
        creator_avatar: creatorInfo?.avatar ? `${config.mediaURL}/${creatorInfo.avatar.replace(/^\/?(media\/)?/, '')}` : null,
        creator_is_vip: creatorInfo?.is_vip || false,
        creator_position: creatorInfo?.position || '',
        thumbnail: thumbnailUrl,
        description: template.description || '',
        category: template.category || 'other',
        viewCount: template.views || 0,
        likes: template.likes || 0,
        downloads: template.downloads || 0,
        isPro: template.is_pro || false,
        isLiked: template.is_liked || false
      }
    })
  } catch (error) {
    console.error('获取模板列表失败:', error)
    templates.value = []
  } finally {
    loading.value = false
  }
}

// 过滤模板列表
const filteredTemplates = computed(() => {
  // 首先过滤出已发布且公开的模板
  let result = templates.value.filter(template => 
    template.status === 1 && template.is_public === true
  )
  
  // 应用分类过滤
  if (currentMainCategory.value !== 'all') {
    result = result.filter(template => template.category === currentMainCategory.value)
  }
  
  // 应用排序
  switch (currentSort.value) {
    case 'newest':
      result.sort((a, b) => new Date(b.created_at || b.date) - new Date(a.created_at || a.date))  // 按创建时间排序
      break
    case 'recommended':
      result = result.filter(template => template.is_recommended === true)  // 只显示推荐的模板
      result.sort((a, b) => new Date(b.created_at || b.date) - new Date(a.created_at || a.date))  // 推荐的模板按创建时间排序
      break
    case 'likes':
      result.sort((a, b) => b.likes - a.likes)  // 按点赞数排序
      break
    case 'views':
      result.sort((a, b) => b.views - a.views)  // 按浏览量排序
      break
  }
  
  return result
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
const handleLike = async (template) => {
  try {
    const res = await templateApi.like(template.id)
    if (res.data) {
      // 更新模板的点赞状态和数量
      template.isLiked = !template.isLiked
      template.likes = template.likes + (template.isLiked ? 1 : -1)
    }
  } catch (error) {
    console.error('点赞失败:', error)
  }
}

// 处理使用模板
const handleUseTemplate = async (template) => {
  try {
    // 先获取模板详情
    const res = await templateApi.getDetail(template.id)
    if (res?.data) {
      // 确保有模板数据后再跳转
      router.push(`/editor/resume/new/${template.id}`)
    } else {
      showToast('获取模板详情失败', 'error')
    }
  } catch (error) {
    console.error('获取模板详情失败:', error)
    showToast('获取模板详情失败', 'error')
  }
}

// 定义菜单组
const menuGroups = ref([
  {
    title: '简历模板',
    items: [
      {
        name: '全部模板',
        path: '/resume/templates/all'
      },
      {
        name: '推荐模板',
        path: '/resume/templates/recommended'
      },
      {
        name: '最新模板',
        path: '/resume/templates/latest'
      }
    ]
  }
])

// 监听分类变化重新加载模板
watch([currentMainCategory], () => {
  loadTemplates()
})

// 组件挂载时加载数据
onMounted(() => {
  loadCategories()
  loadTemplates()
})
</script> 