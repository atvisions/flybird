<template>
  <div class="editor-canvas">
    <!-- 标尺组件移到外层 -->
    <GuideLine
      :width="canvasConfig?.width || 0"
      :height="canvasConfig?.height || 0"
      :snap-threshold="5"
      :snap-targets="getSnapTargets()"
      :show-guide-line="canvasConfig.showGuideLine"
    />
    <div class="canvas-container" :style="containerStyle">
      <div class="canvas-content" :style="contentStyle">
        <div 
          class="canvas-wrapper"
          :style="canvasStyle"
          @dragover.prevent
          @drop="handleDrop"
          @click="handleCanvasClick"
        >
          <!-- 网格 -->
          <div 
            v-if="canvasConfig.showGrid" 
            class="canvas-grid"
            :style="gridStyle"
          ></div>
          
          <div class="elements-container">
            <component
              v-for="element in elements"
              :key="element.id"
              :is="components[element.type]"
              :id="element.id"
              class="canvas-element"
              :class="{ 'element-selected': element.id === selectedElement?.id }"
              :style="getElementStyle(element)"
              :data-id="element.id"
              v-bind="element.props"
              :width="element.width"
              :height="element.height"
              @click.stop.prevent="handleElementSelect(element)"
              @update="(payload) => handleElementUpdate(element, payload)"
            />
          </div>
          <vue-moveable
            v-if="selectedElement"
            ref="moveableRef"
            :target="`[data-id='${selectedElement.id}']`"
            :draggable="true"
            :resizable="true"
            :rotatable="true"
            :scalable="true"
            :origin="true"
            :keepRatio="isKeepingRatio"
            :throttleDrag="0"
            :throttleRotate="0"
            :throttleResize="0"
            :renderDirections="['nw', 'n', 'ne', 'w', 'e', 'sw', 's', 'se']"
            :transformOrigin="'50% 50%'"
            :snappable="true"
            :snapCenter="true"
            :snapThreshold="10"
            :elementGuidelines="getElementGuidelines()"
            :isDisplaySnapDigit="false"
            :isDisplayInnerSnapDigit="false"
            :isDisplayGridGuidelines="false"
            :bounds="{
              left: 0,
              top: 0,
              right: canvasConfig.width,
              bottom: canvasConfig.height
            }"
            :verticalGuidelines="[0, canvasConfig.width / 2, canvasConfig.width]"
            :horizontalGuidelines="[0, canvasConfig.height / 2, canvasConfig.height]"
            :snapGap="false"
            :elementSnapDirections="{
              center: true,
              middle: true
            }"
            :snapDirections="{
              center: true,
              middle: true
            }"
            :snapGridWidth="0"
            :snapGridHeight="0"
            :renderMode="'transform'"
            :stopPropagation="true"
            :preventDefault="true"
            :useAccuratePosition="true"
            :useMutationObserver="false"
            :zoom="1"
            @dragStart="handleDragStart"
            @drag="handleDrag"
            @dragEnd="handleDragEnd"
            @resizeStart="handleResizeStart"
            @resize="handleResize"
            @resizeEnd="handleResizeEnd"
            @rotateStart="handleRotateStart"
            @rotate="handleRotate"
            @rotateEnd="handleRotateEnd"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import VueMoveable from 'vue3-moveable'
import { useHistory } from '../composables/useHistory'
import GuideLine from './GuideLine.vue'

// 导入基础组件
import Rectangle from './shapes/Rectangle.vue'
import Circle from './shapes/Circle.vue'
import Triangle from './shapes/Triangle.vue'
import Line from './shapes/Line.vue'
import Arrow from './shapes/Arrow.vue'
import Star from './shapes/Star.vue'
import Text from './shapes/Text.vue'
import Title from './shapes/Title.vue'

// 注册组件
const components = {
  rectangle: Rectangle,
  circle: Circle,
  triangle: Triangle,
  line: Line,
  arrow: Arrow,
  star: Star,
  text: Text,
  title: Title
}

const props = defineProps({
  scale: {
    type: Number,
    default: 1
  },
  elements: {
    type: Array,
    default: () => []
  },
  currentCanvasId: {
    type: Number,
    required: true
  },
  canvasConfig: {
    type: Object,
    required: true
  },
  selectedElement: {
    type: Object,
    default: null
  }
})

