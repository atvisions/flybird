<template>
  <div class="editor-canvas">
    <!-- 标尺组件移到外层 -->
    <Ruler
      v-if="canvasConfig.showRuler"
      :width="canvasConfig.width"
      :height="canvasConfig.height"
      :scale="scale"
      :startX="rulerOffset.x"
      :startY="rulerOffset.y"
      :shadow="shadow"
      :cornerActive="true"
      :thick="20"
      :rulerColor="canvasConfig.rulerColor || '#999999'"
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
            />
          </div>
          <vue-moveable
            v-if="selectedElement"
            :target="`[data-id='${selectedElement.id}']`"
            :draggable="true"
            :resizable="true"
            :rotatable="true"
            :roundable="selectedElement?.type === 'rectangle'"
            :roundType="'border-radius'"
            :roundClickable="true"
            :roundRadius="selectedElement?.props?.radius || 0"
            :renderDirections="['nw', 'n', 'ne', 'w', 'e', 'sw', 's', 'se']"
            :keepRatio="isKeepingRatio"
            :snappable="true"
            :snapCenter="true"
            :elementSnapDirections="{ top: true, left: true, bottom: true, right: true }"
            :elementGuidelines="elements.map(el => `[data-id='${el.id}']`)"
            :snapThreshold="5"
            :snapGridWidth="canvasConfig.showGrid ? canvasConfig.gridSize : 0"
            :snapGridHeight="canvasConfig.showGrid ? canvasConfig.gridSize : 0"
            :isDisplayGridGuidelines="canvasConfig.showGrid"
            :gridGuidelines="getGridGuidelines()"
            :bounds="{
              left: 0,
              top: 0,
              right: canvasConfig.width,
              bottom: canvasConfig.height
            }"
            :origin="false"
            :hideDefaultLines="false"
            :isDisplaySnapDigit="true"
            :snapDigit="0"
            :snapDistFormat="v => `${v}px`"
            :preventClickDefault="true"
            :preventDragDefault="true"
            :scalable="true"
            :pinchable="true"
            :dragArea="false"
            :transformOrigin="'50% 50%'"
            :verticalGuidelines="[0, canvasConfig.width / 2, canvasConfig.width]"
            :horizontalGuidelines="[0, canvasConfig.height / 2, canvasConfig.height]"
            :zoom="1"
            :padding="{ left: 0, top: 0, right: 0, bottom: 0 }"
            @dragStart="handleDragStart"
            @drag="handleDrag"
            @dragEnd="handleDragEnd"
            @resizeStart="handleResizeStart"
            @resize="handleResize"
            @resizeEnd="handleResizeEnd"
            @rotateStart="handleRotateStart"
            @rotate="handleRotate"
            @rotateEnd="handleRotateEnd"
            @roundStart="handleRoundStart"
            @round="handleRound"
            @roundEnd="handleRoundEnd"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import VueMoveable from 'vue3-moveable'
import { useHistory } from '../composables/useHistory'
import Ruler from './Ruler.vue'  // 导入标尺组件

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

// 计算属性
const contentStyle = computed(() => {
  const scale = props.scale
  const width = props.canvasConfig.width
  const height = props.canvasConfig.height
  
  return {
    position: 'relative',
    minWidth: scale > 1 ? `${width * scale + 200}px` : '100%',
    minHeight: scale > 1 ? `${height * scale + 200}px` : '100%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '40px',
    boxSizing: 'border-box'
  }
})

