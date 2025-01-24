<template>
  <div class="editor-sidebar">
    <div class="sidebar-header">
      <div class="tab-container">
        <div 
          v-for="tab in tabs" 
          :key="tab.key"
          class="tab-item"
          :class="{ active: activeTab === tab.key }"
          @click="switchTab(tab.key)"
        >
          <span class="tab-text">{{ tab.label }}</span>
          <div class="tab-background" v-if="activeTab === tab.key"></div>
        </div>
      </div>
    </div>

    <div class="sidebar-content">
      <template v-if="activeTab === 'components'">
        <div 
          v-for="group in components" 
          :key="group.type"
          class="component-group"
        >
          <div class="group-title">{{ group.title }}</div>
          <div class="group-content">
            <div 
              v-for="item in group.items" 
              :key="item.type"
              class="component-item"
              draggable="true"
              @dragstart="handleDragStart($event, item)"
            >
              <div class="item-icon">
                <component :is="getIconComponent(item.icon)" />
              </div>
              <div class="item-name">{{ item.name }}</div>
            </div>
          </div>
        </div>
      </template>

  

      <template v-else-if="activeTab === 'icons'">
        <IconPanel @select-icon="handleIconSelect" />
      </template>

      <!-- 简历组件面板 -->
      <div v-else-if="activeTab === 'resume'" class="resume-panel">
        <div v-for="group in resumeComponents" :key="group.key" class="resume-category">
          <div class="category-title">{{ group.label }}</div>
          <div class="resume-component-item"
            draggable="true"
            @dragstart="handleDragStart($event, {
              type: 'resume-field',
              component: group.key,
              label: group.label,
              props: {
                background: '#fff',
                padding: '20px',
                borderRadius: '8px',
                boxShadow: '0 1px 2px rgba(0, 0, 0, 0.05)'
              }
            })"
          >
            <div class="component-icon">
              <component :is="getResumeComponentIcon(group.key)" />
            </div>
            <div class="component-info">
              <div class="component-name">{{ group.label }}</div>
              <div class="component-desc">{{ getComponentDescription(group) }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 模板列表 -->
      <div v-else-if="activeTab === 'templates'" class="template-panel">
        <!-- 分类和排序 -->
        <div class="template-header">
          <div class="category-tabs"
            ref="categoryTabsRef"
            @mousedown.prevent="handleMouseDown"
            @mouseleave="handleMouseLeave"
            @mouseup="handleMouseUp"
            @mousemove="handleMouseMove"
            @click="handleCategoryClick"
          >
            <div 
              v-for="cat in ['全部', '推荐', ...categories.map(c => c.name)]" 
              :key="cat"
              class="category-tab-wrapper"
            >
              <div
                class="category-tab"
                :class="{ active: selectedCategory === (cat === '全部' ? '' : cat === '推荐' ? 'recommended' : categories.find(c => c.name === cat)?.id) }"
                @click.stop="handleCategorySelect(cat)"
              >
                {{ cat }}
              </div>
            </div>
          </div>
          <div class="filter-bar">
            <div class="sort-select">
              <select v-model="sortBy" class="select-input">
                <option value="latest">最新发布</option>
                <option value="likes">按点赞量</option>
                <option value="views">按浏览量</option>
              </select>
            </div>
            <div class="view-toggle">
              <label class="toggle-label">
                <input 
                  type="checkbox" 
                  v-model="onlyMyTemplates"
                  class="toggle-input"
                >
                <span class="toggle-text">只看我的</span>
              </label>
            </div>
          </div>
        </div>

        <!-- 模板列表 -->
        <div class="template-list">
          <!-- 加载状态 -->
          <div v-if="loading" class="loading-state">
            <div class="loading-spinner"></div>
            <span>加载中...</span>
          </div>
          
          <!-- 空状态 -->
          <div v-else-if="templates.length === 0" class="empty-state">
            <div class="empty-icon">📭</div>
            <div class="empty-text">{{ onlyMyTemplates ? '暂无个人模版' : '暂无模版' }}</div>
          </div>
          
          <!-- 模板列表 -->
          <div v-else class="template-grid">
            <!-- 统一的模板卡片布局 -->
            <div 
              v-for="template in sortedTemplates"
              :key="template.id"
              class="template-card"
            >
              <div class="template-card-content">
                <div class="template-preview" @click="handlePreviewClick(template)">
                  <img 
                    v-if="template.thumbnail" 
                    :src="template.thumbnail" 
                    :alt="template.name"
                    @error="handleImageError"
                  >
                  <div v-else class="no-thumbnail">无预览图</div>
                </div>
                <div class="template-info">
                  <div class="template-header">
                    <div class="template-name">{{ template.name }}</div>
                    <img 
                      :src="template.creator_avatar || defaultAvatar"
                      class="creator-avatar"
                      :alt="template.creator_name"
                      @error="handleImageError"
                    >
                  </div>
                  <div class="template-desc">{{ template.description || '暂无简介' }}</div>
                  <div class="template-meta">
                    <span>{{ template.pages?.length || 1 }}页</span>
                    <span v-if="template.views">· {{ template.views }}浏览</span>
                    <span v-if="template.likes">· {{ template.likes }}赞</span>
                    <span v-if="onlyMyTemplates" class="template-status" :class="getStatusClass(template.status)">
                      {{ getStatusText(template.status) }}
                    </span>
                  </div>
                </div>
                <div class="template-actions">
                  <template v-if="onlyMyTemplates">
                    <button 
                      class="action-btn"
                      @click="handleEditTemplate(template)"
                    >
                      <Edit theme="outline" :size="14" />
                      编辑
                    </button>
                    <button 
                      class="action-btn danger"
                      @click="handleDeleteTemplate(template)"
                    >
                      <Delete theme="outline" :size="14" />
                      删除
                    </button>
                  </template>
                  <button 
                    class="action-btn primary"
                    @click="handleUseTemplate(template)"
                  >
                    <Plus theme="outline" :size="14" />
                    使用
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 其他面板内容 -->
      <div v-else-if="activeTab === 'element'" class="element-panel">
        <!-- 保持原有的元素面板内容 -->
      </div>
    </div>

    <!-- 添加预览弹窗 -->
    <el-dialog
      v-model="previewVisible"
      :title="previewTemplate?.name"
      width="1000px"
      destroy-on-close
      align-center
    >
      <div class="preview-dialog-content">
        <img 
          v-if="previewTemplate?.thumbnail"
          :src="previewTemplate.thumbnail"
          :alt="previewTemplate?.name"
          class="preview-image"
        >
      </div>
    </el-dialog>

    <!-- 删除确认弹窗 -->
    <TransitionRoot appear :show="showDeleteConfirm" as="template">
      <Dialog as="div" @close="showDeleteConfirm = false" class="relative z-50">
        <TransitionChild
          as="template"
          enter="duration-300 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-200 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-black/25" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div class="flex min-h-full items-center justify-center p-4 text-center">
            <TransitionChild
              as="template"
              enter="duration-300 ease-out"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="duration-200 ease-in"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
            >
              <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900">
                  确认删除模板？
                </DialogTitle>
                <div class="mt-2">
                  <p class="text-sm text-gray-500">
                    此操作将永久删除该模板，且不可恢复。是否继续？
                  </p>
                </div>

                <div class="mt-4 flex justify-end space-x-3">
                  <button
                    type="button"
                    class="inline-flex justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none"
                    @click="showDeleteConfirm = false"
                  >
                    取消
                  </button>
                  <button
                    type="button"
                    class="inline-flex justify-center rounded-md border border-transparent bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700 focus:outline-none"
                    @click="handleConfirmDelete"
                  >
                    确认删除
                  </button>
                </div>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch, nextTick } from 'vue'