const emit = defineEmits([
  'element-select',
  'elements-change'
])

// 历史记录管理
const { pushState, undo, redo, canUndo, canRedo } = useHistory()

// 本地状态
const currentElement = ref(null)
const elementsList = ref([])
const isKeepingRatio = ref(false)
const isOperating = ref(false)  // 添加操作状态标记

// 添加 moveableRef 的声明
const moveableRef = ref(null)

// 计算属性
const contentStyle = computed(() => ({
  position: 'relative',
  minWidth: props.scale >= 1 ? `${props.canvasConfig.width * props.scale + 40}px` : '100%',
  minHeight: props.scale >= 1 ? `${props.canvasConfig.height * props.scale + 40}px` : '100%',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  boxSizing: 'border-box'
}))

const containerStyle = computed(() => ({
  position: 'absolute',
  top: '20px',
  left: '20px',
  bottom: '20px',
  right: '0',  /* 右边不需要间距 */
  overflow: 'auto',
  backgroundColor: '#f0f0f0'
}))

const canvasStyle = computed(() => ({
  position: 'relative',
  width: `${props.canvasConfig.width}px`,
  height: `${props.canvasConfig.height}px`,
  backgroundColor: props.canvasConfig.backgroundColor || '#ffffff',
  boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
  flexShrink: 0,
  transform: `scale(${props.scale})`,
  transformOrigin: 'center'
}))

const gridStyle = computed(() => ({
  backgroundImage: `
    linear-gradient(90deg, ${props.canvasConfig.gridColor} 1px, transparent 0),
    linear-gradient(${props.canvasConfig.gridColor} 1px, transparent 0)
  `,
  backgroundSize: `${props.canvasConfig.gridSize}px ${props.canvasConfig.gridSize}px`,
  width: '100%',
  height: '100%',
  position: 'absolute',
  top: 0,
  left: 0,
  pointerEvents: 'none',
  opacity: 0.5,
  zIndex: 0,
  backgroundPosition: '0 0',
  backgroundRepeat: 'repeat',
  imageRendering: 'pixelated'
}))

// 计算标尺偏移量
const rulerOffset = computed(() => {
  const container = document.querySelector('.canvas-container')
  if (!container) return { x: 0, y: 0 }

  return {
    x: container.scrollLeft / props.scale,
    y: container.scrollTop / props.scale
  }
})

// 添加 shadow 计算属性
const shadow = computed(() => ({
  x: 0,
  y: 0,
  width: props.canvasConfig.width,
  height: props.canvasConfig.height
}))

// 获取元素样式
const getElementStyle = (element) => ({
  position: 'absolute',
  width: `${element.width}px`,
  height: `${element.height}px`,
  transform: `translate(${element.x}px, ${element.y}px) rotate(${element.rotate || 0}deg)`,
  transformOrigin: '50% 50%',
  zIndex: element.zIndex || 1,
  backfaceVisibility: 'hidden',
  perspective: 1000,
  willChange: 'transform'
})

// 监听 props 变化
watch(() => props.selectedElement, (newVal) => {
  currentElement.value = newVal
}, { immediate: true })

watch(() => props.elements, (newVal) => {
  elementsList.value = newVal
}, { immediate: true })

// 监听缩放变化
watch(() => props.scale, (newScale, oldScale) => {
  console.log('Scale changed from', oldScale, 'to', newScale)
  console.log('Container size:', {
    width: document.querySelector('.canvas-container')?.offsetWidth,
    height: document.querySelector('.canvas-container')?.offsetHeight
  })
  console.log('Content size:', {
    width: document.querySelector('.canvas-content')?.offsetWidth,
    height: document.querySelector('.canvas-content')?.offsetHeight
  })
  console.log('Wrapper size:', {
    width: document.querySelector('.canvas-wrapper')?.offsetWidth,
    height: document.querySelector('.canvas-wrapper')?.offsetHeight
  })
})

// 添加调试信息
watch(() => props.canvasConfig, (newConfig) => {
  console.log('Canvas config changed:', {
    showGuideLine: newConfig?.showGuideLine,
    width: newConfig?.width,
    height: newConfig?.height,
    rulerColor: newConfig?.rulerColor
  })
}, { immediate: true, deep: true })