const containerStyle = computed(() => ({
  position: 'absolute',
  inset: '20px',
  overflow: 'auto'
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
  const wrapper = document.querySelector('.canvas-wrapper')
  if (!container || !wrapper) return { x: 0, y: 0 }

  const containerRect = container.getBoundingClientRect()
  const wrapperRect = wrapper.getBoundingClientRect()

  return {
    x: (wrapperRect.left - containerRect.left) / props.scale,
    y: (wrapperRect.top - containerRect.top) / props.scale
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
  transformOrigin: 'center center',
  zIndex: element.zIndex || 1,
  pointerEvents: 'auto',
  touchAction: 'none',
  ...element.style
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

// 处理拖拽
const handleDrag = (e) => {
  console.log('拖拽事件:', e)
  if (!currentElement.value || !e.beforeTranslate) return
  
  const [x, y] = e.beforeTranslate
  
  // 更新当前选中元素的位置，保持其他属性不变
  const updatedElement = {
    ...currentElement.value,
    x: Math.round(x),
    y: Math.round(y)
  }
  
  // 更新元素列表
  const updatedElements = elementsList.value.map(el => 
    el.id === updatedElement.id ? updatedElement : el
  )
  
  // 更新本地状态
  elementsList.value = updatedElements
  currentElement.value = updatedElement
  
  // 触发更新事件
  emit('elements-change', updatedElements)
}

// 处理拖拽开始
const handleDragStart = () => {
  if (!props.selectedElement) return
  isOperating.value = true
  // 在开始拖拽时，保存完整的元素状态
  currentElement.value = { ...props.selectedElement }
}

// 处理拖拽结束
const handleDragEnd = () => {
  if (currentElement.value && isOperating.value) {
    isOperating.value = false
    // 在结束拖拽时，保存完整的元素状态
    emit('element-select', currentElement.value)
    // 保存到历史记录
    pushState(elementsList.value)
    currentElement.value = null
  }
}

// 处理缩放开始
const handleResizeStart = ({ target, clientX, clientY, direction }) => {
  if (!props.selectedElement) return
  isOperating.value = true
  // 保存完整的当前状态
  currentElement.value = { 
    ...props.selectedElement,
    _resizeStartState: {
      width: props.selectedElement.width,
      height: props.selectedElement.height,
      x: props.selectedElement.x,
      y: props.selectedElement.y,
      direction
    }
  }
}

// 处理缩放
const handleResize = ({ target, width, height, drag, transform, dist, direction }) => {
  if (!currentElement.value || !currentElement.value._resizeStartState) return
  
  // 使用 dist 来计算新的尺寸
  const startState = currentElement.value._resizeStartState
  const newWidth = Math.max(10, startState.width + (dist?.[0] || 0))
  const newHeight = Math.max(10, startState.height + (dist?.[1] || 0))
  
  // 计算新的位置
  let newX = currentElement.value.x
  let newY = currentElement.value.y
  
  // 如果有拖拽位置，使用拖拽位置
  if (drag?.beforeTranslate) {
    [newX, newY] = drag.beforeTranslate
  }

  // 创建更新后的元素
  const updatedElement = {
    ...currentElement.value,
    width: Math.round(newWidth),
    height: Math.round(newHeight),
    x: Math.round(newX),
    y: Math.round(newY),
    rotate: transform?.rotate ?? currentElement.value.rotate ?? 0
  }
  
  // 更新当前元素
  currentElement.value = updatedElement
  
  // 更新元素列表
  const updatedElements = elementsList.value.map(el => 
    el.id === updatedElement.id ? updatedElement : el
  )
  
  // 更新元素列表
  elementsList.value = updatedElements
  
  // 触发更新事件
  emit('elements-change', updatedElements)
}

// 处理缩放结束
const handleResizeEnd = ({ target, isDrag, clientX, clientY }) => {
  if (currentElement.value && isOperating.value) {
    isOperating.value = false
    // 删除临时状态
    const { _resizeStartState, ...cleanElement } = currentElement.value
    
    // 更新元素列表
    const updatedElements = elementsList.value.map(el => 
      el.id === cleanElement.id ? cleanElement : el
    )
    
    // 更新状态
    elementsList.value = updatedElements
    currentElement.value = cleanElement
    
    // 触发更新事件
    emit('elements-change', updatedElements)
    emit('element-select', cleanElement)
    // 保存到历史记录
    pushState(updatedElements)
  }
}

// 处理旋转
const handleRotate = (e) => {
  if (!props.selectedElement || typeof e.rotate !== 'number') return
  
  // 创建更新后的元素，四舍五入角度值
  const updatedElement = {
    ...props.selectedElement,
    rotate: Math.round(e.rotate)
  }
  
  // 更新元素列表
  const updatedElements = elementsList.value.map(el => 
    el.id === props.selectedElement.id ? updatedElement : el
  )
  
  // 更新本地状态
  elementsList.value = updatedElements
  
  // 触发更新事件
  emit('elements-change', updatedElements)
  
  // 触发选中元素更新事件，实时更新右侧面板
  emit('element-select', updatedElement)
}

// 处理旋转开始
const handleRotateStart = () => {
  if (!props.selectedElement) return
  isOperating.value = true
}

// 处理旋转结束
const handleRotateEnd = () => {
  if (currentElement.value && isOperating.value) {
    isOperating.value = false
    // 保存到历史记录
    pushState(elementsList.value)
  }
}

// 处理圆角开始
const handleRoundStart = () => {
  if (!currentElement.value || currentElement.value.type !== 'rectangle') return
  isOperating.value = true
  currentElement.value._roundStartState = currentElement.value
}

const handleRound = ({ target, borderRadius }) => {
  if (!currentElement.value || currentElement.value.type !== 'rectangle') return
  
  // 更新当前选中元素的圆角
  const updatedElement = {
    ...currentElement.value,
    props: {
      ...currentElement.value.props,
      radius: Math.round(borderRadius)
    }
  }
  
  // 更新当前元素引用
  currentElement.value = updatedElement
  
  // 更新元素列表
  const updatedElements = elementsList.value.map(el => 
    el.id === updatedElement.id ? updatedElement : el
  )
  
  // 更新元素列表
  elementsList.value = updatedElements
  
  // 触发更新事件
  emit('elements-change', updatedElements)
  
  // 触发选中元素更新事件，实时更新右侧面板
  emit('element-select', updatedElement)
}

// 处理圆角结束
const handleRoundEnd = () => {
  if (currentElement.value && isOperating.value) {
    isOperating.value = false
    const { _roundStartState, ...cleanElement } = currentElement.value
    
    // 更新元素列表
    const updatedElements = elementsList.value.map(el => 
      el.id === cleanElement.id ? cleanElement : el
    )
    
    // 更新状态
    elementsList.value = updatedElements
    currentElement.value = cleanElement
    
    // 触发更新事件
    emit('elements-change', updatedElements)
    emit('element-select', cleanElement)
    // 保存到历史记录
    pushState(updatedElements)
  }
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
}

.canvas-container {
  position: absolute;
  inset: 20px;  /* 为标尺留出空间 */
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
  padding: 40px;
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
  pointer-events: auto !important;
}

:deep(.moveable-line) {
  background-color: #1890ff;
  pointer-events: none;
}

:deep(.moveable-control) {
  background-color: #fff;
  border: 2px solid #1890ff;
  pointer-events: auto !important;
}

:deep(.moveable-round) {
  position: absolute;
  width: 12px !important;
  height: 12px !important;
  margin-left: -6px !important;
  margin-top: -6px !important;
  background-color: #fff !important;
  border: 2px solid #1890ff !important;
  border-radius: 50% !important;
  cursor: pointer !important;
  z-index: 150 !important;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
}

:deep(.moveable-round:hover) {
  transform: scale(1.2) !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15) !important;
}

:deep(.moveable-round-line) {
  background-color: #1890ff !important;
  height: 1px !important;
  width: 1px !important;
  transform-origin: 0 0 !important;
  z-index: 149 !important;
  opacity: 0.5 !important;
}

:deep(.moveable-round-group) {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 101 !important;
}

:deep(.moveable-round-control) {
  display: block !important;
  position: absolute !important;
  width: 16px !important;
  height: 16px !important;
  margin-left: -8px !important;
  margin-top: -8px !important;
  background-color: #fff !important;
  border: 2px solid #1890ff !important;
  border-radius: 50% !important;
  cursor: pointer !important;
  z-index: 102 !important;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
}

:deep(.moveable-round-control:hover) {
  transform: scale(1.2) !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15) !important;
}

:deep(.moveable-round-group .moveable-line) {
  background-color: #1890ff !important;
  height: 2px !important;
  opacity: 0.5 !important;
}

.radius-control {
  display: none;
}
</style>