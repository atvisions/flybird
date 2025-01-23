<template>
  <div class="template-editor">
    <!-- 加载页面 -->
    <LoadingScreen
      v-if="isLoading"
      :template-id="templateId"
      :mode="currentTemplateId ? 'edit' : 'use'"
      @load-complete="handleLoadComplete"
    />

    <!-- 编辑器内容 -->
    <template v-else>
      <!-- 顶部工具栏 -->
      <EditorToolbar
        :can-undo="canUndo"
        :can-redo="canRedo"
        :scale="scale"
        :button-text="saveButtonText"
        :current-template="currentTemplateData"
        @clear="handleClear"
        @save="handleSave"
        @undo="handleUndo"
        @redo="handleRedo"
        @scale-change="handleScaleChange"
        @update:template="handleTemplateUpdate"
      />

      <!-- 主要内容区域 -->
      <div class="editor-content">
        <!-- 左侧面板 -->
        <EditorSidebar 
          ref="sidebarRef"
          @edit-template="handleEditTemplate"
          @use-template="handleUseTemplate"
        />

        <!-- 中间画布区域 -->
        <div class="editor-main">
          <div class="canvas-container">
            <EditorCanvas
              ref="canvasRef"
              :scale="scale"
              :elements="getCurrentCanvas()?.elements || []"
              :canvas-list="templateData.canvases"
              :current-canvas-id="currentCanvasId"
              :canvas-config="getCurrentCanvas()?.config"
              :selected-element="selectedElement"
              :selected-elements="selectedElements"
              @element-select="handleElementSelect"
              @elements-change="updateCanvasElements"
              @delete-canvas="removeCanvas"
              @element-add="handleElementAdd"
              @selected-elements-change="handleSelectedElementsChange"
              @update:canUndo="canUndo = $event"
              @update:canRedo="canRedo = $event"
            />
          </div>
          <div class="editor-footer">
            <span class="canvas-pages">Page {{ currentCanvasId }}/{{ templateData.canvases.length }}</span>
            <div class="footer-content">
              <div class="zoom-control">
                <button class="zoom-btn" @click="handleZoomOut" :disabled="scale <= MIN_SCALE">
                  <Minus theme="outline" :size="16" />
                </button>
                <div class="zoom-slider">
                  <div class="zoom-track" @mousedown="handleTrackClick">
                    <div class="zoom-progress" :style="{ width: `${((scale - MIN_SCALE) / (MAX_SCALE - MIN_SCALE)) * 100}%` }"></div>
                    <div class="zoom-ticks">
                      <div class="zoom-tick" style="left: 0%"></div>
                      <div class="zoom-tick" style="left: 25%"></div>
                      <div class="zoom-tick zoom-tick-100" style="left: 50%"></div>
                      <div class="zoom-tick" style="left: 75%"></div>
                      <div class="zoom-tick" style="left: 100%"></div>
                    </div>
                    <div 
                      class="zoom-handle" 
                      :style="{ left: `${((scale - MIN_SCALE) / (MAX_SCALE - MIN_SCALE)) * 100}%` }"
                      @mousedown.stop="startDrag"
                    >
                      <div class="zoom-tooltip">{{ Math.round(scale * 100) }}%</div>
                    </div>
                  </div>
                </div>
                <button class="zoom-btn" @click="handleZoomIn" :disabled="scale >= MAX_SCALE">
                  <Plus theme="outline" :size="16" />
                </button>
              </div>
              <button class="fullscreen-btn" @click="toggleFullscreen" :title="isFullscreen ? '退出全屏' : '全屏'">
                <FullScreen v-if="!isFullscreen" theme="outline" :size="18" />
                <OffScreen v-else theme="outline" :size="18" />
              </button>
            </div>
          </div>
        </div>

        <!-- 右侧属性面板 -->
        <EditorPanel
          :element="selectedElement"
          :canvas-list="templateData.canvases"
          :current-canvas-id="currentCanvasId"
          :canvas-config="getCurrentCanvas()?.config"
          :selected-elements="selectedElements"
          @update="handleElementUpdate"
          @element-select="handleElementSelect"
          @add-canvas="handleAddCanvas"
          @delete-canvas="removeCanvas"
          @switch-canvas="handleSwitchCanvas"
          @update-canvas-config="updateCanvasConfig"
          @align-horizontal-to-canvas="handleAlignHorizontalToCanvas"
          @align-vertical-to-canvas="handleAlignVerticalToCanvas"
          @align-left="handleAlignLeft"
          @align-horizontal-center="handleAlignHorizontalCenter"
          @align-right="handleAlignRight"
          @align-top="handleAlignTop"
          @align-vertical-center="handleAlignVerticalCenter"
          @align-bottom="handleAlignBottom"
          @align-elements="handleAlignElements"
          @distribute-elements="handleDistributeElements"
          @spacing-change="handleSpacingChange"
        />
      </div>

      <!-- 保存模板对话框 -->
      <SaveTemplateDialog
        v-if="showSaveDialog"
        :visible="showSaveDialog"
        :default-data="defaultTemplateData"
        :is-edit="!!currentTemplateId"
        @update:visible="showSaveDialog = $event"
        @save="handleSaveTemplate"
      />
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, computed, watch } from 'vue'
import { Minus, Plus, FullScreen, OffScreen } from '@icon-park/vue-next'
import { ElMessage } from 'element-plus'
import EditorCanvas from './components/EditorCanvas.vue'
import EditorToolbar from './components/EditorToolbar.vue'
import EditorSidebar from './components/EditorSidebar.vue'
import EditorPanel from './components/EditorPanel.vue'
import SaveTemplateDialog from './components/SaveTemplateDialog.vue'
import LoadingScreen from '@/components/common/LoadingScreen.vue'
import { templateApi } from '@/api/template'
import { showToast } from '@/components/ToastMessage'
import { useRoute, useRouter } from 'vue-router'

