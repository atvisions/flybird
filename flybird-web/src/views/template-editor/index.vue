<template>
  <div class="template-editor">
    <!-- 加载页面 -->
    <LoadingScreen
      v-if="isLoading"
      :template-id="templateId"
      :mode="editorMode"
      @load-complete="(data) => {
        console.log('【index】接收到LoadingScreen事件:', data)
        handleLoadComplete(data)
      }"
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
        @update:template="handleTemplateUpdate"
        @print-preview="handlePrintPreview"
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
              @update-canvas-config="updateCanvasConfig"
            />
          </div>
          <div class="editor-footer">
            <div class="canvas-pages">
              第 {{ currentCanvasId + 1 }} 页 / 共 {{ templateData.canvases.length }} 页
            </div>
            <div class="footer-center">
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
            </div>
            <div class="footer-right">
              <button class="clear-btn" @click="showClearConfirm = true">
                <Clear theme="outline" :size="16" />
              </button>
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

      <!-- 清除确认弹窗 -->
      <TransitionRoot appear :show="showClearConfirm" as="template">
        <Dialog as="div" @close="showClearConfirm = false" class="relative z-50">
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
                    确认清空画布？
                  </DialogTitle>
                  <div class="mt-2">
                    <p class="text-sm text-gray-500">
                      此操作将清空当前画布上的所有内容，且不可恢复。是否继续？
                    </p>
                  </div>

                  <div class="mt-4 flex justify-end space-x-3">
                    <button
                      type="button"
                      class="inline-flex justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none"
                      @click="showClearConfirm = false"
                    >
                      取消
                    </button>
                    <button
                      type="button"
                      class="inline-flex justify-center rounded-md border border-transparent bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700 focus:outline-none"
                      @click="handleConfirmClear"
                    >
                      确认清空
                    </button>
                  </div>
                </DialogPanel>
              </TransitionChild>
            </div>
          </div>
        </Dialog>
      </TransitionRoot>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, computed, watch } from 'vue'
import { Minus, Plus, FullScreen, OffScreen, Clear } from '@icon-park/vue-next'
import { ElMessage } from 'element-plus'
import EditorCanvas from './components/EditorCanvas.vue'
import EditorToolbar from './components/EditorToolbar.vue'
import EditorSidebar from './components/EditorSidebar.vue'
import EditorPanel from './components/EditorPanel.vue'
import LoadingScreen from '@/components/common/LoadingScreen.vue'
import { templateApi } from '@/api/template'
import { showToast } from '@/components/ToastMessage'
import { useRoute, useRouter } from 'vue-router'
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue'
import { mapProfileDataToElements } from '@/utils/dataMapping'

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
  removeCanvas: _removeCanvas,  // 重命名原始的 removeCanvas
  switchCanvas, 
  getCurrentCanvas,
  updateCanvasElements,
  updateCanvasData,
  A4_CONFIG,
  selectedElement,
  handleElementSelect,
  handleElementUpdate,
  handleClear,
  updateCanvasConfig
} = useCanvas()

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
const templateId = computed(() => {
  if (route.name === 'template-create') {
    return null
  }
  return route.params.templateId || route.params.id
})

// 编辑器模式
const editorMode = computed(() => {
  if (route.path.includes('/editor/create')) {
    console.log('【index】编辑器模式: create')
    return 'create'
  }
  if (route.path.includes('/editor/edit')) {
    console.log('【index】编辑器模式: edit')
    return 'edit'
  }
  console.log('【index】编辑器模式: use')
  return 'use'
})

// 保存按钮文本
const saveButtonText = computed(() => {
  switch (editorMode.value) {
    case 'create':
      return '创建模板'
    case 'edit':
      return '保存修改'
    case 'use':
      return '保存简历'
    default:
      return '保存'
  }
})

// 添加画布总数计算属性
const canvasCount = computed(() => templateData.value.canvases.length)

// 在 script setup 中添加
const userProfileData = ref(null)

