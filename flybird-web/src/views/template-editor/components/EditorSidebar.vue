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
        <!-- 分类选择 -->
        <div class="category-select">
          <select v-model="selectedCategory" class="select-input">
            <option value="">全部分类</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
          <div class="filter-options">
            <label class="filter-label">
              <input type="checkbox" v-model="onlyMyTemplates"> 只看我的
            </label>
          </div>
        </div>

        <!-- 模板列表 -->
        <div class="template-list">
          <div v-if="loading" class="loading-state">
            加载中...
          </div>
          <template v-else>
            <div v-if="templates.length === 0" class="empty-state">
              暂无模板
            </div>
            <div v-else class="template-grid">
              <div
                v-for="template in templates"
                :key="template.id"
                class="template-item"
              >
                <div class="template-preview" @click="handleTemplateSelect(template)">
                  <img v-if="template.thumbnail" :src="template.thumbnail" :alt="template.name">
                  <div v-else class="no-thumbnail">暂无预览图</div>
                </div>
                <div class="template-info">
                  <div class="template-name">{{ template.name }}</div>
                  <div class="template-meta">
                    <span>{{ template.pages?.length || 1 }}页</span>
                    <div class="template-actions">
                      <button 
                        v-if="template.creator === accountStore.userInfo?.id"
                        class="action-btn"
                        @click="handleEditTemplate(template)"
                      >
                        <Edit theme="outline" :size="16" />
                        <span>编辑</span>
                      </button>

                      <button 
                        class="action-btn primary"
                        @click="handleUseTemplate(template)"
                      >
                        <Plus theme="outline" :size="16" />
                        <span>使用</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- 添加创建模板按钮 -->
            <div v-if="onlyMyTemplates" class="create-template-btn-container">
              <button class="create-template-btn" @click="handleCreateTemplate">
                <span class="plus-icon">+</span>
                创建新模板
              </button>
            </div>
          </template>
        </div>
      </div>

      <!-- 其他面板内容 -->
      <div v-else-if="activeTab === 'element'" class="element-panel">
        <!-- 保持原有的元素面板内容 -->
      </div>
    </div>
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
import { Edit, Plus } from '@icon-park/vue-next'

const { activeTab, tabs, switchTab } = useTabs()
const { components } = useComponents()

const loading = ref(false)
const categories = ref([])
const templates = ref([])
const selectedCategory = ref('')
const onlyMyTemplates = ref(false)
const accountStore = useAccountStore()
const router = useRouter()

const emit = defineEmits(['edit-template', 'use-template', 'create-resume'])

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

// 获取分类列表
const loadCategories = async () => {
  try {
    const res = await categoryApi.getList()
    categories.value = Array.isArray(res) ? res : []
  } catch (error) {
    console.error('获取分类列表失败:', error)
    showToast('获取分类列表失败', 'error')
  }
}

// 获取模板列表
const loadTemplates = async () => {
  loading.value = true
  try {
    const params = {}
    if (selectedCategory.value) {
      params.category = selectedCategory.value
    }
    console.log('开始加载模板列表，参数:', params)
    const res = await templateApi.getTemplates(params)
    console.log('获取到的模板数据:', res)
    
    let templateData = []
    if (res.data?.results) {
      templateData = res.data.results
    } else if (Array.isArray(res.data)) {
      templateData = res.data
    } else if (Array.isArray(res)) {
      templateData = res
    }
    
    // 在前端进行过滤前，打印用户信息
    const currentUserId = accountStore.userInfo?.id
    console.log('当前用户信息:', {
      userId: currentUserId,
      userInfo: accountStore.userInfo
    })
    
    // 先按分类过滤
    if (selectedCategory.value) {
      templateData = templateData.filter(template => template.category === selectedCategory.value)
    }
    
    // 再按用户和状态过滤
    if (onlyMyTemplates.value) {
      // 只看我的：显示所有我创建的模板
      templateData = templateData.filter(template => {
        const isMyTemplate = template.creator === currentUserId
        console.log('模板过滤(只看我的):', {
          templateId: template.id,
          templateName: template.name,
          creator: template.creator,
          currentUserId,
          category: template.category,
          selectedCategory: selectedCategory.value,
          isMyTemplate
        })
        return isMyTemplate
      })
    } else {
      // 不是只看我的：显示已发布的公开模板和我的所有模板
      templateData = templateData.filter(template => {
        const isMyTemplate = template.creator === currentUserId
        const isPublished = template.status === 1
        console.log('模板过滤:', {
          templateId: template.id,
          templateName: template.name,
          creator: template.creator,
          currentUserId,
          category: template.category,
          selectedCategory: selectedCategory.value,
          status: template.status,
          isPublic: template.is_public,
          isMyTemplate,
          isPublished,
          shouldShow: isMyTemplate || (isPublished && template.is_public)
        })
        return isMyTemplate || (isPublished && template.is_public)
      })
    }

    console.log('过滤后的模板数据:', {
      total: templateData.length,
      templates: templateData,
      selectedCategory: selectedCategory.value
    })
    templates.value = templateData
  } catch (error) {
    console.error('获取模板列表失败:', error)
    showToast('获取模板列表失败', 'error')
    templates.value = []
  } finally {
    loading.value = false
  }
}

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

