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
        v-model:onlyMine="onlyMine"
        class="hidden md:block"
      />

      <!-- 模板列表 -->
      <div class="max-w-7xl mx-auto mt-6">
        <!-- 加载状态 -->
        <div v-if="loading" class="grid grid-cols-5 gap-4">
          <div v-for="i in 15" :key="i" class="animate-pulse">
            <div class="aspect-[3/4] bg-gray-100 rounded-lg mb-3"></div>
            <div class="h-4 bg-gray-100 rounded w-3/4 mb-2"></div>
            <div class="h-3 bg-gray-100 rounded w-1/2"></div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-else-if="!filteredTemplates.length" class="text-center py-12">
          <DocumentIcon class="w-12 h-12 text-gray-300 mx-auto mb-4" />
          <p class="text-gray-500">暂无相关模版</p>
        </div>

        <!-- 模板列表 -->
        <template v-else>
          <div class="grid grid-cols-5 gap-4">
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
              :like-loading="likeLoading.has(template.id)"
              :only-mine="onlyMine"
              @like="handleLike(template)"
              @use="handleUseTemplate"
              @edit="handleEditTemplate"
              @delete="handleDeleteTemplate"
            />
          </div>

          <!-- 加载更多 -->
          <div v-if="hasMore" class="flex justify-center mt-8">
            <button
              @click="loadMore"
              :disabled="loadingMore"
              class="px-6 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:border-gray-400 transition-colors"
            >
              {{ loadingMore ? '加载中...' : '加载更多' }}
            </button>
          </div>
        </template>
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
  LanguageIcon,
  DocumentIcon
} from '@heroicons/vue/24/outline'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAccountStore } from '@/stores/account'

const route = useRoute()
const router = useRouter()
const accountStore = useAccountStore()

// 分类相关状态
const currentMainCategory = ref('all')
const currentSubCategory = ref('')
const currentThirdCategory = ref('')
const currentLevel = ref('main')
const showCategoryMenu = ref(false)

// 排序相关状态
const currentSort = ref('newest')

// 添加只看我的状态
const onlyMine = ref(false)

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

// 添加点赞锁定状态
const likeLoading = ref(new Set())

// 添加分页相关状态
const pageSize = 15
const currentPage = ref(1)
const hasMore = ref(true)
const loadingMore = ref(false)

