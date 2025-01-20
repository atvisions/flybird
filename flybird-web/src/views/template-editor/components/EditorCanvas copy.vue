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
            <div
              v-for="element in elementsList"
              :key="element.id"
              class="element-wrapper"
              :style="getElementStyle(element)"
              :data-id="element.id"
              @click.stop="handleElementSelect(element)"
            >
              <component
                :is="components[element.type]"
                :id="element.id"
                class="canvas-element"
                :class="{ 'element-selected': element.id === selectedElement?.id }"
                v-bind="element.props"
              />
              <div 
                v-if="element.id === selectedElement?.id"
                class="delete-button"
                @click.stop.prevent="handleElementDelete(element)"
                @mousedown.stop.prevent
              >
                <svg viewBox="0 0 1024 1024" width="16" height="16">
                  <path fill="currentColor" d="M512 64C264.6 64 64 264.6 64 512s200.6 448 448 448 448-200.6 448-448S759.4 64 512 64zm165.4 618.2l-66-.3L512 563.4l-99.3 118.4-66.1.3c-4.4 0-8-3.5-8-8 0-1.9.7-3.7 1.9-5.2l130.1-155L340.5 359c-1.2-1.5-1.9-3.3-1.9-5.2 0-4.4 3.6-8 8-8l66.1.3L512 464.6l99.3-118.4 66-.3c4.4 0 8 3.5 8 8 0 1.9-.7 3.7-1.9 5.2L553.5 514l130 155c1.2 1.5 1.9 3.3 1.9 5.2 0 4.4-3.6 8-8 8z"/>
                </svg>
              </div>
            </div>
          </div>
          <vue-moveable
            v-if="selectedElement"
            :target="`[data-id='${selectedElement.id}']`"
            :draggable="true"
            :resizable="true"
            :rotatable="true"
            :renderDirections="['nw', 'n', 'ne', 'w', 'e', 'sw', 's', 'se']"
            :keepRatio="isKeepingRatio"
            :snappable="true"
            :snapCenter="true"
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
            :preventClickDefault="false"
            :preventDragDefault="false"
            :scalable="false"
            :pinchable="false"
            :dragArea="false"
            :transformOrigin="'50% 50%'"
            :zoom="scale"
            :throttleResize="0"
            :throttleDrag="0"
            :throttleRotate="0"
            :resizeFormat="v => Math.round(v)"
            :defaultGroupRotate="0"
            :defaultGroupOrigin="'50% 50%'"
            :useMutationObserver="true"
            :useResizeObserver="true"
            :checkInput="true"
            :dragTarget="'.element-wrapper'"
            :dragTargetSelf="true"
            :stopPropagation="true"
            :stopDrag="false"
            :stopResize="false"
            :stopRotate="false"
            :resizeUpdateTarget="true"
            :resizeObserveParent="true"
            :resizeWithTransform="false"
            :resizeRelative="false"
            :resizeDirections="['nw', 'n', 'ne', 'w', 'e', 'sw', 's', 'se']"
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

// 本地状态
const currentElement = ref(null)
const elementsList = ref([])
const mounted = ref(false)
const isKeepingRatio = ref(false)

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
  '--width': `${element.width}px`,
  '--height': `${element.height}px`,
  pointerEvents: 'auto',
  touchAction: 'none',
  ...element.style
})

// 监听 props 变化
watch(() => props.selectedElement, (newVal) => {
  console.log('selectedElement changed:', newVal)
  currentElement.value = newVal
}, { immediate: true })

watch(() => props.elements, (newVal) => {
  console.log('elements changed:', newVal)
  elementsList.value = newVal
}, { immediate: true })