// 导入组合式函数
import { useZoom } from './composables/useZoom'
import { useCanvas } from './composables/useCanvas'
import { useCanvasConfig } from './composables/useCanvasConfig'
import { useTabs } from './composables/useTabs'

// 导入 profile store
import { useProfileStore } from '@/stores/profile'

// 获取默认画布配置
const { canvasConfig: DEFAULT_CANVAS_CONFIG } = useCanvasConfig()

// 使用useTabs
const { switchTab } = useTabs()

// 画布引用
const canvasRef = ref(null)

// 添加 sidebarRef
const sidebarRef = ref(null)

// 使用组合式函数
const { scale, MIN_SCALE, MAX_SCALE, SCALE_STEP, handleZoomIn, handleZoomOut, handleZoomChange } = useZoom()
const { 
  templateData,
  currentCanvasId, 
  addCanvas, 
  removeCanvas, 
  switchCanvas, 
  getCurrentCanvas,
  updateCanvasElements,
  updateCanvasConfig,
  updateCanvasData,
  A4_CONFIG,
  selectedElement,
  handleElementSelect,
  handleElementUpdate,
  handleClear
} = useCanvas()

const { canvasConfig } = useCanvasConfig()

// 添加路由实例
const route = useRoute()
const router = useRouter()

// 添加默认模板数据
const defaultTemplateData = ref({
  name: '',
  description: '',
  category: '',
  keywords: '',
  is_public: true,
  status: 0
})

// 添加加载状态
const isLoading = ref(true)
const templateId = computed(() => route.params.templateId || route.params.id)

// 处理加载完成
const handleLoadComplete = ({ success, templateData, error }) => {
  if (success && templateData) {
    handleEditTemplate(templateData)
  } else {
    showToast(error || '加载失败', 'error')
    router.push('/resume/templates')
  }
  isLoading.value = false
}

// 监听路由参数变化
watch(templateId, async (newId) => {
  if (newId) {
    isLoading.value = true
    try {
      const res = await templateApi.getDetail(newId)
      if (res?.data) {
        handleEditTemplate(res.data)
      } else {
        showToast('获取模板详情失败', 'error')
        router.push('/resume/templates')
      }
    } catch (error) {
      console.error('获取模板详情失败:', error)
      showToast('获取模板详情失败', 'error')
      router.push('/resume/templates')
    } finally {
      isLoading.value = false
    }
  }
}, { immediate: true })

const handleTrackClick = (e) => {
  if (e.target.classList.contains('zoom-handle')) return
  
  const slider = e.currentTarget.closest('.zoom-slider')
  const sliderRect = slider.getBoundingClientRect()
  const sliderWidth = sliderRect.width - 20
  const left = Math.max(0, Math.min(sliderWidth, e.clientX - sliderRect.left - 10))
  const percentage = left / sliderWidth
  const newScale = MIN_SCALE + percentage * (MAX_SCALE - MIN_SCALE)
  handleZoomChange(Number(newScale.toFixed(2)))
}