// 处理元素选中
const handleElementSelect = (element) => {
  emit('element-select', element)
}

// 处理画布点击
const handleCanvasClick = (e) => {
  if (e.target.closest('.moveable-control-box') || 
      e.target.closest('.canvas-element')) {
    return
  }
  emit('element-select', null)
}

// 处理拖拽开始
const handleDragStart = () => {
  if (!props.selectedElement) return
  isOperating.value = true
  currentElement.value = { ...props.selectedElement }
}

// 处理拖拽
const handleDrag = ({ beforeTranslate }) => {
  if (!currentElement.value) return
  
  const [x, y] = beforeTranslate
  
  // 确保元素不会超出画布边界
  const boundedX = Math.max(0, Math.min(x, props.canvasConfig.width - currentElement.value.width))
  const boundedY = Math.max(0, Math.min(y, props.canvasConfig.height - currentElement.value.height))
  
  const updatedElement = {
    ...currentElement.value,
    x: Math.round(boundedX),
    y: Math.round(boundedY)
  }
  
  // 直接更新 DOM 样式
  const element = document.querySelector(`[data-id='${updatedElement.id}']`)
  if (element) {
    element.style.transform = `translate(${updatedElement.x}px, ${updatedElement.y}px) rotate(${updatedElement.rotate || 0}deg)`
  }
  
  currentElement.value = updatedElement
}

// 处理拖拽结束
const handleDragEnd = () => {
  if (!currentElement.value) return
  isOperating.value = false
  
  // 更新 DOM 样式
  const element = document.querySelector(`[data-id='${currentElement.value.id}']`)
  if (element) {
    element.style.transform = `translate(${currentElement.value.x}px, ${currentElement.value.y}px) rotate(${currentElement.value.rotate || 0}deg)`
  }
  
  updateElement(currentElement.value)
  emit('element-select', currentElement.value)
  pushState(elementsList.value)
  currentElement.value = null
}

// 处理缩放开始
const handleResizeStart = () => {
  if (!props.selectedElement) return
  currentElement.value = { ...props.selectedElement }
}

// 处理缩放
const handleResize = ({ width, height, drag }) => {
  if (!currentElement.value) return
  isOperating.value = true
  
  const [x, y] = drag?.beforeTranslate || [currentElement.value.x, currentElement.value.y]
  
  // 限制宽度和高度不超出画布
  const maxWidth = props.canvasConfig.width - x
  const maxHeight = props.canvasConfig.height - y
  const boundedWidth = Math.min(width, maxWidth)
  const boundedHeight = Math.min(height, maxHeight)
  
  // 限制位置不超出画布
  const boundedX = Math.max(0, Math.min(x, props.canvasConfig.width - boundedWidth))
  const boundedY = Math.max(0, Math.min(y, props.canvasConfig.height - boundedHeight))
  
  const updatedElement = {
    ...currentElement.value,
    width: Math.round(boundedWidth),
    height: Math.round(boundedHeight),
    x: Math.round(boundedX),
    y: Math.round(boundedY)
  }
  
  // 直接更新 DOM 样式
  const element = document.querySelector(`[data-id='${updatedElement.id}']`)
  if (element) {
    element.style.width = `${updatedElement.width}px`
    element.style.height = `${updatedElement.height}px`
    element.style.transform = `translate(${updatedElement.x}px, ${updatedElement.y}px) rotate(${updatedElement.rotate || 0}deg)`
  }
  
  currentElement.value = updatedElement
}

// 处理缩放结束
const handleResizeEnd = () => {
  if (!currentElement.value) return
  isOperating.value = false
  
  // 更新 DOM 样式
  const element = document.querySelector(`[data-id='${currentElement.value.id}']`)
  if (element) {
    element.style.width = `${currentElement.value.width}px`
    element.style.height = `${currentElement.value.height}px`
    element.style.transform = `translate(${currentElement.value.x}px, ${currentElement.value.y}px) rotate(${currentElement.value.rotate || 0}deg)`
  }
  
  updateElement(currentElement.value)
  emit('element-select', currentElement.value)
  pushState(elementsList.value)
  currentElement.value = null
}