// 监听路由参数变化
watch(templateId, async (newId) => {
  console.log('【index】templateId变化:', {
    newId,
    routeName: route.name,
    editorMode: editorMode.value,
    isLoading: isLoading.value
  })

  // 如果是创建新模板的路由，不需要加载模板数据
  if (route.name === 'template-create') {
    console.log('【index】创建模式，不加载模板数据')
    isLoading.value = false
    return
  }

  // 如果是use模式，由LoadingScreen组件处理数据加载
  if (editorMode.value === 'use') {
    console.log('【index】使用模式，由LoadingScreen处理数据加载')
    // 确保isLoading为true，这样LoadingScreen组件会显示
    isLoading.value = true
    return
  }

  // 编辑模式下的模板加载
  if (newId && editorMode.value === 'edit') {
    isLoading.value = true
    try {
      console.log('【index】开始加载模板详情:', newId)
      const res = await templateApi.getDetail(newId)
      if (res?.data) {
        console.log('【index】获取模板详情成功:', res.data)
        handleEditTemplate(res.data)
      } else {
        console.warn('【index】获取模板详情失败: 响应数据为空')
        showToast('获取模板详情失败', 'error')
        router.push('/templates/resume')
      }
    } catch (error) {
      console.error('【index】获取模板详情失败:', error)
      showToast('获取模板详情失败', 'error')
      router.push('/templates/resume')
    } finally {
      isLoading.value = false
    }
  }
}, { immediate: true })

// 处理加载完成事件
const handleLoadComplete = async (data) => {
  console.log('【index】handleLoadComplete被调用，参数:', {
    hasTemplateData: !!data.templateData,
    templateDataType: typeof data.templateData,
    hasProfileData: !!data.profileData,
    profileDataType: typeof data.profileData,
    mode: editorMode.value,
    profileDataStructure: data.profileData ? {
      code: data.profileData.code,
      message: data.profileData.message,
      hasData: !!data.profileData.data,
      dataKeys: data.profileData.data ? Object.keys(data.profileData.data) : []
    } : null
  })

  try {
    // 保存用户档案数据
    if (data.profileData?.data) {
      console.log('【index】开始保存用户档案数据:', {
        hasData: true,
        dataKeys: Object.keys(data.profileData.data),
        dataStructure: JSON.stringify(data.profileData.data)
      })
      userProfileData.value = data.profileData.data
      console.log('【index】用户档案数据已保存:', {
        hasData: !!userProfileData.value,
        dataKeys: Object.keys(userProfileData.value),
        dataStructure: JSON.stringify(userProfileData.value)
      })
    }

    // 处理模板数据
    if (data.templateData) {
      console.log('【index】开始处理模板数据:', {
        canvasCount: data.templateData.canvases.length,
        hasCanvases: !!data.templateData.canvases,
        firstCanvasElements: data.templateData.canvases[0]?.elements?.length
      })

      // 数据映射
      if (editorMode.value === 'use' && userProfileData.value) {
        console.log('【index】开始数据映射:', {
          mode: editorMode.value,
          hasUserProfileData: !!userProfileData.value,
          profileDataKeys: Object.keys(userProfileData.value),
          profileDataStructure: JSON.stringify(userProfileData.value)
        })

        // 处理每个画布的元素
        data.templateData.canvases.forEach((canvas, index) => {
          console.log(`【index】处理第${index + 1}页画布:`, {
            elementsCount: canvas.elements.length,
            hasElements: !!canvas.elements,
            elementsWithDataPath: canvas.elements.filter(e => e.dataPath).length
          })

          // 映射数据
          canvas.elements = mapProfileDataToElements(canvas.elements, userProfileData.value)

          console.log(`【index】第${index + 1}页画布处理完成:`, {
            elementsCount: canvas.elements.length,
            hasElements: !!canvas.elements,
            mappedElementsCount: canvas.elements.filter(e => e.content).length
          })
        })
      }

      // 更新模板数据
      templateData.value = data.templateData
      console.log('【index】模板数据更新完成:', {
        canvasCount: templateData.value.canvases.length,
        totalElements: templateData.value.canvases.reduce((sum, canvas) => sum + canvas.elements.length, 0)
      })
    }

    // 等待下一个渲染周期，确保数据已更新到视图
    await nextTick()
    
    // 设置加载状态为false
    isLoading.value = false
    console.log('【index】加载完成，isLoading设置为false')
  } catch (error) {
    console.error('【index】处理数据时出错:', error)
    showToast('加载数据失败', 'error')
    isLoading.value = false
  }
}

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
  console.log('【index】开始处理模板数据:', templateData)
  currentTemplateId.value = templateData.id
  
  try {
    // 构造新的画布数据
    const canvases = templateData.pages.map((page, index) => {
      console.log(`【index】处理第${index + 1}页数据:`, page)
      return {
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

          console.log('【index】处理元素:', baseElement)
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
      }
    })

    console.log('【index】构造的画布数据:', canvases)

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

    console.log('【index】模板数据加载完成:', {
      canvasCount: canvases.length,
      currentCanvasId: currentCanvasId.value,
      defaultTemplateData: defaultTemplateData.value
    })
  } catch (error) {
    console.error('【index】加载模板数据失败:', error)
    showToast('加载模板数据失败', 'error')
  }
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
          ...canvas.config,  // 保留所有原有配置
          width: canvas.config?.width || 794,
          height: canvas.config?.height || 1123,
          showGuideLine: canvas.config?.showGuideLine ?? true,
          backgroundColor: canvas.config?.backgroundColor || '#ffffff',
          showGrid: canvas.config?.showGrid ?? true,  // 修改默认值为 true
          gridSize: canvas.config?.gridSize || 10,
          gridColor: canvas.config?.gridColor || 'rgba(0, 0, 0, 0.15)'
        }
      }
    }))
  }
})