const startDrag = (e) => {
  e.preventDefault()
  
  const handle = e.target
  const slider = handle.closest('.zoom-slider')
  const sliderRect = slider.getBoundingClientRect()
  const sliderWidth = sliderRect.width - 20  // 减去左右padding
  
  const updatePosition = (clientX) => {
    const left = Math.max(0, Math.min(sliderWidth, clientX - sliderRect.left - 10))  // 10是左padding
    const percentage = left / sliderWidth
    const newScale = MIN_SCALE + percentage * (MAX_SCALE - MIN_SCALE)
    handleZoomChange(Number(newScale.toFixed(2)))
  }
  
  const handleDrag = (e) => {
    e.preventDefault()
    updatePosition(e.clientX)
  }
  
  const stopDrag = () => {
    document.removeEventListener('mousemove', handleDrag)
    document.removeEventListener('mouseup', stopDrag)
    document.body.style.cursor = ''
    document.body.style.userSelect = ''
  }
  
  document.body.style.cursor = 'grabbing'
  document.body.style.userSelect = 'none'
  
  document.addEventListener('mousemove', handleDrag)
  document.addEventListener('mouseup', stopDrag)
}

// 全屏状态
const isFullscreen = ref(false)

// 切换全屏
const toggleFullscreen = () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen()
    isFullscreen.value = true
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen()
      isFullscreen.value = false
    }
  }
}

// 监听全屏变化
onMounted(() => {
  document.addEventListener('fullscreenchange', () => {
    isFullscreen.value = !!document.fullscreenElement
  })
})

onUnmounted(() => {
  document.removeEventListener('fullscreenchange', () => {
    isFullscreen.value = !!document.fullscreenElement
  })
})

// 处理元素更新
const handleElementsChange = (newElements) => {
  // Implementation needed
}

// 处理撤销
const handleUndo = () => {
  canvasRef.value?.handleUndo()
}

// 处理重做
const handleRedo = () => {
  canvasRef.value?.handleRedo()
}

// 添加对齐方法
const handleAlignHorizontalToCanvas = () => {
  canvasRef.value?.alignHorizontalToCanvas()
}

const handleAlignVerticalToCanvas = () => {
  canvasRef.value?.alignVerticalToCanvas()
}

const handleAlignLeft = () => {
  canvasRef.value?.alignLeft()
}

const handleAlignHorizontalCenter = () => {
  canvasRef.value?.alignHorizontalCenter()
}

const handleAlignRight = () => {
  canvasRef.value?.alignRight()
}

const handleAlignTop = () => {
  canvasRef.value?.alignTop()
}

const handleAlignVerticalCenter = () => {
  canvasRef.value?.alignVerticalCenter()
}

const handleAlignBottom = () => {
  canvasRef.value?.alignBottom()
}

// 添加多选状态
const selectedElements = ref([])

// 添加多选状态处理函数
const handleSelectedElementsChange = (elements) => {
  // 获取画布中最新的元素位置信息
  const canvas = getCurrentCanvas()
  if (!canvas) {
    selectedElements.value = elements
    return
  }
  
  // 根据传入的elements id获取画布中最新的元素信息
  const updatedElements = elements.map(el => {
    const latest = canvas.elements.find(canvasEl => canvasEl.id === el.id)
    return latest || el
  })
  
  selectedElements.value = updatedElements
}