import { useTabs } from '../composables/useTabs'
import { useComponents } from '../composables/useComponents'
import * as Icons from '@icon-park/vue-next'
import IconPanel from './icons/IconPanel.vue'
import { resumeComponents } from '../config/resume-components'
import { categoryApi } from '@/api/category'
import { templateApi } from '@/api/template'
import { showToast } from '@/components/ToastMessage'
import { useAccountStore } from '@/stores/account'
import { useRouter } from 'vue-router'
import { Edit, Plus, Delete } from '@icon-park/vue-next'
import { ElMessageBox, ElDialog } from 'element-plus'
import { account } from '@/api/account'
import config from '@/config'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue'

const { activeTab, tabs, switchTab } = useTabs()
const { components } = useComponents()

const loading = ref(false)
const categories = ref([])
const templates = ref([])
const selectedCategory = ref('')
const STORAGE_KEY = 'template_only_my'
const onlyMyTemplates = ref(localStorage.getItem(STORAGE_KEY) === 'true')
const accountStore = useAccountStore()
const router = useRouter()
const authStore = useAuthStore()

const emit = defineEmits(['edit-template', 'use-template', 'create-resume'])

// 在 script setup 开始处添加
console.log('EditorSidebar setup start')

// 监听 activeTab 变化
watch(activeTab, (newValue) => {
  console.log('activeTab changed:', newValue)
  if (newValue === 'templates') {
    loadCategories()
    loadTemplates()
  }
})

