<template>
  <div class="template-editor">
    <!-- 顶部工具栏 -->
    <EditorToolbar
      :can-undo="canUndo"
      :can-redo="canRedo"
      :scale="scale"
      @clear="handleClear"
      @save="handleSave"
      @undo="handleUndo"
      @redo="handleRedo"
      @scale-change="handleScaleChange"
    />

    <!-- 主要内容区域 -->
    <div class="editor-content">
      <!-- 左侧面板 -->
      <EditorSidebar />

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
            @switch-canvas="switchCanvas"
            @add-canvas="addCanvas"
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
        @add-canvas="addCanvas"
        @delete-canvas="removeCanvas"
        @switch-canvas="switchCanvas"
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
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Minus, Plus, FullScreen, OffScreen } from '@icon-park/vue-next'
import EditorCanvas from './components/EditorCanvas.vue'
import EditorToolbar from './components/EditorToolbar.vue'
import EditorSidebar from './components/EditorSidebar.vue'
import EditorPanel from './components/EditorPanel.vue'

// 导入组合式函数
import { useZoom } from './composables/useZoom'
import { useCanvas } from './composables/useCanvas'
import { useCanvasConfig } from './composables/useCanvasConfig'

// 画布引用
const canvasRef = ref(null)

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
  A4_CONFIG,
  selectedElement,
  handleElementSelect,
  handleElementUpdate,
  handleClear,
  handleSave
} = useCanvas()

const { canvasConfig } = useCanvasConfig()

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
</script>

<style>
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