// 对齐元素处理函数
const handleAlignElements = ({ elements, direction }) => {
  if (!elements || elements.length < 2) return
  
  // 获取画布中最新的元素位置信息
  const canvas = getCurrentCanvas()
  if (!canvas) return
  
  // 根据传入的elements id获取画布中最新的元素信息
  const elementsToAlign = elements.map(el => {
    const latest = canvas.elements.find(canvasEl => canvasEl.id === el.id)
    return latest || el
  })
  
  // 计算对齐位置
  let alignValue
  switch (direction) {
    case 'left': {
      alignValue = Math.min(...elementsToAlign.map(el => el.x))
      const newElements = [...canvas.elements]
      elementsToAlign.forEach(element => {
        const index = newElements.findIndex(el => el.id === element.id)
        if (index !== -1) {
          newElements[index] = {
            ...newElements[index],
            x: alignValue
          }
        }
      })
      updateCanvasElements(newElements)
      // 更新选中元素状态
      handleSelectedElementsChange(elementsToAlign.map(el => ({
        ...el,
        x: alignValue
      })))
      break
    }
    case 'center': {
      const leftmost = Math.min(...elementsToAlign.map(el => el.x))
      const rightmost = Math.max(...elementsToAlign.map(el => el.x + el.width))
      const centerX = leftmost + (rightmost - leftmost) / 2
      const newElements = [...canvas.elements]
      const updatedElements = []
      elementsToAlign.forEach(element => {
        const index = newElements.findIndex(el => el.id === element.id)
        if (index !== -1) {
          const newX = Math.round(centerX - element.width / 2)
          newElements[index] = {
            ...newElements[index],
            x: newX
          }
          updatedElements.push({
            ...element,
            x: newX
          })
        }
      })
      updateCanvasElements(newElements)
      // 更新选中元素状态
      handleSelectedElementsChange(updatedElements)
      break
    }
    case 'right': {
      const rightmost = Math.max(...elementsToAlign.map(el => el.x + el.width))
      const newElements = [...canvas.elements]
      const updatedElements = []
      elementsToAlign.forEach(element => {
        const index = newElements.findIndex(el => el.id === element.id)
        if (index !== -1) {
          const newX = Math.round(rightmost - element.width)
          newElements[index] = {
            ...newElements[index],
            x: newX
          }
          updatedElements.push({
            ...element,
            x: newX
          })
        }
      })
      updateCanvasElements(newElements)
      // 更新选中元素状态
      handleSelectedElementsChange(updatedElements)
      break
    }
    case 'top': {
      alignValue = Math.min(...elementsToAlign.map(el => el.y))
      const newElements = [...canvas.elements]
      const updatedElements = []
      elementsToAlign.forEach(element => {
        const index = newElements.findIndex(el => el.id === element.id)
        if (index !== -1) {
          newElements[index] = {
            ...newElements[index],
            y: alignValue
          }
          updatedElements.push({
            ...element,
            y: alignValue
          })
        }
      })
      updateCanvasElements(newElements)
      // 更新选中元素状态
      handleSelectedElementsChange(updatedElements)
      break
    }
    case 'middle': {
      const topmost = Math.min(...elementsToAlign.map(el => el.y))
      const bottommost = Math.max(...elementsToAlign.map(el => el.y + el.height))
      const centerY = topmost + (bottommost - topmost) / 2
      const newElements = [...canvas.elements]
      const updatedElements = []
      elementsToAlign.forEach(element => {
        const index = newElements.findIndex(el => el.id === element.id)
        if (index !== -1) {
          const newY = Math.round(centerY - element.height / 2)
          newElements[index] = {
            ...newElements[index],
            y: newY
          }
          updatedElements.push({
            ...element,
            y: newY
          })
        }
      })
      updateCanvasElements(newElements)
      // 更新选中元素状态
      handleSelectedElementsChange(updatedElements)
      break
    }
    case 'bottom': {
      const bottommost = Math.max(...elementsToAlign.map(el => el.y + el.height))
      const newElements = [...canvas.elements]
      const updatedElements = []
      elementsToAlign.forEach(element => {
        const index = newElements.findIndex(el => el.id === element.id)
        if (index !== -1) {
          const newY = Math.round(bottommost - element.height)
          newElements[index] = {
            ...newElements[index],
            y: newY
          }
          updatedElements.push({
            ...element,
            y: newY
          })
        }
      })
      updateCanvasElements(newElements)
      // 更新选中元素状态
      handleSelectedElementsChange(updatedElements)
      break
    }
  }
}