// 获取图标组件
const getIconComponent = (iconName) => {
  const componentName = iconName
    .split('-')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join('')
  return Icons[componentName] || Icons.Help
}

// 处理图标选择
const handleIconSelect = (iconData) => {
  // 创建一个模拟的拖拽事件
  const e = new DragEvent('dragstart', {
    bubbles: true,
    cancelable: true
  })
  
  // 设置拖拽数据
  const dragData = {
    type: 'icon',
    props: {
      name: iconData.name,
      size: 24,
      color: '#333333'
    }
  }
  
  // 创建一个新的 DataTransfer 对象
  const dataTransfer = new DataTransfer()
  dataTransfer.setData('text/plain', JSON.stringify(dragData))
  Object.defineProperty(e, 'dataTransfer', {
    value: dataTransfer,
    writable: false
  })
  
  handleDragStart(e, dragData)
}

// 处理拖拽开始
const handleDragStart = (e, item) => {
  let dragData = null
  
  if (item.type === 'resume-field') {
    // 处理简历字段组件
    dragData = {
      type: item.component === 'basicInfo' ? 'basic-info' : 'resume-field',
      component: item.component,
      label: item.label,
      props: {
        ...item.props,
        isPreview: false,
        dataPath: item.component
      }
    }
    console.log('拖拽数据:', dragData)
  } else if (item.type === 'icon') {
    // 处理图标组件
    dragData = {
      type: 'icon',
      props: item.props
    }
  } else {
    // 处理基础组件
    dragData = {
      type: item.type,
      props: item.defaultProps || {}
    }
  }
  
  e.dataTransfer.setData('text/plain', JSON.stringify(dragData))
  e.dataTransfer.effectAllowed = 'copy'
}

// 获取字段图标
const getFieldIcon = (type) => {
  const iconMap = {
    name: Icons.User,
    phone: Icons.Phone,
    email: Icons.Email,
    location: Icons.Location,
    personal_summary: Icons.Notes,
    company: Icons.Building,
    position: Icons.IdCard,
    duration: Icons.Calendar,
    description: Icons.Doc,
    school: Icons.School,
    major: Icons.Book,
    degree: Icons.Certificate,
    skills: Icons.Star,
    level: Icons.Level
  }
  return iconMap[type] || Icons.Help
}

// 获取简历组件图标
const getResumeComponentIcon = (key) => {
  const iconMap = {
    basicInfo: Icons.User,
    jobIntention: Icons.Target,
    education: Icons.School,
    workExperience: Icons.Office,
    skills: Icons.Star,
    languages: Icons.Language,
    certificates: Icons.Certificate,
    projects: Icons.Folder,
    portfolio: Icons.Pic,
    social: Icons.Link
  }
  return iconMap[key] || Icons.Help
}