// 处理元素拖放
const handleDrop = (e) => {
  e.preventDefault()
  e.stopPropagation()
  
  const data = e.dataTransfer.getData('component')
  if (!data) return
  
  const componentData = JSON.parse(data)
  
  const canvasRect = e.currentTarget.getBoundingClientRect()
  const x = (e.clientX - canvasRect.left) / props.scale
  const y = (e.clientY - canvasRect.top) / props.scale
  
  // 根据组件类型设置不同的默认宽高
  let defaultWidth = 100
  let defaultHeight = 100
  let defaultProps = {
    fill: '#1890ff',
    stroke: '#096dd9',
    strokeWidth: 2,
    strokeStyle: 'solid',
    opacity: 1,
    radius: 0
  }
  
  // 根据组件类型设置不同的默认尺寸和属性
  switch (componentData.type) {
    case 'title':
      defaultWidth = 100
      defaultHeight = 30
      break
    case 'text':
      defaultWidth = 200
      defaultHeight = 60
      break
    case 'triangle':
      defaultWidth = 100
      defaultHeight = 100
      defaultProps = {
        ...defaultProps,
        fill: '#1890ff',
        stroke: '#096dd9',
        strokeWidth: 2
      }
      break
    case 'arrow':
      defaultWidth = 200
      defaultHeight = 40
      defaultProps = {
        ...defaultProps,
        stroke: '#096dd9',
        strokeWidth: 2,
        startArrow: 'none', // none, arrow, dot, diamond
        endArrow: 'arrow',  // none, arrow, dot, diamond
        startArrowSize: 10,
        endArrowSize: 10,
        lineCap: 'butt',   // butt, round, square
        lineJoin: 'miter'  // miter, round, bevel
      }
      break
    case 'line':
      defaultWidth = 200
      defaultHeight = 2
      defaultProps = {
        ...defaultProps,
        stroke: '#096dd9',
        strokeWidth: 2,
        startArrow: 'none',
        endArrow: 'none',
        startArrowSize: 10,
        endArrowSize: 10,
        lineCap: 'butt',
        lineJoin: 'miter'
      }
      break
    default:
      break
  }
  
  const newElement = {
    id: Date.now(),
    type: componentData.type,
    x,
    y,
    width: defaultWidth,
    height: defaultHeight,
    rotate: 0,
    props: {
      ...defaultProps,
      ...componentData.props
    },
    style: {
      cursor: 'pointer',
      userSelect: 'none',
      touchAction: 'none'
    }
  }
  
  emit('elements-change', [...props.elements, newElement])
  emit('element-select', newElement)
  // 保存到历史记录
  pushState([...props.elements, newElement])
}

// 处理撤销
const handleUndo = () => {
  const previousState = undo()
  if (previousState) {
    elementsList.value = previousState
    emit('elements-change', previousState)
    emit('element-select', null)
  }
}

// 处理重做
const handleRedo = () => {
  const nextState = redo()
  if (nextState) {
    elementsList.value = nextState
    emit('elements-change', nextState)
    emit('element-select', null)
  }
}

// 处理键盘快捷键
const handleKeyDown = (e) => {
  if (e.key === 'Shift') {
    isKeepingRatio.value = true
  }
  
  // 处理删除键
  if ((e.key === 'Delete' || e.key === 'Backspace') && props.selectedElement) {
    // 过滤掉被删除的元素
    const updatedElements = elementsList.value.filter(el => el.id !== props.selectedElement.id)
    
    // 更新元素列表
    elementsList.value = updatedElements
    
    // 触发更新事件
    emit('elements-change', updatedElements)
    
    // 清除选中状态
    emit('element-select', null)
  }

  // 撤销快捷键 (Cmd/Ctrl + Z)
  if ((e.metaKey || e.ctrlKey) && e.key === 'z' && !e.shiftKey) {
    e.preventDefault()
    handleUndo()
  }

  // 重做快捷键 (Cmd/Ctrl + Shift + Z 或 Cmd/Ctrl + Y)
  if ((e.metaKey || e.ctrlKey) && (e.key === 'y' || (e.key === 'z' && e.shiftKey))) {
    e.preventDefault()
    handleRedo()
  }
}