// 分布元素处理函数
const handleDistributeElements = ({ elements, direction }) => {
  if (elements.length < 3) return
  
  // 获取画布中最新的元素位置信息
  const canvas = getCurrentCanvas()
  if (!canvas) return
  
  // 根据传入的elements id获取画布中最新的元素信息
  const latestElements = elements.map(el => {
    const latest = canvas.elements.find(canvasEl => canvasEl.id === el.id)
    return latest || el
  })
  
  const sortedElements = [...latestElements]
  const newElements = [...canvas.elements]
  const updatedElements = []
  
  if (direction === 'horizontal') {
    // 水平分布时，保持y值不变
    sortedElements.sort((a, b) => a.x - b.x)
    const firstElement = sortedElements[0]
    const lastElement = sortedElements[sortedElements.length - 1]
    
    // 计算总的水平空间（从第一个元素的左边到最后一个元素的右边）
    const totalSpace = (lastElement.x + lastElement.width) - firstElement.x
    // 计算所有元素的总宽度
    const totalWidth = sortedElements.reduce((sum, el) => sum + el.width, 0)
    // 计算需要分配的间隙总量
    const totalGap = totalSpace - totalWidth
    // 计算每个间隙的大小
    const gap = totalGap / (sortedElements.length - 1)
    
    let currentX = firstElement.x
    sortedElements.forEach((element, index) => {
      if (index === 0) {
        currentX += element.width
        updatedElements.push(element)
        return
      }
      if (index === sortedElements.length - 1) {
        updatedElements.push(element)
        return
      }
      
      const newX = Math.round(currentX + gap)
      const elementIndex = newElements.findIndex(el => el.id === element.id)
      if (elementIndex !== -1) {
        newElements[elementIndex] = {
          ...newElements[elementIndex],
          x: newX
        }
        updatedElements.push({
          ...element,
          x: newX
        })
      }
      currentX = newX + element.width
    })
    updateCanvasElements(newElements)
    // 更新选中元素状态
    handleSelectedElementsChange(updatedElements)
  } else {
    // 垂直分布时，保持x值不变
    sortedElements.sort((a, b) => a.y - b.y)
    const firstElement = sortedElements[0]
    const lastElement = sortedElements[sortedElements.length - 1]
    
    // 计算总的垂直空间（从第一个元素的顶部到最后一个元素的底部）
    const totalSpace = (lastElement.y + lastElement.height) - firstElement.y
    // 计算所有元素的总高度
    const totalHeight = sortedElements.reduce((sum, el) => sum + el.height, 0)
    // 计算需要分配的间隙总量
    const totalGap = totalSpace - totalHeight
    // 计算每个间隙的大小
    const gap = totalGap / (sortedElements.length - 1)
    
    let currentY = firstElement.y
    sortedElements.forEach((element, index) => {
      if (index === 0) {
        currentY += element.height
        updatedElements.push(element)
        return
      }
      if (index === sortedElements.length - 1) {
        updatedElements.push(element)
        return
      }
      
      const newY = Math.round(currentY + gap)
      const elementIndex = newElements.findIndex(el => el.id === element.id)
      if (elementIndex !== -1) {
        newElements[elementIndex] = {
          ...newElements[elementIndex],
          y: newY
        }
        updatedElements.push({
          ...element,
          y: newY
        })
      }
      currentY = newY + element.height
    })
    updateCanvasElements(newElements)
    // 更新选中元素状态
    handleSelectedElementsChange(updatedElements)
  }
}

// 间距调整处理函数
const handleSpacingChange = ({ elements, spacing }) => {
  if (elements.length < 2) return
  
  const sortedElements = [...elements]
  
  // 默认按水平方向调整间距
  sortedElements.sort((a, b) => a.x - b.x)
  
  sortedElements.forEach((element, index) => {
    if (index === 0) return
    
    updateElement({
      ...element,
      x: Math.round(sortedElements[index - 1].x + sortedElements[index - 1].width + spacing)
    })
  })
}

// 更新单个元素
const updateElement = (updatedElement) => {
  const canvas = getCurrentCanvas()
  if (!canvas) return

  const elementIndex = canvas.elements.findIndex(el => el.id === updatedElement.id)
  if (elementIndex === -1) return

  // 获取当前画布中的最新元素状态
  const currentElement = canvas.elements[elementIndex]
  
  // 创建新的元素，只更新传入的属性
  const newElement = {
    ...currentElement  // 保留所有当前状态
  }

  // 只更新传入的属性
  Object.keys(updatedElement).forEach(key => {
    if (key !== 'id') {
      newElement[key] = updatedElement[key]
    }
  })

  const newElements = [...canvas.elements]
  newElements[elementIndex] = newElement
  
  // 更新画布元素
  updateCanvasElements(newElements)
}

// 添加撤销重做状态
const canUndo = ref(false)
const canRedo = ref(false)

// 保存相关状态和方法
const showSaveDialog = ref(false)

const getCurrentElements = () => {
  const currentCanvas = getCurrentCanvas()
  return currentCanvas?.elements || []
}

const getCurrentConfig = () => {
  const currentCanvas = getCurrentCanvas()
  return currentCanvas?.config || {
    width: 794,
    height: 1123,
    showGuideLine: true
  }
}

// 添加 currentTemplateId ref
const currentTemplateId = ref(null)