// 获取组件描述
const getComponentDescription = (component) => {
  const descriptions = {
    basicInfo: '姓名、头像、联系方式等基本信息',
    jobIntention: '期望职位、薪资、城市等求职意向',
    education: '学历、专业、学校等教育经历',
    workExperience: '公司、职位、工作内容等经历',
    skills: '专业技能及熟练程度',
    languages: '语言能力水平',
    certificates: '获得的证书和奖项',
    projects: '参与的项目经历',
    portfolio: '作品集展示',
    social: '社交账号链接'
  }
  return descriptions[component.key] || '简历组件'
}

// 修改分类加载方法
const loadCategories = async () => {
  console.log('开始加载分类')
  try {
    const res = await categoryApi.getList()
    console.log('获取到的分类数据:', res)
    categories.value = Array.isArray(res) ? res : []
    // 如果没有选择分类，默认选择"全部"
    if (!selectedCategory.value) {
      handleCategorySelect('全部')
    }
  } catch (error) {
    console.error('获取分类列表失败:', error)
    showToast('获取分类列表失败', 'error')
  }
}

// 添加排序选项
const sortBy = ref('latest')

// 修改分类选择处理
const handleCategorySelect = (category) => {
  console.log('选择分类:', category)
  
  if (category === '全部') {
    selectedCategory.value = ''
  } else if (category === '推荐') {
    selectedCategory.value = 'recommended'
  } else {
    const categoryObj = categories.value.find(c => c.name === category)
    selectedCategory.value = categoryObj ? categoryObj.id : ''
  }
  console.log('设置的分类值:', selectedCategory.value)
  loadTemplates()
}

// 添加状态文本和样式处理
const getStatusText = (status) => {
  const statusMap = {
    0: '草稿',
    1: '已发布',
    2: '待审核'
  }
  return statusMap[status] || '未知'
}

const getStatusClass = (status) => {
  const classMap = {
    0: 'status-draft',
    1: 'status-published',
    2: 'status-pending'
  }
  return classMap[status] || ''
}

// 添加排序后的模版列表
const sortedTemplates = computed(() => {
  let sorted = [...templates.value]
  
  switch (sortBy.value) {
    case 'likes':
      sorted.sort((a, b) => (b.likes || 0) - (a.likes || 0))
      break
    case 'views':
      sorted.sort((a, b) => (b.views || 0) - (a.views || 0))
      break
    case 'latest':
    default:
      sorted.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
      break
  }
  
  return sorted
})

