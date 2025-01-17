<template>
  <div class="toolbar-panel">
    <!-- 左侧垂直选项卡 -->
    <div class="toolbar-tabs">
      <div
        v-for="tab in tabs"
        :key="tab.value"
        class="toolbar-tab"
        :class="{ active: activeTab === tab.value }"
        @click="activeTab = tab.value"
      >
        <v-icon :icon="tab.icon" size="24" class="mb-1"></v-icon>
        <span class="tab-text">{{ tab.label }}</span>
      </div>
    </div>

    <!-- 右侧内容区域 -->
    <div class="toolbar-content">
      <!-- 模板列表 -->
      <div v-if="activeTab === 'template'" class="template-list">
        <!-- 筛选器 -->
        <div class="filter-section">
          <div 
            ref="categoryFilter"
            class="category-filter"
          >
            <div
              v-for="category in allCategories"
              :key="category.id"
              class="category-item"
              :class="{ active: selectedCategory === category.id }"
              @click="selectedCategory = category.id"
            >
              {{ category.name }}
            </div>
          </div>
          <div class="vip-filter">
            <div class="vip-label">
              <v-icon icon="mdi-crown" color="warning" size="16" class="mr-1"></v-icon>
              <span>会员模板</span>
            </div>
            <v-switch
              v-model="showVipOnly"
              color="warning"
              hide-details
              density="compact"
              class="vip-switch"
              inset
              false-icon="mdi-close"
              true-icon="mdi-check"
            ></v-switch>
          </div>
        </div>

        <!-- 加载状态 -->
        <div v-if="loading" class="loading-state">
          <v-progress-circular indeterminate></v-progress-circular>
        </div>

        <!-- 模板列表 -->
        <template v-else>
          <div class="template-grid">
            <div
              v-for="template in filteredTemplates"
              :key="template.id"
              class="template-item"
            >
              <div class="template-preview">
                <img 
                  :src="template.thumbnail || '/template-default.png'" 
                  alt="模板预览"
                  @click.stop="handlePreviewImage(template)"
                  style="cursor: pointer;"
                >
                <div v-if="template.is_vip" class="template-vip">
                  <v-chip color="warning" size="small">VIP</v-chip>
                </div>
              </div>
              <div class="template-info">
                <div class="template-name">{{ template.name }}</div>
                <div class="template-desc">{{ template.description }}</div>
              </div>
              <div class="template-actions">
                <button 
                  class="use-template-btn"
                  :class="{ vip: template.is_vip }"
                  @click.stop="handleTemplateSelect(template)"
                >
                  使用此模板
                </button>
              </div>
            </div>
          </div>
        </template>
      </div>

      <!-- 元素列表 -->
      <div v-else-if="activeTab === 'element'" class="element-list">
        <div
          v-for="element in elements"
          :key="element.type"
          class="element-item"
          draggable="true"
          @dragstart="handleElementDragStart($event, element)"
        >
          <v-icon :icon="element.icon" size="24" class="element-icon"></v-icon>
          <span class="element-name">{{ element.name }}</span>
        </div>
      </div>

      <!-- 文本列表 -->
      <div v-else-if="activeTab === 'text'" class="text-list">
        <div
          v-for="text in textStyles"
          :key="text.type"
          class="text-item"
          draggable="true"
          @dragstart="handleElementDragStart($event, { type: 'text', ...text })"
        >
          <div class="text-preview" :style="text.styles">{{ text.name }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { useTemplateStore } from '@/stores/template'

const templateStore = useTemplateStore()
const templates = ref([])
const activeTab = ref('template')

// 标签页配置
const tabs = [
  { label: '模板', value: 'template', icon: 'mdi-file-document-outline' },
  { label: '元素', value: 'element', icon: 'mdi-shape-outline' },
  { label: '文本', value: 'text', icon: 'mdi-format-text' }
]

// 元素配置
const elements = [
  { type: 'circle', name: '圆形', icon: 'mdi-circle-outline' },
  { type: 'rectangle', name: '矩形', icon: 'mdi-rectangle-outline' },
  { type: 'triangle', name: '三角形', icon: 'mdi-triangle-outline' },
  { type: 'image', name: '图片', icon: 'mdi-image-outline' }
]

// 文本样式配置
const textStyles = [
  { 
    name: '标题', 
    styles: { 
      fontSize: '24px',
      fontWeight: 'bold'
    }
  },
  { 
    name: '副标题', 
    styles: { 
      fontSize: '18px',
      fontWeight: '500'
    }
  },
  { 
    name: '正文', 
    styles: { 
      fontSize: '14px'
    }
  },
  { 
    name: '说明文本', 
    styles: { 
      fontSize: '12px',
      color: '#666'
    }
  }
]

const loading = ref(false)
const categories = ref([])

// 分类和筛选相关
const selectedCategory = ref('all')
const showVipOnly = ref(false)
const allCategories = ref([
  { id: 'all', name: '全部' }
])

const categoryFilter = ref(null)
let isMouseDown = false
let startX
let scrollLeft

// 处理鼠标按下
const handleMouseDown = (e) => {
  isMouseDown = true
  const slider = categoryFilter.value
  startX = e.pageX - slider.offsetLeft
  scrollLeft = slider.scrollLeft
}

// 处理鼠标移动
const handleMouseMove = (e) => {
  if (!isMouseDown) return
  e.preventDefault()
  const slider = categoryFilter.value
  const x = e.pageX - slider.offsetLeft
  const walk = (x - startX) * 2 // 滚动速度
  slider.scrollLeft = scrollLeft - walk
}

// 处理鼠标释放
const handleMouseUp = () => {
  isMouseDown = false
}

// 获取模板列表和分类
const refreshTemplates = async () => {
  loading.value = true
  try {
    // 获取分类列表
    const categoryResponse = await templateStore.getCategories()
    if (categoryResponse?.data?.results) {
      allCategories.value = [
        { id: 'all', name: '全部' },
        ...categoryResponse.data.results
      ]
    }

    // 获取模板列表
    const response = await templateStore.getTemplates({
      page: 1,
      page_size: 50,
      ordering: '-created_at',
      status: 'pending,approved'
    })
    
    if (response?.data?.results) {
      templates.value = response.data.results
    }
  } catch (error) {
    console.error('获取数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 过滤后的模板列表
const filteredTemplates = computed(() => {
  let result = templates.value

  // 分类筛选
  if (selectedCategory.value !== 'all') {
    result = result.filter(template => template.category === selectedCategory.value)
  }

  // 会员筛选
  if (showVipOnly.value) {
    result = result.filter(template => template.is_vip)
  }

  return result
})

// 处理模板选择
const handleTemplateSelect = (template) => {
  emit('template-select', template)
}

// 处理元素拖拽开始
const handleElementDragStart = (event, element) => {
  const elementConfig = {
    width: 100,
    height: 100,
    styles: {
      ...element.styles,
      borderRadius: element.type === 'circle' ? '50%' : '0'
    }
  }

  event.dataTransfer.setData('element-type', element.type)
  event.dataTransfer.setData('element-config', JSON.stringify(elementConfig))
  emit('element-dragstart', { type: element.type, config: elementConfig })
}

// 处理查看大图
const handlePreviewImage = (template) => {
  emit('preview-image', template.thumbnail || '/template-default.png')
}

const emit = defineEmits(['template-select', 'element-dragstart', 'preview-image'])

defineExpose({
  refreshTemplates
})

onMounted(() => {
  refreshTemplates()
  
  const slider = categoryFilter.value
  if (slider) {
    slider.addEventListener('mousedown', handleMouseDown)
    slider.addEventListener('mousemove', handleMouseMove)
    slider.addEventListener('mouseup', handleMouseUp)
    slider.addEventListener('mouseleave', handleMouseUp)
  }
})

onUnmounted(() => {
  const slider = categoryFilter.value
  if (slider) {
    slider.removeEventListener('mousedown', handleMouseDown)
    slider.removeEventListener('mousemove', handleMouseMove)
    slider.removeEventListener('mouseup', handleMouseUp)
    slider.removeEventListener('mouseleave', handleMouseUp)
  }
})
</script>

<style scoped>
.toolbar-panel {
  width: 320px;
  height: 100%;
  display: flex;
  background: #fff;
  border-right: 1px solid #e0e0e0;
}

.toolbar-tabs {
  width: 80px;
  height: 100%;
  background: #f8f9fa;
  border-right: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  padding: 12px 0;
}

.toolbar-tab {
  height: 64px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #606266;
  transition: all 0.3s;
  position: relative;
}

.toolbar-tab.active {
  color: var(--v-theme-primary);
  background: #fff;
}

.toolbar-tab.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: var(--v-theme-primary);
}

.tab-text {
  font-size: 12px;
  margin-top: 4px;
}

.toolbar-content {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
}

.template-item {
  width: 200px;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);

    .template-actions {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .template-preview {
    position: relative;
    width: 100%;
    height: 282px;
    overflow: hidden;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;

    img {
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
    }

    .template-vip {
      position: absolute;
      top: 8px;
      left: 8px;
      z-index: 1;
    }
  }

  .template-info {
    padding: 10px;
    width: 100%;
    box-sizing: border-box;

    .template-name {
      font-size: 14px;
      font-weight: 500;
      margin-bottom: 4px;
      color: #333;
    }

    .template-desc {
      font-size: 12px;
      color: #666;
      line-height: 1.4;
    }
  }

  .template-actions {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 12px;
    background: linear-gradient(to top, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.8));
    opacity: 0;
    transform: translateY(10px);
    transition: all 0.3s ease;
    backdrop-filter: blur(4px);
    width: 100%;
    box-sizing: border-box;

    .use-template-btn {
      width: 100%;
      height: 36px;
      border: none;
      border-radius: 4px;
      background: #1976d2;
      color: white;
      font-size: 14px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s ease;

      &:hover {
        background: #1565c0;
      }

      &.vip {
        background: linear-gradient(45deg, #FFB300, #FF8F00);

        &:hover {
          background: linear-gradient(45deg, #FFA000, #FF6F00);
        }
      }
    }
  }
}

.element-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.element-item {
  height: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  cursor: move;
  transition: all 0.3s;
}

.element-item:hover {
  border-color: var(--v-theme-primary);
  background: #f8f9fa;
}

.element-icon {
  margin-bottom: 8px;
}

.element-name {
  font-size: 12px;
  color: #606266;
}

.text-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.text-item {
  padding: 12px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  cursor: move;
  transition: all 0.3s;
}

.text-item:hover {
  border-color: var(--v-theme-primary);
  background: #f8f9fa;
}

.text-preview {
  text-align: center;
}

.loading-state {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 0;
}

.template-category {
  margin-bottom: 24px;
}

.category-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.category-title {
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.category-count {
  font-size: 12px;
  color: #999;
}

.template-grid {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.template-vip {
  position: absolute;
  top: 8px;
  left: 8px;
}

.template-preview {
  position: relative;
}

.filter-section {
  margin-bottom: 16px;
  padding: 12px 0;
  border-bottom: 1px solid #e0e0e0;
}

.category-filter {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
  overflow-x: auto;
  white-space: nowrap;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
  padding-bottom: 4px;
  cursor: grab;
  -webkit-user-select: none;
  user-select: none;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch; /* 在iOS上启用惯性滚动 */
}

.category-filter:active {
  cursor: grabbing;
}

/* 隐藏 Webkit 浏览器的滚动条 */
.category-filter::-webkit-scrollbar {
  display: none;
}

.category-item {
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 14px;
  color: #606266;
  cursor: pointer;
  transition: all 0.3s;
  flex-shrink: 0; /* 防止项目被压缩 */
}

.category-item:hover {
  background: #f5f5f5;
}

.category-item.active {
  color: var(--v-theme-primary);
  background: #ecf5ff;
}

.vip-filter {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 12px;
  border-radius: 6px;
  background: linear-gradient(145deg, #fff9e6, #fff4d4);
  border: 1px solid rgba(255, 213, 79, 0.5);
  box-shadow: 0 2px 4px rgba(255, 213, 79, 0.1);
  gap: 8px;
}

.vip-label {
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #f57c00;
  font-weight: 500;
  white-space: nowrap;
}

.vip-label .v-icon {
  margin-right: 6px;
  filter: drop-shadow(0 1px 2px rgba(245, 124, 0, 0.2));
}

.vip-switch {
  margin: 0;
  margin-left: auto;
}

.vip-switch :deep(.v-switch__track) {
  opacity: 1;
  border: 1px solid rgba(255, 213, 79, 0.8);
  background-color: white !important;
}

.vip-switch :deep(.v-switch__thumb) {
  background-color: #f57c00;
  color: white;
}

.vip-switch :deep(.v-switch--inset .v-switch__track) {
  background-color: rgba(255, 213, 79, 0.1) !important;
}

.vip-switch :deep(.v-switch__thumb .v-icon) {
  font-size: 12px;
}
</style> 