// 修改 handleEditTemplate 方法
const handleEditTemplate = async (templateData) => {
  currentTemplateId.value = templateData.id
  console.log('开始编辑模板:', templateData)
  
  try {
    // 构造新的画布数据
    const canvases = templateData.pages.map((page, index) => ({
      id: index,
      elements: page.page_data.elements.map(element => {
        // 先提取基本属性
        const baseElement = {
          id: element.id || `element-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
          type: element.type || 'text',
          x: element.position?.x || 0,
          y: element.position?.y || 0,
          width: element.width || 100,
          height: element.height || 100,
          content: element.content || '',
          style: element.style || {},
          props: element.props || {},
          // 添加可拖拽相关的属性
          draggable: true,
          resizable: true,
          rotatable: true,
          lockAspectRatio: false,
          selected: false,
          zIndex: element.zIndex || 1,
          // 添加变换相关的属性
          transform: element.transform || {
            rotate: 0,
            scaleX: 1,
            scaleY: 1
          }
        }

        // 根据元素类型添加特定属性
        if (element.type === 'text') {
          baseElement.editable = true
        }

        return baseElement
      }),
      config: {
        width: DEFAULT_CANVAS_CONFIG.width,
        height: DEFAULT_CANVAS_CONFIG.height,
        backgroundColor: '#ffffff',
        showGrid: false,
        showGuideLine: true,
        ...(page.page_data.config || {})
      }
    }))

    // 更新画布数据
    updateCanvasData(canvases)

    // 设置当前画板为第一个
    currentCanvasId.value = 0

    // 保存模板的基本信息
    defaultTemplateData.value = {
      name: templateData.name || '',
      description: templateData.description || '',
      category: templateData.category || '',
      keywords: Array.isArray(templateData.keywords) ? templateData.keywords.join(',') : '',
      is_public: templateData.is_public ?? true
    }

    console.log('设置的默认模板数据:', defaultTemplateData.value)
    console.log('更新后的画布数据:', canvases)
  } catch (error) {
    console.error('编辑模板失败:', error)
    showToast('加载模板数据失败', 'error')
  }
}

// 修改工具栏按钮的文本
const saveButtonText = computed(() => {
  return currentTemplateId.value ? '保存模板' : '创建模板'
})

const handleSave = async ({ mode, action, data, callback }) => {
  try {
    // 获取所有页面数据
    const pages = templateData.value.canvases.map((canvas, index) => {
      console.log(`处理画布 ${index}:`, canvas)
      return {
        page_index: index,
        page_data: {
          elements: canvas.elements.map(element => ({
            type: element.type || 'text',
            position: {
              x: element.x || 0,
              y: element.y || 0
            },
            style: element.style || {},
            content: element.content || '',
            props: element.props || {},
            width: element.width || 100,
            height: element.height || 100
          })),
          config: {
            width: canvas.config?.width || 794,
            height: canvas.config?.height || 1123,
            backgroundColor: canvas.config?.backgroundColor || '#ffffff',
            showGrid: canvas.config?.showGrid || false,
            showGuideLine: canvas.config?.showGuideLine !== false,
            scale: canvas.config?.scale || 1
          }
        }
      }
    })

    // 准备提交的模板数据
    const submitData = {
      name: data.name,
      category: data.category,
      description: data.description || '',
      is_public: data.is_public ?? true,
      keywords: data.keywords ? (Array.isArray(data.keywords) ? data.keywords : data.keywords.split(',').map(k => k.trim())) : [],
      status: action === 'draft' ? 0 : 2,  // 0: 草稿, 2: 待审核
      pages: pages  // 直接提交 pages 数组，不需要包装在 content 对象中
    }

    console.log('准备提交的模板数据:', submitData)

    let res
    if (currentTemplateId.value) {
      console.log('更新模板:', currentTemplateId.value)
      // 获取当前画布元素
      const canvasWrapper = document.querySelector('.canvas-wrapper')
      // 等待下一个渲染周期，确保画布内容已更新
      await nextTick()
      res = await templateApi.update(currentTemplateId.value, submitData, canvasWrapper)
    } else {
      console.log('创建新模板')
      // 获取当前画布元素
      const canvasWrapper = document.querySelector('.canvas-wrapper')
      // 等待下一个渲染周期，确保画布内容已更新
      await nextTick()
      res = await templateApi.create(submitData, canvasWrapper)
    }

    if (callback) {
      callback(true)
    }

    showToast(action === 'draft' ? '保存草稿成功' : '提交审核成功', 'success')
    return res
  } catch (error) {
    console.error('保存模板失败:', error)
    if (callback) {
      callback(false)
    }
    showToast(error.response?.data?.message || error.message || '保存失败', 'error')
    throw error
  }
}

// 处理使用模板
const handleUseTemplate = async (templateData) => {
  try {
    isLoading.value = true  // 在开始加载时显示 LoadingScreen
    
    // 获取用户档案数据
    const profileStore = useProfileStore()
    if (!profileStore.profileData) {
      await profileStore.loadProfileData()
    }

    // 将 Proxy 对象转换为普通对象
    const profileData = JSON.parse(JSON.stringify(profileStore.profileData))
    console.log('转换后的用户档案数据:', profileData)

    // 预加载样式
    await new Promise(resolve => {
      const styleSheets = Array.from(document.styleSheets)
      const promises = styleSheets.map(sheet => {
        if (sheet.href) {
          return new Promise((resolve) => {
            const link = document.createElement('link')
            link.rel = 'stylesheet'
            link.href = sheet.href
            link.onload = resolve
            document.head.appendChild(link)
          })
        }
        return Promise.resolve()
      })
      Promise.all(promises).then(resolve)
    })

    // 构造新的画布数据
    const canvases = templateData.pages.map((page, index) => {
      // 处理每个元素，替换档案数据
      const elements = page.page_data.elements.map(element => {
        // 如果是简历字段组件，需要处理数据绑定
        if (element.type === 'resume-field') {
          const { dataPath } = element.props
          if (dataPath) {
            try {
              // 从档案数据中获取对应的值
              const pathParts = dataPath.split('.')
              let value = profileData
              
              // 遍历路径获取嵌套值
              for (const part of pathParts) {
                if (value && typeof value === 'object' && part in value) {
                  value = value[part]
                } else {
                  console.warn(`找不到数据路径: ${dataPath}`)
                  value = ''
                  break
                }
              }

              // 确保值是字符串类型
              value = value?.toString() || ''
              console.log(`设置字段 ${dataPath} 的值:`, value)

              // 更新元素的值
              return {
                ...element,
                props: {
                  ...element.props,
                  value: value
                }
              }
            } catch (error) {
              console.error(`处理数据路径 ${dataPath} 时出错:`, error)
              return element
            }
          }
        }
        return element
      })

      return {
        id: index,
        elements,
        config: {
          width: DEFAULT_CANVAS_CONFIG.width,
          height: DEFAULT_CANVAS_CONFIG.height,
          backgroundColor: '#ffffff',
          showGrid: false,
          showGuideLine: true,
          ...(page.page_data.config || {})
        }
      }
    })

    // 等待下一个渲染周期，确保 DOM 更新完成
    await nextTick()

    // 更新画布数据
    updateCanvasData(canvases)

    // 设置当前画板为第一个
    currentCanvasId.value = 0

    // 清除当前模板ID，表示这是一个新实例
    currentTemplateId.value = null

    // 设置默认的模板数据
    defaultTemplateData.value = {
      name: `${templateData.name} 的副本`,
      description: templateData.description || '',
      category: templateData.category || '',
      keywords: Array.isArray(templateData.keywords) ? templateData.keywords.join(',') : '',
      is_public: templateData.is_public ?? true
    }

    console.log('使用模板，更新后的画布数据:', canvases)

    // 给样式加载一个短暂的延迟，确保所有样式都已应用
    await new Promise(resolve => setTimeout(resolve, 100))
    
    isLoading.value = false  // 所有数据和样式都准备好后再隐藏 LoadingScreen
  } catch (error) {
    console.error('使用模板失败:', error)
    showToast('加载模板数据失败', 'error')
    isLoading.value = false
  }
}

// 处理缩放变化
const handleScaleChange = (newScale) => {
  scale.value = newScale
}

// 处理元素添加
const handleElementAdd = (element) => {
  if (!element) return
  
  // 更新元素列表
  const updatedElements = [...templateData.value.canvases[currentCanvasId.value - 1].page_data.elements, element]
  templateData.value.canvases[currentCanvasId.value - 1].page_data.elements = updatedElements
  
  // 触发更新事件
  emit('elements-change', updatedElements)
  
  // 保存到历史记录
  pushState(updatedElements)
}

// 计算当前模板数据
const currentTemplateData = computed(() => {
  const currentCanvas = getCurrentCanvas()
  if (!currentCanvas) return null

  return {
    id: currentTemplateId.value,
    name: defaultTemplateData.value.name,
    category: defaultTemplateData.value.category,
    description: defaultTemplateData.value.description,
    is_public: defaultTemplateData.value.is_public,
    keywords: defaultTemplateData.value.keywords ? defaultTemplateData.value.keywords.split(',').filter(Boolean) : [],
    status: defaultTemplateData.value.status || 0,
    pages: templateData.value.canvases.map((canvas, index) => ({
      page_index: index,
      page_data: {
        elements: canvas.elements || [],
        config: {
          width: canvas.config?.width || 794,
          height: canvas.config?.height || 1123,
          showGuideLine: canvas.config?.showGuideLine !== false,
          backgroundColor: canvas.config?.backgroundColor || '#ffffff',
          showGrid: canvas.config?.showGrid || false
        }
      }
    }))
  }
})

// 添加模板更新处理函数
const handleTemplateUpdate = (updatedTemplate) => {
  console.log('更新模板数据:', updatedTemplate)
  // 更新默认模板数据
  defaultTemplateData.value = {
    name: updatedTemplate.name,
    description: updatedTemplate.description,
    category: updatedTemplate.category,
    keywords: Array.isArray(updatedTemplate.keywords) ? updatedTemplate.keywords.join(',') : '',
    is_public: updatedTemplate.is_public,
    status: updatedTemplate.status
  }
}

// 添加画布
const handleAddCanvas = (newCanvas) => {
  // 添加新画布
  templateData.value.canvases.push(newCanvas)
  // 立即切换到新画布
  currentCanvasId.value = newCanvas.id
}

// 切换画布
const handleSwitchCanvas = (canvasId) => {
  currentCanvasId.value = canvasId
}
</script>

<style>
/* 添加全局过渡效果 */
.template-editor {
  opacity: 1;
  transition: opacity 0.3s ease-in-out;
}

.template-editor.loading {
  opacity: 0;
}

/* 为画布元素添加过渡效果 */
.canvas-container {
  opacity: 1;
  transition: all 0.3s ease-in-out;
}

.canvas-container.loading {
  opacity: 0;
}

/* 为元素添加过渡效果 */
.canvas-element {
  transition: all 0.2s ease-in-out;
}

/* 确保所有样式在加载时都有过渡效果 */
.editor-content * {
  transition: background-color 0.2s ease-in-out,
              border-color 0.2s ease-in-out,
              box-shadow 0.2s ease-in-out;
}

@import './styles/editor.css';
@import './styles/drag.css';
</style>

<style scoped>
@import './styles/editor.css';

.editor-footer {
  padding: 8px 24px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  display: flex;
  align-items: center;
  background: #fff;
  box-shadow: 0 -1px 2px rgba(0, 0, 0, 0.02);
}

.canvas-pages {
  font-size: 13px;
  color: #666;
  margin-right: auto;
  font-weight: 500;
}

.footer-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.zoom-control {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(to bottom, #fafafa, #f5f5f5);
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 8px;
  padding: 4px;
  box-shadow: 
    0 1px 2px rgba(0, 0, 0, 0.04),
    inset 0 1px 1px rgba(255, 255, 255, 0.9);
}

.zoom-slider {
  width: 140px;
  height: 28px;
  position: relative;
  display: flex;
  align-items: center;
  padding: 0 10px;
}

.zoom-track {
  width: 100%;
  height: 4px;
  background: #e8e8e8;
  border-radius: 2px;
  position: relative;
}

.zoom-progress {
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  background: #1890ff;
  border-radius: 2px;
}

.zoom-handle {
  position: absolute;
  top: 50%;
  width: 16px;
  height: 16px;
  margin-top: -8px;
  margin-left: -8px;
  background: white;
  border: 2px solid #1890ff;
  border-radius: 50%;
  cursor: grab;
  transition: transform 0.2s;
  z-index: 10;
}

.zoom-handle:hover {
  transform: scale(1.1);
}

.zoom-handle:active {
  cursor: grabbing;
  transform: scale(1.1);
}

.zoom-ticks {
  position: absolute;
  left: 0;
  right: 0;
  top: 50%;
  margin-top: -3px;
  height: 6px;
  pointer-events: none;
}

.zoom-tick {
  position: absolute;
  width: 2px;
  height: 6px;
  background: #e8e8e8;
  margin-left: -1px;
}

.zoom-tick-100 {
  height: 8px;
  margin-top: -1px;
  background: #d9d9d9;
}

.zoom-tooltip {
  position: absolute;
  top: -25px;
  left: 50%;
  transform: translateX(-50%);
  background: #1890ff;
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
  white-space: nowrap;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.2s;
}

.zoom-handle:hover .zoom-tooltip {
  opacity: 1;
}

.zoom-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: none;
  background: transparent;
  color: #666;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 6px;
}

.zoom-btn:hover:not(:disabled) {
  color: #1890ff;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 
    0 2px 6px rgba(24, 144, 255, 0.1),
    inset 0 1px 1px rgba(255, 255, 255, 1);
}

.zoom-btn:active:not(:disabled) {
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 
    0 1px 2px rgba(24, 144, 255, 0.1),
    inset 0 1px 1px rgba(255, 255, 255, 1);
}

.zoom-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.fullscreen-btn {
  position: absolute;
  right: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
  border-radius: 6px;
}

.fullscreen-btn:hover {
  color: #1890ff;
  background: rgba(24, 144, 255, 0.1);
}

.fullscreen-btn:active {
  background: rgba(24, 144, 255, 0.2);
}
</style> 