// 添加模板更新处理函数
const handleTemplateUpdate = (updatedTemplate) => {
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

// 重写画布删除方法
const removeCanvas = (canvasId) => {
  const index = templateData.value.canvases.findIndex(canvas => canvas.id === canvasId)
  if (index === -1) return

  // 删除画布
  templateData.value.canvases.splice(index, 1)

  // 重新分配所有画布的ID
  templateData.value.canvases = templateData.value.canvases.map((canvas, idx) => ({
    ...canvas,
    id: idx
  }))

  // 如果删除的是当前画布，切换到前一个画布
  if (canvasId === currentCanvasId.value) {
    currentCanvasId.value = Math.max(0, index - 1)
  } else if (canvasId < currentCanvasId.value) {
    // 如果删除的画布在当前画布之前，当前画布ID需要减1
    currentCanvasId.value--
  }
}

// 修改添加画布的方法
const handleAddCanvas = (newCanvas) => {
  // 使用当前画布数量作为新画布的ID
  const newCanvasId = templateData.value.canvases.length
  const canvas = {
    ...newCanvas,
    id: newCanvasId
  }
  // 添加新画布
  templateData.value.canvases.push(canvas)
  // 立即切换到新画布
  currentCanvasId.value = newCanvasId
}

// 修改切换画布的方法
const handleSwitchCanvas = (canvasId) => {
  if (canvasId >= 0 && canvasId < templateData.value.canvases.length) {
    currentCanvasId.value = canvasId
  }
}

// 清除确认弹窗状态
const showClearConfirm = ref(false)

// 处理确认清除
const handleConfirmClear = () => {
  handleClear()
  showClearConfirm.value = false
}

// 处理保存
const handleSave = async ({ mode, action, data, callback }) => {
  try {
    // 获取所有页面数据
    const pages = templateData.value.canvases.map((canvas, index) => {
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
      name: data?.name || defaultTemplateData.value.name,
      category: data?.category || defaultTemplateData.value.category,
      description: data?.description || defaultTemplateData.value.description || '',
      is_public: data?.is_public ?? defaultTemplateData.value.is_public ?? true,
      keywords: data?.keywords ? (Array.isArray(data.keywords) ? data.keywords : data.keywords.split(',').map(k => k.trim())) : [],
      status: action === 'draft' ? 0 : 2,  // 0: 草稿, 2: 待审核
      pages: pages
    }


    let res
    // 获取当前画布元素
    const canvasWrapper = document.querySelector('.canvas-wrapper')
    // 等待下一个渲染周期，确保画布内容已更新
    await nextTick()

    if (mode === 'edit') {
      res = await templateApi.update(templateId.value, submitData, canvasWrapper)
    } else {
      res = await templateApi.create(submitData, canvasWrapper)
      // 如果创建成功，更新templateId并修改路由
      if (res?.data?.id) {
        templateId.value = res.data.id
        // 使用replace而不是push，这样用户点击返回时不会回到创建页面
        router.replace(`/editor/edit/${res.data.id}`)
      }
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

// 处理打印预览
const handlePrintPreview = () => {
  // 创建一个新窗口用于打印预览
  const printWindow = window.open('', '_blank')
  if (!printWindow) {
    ElMessage.error('打印预览窗口被浏览器拦截，请允许弹出窗口后重试')
    return
  }

  // 获取当前模板的所有页面内容
  const canvasWrappers = document.querySelectorAll('.canvas-wrapper')
  if (!canvasWrappers.length) {
    ElMessage.error('未找到画布内容')
    printWindow.close()
    return
  }

  // 获取所有页面的HTML内容
  const pages = Array.from(canvasWrappers).map((wrapper, index) => {
    // 克隆节点以避免修改原始内容
    const clonedWrapper = wrapper.cloneNode(true)
    
    // 移除不需要打印的元素
    const elementsToRemove = clonedWrapper.querySelectorAll('.element-controls, .element-resize-handle, .element-rotate-handle')
    elementsToRemove.forEach(el => el.remove())

    return `
      <div class="print-page">
        <div class="page-content">
          ${clonedWrapper.innerHTML}
        </div>
      </div>
    `
  }).join('')

  // 构建打印预览页面的HTML
  const printContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>打印预览 - ${currentTemplateData.value?.name || '未命名模板'}</title>
      <style>
        @media print {
          @page {
            size: A4;
            margin: 0;
          }
          body {
            margin: 0;
          }
          .print-page {
            margin: 0 !important;
            box-shadow: none !important;
          }
          .no-print {
            display: none !important;
          }
        }
        
        body {
          margin: 0;
          background: #f0f2f5;
          min-height: 100vh;
        }
        
        .print-header {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          z-index: 1000;
          height: 48px;
          background: white;
          box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 0 24px;
        }
        
        .header-title {
          font-size: 16px;
          color: #333;
          margin: 0;
          font-weight: 500;
        }
        
        .print-btn {
          background: #1890ff;
          color: white;
          border: none;
          padding: 6px 16px;
          border-radius: 4px;
          cursor: pointer;
          font-size: 14px;
          transition: all 0.2s;
        }
        
        .print-btn:hover {
          background: #40a9ff;
        }
        
        .print-container {
          padding-top: 48px;
          display: flex;
          flex-direction: column;
          align-items: center;
          min-height: 100vh;
          box-sizing: border-box;
        }
        
        .print-page {
          width: 210mm;
          min-height: 297mm;
          background: white;
          margin-bottom: 16px;
          position: relative;
          box-sizing: border-box;
        }
        
        .page-content {
          position: relative;
          min-height: 297mm;
        }
        
        /* 保持元素样式 */
        .canvas-element {
          position: absolute !important;
          box-sizing: border-box;
        }
        
        .text-element {
          white-space: pre-wrap;
          word-break: break-word;
        }
        
        .image-element img {
          width: 100%;
          height: 100%;
          object-fit: contain;
        }
      </style>
    </head>
    <body>
      <div class="print-header no-print">
        <h2 class="header-title">${currentTemplateData.value?.name || '未命名模板'} - 打印预览</h2>
        <button class="print-btn" onclick="window.print()">打印文档</button>
      </div>
      <div class="print-container">
        ${pages}
      </div>
    </body>
    </html>
  `

  // 写入打印预览内容
  printWindow.document.open()
  printWindow.document.write(printContent)
  printWindow.document.close()
}


const handleUseTemplate = async (template) => {
  console.log('【index】开始使用模板:', template)
  
  try {
    // 只需要更新当前模板ID并跳转到use模式
    templateId.value = template.id
    
    // 跳转到use模式，LoadingScreen组件会自动处理数据加载
    await router.push(`/editor/use/${template.id}`)
    
    console.log('【index】已跳转到use模式，等待LoadingScreen加载数据')
    
  } catch (error) {
    console.error('【index】跳转失败:', error)
    showToast('使用模板失败', 'error')
  }
}

const handleElementAdd = (element) => {
  // 处理添加元素的逻辑
  console.log('添加元素:', element)
  if (canvasRef.value) {
    canvasRef.value.addElement(element)
  }
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
  font-weight: 500;
  flex: 1;
}

.footer-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.footer-right {
  flex: 1;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.zoom-control {
  display: inline-flex;
  align-items: center;
  gap: 8px;
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
  transition: all 0.2s;
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

.clear-btn,
.fullscreen-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  color: #666;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 6px;
}

.clear-btn:hover {
  color: #ff4d4f;
  background: rgba(255, 77, 79, 0.1);
}

.clear-btn:active {
  background: rgba(255, 77, 79, 0.2);
}

.fullscreen-btn:hover {
  color: #1890ff;
  background: rgba(24, 144, 255, 0.1);
}

.fullscreen-btn:active {
  background: rgba(24, 144, 255, 0.2);
}
</style> 