// 处理元素选中
const handleElementSelect = (element) => {
  console.log('选中元素:', element)
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
  console.log('拖拽事件:', e)
  if (!currentElement.value || !e.beforeTranslate) return
  
  const [x, y] = e.beforeTranslate
  
  // 更新当前选中元素的位置
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

// 处理缩放
const handleResize = ({ target, width, height, drag, dist }) => {
  if (!currentElement.value) return
  
  // 使用 dist 来计算新的尺寸
  const newWidth = Math.max(10, currentElement.value.width + (dist?.[0] || 0))
  const newHeight = Math.max(10, currentElement.value.height + (dist?.[1] || 0))
  
  // 创建更新后的元素
  const updatedElement = {
    ...currentElement.value,
    width: Math.round(newWidth),
    height: Math.round(newHeight),
    x: Math.round(drag.beforeTranslate[0]),
    y: Math.round(drag.beforeTranslate[1])
  }
  
  // 更新当前选中的元素
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

// 处理缩放开始
const handleResizeStart = ({ target, clientX, clientY }) => {
  console.log('开始缩放，当前选中元素:', props.selectedElement)
  if (!props.selectedElement) return
  currentElement.value = { ...props.selectedElement }
  console.log('缩放开始，currentElement:', currentElement.value)
}

const handleResizeEnd = ({ target }) => {
  console.log('结束缩放')
  console.log('结束时的 currentElement:', currentElement.value)
  if (currentElement.value) {
    emit('element-select', currentElement.value)
  }
  currentElement.value = null
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

// 处理圆角
const handleRound = ({ target, borderRadius, dist }) => {
  if (!currentElement.value || currentElement.value.type !== 'rectangle') return
  
  const element = elementsList.value.find(el => el.id === currentElement.value.id)
  if (!element) return
  
  const startRadius = element.props?.radius || 0
  const newRadius = Math.max(0, Math.min(50, startRadius + (dist?.[0] || 0)))
  
  const updatedElements = elementsList.value.map(el => {
    if (el.id === currentElement.value.id) {
      return {
        ...el,
        props: {
          ...el.props,  // 保持所有现有属性
          radius: Math.round(newRadius)  // 只更新圆角值
        }
      }
    }
    return el
  })
  
  elementsList.value = updatedElements
  emit('elements-change', updatedElements)
}

// 处理元素拖放
const handleDrop = (e) => {
  e.preventDefault()
  e.stopPropagation()
  
  const data = e.dataTransfer.getData('component')
  if (!data) return
  
  const componentData = JSON.parse(data)
  console.log('拖放的组件数据:', componentData)
  
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
  
  console.log('创建的新元素:', newElement)
  
  // 更新元素数组
  const updatedElements = [...elementsList.value, newElement]
  elementsList.value = updatedElements
  emit('elements-change', updatedElements)
  
  // 选中新元素
  emit('element-select', newElement)
}

const handleDragStart = () => {
  if (!props.selectedElement) return
  currentElement.value = { ...props.selectedElement }
}

const handleDragEnd = () => {
  if (currentElement.value) {
    emit('element-select', currentElement.value)
    currentElement.value = null
  }
}


// 处理圆角开始
const handleRoundStart = (e) => {
  if (!currentElement.value || currentElement.value.type !== 'rectangle') return
  
  const element = elementsList.value.find(el => el.id === currentElement.value.id)
  if (element) {
    element._roundStartRadius = element.props?.radius || 0
  }
}

// 处理圆角结束
const handleRoundEnd = (e) => {
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
  console.log('组件已挂载')
  window.addEventListener('keydown', handleKeyDown)
  window.addEventListener('keyup', handleKeyUp)
  mounted.value = true
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown)
  window.removeEventListener('keyup', handleKeyUp)
  mounted.value = false
})

// 添加删除事件处理函数
const handleElementDelete = (element) => {
  const updatedElements = elementsList.value.filter(el => el.id !== element.id)
  elementsList.value = updatedElements
  emit('elements-change', updatedElements)
  emit('element-select', null)
}
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
  position: relative;
  width: 100%;
  height: 100%;
  user-select: none;
  touch-action: none;
  outline: 2px solid transparent;
  transition: outline-color 0.2s;
  cursor: pointer;
  z-index: 1;
  pointer-events: auto;
  box-sizing: border-box;
  will-change: transform;
}

.element-selected {
  outline-color: #1890ff !important;
  z-index: 2 !important;
}

/* 修改选择框和控制点的样式 */
:deep(.moveable-control-box) {
  --moveable-color: #1890ff;
  z-index: 100;
  pointer-events: auto !important;
  will-change: transform;
}

:deep(.moveable-control) {
  width: 14px !important;
  height: 14px !important;
  margin-top: -7px !important;
  margin-left: -7px !important;
  background-color: #fff !important;
  border: 2px solid #1890ff !important;
  border-radius: 50% !important;
  pointer-events: auto !important;
  cursor: pointer !important;
  z-index: 101 !important;
}

:deep(.moveable-line) {
  background-color: #1890ff !important;
  pointer-events: none !important;
  z-index: 99 !important;
}

:deep(.moveable-direction) {
  width: 14px !important;
  height: 14px !important;
  margin-top: -7px !important;
  margin-left: -7px !important;
  background-color: #fff !important;
  border: 2px solid #1890ff !important;
  border-radius: 50% !important;
  cursor: pointer !important;
  z-index: 101 !important;
}

.radius-control {
  display: none;
}

.element-wrapper {
  position: absolute;
  width: var(--width);
  height: var(--height);
  transform-origin: center center;
  pointer-events: auto;
  touch-action: none;
  user-select: none;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: center;
  will-change: transform;
}

.delete-button {
  position: absolute;
  top: -20px;
  right: -20px;
  width: 20px;
  height: 20px;
  background-color: #ff4d4f;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: white;
  z-index: 1000;
  transition: all 0.2s;
}

.delete-button:hover {
  transform: scale(1.1);
  background-color: #ff7875;
}

.delete-button svg {
  width: 14px;
  height: 14px;
}

/* 修改对齐线样式 */
:deep(.guideline) {
  background-color: #ff4d4f !important;
  pointer-events: none;
}

:deep(.guideline.vertical) {
  width: 1px !important;
}

:deep(.guideline.horizontal) {
  height: 1px !important;
}

:deep(.guideline.center) {
  background-color: #ff4d4f !important;
  width: 1px !important;
}

:deep(.guideline.middle) {
  background-color: #ff4d4f !important;
  height: 1px !important;
}

:deep(.moveable-gap) {
  background-color: #ff4d4f !important;
  opacity: 0.8;
}

:deep(.moveable-gap-text) {
  background-color: #ff4d4f !important;
  color: white;
  font-size: 12px;
  padding: 2px 4px;
  border-radius: 2px;
  transform: translate(-50%, -50%);
}
</style>