const handleKeyUp = (e) => {
  if (e.key === 'Shift') {
    isKeepingRatio.value = false
  }
}

// 组件挂载和卸载时添加/移除事件监听
onMounted(() => {
  window.addEventListener('keydown', handleKeyDown)
  window.addEventListener('keyup', handleKeyUp)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown)
  window.removeEventListener('keyup', handleKeyUp)
})

// 生成网格参考线
const getGridGuidelines = () => {
  if (!props.canvasConfig.showGrid) return []
  
  const guidelines = []
  const gridSize = props.canvasConfig.gridSize
  
  // 生成垂直网格线
  for (let x = 0; x <= props.canvasConfig.width; x += gridSize) {
    guidelines.push({ type: 'vertical', pos: x })
  }
  
  // 生成水平网格线
  for (let y = 0; y <= props.canvasConfig.height; y += gridSize) {
    guidelines.push({ type: 'horizontal', pos: y })
  }
  
  return guidelines
}

// 添加获取吸附目标的方法
const getSnapTargets = () => {
  if (!props.elements) return []
  
  const targets = []
  
  // 添加画布边界
  targets.push(
    { x: 0, y: 0 },
    { x: props.canvasConfig.width, y: 0 },
    { x: 0, y: props.canvasConfig.height },
    { x: props.canvasConfig.width, y: props.canvasConfig.height }
  )
  
  // 添加画布中心线
  targets.push(
    { x: props.canvasConfig.width / 2, y: props.canvasConfig.height / 2 }
  )
  
  // 添加元素的边界点
  props.elements.forEach(element => {
    targets.push(
      { x: element.x, y: element.y }, // 左上角
      { x: element.x + element.width, y: element.y }, // 右上角
      { x: element.x, y: element.y + element.height }, // 左下角
      { x: element.x + element.width, y: element.y + element.height }, // 右下角
      { x: element.x + element.width / 2, y: element.y + element.height / 2 } // 中心点
    )
  })
  
  return targets
}

// 处理元素更新
const handleElementUpdate = (element, payload) => {
  const updatedElement = {
    ...element,
    props: {
      ...element.props,
      ...(payload.props || {})
    }
  }
  
  // 先更新当前选中元素
  if (props.selectedElement?.id === element.id) {
    emit('element-select', updatedElement)
  }
  
  // 更新元素列表
  const updatedElements = elementsList.value.map(el => 
    el.id === element.id ? updatedElement : el
  )
  elementsList.value = updatedElements
  
  // 触发元素列表更新
  emit('elements-change', updatedElements)
  
  // 保存到历史记录
  pushState(updatedElements)
  
  // 强制更新 DOM
  nextTick(() => {
    const element = document.querySelector(`[data-id='${updatedElement.id}']`)
    if (element) {
      // 更新所有可能的样式属性
      Object.entries(updatedElement.props).forEach(([key, value]) => {
        if (key === 'opacity') {
          element.style.opacity = value
        } else if (key === 'fill') {
          element.style.fill = value
        } else if (key === 'stroke') {
          element.style.stroke = value
        }
      })
    }
  })
}

// 简化旋转处理函数
const handleRotateStart = () => {
  if (!props.selectedElement) return
  currentElement.value = { ...props.selectedElement }
}

// 处理旋转
const handleRotate = ({ rotate }) => {
  if (!currentElement.value) return
  isOperating.value = true
  
  const updatedElement = {
    ...currentElement.value,
    rotate: Math.round(rotate % 360)
  }
  
  // 直接更新 DOM 样式
  const element = document.querySelector(`[data-id='${updatedElement.id}']`)
  if (element) {
    element.style.transform = `translate(${updatedElement.x}px, ${updatedElement.y}px) rotate(${updatedElement.rotate}deg)`
  }
  
  currentElement.value = updatedElement
  
  // 更新元素列表
  const index = elementsList.value.findIndex(el => el.id === updatedElement.id)
  if (index !== -1) {
    elementsList.value[index] = updatedElement
    // 触发更新事件
    emit('elements-change', [...elementsList.value])
  }
  
  // 更新选中元素
  emit('element-select', updatedElement)
}

