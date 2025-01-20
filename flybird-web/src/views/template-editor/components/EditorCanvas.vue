<template>
  <div class="editor-canvas">
    <div class="canvas-container">
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
            v-show="canvasConfig.showGrid" 
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
              @click.stop.prevent="handleElementSelect(element)"
            />
          </div>
          <vue-moveable
            v-if="selectedElement"
            :target="`[data-id='${selectedElement.id}']`"
            :draggable="true"
            :resizable="true"
            :rotatable="true"
            :roundable="true"
            :roundType="'border-radius'"
            :roundClickable="true"
            :roundRadius="0"
            :renderDirections="['nw', 'n', 'ne', 'w', 'e', 'sw', 's', 'se']"
            :keepRatio="isKeepingRatio"
            :snappable="true"
            :snapCenter="true"
            :elementSnapDirections="{ top: true, left: true, bottom: true, right: true }"
            :elementGuidelines="elements.map(el => `[data-id='${el.id}']`)"
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

const emit = defineEmits(['element-select', 'elements-change'])

// 计算属性
const contentStyle = computed(() => ({
  transform: `scale(${props.scale})`,
  transformOrigin: 'center top'
}))

const canvasStyle = computed(() => ({
  width: `${props.canvasConfig.width}px`,
  height: `${props.canvasConfig.height}px`,
  backgroundColor: props.canvasConfig.backgroundColor || '#ffffff'
}))

const gridStyle = computed(() => ({
  backgroundImage: `
    linear-gradient(${props.canvasConfig.gridColor} 1px, transparent 0),
    linear-gradient(90deg, ${props.canvasConfig.gridColor} 1px, transparent 0)
  `,
  backgroundSize: `${props.canvasConfig.gridSize}px ${props.canvasConfig.gridSize}px`,
  width: '100%',
  height: '100%',
  position: 'absolute',
  top: 0,
  left: 0,
  pointerEvents: 'none'
}))

// 获取元素样式
const getElementStyle = (element) => ({
  position: 'absolute',
  width: `${element.width}px`,
  height: `${element.height}px`,
  transform: `translate(${element.x}px, ${element.y}px) rotate(${element.rotate || 0}deg)`,
  transformOrigin: 'center center',
  zIndex: element.zIndex || 1,
  ...element.style
})

// 本地状态
const currentElement = ref(null)
const elementsList = ref([])

// 添加等比缩放控制
const isKeepingRatio = ref(false)

// 监听 props 变化
watch(() => props.selectedElement, (newVal) => {
  currentElement.value = newVal
}, { immediate: true })

watch(() => props.elements, (newVal) => {
  elementsList.value = newVal
}, { immediate: true })

// 处理元素选中
const handleElementSelect = (element) => {
  emit('element-select', element)
}

// 处理画布点击
const handleCanvasClick = (e) => {
  // 如果点击的是 moveable 控制点或元素，不处理
  if (e.target.closest('.moveable-control-box') || 
      e.target.closest('.canvas-element')) {
    return
  }
  
  // 如果点击的是画布空白区域，清除选中状态
  emit('element-select', null)
}

// 处理拖拽
const handleDrag = (e) => {
  if (!props.selectedElement || !e.beforeTranslate) return
  const [x, y] = e.beforeTranslate
  emit('elements-change', props.elements.map(el => 
    el.id === props.selectedElement.id 
      ? { ...el, x, y }
      : el
  ))
}

// 处理缩放
const handleResize = ({ target, width, height, drag, transform, dist, direction }) => {
  if (!currentElement.value) return
  
  console.log('handleResize 参数:', {
    width,
    height,
    drag,
    transform,
    dist,
    direction
  })

  // 获取当前选中的元素
  const element = elementsList.value.find(el => el.id === currentElement.value.id)
  if (!element) return

  console.log('当前元素:', element)
  
  const updatedElements = elementsList.value.map(el => {
    if (el.id === currentElement.value.id) {
      const rotate = transform?.rotate ?? el.rotate ?? 0
      
      // 使用 dist 来计算新的尺寸
      const startState = el._resizeStartState || { width: el.width, height: el.height }
      const newWidth = Math.max(10, startState.width + (dist?.[0] || 0))
      const newHeight = Math.max(10, startState.height + (dist?.[1] || 0))
      
      // 计算新的位置
      let newX = el.x
      let newY = el.y
      
      // 如果有拖拽位置，使用拖拽位置
      if (drag?.beforeTranslate) {
        [newX, newY] = drag.beforeTranslate
      }

      const updatedElement = {
        ...el,
        width: Math.round(newWidth),
        height: Math.round(newHeight),
        x: Math.round(newX),
        y: Math.round(newY),
        rotate,
        _resizeStartState: el._resizeStartState // 保持初始状态
      }

      console.log('更新后的元素:', updatedElement)
      return updatedElement
    }
    return el
  })
  
  // 更新元素列表
  elementsList.value = updatedElements
  // 触发更新事件
  emit('elements-change', updatedElements)
}