// 修改模版加载方法
const loadTemplates = async () => {
  console.log('开始加载模版，当前状态:', {
    activeTab: activeTab.value,
    selectedCategory: selectedCategory.value,
    onlyMyTemplates: onlyMyTemplates.value,
    sortBy: sortBy.value,
    currentUserId: accountStore.userInfo?.id
  })
  
  loading.value = true
  try {
    const params = {}
    
    if (onlyMyTemplates.value) {
      // 只看我的模式：获取当前用户的所有状态模版
      if (!accountStore.userInfo?.id) {
        console.warn('未找到当前用户ID')
        templates.value = []
        return
      }
      params.creator = accountStore.userInfo.id
    } else {
      // 公开模式：只显示已发布的公开模版
      params.status = 1
      params.is_public = true
      
      // 根据分类和排序设置参数
      if (selectedCategory.value === 'recommended') {
        params.is_recommended = true
      } else if (selectedCategory.value) {
        params.category = selectedCategory.value
      }
    }

    // 设置排序参数
    if (sortBy.value) {
      params.sort = sortBy.value
    }
    
    console.log('加载模版参数:', params)
    const res = await templateApi.getTemplates(params)
    console.log('获取到的模版数据:', res)
    
    let templateData = []
    if (res?.data?.results) {
      templateData = res.data.results
    } else if (res?.data) {
      templateData = res.data
    } else if (Array.isArray(res)) {
      templateData = res
    }

    // 在"只看我的"模式下，再次确保只显示当前用户的模版
    if (onlyMyTemplates.value) {
      templateData = templateData.filter(template => template.creator === accountStore.userInfo?.id)
    }

    // 获取所有模板创建者的用户信息
    const creatorIds = [...new Set(templateData.map(t => t.creator))].filter(Boolean)
    console.log('需要获取的创建者信息:', creatorIds)
    
    const creatorInfoMap = new Map()
    
    for (const creatorId of creatorIds) {
      try {
        const userRes = await account.getUserPublicInfo(creatorId)
        console.log(`获取用户 ${creatorId} 信息:`, userRes)
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

    // 处理模板数据，添加创建者信息
    templates.value = templateData.map(template => {
      const creatorInfo = creatorInfoMap.get(template.creator)
      const avatar = creatorInfo?.avatar
      const avatarUrl = avatar ? (
        avatar.startsWith('http') ? avatar : `${config.mediaURL}/${avatar.replace(/^\/?(media\/)?/, '')}`
      ) : null

      const processedTemplate = {
        ...template,
        creator_name: creatorInfo?.name || template.creator_name || '匿名用户',
        creator_avatar: avatarUrl,
        creator_is_vip: creatorInfo?.is_vip || false,
        creator_position: creatorInfo?.position || ''
      }
      console.log('处理后的模板数据:', processedTemplate)
      return processedTemplate
    })
  } catch (error) {
    console.error('获取模板列表失败:', error)
    showToast('获取模板列表失败', 'error')
    templates.value = []
  } finally {
    loading.value = false
  }
}

// 监听分类和排序变化
watch([selectedCategory, sortBy], () => {
  loadTemplates()
})

// 监听"只看我的"变化
watch(onlyMyTemplates, (newValue) => {
  console.log('只看我的状态变化:', newValue)
  localStorage.setItem(STORAGE_KEY, newValue.toString())
  loadTemplates()
})

// 选择模板
const handleTemplateSelect = (template) => {
  // TODO: 实现模板选择逻辑
  console.log('选择模板:', template)
}

// 判断模板是否可编辑
const isTemplateEditable = (template) => {
  const currentUserId = accountStore.userInfo?.id
  console.log('模板权限检查:', {
    templateId: template.id,
    templateCreator: template.creator,
    currentUserId: currentUserId,
    isMatch: template.creator === currentUserId
  })
  return template.creator === currentUserId
}

// 处理编辑模板
const handleEditTemplate = (template) => {
  router.push(`/editor/edit/${template.id}`)
}

// 处理使用模板
const handleUseTemplate = (template) => {
  router.push(`/editor/use/${template.id}`)
}

// 添加临时存储要删除的模板
const templateToDelete = ref(null)

// 处理删除模板
const handleDeleteTemplate = async (template) => {
  templateToDelete.value = template
  showDeleteConfirm.value = true
}

// 添加预览相关的状态
const previewVisible = ref(false)
const previewTemplate = ref(null)

// 添加预览点击处理函数
const handlePreviewClick = (template) => {
  previewTemplate.value = template
  previewVisible.value = true
}

// 添加拖动相关的变量
const isMouseDown = ref(false)
const startX = ref(0)
const scrollLeft = ref(0)
const categoryTabsRef = ref(null)

// 添加拖动相关的方法
const handleMouseDown = (e) => {
  isMouseDown.value = true
  const categoryTabs = categoryTabsRef.value
  if (!categoryTabs) return
  
  categoryTabs.style.cursor = 'grabbing'
  startX.value = e.pageX - categoryTabs.offsetLeft
  scrollLeft.value = categoryTabs.scrollLeft
}

const handleMouseUp = () => {
  isMouseDown.value = false
  const categoryTabs = categoryTabsRef.value
  if (!categoryTabs) return
  
  categoryTabs.style.cursor = 'grab'
}

const handleMouseLeave = () => {
  isMouseDown.value = false
  const categoryTabs = categoryTabsRef.value
  if (!categoryTabs) return
  
  categoryTabs.style.cursor = 'grab'
}

const handleMouseMove = (e) => {
  if (!isMouseDown.value) return
  
  const categoryTabs = categoryTabsRef.value
  if (!categoryTabs) return
  
  e.preventDefault()
  const x = e.pageX - categoryTabs.offsetLeft
  const walk = (x - startX.value) * 2
  categoryTabs.scrollLeft = scrollLeft.value - walk
}

// 添加新的点击处理方法
const handleCategoryClick = (e) => {
  // 如果是拖动操作，不触发点击
  if (isMouseDown.value) {
    e.preventDefault()
    e.stopPropagation()
  }
}

// 组件挂载时初始化
onMounted(() => {
  console.log('组件挂载，开始初始化')
  console.log('初始只看我的状态:', onlyMyTemplates.value)
  loadCategories()
  loadTemplates()
})

// 导出需要的方法和数据
defineExpose({
  loadTemplates
})

// 处理模板点赞
const handleLike = async (template) => {
  if (!authStore.isLoggedIn || !accountStore.userInfo) {
    ElMessage.warning('请先登录后再点赞')
    router.push(`/login?redirect=${encodeURIComponent(window.location.pathname)}`)
    return
  }

  try {
    const res = await templateApi.like(template.id)
    if (res.data) {
      // 更新模板的点赞状态和数量
      template.isLiked = !template.isLiked
      template.likes = template.likes + (template.isLiked ? 1 : -1)
    }
  } catch (error) {
    console.error('点赞失败:', error)
    if (error.response?.status === 403) {
      ElMessage.warning('登录已过期，请重新登录')
      authStore.clearAuth()
      router.push(`/login?redirect=${encodeURIComponent(window.location.pathname)}`)
    } else {
      ElMessage.error('点赞失败，请稍后重试')
    }
  }
}

// 添加删除确认状态
const showDeleteConfirm = ref(false)

// 添加删除确认处理函数
const handleConfirmDelete = async () => {
  if (!templateToDelete.value) {
    showDeleteConfirm.value = false
    return
  }

  try {
    // 调用删除 API
    await templateApi.delete(templateToDelete.value.id)
    
    // 从列表中移除该模板
    templates.value = templates.value.filter(t => t.id !== templateToDelete.value.id)
    
    // 显示成功提示
    ElMessage.success('删除成功')
  } catch (error) {
    console.error('删除模板失败:', error)
    ElMessage.error(error.response?.data?.message || '删除失败，请稍后重试')
  } finally {
    showDeleteConfirm.value = false
    templateToDelete.value = null
  }
}
</script>

<style scoped>
.editor-sidebar {
  width: 260px;
  height: 100%;
  background: #fff;
  display: flex;
  flex-direction: column;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 
    0 4px 20px rgba(0, 0, 0, 0.08),
    0 0 0 1px rgba(0, 0, 0, 0.04);
}

.sidebar-header {
  padding: 16px;
  background: linear-gradient(to bottom, #fff, rgba(255, 255, 255, 0.95));
  backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.02);
}

.tab-container {
  position: relative;
  display: flex;
  background: rgba(28, 31, 35, 0.06);
  border-radius: 12px;
  padding: 4px;
  gap: 4px;
}

.tab-item {
  position: relative;
  flex: 1;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 8px;
  overflow: hidden;
  user-select: none;
}

.tab-text {
  position: relative;
  z-index: 2;
  font-size: 14px;
  font-weight: 500;
  color: #666;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.tab-background {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #fff 0%, rgba(255, 255, 255, 0.95) 100%);
  box-shadow: 
    0 2px 8px rgba(0, 0, 0, 0.08),
    inset 0 0 0 1px rgba(255, 255, 255, 0.6);
  border-radius: 8px;
  z-index: 1;
  animation: slideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.tab-item:hover .tab-text {
  color: #1890ff;
}

.tab-item.active .tab-text {
  color: #1890ff;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: scale(0.96);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.sidebar-content {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0.95), #fff);
}

.sidebar-content::-webkit-scrollbar {
  width: 4px;
}

.sidebar-content::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-content::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 2px;
}

.component-group {
  margin-bottom: 24px;
}

.group-title {
  font-size: 13px;
  color: #999;
  margin-bottom: 12px;
  padding-left: 4px;
}

.group-content {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.component-item {
  height: 80px;
  background: #fff;
  border: 1px solid rgba(0, 0, 0, 0.04);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: move;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  user-select: none;
}

.component-item:hover {
  border-color: rgba(24, 144, 255, 0.2);
  transform: translateY(-1px);
  box-shadow: 
    0 4px 16px rgba(24, 144, 255, 0.1),
    0 1px 4px rgba(24, 144, 255, 0.05);
}

.component-item:active {
  transform: translateY(0);
}

.item-icon {
  font-size: 24px;
  color: #666;
  margin-bottom: 8px;
  transition: all 0.3s;
}

.component-item:hover .item-icon {
  color: #1890ff;
  transform: scale(1.1);
}

.item-name {
  font-size: 12px;
  color: #666;
  transition: color 0.3s;
}

.component-item:hover .item-name {
  color: #1890ff;
}

.layers-panel,
.templates-panel {
  color: #999;
  text-align: center;
  padding: 40px 0;
}

.resume-panel {
  padding: 16px;
}

.resume-category {
  margin-bottom: 20px;
}

.category-title {
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin-bottom: 12px;
}

.resume-component-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #fff;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  cursor: move;
  transition: all 0.3s;
}

.resume-component-item:hover {
  border-color: #1890ff;
  box-shadow: 0 2px 8px rgba(24, 144, 255, 0.15);
}

.component-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  border-radius: 6px;
  color: #666;
}

.component-info {
  flex: 1;
  min-width: 0;
}

.component-name {
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin-bottom: 4px;
}

.component-desc {
  font-size: 12px;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.template-panel {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.template-header {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 0 10px 10px 10px;
  position: sticky;
  top: -10px;
  background: white;
  z-index: 10;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  margin: -10px -10px 4px -10px;
  padding: 10px 20px 10px 20px;
}

.category-tabs {
  display: flex;
  gap: 8px;
  padding: 4px 0;
  position: relative;
  overflow-x: auto;
  cursor: grab;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
  -ms-overflow-style: none;
  white-space: nowrap;
  width: 220px;
  user-select: none;
}

.category-tabs::-webkit-scrollbar {
  display: none;
}

.category-tabs:active {
  cursor: grabbing;
}

/* 添加滚动提示阴影 */
.category-tabs::before,
.category-tabs::after {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  width: 24px;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.2s;
}

.category-tabs::before {
  left: 0;
  background: linear-gradient(to right, rgba(255, 255, 255, 0.9), transparent);
}

.category-tabs::after {
  right: 0;
  background: linear-gradient(to left, rgba(255, 255, 255, 0.9), transparent);
}

.category-tabs:hover::before,
.category-tabs:hover::after {
  opacity: 1;
}

.category-tab-wrapper {
  pointer-events: none;
}

.category-tab {
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  color: #666;
  background: transparent;
  transition: all 0.2s;
  border: 1px solid transparent;
  flex-shrink: 0;
  pointer-events: auto;
  cursor: pointer;
}

.category-tab:hover {
  color: #1890ff;
  background: rgba(24, 144, 255, 0.04);
}

.category-tab.active {
  color: #1890ff;
  background: rgba(24, 144, 255, 0.08);
  border-color: #1890ff;
  font-weight: 500;
}

.filter-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 0 0;
  border-top: 1px solid #f0f0f0;
  width: 220px;
}

.sort-select {
  position: relative;
  flex: 1;
  min-width: 0;
}

.select-input {
  width: 100%;
  appearance: none;
  padding: 6px 28px 6px 12px;
  border: 1px solid #e8e8e8;
  border-radius: 6px;
  font-size: 13px;
  color: #666;
  background: white url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23999' d='M2.293 4.293a1 1 0 0 1 1.414 0L6 6.586l2.293-2.293a1 1 0 1 1 1.414 1.414l-3 3a1 1 0 0 1-1.414 0l-3-3a1 1 0 0 1 0-1.414z'/%3E%3C/svg%3E") no-repeat right 8px center;
  cursor: pointer;
  transition: all 0.2s;
}

.select-input:hover {
  border-color: #1890ff;
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 6px;
  background: #f5f5f5;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
  flex-shrink: 0;
}

.toggle-label:hover {
  background: #e8e8e8;
}

.toggle-input {
  appearance: none;
  width: 14px;
  height: 14px;
  border: 2px solid #d9d9d9;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.toggle-input:checked {
  background: #1890ff;
  border-color: #1890ff;
}

.toggle-input:checked::after {
  content: '';
  position: absolute;
  left: 4px;
  top: 1px;
  width: 4px;
  height: 8px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.toggle-text {
  font-size: 13px;
  color: #666;
}

.template-list {
  margin-bottom: 16px;
}

.template-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, 220px);
  gap: 16px;
  justify-content: space-between;
}

.template-card {
  position: relative;
  z-index: 1;
  width: 220px;
  height: auto;
  min-height: 280px;
  background: white;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s;
}

.template-card:hover {
  border-color: #e6e6e6;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.template-card-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.template-preview {
  width: 100%;
  height: 120px;
  background: #f5f5f5;
  overflow: hidden;
  cursor: pointer;
  transition: opacity 0.2s;
}

.template-preview:hover {
  opacity: 0.9;
}

.template-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: top center;
}