// 处理旋转结束
const handleRotateEnd = () => {
  if (!currentElement.value) return
  isOperating.value = false
  
  // 更新 DOM 样式
  const element = document.querySelector(`[data-id='${currentElement.value.id}']`)
  if (element) {
    element.style.transform = `translate(${currentElement.value.x}px, ${currentElement.value.y}px) rotate(${currentElement.value.rotate}deg)`
  }
  
  // 更新元素列表
  const index = elementsList.value.findIndex(el => el.id === currentElement.value.id)
  if (index !== -1) {
    elementsList.value[index] = currentElement.value
    // 触发更新事件
    emit('elements-change', [...elementsList.value])
  }
  
  // 更新选中元素
  emit('element-select', currentElement.value)
  
  // 保存到历史记录
  pushState(elementsList.value)
  currentElement.value = null
}

// 修改 getElementGuidelines 函数
const getElementGuidelines = () => {
  return props.elements
    .filter(el => el.id !== props.selectedElement?.id)
    .map(el => ({
      element: `[data-id='${el.id}']`,
      className: 'guideline',
      centerRect: true
    }))
}

// 修改 updateElement 函数
const updateElement = (updatedElement) => {
  const index = elementsList.value.findIndex(el => el.id === updatedElement.id)
  if (index !== -1) {
    elementsList.value[index] = updatedElement
    
    // 如果是当前选中的元素，立即更新选中状态
    if (props.selectedElement?.id === updatedElement.id) {
      emit('element-select', null)  // 先取消选中
      nextTick(() => {
        emit('element-select', updatedElement)  // 再重新选中
      })
    }
    
    // 触发更新事件
    emit('elements-change', [...elementsList.value])
  }
}

// 导出方法和状态给父组件
defineExpose({
  handleUndo,
  handleRedo,
  canUndo,
  canRedo
})
</script>

<style scoped>
.editor-canvas {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background-color: #f5f5f5;
  padding: 20px 0 0 20px; /* 为标尺留出空间 */
}

/* 修改标尺样式 */
:deep(.sketch-ruler) {
  position: absolute;
  z-index: 3;
  left: 20px; /* 对齐内容区域 */
  top: 20px;  /* 对齐内容区域 */
  right: 0;
  bottom: 0;
  pointer-events: auto;
}

:deep(.sketch-ruler .indicator) {
  z-index: 4;
}

.canvas-container {
  position: absolute;
  overflow: auto;
  background-color: #f0f0f0;
}

.canvas-content {
  position: relative;
  min-width: 100%;
  min-height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
}

.canvas-wrapper {
  position: relative;
  background-color: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  transform-origin: center center;
  flex-shrink: 0;
  margin: auto;
}

.elements-container {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.canvas-element {
  pointer-events: auto;
}

.element-selected {
  outline: 1px solid #1890ff;
}

:deep(.moveable-control-box) {
  --moveable-color: #1890ff;
  z-index: 100;
  pointer-events: none !important;
}

:deep(.moveable-control) {
  pointer-events: auto !important;
  background-color: #fff !important;
  border: 2px solid #1890ff !important;
  width: 12px !important;
  height: 12px !important;
  margin-left: -6px !important;
  margin-top: -6px !important;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
}

:deep(.moveable-line) {
  background-color: #ff4d4f !important;
  opacity: 1 !important;
  height: 2px !important;
  box-shadow: 0 0 4px rgba(255, 77, 79, 0.5) !important;
}

:deep(.moveable-line.moveable-vertical) {
  width: 2px !important;
}

:deep(.moveable-line.moveable-horizontal) {
  height: 2px !important;
}

:deep(.moveable-guideline) {
  background-color: #ff4d4f !important;
  opacity: 1 !important;
  z-index: 100;
  position: absolute !important;
}

:deep(.moveable-guideline.moveable-vertical) {
  width: 2px !important;
  height: 100vh !important;
  top: 0 !important;
  transform: translateX(-50%) !important;
}

:deep(.moveable-guideline.moveable-horizontal) {
  height: 2px !important;
  width: 100vw !important;
  left: 0 !important;
  transform: translateY(-50%) !important;
}

:deep(.moveable-gap) {
  display: none !important;
}

:deep(.moveable-gap-text) {
  display: none !important;
}
</style>