// 处理旋转
const handleRotate = (e) => {
  if (!props.selectedElement || typeof e.rotate !== 'number') return
  emit('elements-change', props.elements.map(el => 
    el.id === props.selectedElement.id 
      ? { ...el, rotate: e.rotate }
      : el
  ))
}

// 处理元素拖放
const handleDrop = (e) => {
  e.preventDefault()
  e.stopPropagation()
  
  const data = e.dataTransfer.getData('component')
  if (!data) return
  
  const componentData = JSON.parse(data)
  
  // 获取画布相对位置
  const canvasRect = e.currentTarget.getBoundingClientRect()
  const x = (e.clientX - canvasRect.left) / props.scale
  const y = (e.clientY - canvasRect.top) / props.scale
  
  // 创建新元素
  const newElement = {
    id: Date.now(),
    type: componentData.type,
    x,
    y,
    width: 100,
    height: 100,
    rotate: 0,
    props: {
      fill: '#1890ff',
      stroke: '#096dd9',
      strokeWidth: 2,
      strokeStyle: 'solid',
      opacity: 1,
      radius: 0,
      ...componentData.props
    },
    style: {
      cursor: 'pointer',
      userSelect: 'none',
      touchAction: 'none'
    }
  }
  
  // 更新元素数组
  emit('elements-change', [...props.elements, newElement])
  
  // 选中新元素
  emit('element-select', newElement)
}

// 添加事件处理函数
const handleDragStart = () => {
  // 开始拖拽时的处理
}

const handleDragEnd = () => {
  // 结束拖拽时的处理
}

const handleResizeStart = ({ target, clientX, clientY, direction }) => {
  console.log('handleResizeStart:', {
    target,
    clientX,
    clientY,
    direction
  })

  // 记录初始状态和缩放方向
  const element = elementsList.value.find(el => el.id === currentElement.value?.id)
  if (element) {
    // 保存初始状态
    element._resizeStartState = {
      width: element.width,
      height: element.height,
      x: element.x,
      y: element.y,
      direction
    }
    console.log('缩放开始状态:', element._resizeStartState)
  }
}

const handleResizeEnd = ({ target, isDrag, clientX, clientY }) => {
  // 清理临时状态
  const element = elementsList.value.find(el => el.id === currentElement.value?.id)
  if (element) {
    delete element._resizeStartState
  }
}

const handleRotateStart = () => {
  // 开始旋转时的处理
}

const handleRotateEnd = () => {
  // 结束旋转时的处理
}

// 圆角控制
const handleRoundStart = (e) => {
  console.log('圆角调整开始:', e)
  if (!currentElement.value || currentElement.value.type !== 'rectangle') return
  
  // 记录开始状态
  const element = elementsList.value.find(el => el.id === currentElement.value.id)
  if (element) {
    element._roundStartRadius = element.props.radius || 0
  }
}

const handleRound = ({ target, borderRadius, dist }) => {
  if (!currentElement.value || currentElement.value.type !== 'rectangle') return
  
  const element = elementsList.value.find(el => el.id === currentElement.value.id)
  if (!element) return
  
  console.log('圆角调整中:', {
    borderRadius,
    dist,
    currentElement: currentElement.value
  })
  
  // 使用 dist 来计算新的圆角值
  const startRadius = element._roundStartRadius || 0
  const newRadius = Math.max(0, Math.min(50, startRadius + dist[0]))
  
  const updatedElements = elementsList.value.map(el => {
    if (el.id === currentElement.value.id) {
      return {
        ...el,
        props: {
          ...el.props,
          radius: Math.round(newRadius)
        }
      }
    }
    return el
  })
  
  // 更新元素列表
  elementsList.value = updatedElements
  // 触发更新事件
  emit('elements-change', updatedElements)
}

const handleRoundEnd = (e) => {
  console.log('圆角调整结束:', e)
  
  // 清理临时状态
  const element = elementsList.value.find(el => el.id === currentElement.value?.id)
  if (element) {
    delete element._roundStartRadius
  }
}

// 处理键盘事件
const handleKeyDown = (e) => {
  if (e.key === 'Shift') {
    isKeepingRatio.value = true
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
</script>

<style scoped>
.editor-canvas {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: #f5f5f5;
}

.canvas-container {
  min-width: 100%;
  min-height: 100%;
  padding: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
}

.canvas-content {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  will-change: transform;
}

.canvas-wrapper {
  position: relative;
  background-color: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
  margin: auto;
  transition: background-color 0.3s;
}

.elements-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.canvas-grid {
  opacity: 0.5;
  transition: opacity 0.3s;
}

.canvas-element {
  position: absolute;
  user-select: none;
  touch-action: none;
  outline: 2px solid transparent;
  transition: outline-color 0.2s;
  cursor: pointer;
  z-index: 1;
}

.element-selected {
  outline-color: #1890ff !important;
  z-index: 2 !important;
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