.template-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px;
  min-height: 100px;
}

.template-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
}

.template-name {
  font-size: 13px;
  font-weight: 500;
  color: #333;
  flex: 1;
  line-height: 1.4;
}

.creator-avatar {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.template-desc {
  font-size: 12px;
  color: #666;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  margin: 0;
}

.template-meta {
  font-size: 11px;
  color: #999;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 4px;
  margin: 0;
}

.template-status {
  padding: 1px 4px;
  border-radius: 2px;
  font-size: 11px;
  color: white;
}

.status-draft {
  background-color: #faad14;
}

.status-published {
  background-color: #52c41a;
}

.status-pending {
  background-color: #1890ff;
}

.template-actions {
  display: flex;
  gap: 4px;
  padding: 12px;
  border-top: 1px solid #f0f0f0;
}

.action-btn {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  height: 28px;
  padding: 0 8px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 12px;
  background: white;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  border-color: #40a9ff;
  color: #40a9ff;
}

.action-btn.primary {
  color: #1890ff;
  border-color: #1890ff;
}

.action-btn.primary:hover {
  background: #1890ff;
  color: white;
}

.action-btn.danger {
  color: #ff4d4f;
  border-color: #ff4d4f;
}

.action-btn.danger:hover {
  background: #ff4d4f;
  color: white;
}

.action-btn .i-icon {
  font-size: 12px;
}

.no-thumbnail {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-size: 12px;
  background: #f5f5f5;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  color: #999;
}

.loading-spinner {
  width: 24px;
  height: 24px;
  border: 2px solid #f3f3f3;
  border-top: 2px solid #1890ff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 8px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  color: #999;
}

.empty-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.empty-text {
  font-size: 14px;
}

.create-template-btn-container {
  display: flex;
  justify-content: center;
  margin-top: 16px;
}

.create-template-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.create-template-btn:hover {
  background: #40a9ff;
}

.plus-icon {
  font-size: 16px;
  font-weight: bold;
}

/* 添加预览弹窗样式 */
.preview-dialog-content {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 24px;
  border-radius: 8px;
  min-height: 80vh;
  width: 794px;
  margin: 0 auto;
}

.preview-image {
  width: 794px;
  height: auto;
  min-height: 80vh;
  max-height: 85vh;
  object-fit: contain;
  border-radius: 4px;
  padding: 40px 0;
}

:deep(.el-dialog) {
  border-radius: 8px;
  overflow: hidden;
  margin: 0 auto !important;
  width: 842px !important;
  height: 90vh;
  display: flex;
  flex-direction: column;
}

:deep(.el-dialog__body) {
  padding: 0;
  flex: 1;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  background: white;
}

:deep(.el-dialog__header) {
  margin: 0;
  padding: 16px 24px;
  border-bottom: 1px solid #f0f0f0;
}

:deep(.el-dialog__title) {
  font-size: 16px;
  font-weight: 500;
}

/* 添加一个包装容器来处理点击事件 */
.category-tab-wrapper {
  cursor: pointer;
  pointer-events: auto;
}
</style> 