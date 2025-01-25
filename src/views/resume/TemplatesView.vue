<!-- 模板列表 -->
<template v-else>
  <div class="grid grid-cols-5 gap-4">
    <ResumeCard
      v-for="template in filteredTemplates"
      :key="template.id"
      :template="{
        ...template,
        id: template.id || '',
        name: template.name || '',
        description: template.description || '',
        thumbnail: template.thumbnail || '',
        category: getTemplateCategoryName(template.category) || '其他',
        creator: template.creator || '',
        creator_name: template.creator_name || '匿名用户',
        creator_avatar: template.creator_avatar || '',
        creator_is_vip: template.creator_is_vip || false,
        useCount: template.downloads || 0,
        viewCount: template.views || 0,
        likes: template.likes || 0,
        isPro: template.isPro || false,
        is_recommended: template.is_recommended || false,
        isLiked: template.isLiked || false,
        is_owner: template.is_owner || false
      }"
      :like-loading="likeLoading.has(template.id)"
      :only-mine="onlyMine"
      @like="handleLike(template)"
      @use="handleUseTemplate"
      @edit="handleEditTemplate"
      @delete="handleDeleteTemplate"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { categoryApi } from '@/api/category'
import { templateApi } from '@/api/template'
import config from '@/config'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// 分类相关状态
const categoryList = ref([])
const currentMainCategory = ref('all')
const currentSubCategory = ref('')
const currentThirdCategory = ref('')
const currentLevel = ref('main')
const showCategoryMenu = ref(false)

// 排序相关状态
const currentSort = ref('newest')

// 添加只看我的状态
const onlyMine = ref(false)

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

// 获取模板分类名称
const getTemplateCategoryName = (categoryId) => {
  if (!categoryId) return '其他'
  if (categoryId === 'all') return '全部'
  if (categoryId === 'recommended') return '推荐'
  
  // 如果分类列表还没有加载完成，返回原始分类ID
  if (!categoryList.value || categoryList.value.length === 0) {
    return categoryId
  }
  
  const category = categoryList.value.find(c => c.id === categoryId)
  return category?.name || '其他'
}

// 在组件挂载时加载分类数据
onMounted(() => {
  loadCategories()
})
</script> 