// 编辑模板
const handleEditTemplate = async (template) => {
  try {
    // 先获取模板详情
    const res = await templateApi.getDetail(template.id)
    if (res?.data) {  // 确保有 data 属性
      // 发出编辑事件，传递模板数据
      emit('edit-template', res.data)
      
      // 然后跳转到编辑页面
      router.push({
        name: 'template-edit',
        params: { id: template.id }
      })
    }
  } catch (error) {
    console.error('获取模板详情失败:', error)
    showToast('获取模板详情失败', 'error')
  }
}

// 使用模板创建简历
const handleUseTemplate = async (template) => {
  try {
    // 获取模板详情
    const res = await templateApi.getDetail(template.id)
    if (res?.data) {  // 确保有 data 属性
      console.log('获取到模板详情:', res.data)  // 使用 res.data
      
      // 确保数据格式正确
      if (!Array.isArray(res.data.pages)) {
        // 如果没有 pages 数组，构造一个默认的
        res.data.pages = [{
          page_index: 0,
          page_data: {
            elements: res.data.elements || [],
            config: {
              width: 794,
              height: 1123,
              backgroundColor: '#ffffff',
              showGrid: false,
              showGuideLine: true,
              ...(res.data.config || {})
            }
          }
        }]
      }

      // 触发父组件的 use-template 事件，传递模板数据
      emit('use-template', res.data)  // 传递 res.data

      // 等待一段时间确保数据更新完成
      await new Promise(resolve => setTimeout(resolve, 300))
      
      // 最后再跳转路由
      router.push({
        name: 'resume-create-from-template',
        params: { templateId: template.id }
      })
    }
  } catch (error) {
    console.error('获取模板详情失败:', error)
    showToast('获取模板详情失败', 'error')
  }
}

// 创建新模板
const handleCreateTemplate = () => {
  const currentUserId = accountStore.userInfo?.id
  console.log('创建模板时的用户信息:', {
    userId: currentUserId,
    userInfo: accountStore.userInfo
  })

  const newTemplate = {
    id: null,
    name: '新建模板',
    creator: currentUserId,
    category: selectedCategory.value || null,
    is_public: false,
    status: 0,  // 新创建的模板默认为草稿状态
    pages: [{
      page_index: 0,  // 从0开始
      page_data: {
        elements: [],
        config: {
          width: 794,
          height: 1123,
          backgroundColor: '#ffffff',
          showGrid: true,
          showGuideLine: true
        }
      }
    }]
  }
  
  console.log('新创建的模板数据:', newTemplate)
  console.log('模板数据结构验证:', {
    hasPages: !!newTemplate.pages,
    pagesLength: newTemplate.pages?.length,
    hasPageData: !!newTemplate.pages?.[0]?.page_data,
    hasElements: !!newTemplate.pages?.[0]?.page_data?.elements,
    hasConfig: !!newTemplate.pages?.[0]?.page_data?.config
  })
  
  // 直接发出编辑事件，不需要调用 handleEditTemplate
  emit('edit-template', newTemplate)
}

// 监听筛选条件变化
watch([selectedCategory, onlyMyTemplates], () => {
  console.log('筛选条件变更:', { 
    category: selectedCategory.value, 
    onlyMine: onlyMyTemplates.value 
  })
  loadTemplates()
})

// 组件挂载时加载数据
onMounted(() => {
  console.log('组件挂载，开始加载数据')
  loadCategories()
  loadTemplates()
})

// 导出需要的方法和数据
defineExpose({
  loadTemplates
})
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
  padding: 16px;
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
  margin-top: 16px;
}

.category-select {
  margin-bottom: 16px;
}

.select-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  outline: none;
}

.template-list {
  margin-bottom: 16px;
}

.template-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.template-item {
  cursor: pointer;
  border: 1px solid #e8e8e8;
  border-radius: 4px;
  overflow: hidden;
  transition: all 0.3s;
}

.template-item:hover {
  border-color: #1890ff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.09);
}

.template-preview {
  aspect-ratio: 1;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.no-thumbnail {
  color: #999;
  font-size: 12px;
}

.template-info {
  padding: 8px;
}

.template-name {
  font-size: 14px;
  color: #333;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.template-meta {
  font-size: 12px;
  color: #999;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 32px;
  color: #999;
}

.filter-options {
  margin-top: 8px;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #666;
  cursor: pointer;
}

.template-actions {
  display: flex;
  gap: 8px;
  margin-top: 4px;
}

.action-btn {
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.action-btn.edit {
  background-color: #e6f7ff;
  color: #1890ff;
}

.action-btn.edit:hover {
  background-color: #bae7ff;
}

.action-btn.use {
  background-color: #f6ffed;
  color: #52c41a;
}

.action-btn.use:hover {
  background-color: #d9f7be;
}

.create-template-btn-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.create-template-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(24, 144, 255, 0.2);
}

.create-template-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.3);
}

.create-template-btn:active {
  transform: translateY(0);
}

.plus-icon {
  font-size: 18px;
  font-weight: bold;
}
</style> 