// 修改加载模板数据的函数
const loadTemplates = async (isLoadMore = false) => {
  if (!isLoadMore) {
    loading.value = true
    currentPage.value = 1
  } else {
    loadingMore.value = true
  }

  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize
    }
    
    // 只看我的模式
    if (onlyMine.value) {
      if (!accountStore.userInfo?.id) {
        ElMessage.warning('请先登录')
        router.push(`/login?redirect=${encodeURIComponent(window.location.pathname)}`)
        return
      }
      params.creator = accountStore.userInfo.id
    } else {
      // 非只看我的模式，只显示已发布的公开模板
      params.status = 1
      params.is_public = true
    }
    
    // 根据分类和排序设置参数
    if (currentMainCategory.value === 'recommended') {
      params.is_recommended = true
    } else if (currentMainCategory.value !== 'all') {
      params.category = currentMainCategory.value
    }

    // 设置排序参数
    if (currentSort.value) {
      params.sort = currentSort.value
    }
    
    console.log('请求参数:', params)
    const res = await templateApi.getTemplates(params)
    console.log('API返回的原始数据:', res)
    
    let templateList = []
    if (res.data?.results) {
      templateList = res.data.results
      // 更新是否有更多数据的状态
      hasMore.value = res.data.next !== null
    } else if (Array.isArray(res.data)) {
      templateList = res.data
      hasMore.value = templateList.length === pageSize
    } else if (Array.isArray(res)) {
      templateList = res
      hasMore.value = templateList.length === pageSize
    }
    
    // 在"只看我的"模式下，确保只显示当前用户的模板
    if (onlyMine.value && accountStore.userInfo?.id) {
      templateList = templateList.filter(template => template.creator === accountStore.userInfo.id)
    }

    // 获取所有模板创建者的用户信息
    const creatorIds = [...new Set(templateList.map(t => t.creator))].filter(Boolean)
    const creatorInfoMap = new Map()
    
    for (const creatorId of creatorIds) {
      try {
        const userRes = await account.getUserPublicInfo(creatorId)
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

    // 处理模板数据
    const processedTemplates = templateList.map(template => {
      const creatorInfo = creatorInfoMap.get(template.creator)
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

    // 更新模板列表
    if (isLoadMore) {
      templates.value = [...templates.value, ...processedTemplates]
    } else {
      templates.value = processedTemplates
    }

  } catch (error) {
    console.error('获取模板列表失败:', error)
    if (!isLoadMore) {
      templates.value = []
    }
  } finally {
    if (isLoadMore) {
      loadingMore.value = false
    } else {
      loading.value = false
    }
  }
}

// 添加加载更多方法
const loadMore = async () => {
  if (loadingMore.value || !hasMore.value) return
  currentPage.value++
  await loadTemplates(true)
}

// 过滤模板列表
const filteredTemplates = computed(() => {
  console.log('开始过滤模板，当前模板数量:', templates.value.length)
  console.log('当前分类:', currentMainCategory.value)
  console.log('只看我的状态:', onlyMine.value)
  
  let result = templates.value

  // 应用分类过滤
  if (currentMainCategory.value === 'recommended') {
    result = result.filter(template => template.is_recommended === true)
    console.log('推荐模板数量:', result.length)
  } else if (currentMainCategory.value !== 'all') {
    result = result.filter(template => template.category === currentMainCategory.value)
    console.log('分类过滤后的模板数量:', result.length)
  }
  
  // 应用排序
  switch (currentSort.value) {
    case 'newest':
      result.sort((a, b) => new Date(b.created_at || b.date) - new Date(a.created_at || a.date))
      break
    case 'likes':
      result.sort((a, b) => b.likes - a.likes)
      break
    case 'views':
      result.sort((a, b) => b.views - a.views)
      break
  }
  
  console.log('最终返回的模板数量:', result.length)
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
    // 检查登录状态
    if (!accountStore.userInfo) {
      ElMessage.warning('请先登录后再点赞')
      router.push(`/login?redirect=${encodeURIComponent(window.location.pathname)}`)
      return
    }

    // 检查是否正在处理点赞
    if (likeLoading.value.has(template.id)) {
      return
    }

    // 添加锁定状态
    likeLoading.value.add(template.id)

    const res = await templateApi.like(template.id)
    console.log('点赞响应:', res)

    if (res?.data) {
      // 更新模板的点赞状态和数量
      const newLikeStatus = res.data.is_liked !== undefined ? res.data.is_liked : !template.isLiked
      template.isLiked = newLikeStatus
      template.likes = res.data.likes || (template.likes + (newLikeStatus ? 1 : -1))
      ElMessage.success(newLikeStatus ? '点赞成功' : '取消点赞成功')
    }
  } catch (error) {
    console.error('点赞失败:', error)
    if (error.response?.status === 403) {
      ElMessage.warning('登录已过期，请重新登录')
      router.push(`/login?redirect=${encodeURIComponent(window.location.pathname)}`)
    } else {
      ElMessage.error('点赞失败，请稍后重试')
    }
  } finally {
    // 移除锁定状态
    setTimeout(() => {
      likeLoading.value.delete(template.id)
    }, 5000) // 增加到5秒的冷却时间
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

// 处理编辑模板
const handleEditTemplate = async (template) => {
  try {
    // 获取模板详情
    const res = await templateApi.getDetail(template.id)
    if (res?.data) {
      // 跳转到编辑页面
      router.push(`/editor/template/${template.id}`)
    }
  } catch (error) {
    console.error('获取模板详情失败:', error)
    ElMessage.error('获取模板详情失败')
  }
}

// 处理删除模板
const handleDeleteTemplate = async (template) => {
  try {
    // 调用删除 API
    await templateApi.delete(template.id)
    
    // 从列表中移除该模板
    templates.value = templates.value.filter(t => t.id !== template.id)
    
    // 显示成功提示
    ElMessage.success('删除成功')
  } catch (error) {
    console.error('删除模板失败:', error)
    ElMessage.error('删除失败')
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

// 监听分类和只看我的变化重新加载模板
watch([currentMainCategory, onlyMine], () => {
  loadTemplates()
})

// 组件挂载时加载数据
onMounted(() => {
  loadCategories()
  loadTemplates()
})
</script> 