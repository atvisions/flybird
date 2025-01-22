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
            <div
              v-for="element in elements"
              :key="element.id"
              class="element-wrapper"
              :data-id="element.id"
              :style="getElementStyle(element)"
              @click.stop.prevent="handleElementSelect(element, $event)"
              @mousedown.stop="handleElementDragStart($event, element)"
            >
              <component
                :is="components[element.type]"
                :id="element.id"
                class="canvas-element"
                :class="{ 
                  'element-selected': element.id === selectedElement?.id && !selectedElements.length,
                  'element-multi-selected': selectedElements.includes(element)
                }"
                v-bind="element.props"
                :width="element.width"
                :height="element.height"
                @update="(payload) => handleElementUpdate(element, payload)"
                :style="{
                  width: '100%',
                  height: '100%'
                }"
                @update:value="(value) => handleElementValueUpdate(element, value)"
              />
              <div 
                v-if="element.id === selectedElement?.id && !selectedElements.length"
                class="element-delete-btn"
                :style="{
                  position: 'absolute',
                  top: '-20px',
                  right: '-30px',
                  transform: 'translate(0, 0)',
                  transformOrigin: 'center',
                  zIndex: 999999
                }"
                @click.stop="handleElementDelete(element)"
                @mousedown.stop
              >×</div>
            </div>
          </div>
          <vue-moveable
            v-if="selectedElement && !selectedElements.length"
            ref="moveableRef"
            :target="`[data-id='${selectedElement.id}']`"
            :draggable="true"
            :resizable="true"
            :rotatable="true"
            :scalable="true"
            :origin="false"
            :hideDefaultLines="true"
            :hideRotationControls="false"
            :hideDefaultControls="true"
            :keepRatio="isKeepingRatio"
            :renderDirections="['nw', 'n', 'ne', 'w', 'e', 'sw', 's', 'se']"
            :transformOrigin="'50% 50%'"
            :snappable="true"
            :snapCenter="true"
            :snapThreshold="5"
            :verticalGuidelines="[0, canvasConfig.width / 2, canvasConfig.width]"
            :horizontalGuidelines="[0, canvasConfig.height / 2, canvasConfig.height]"
            :elementSnapDirections="{
              top: true,
              right: true,
              bottom: true,
              left: true,
              center: true,
              middle: true
            }"
            :snapDirections="{
              top: true,
              right: true,
              bottom: true,
              left: true,
              center: true,
              middle: true
            }"
            :snapGap="true"
            :isDisplaySnapDigit="true"
            :elementGuidelines="getElementGuidelines()"
            :bounds="{
              left: 0,
              top: 0,
              right: canvasConfig.width,
              bottom: canvasConfig.height
            }"
            :renderMode="'transform'"
            @dragStart="handleDragStart"
            @drag="handleDrag"
            @dragEnd="handleDragEnd"
            @resizeStart="handleResizeStart"
            @resize="handleResize"
            @resizeEnd="handleResizeEnd"
            @rotateStart="handleRotateStart"
            @rotate="handleRotate"
            @rotateEnd="handleRotateEnd"
            @delete="handleElementDelete(selectedElement)"
          />
          <vue-moveable
            v-if="selectedElements.length > 0"
            ref="multiMoveableRef"
            class="group-moveable"
            :target="selectedElements.map(el => `[data-id='${el.id}']`)"
            :draggable="true"
            :resizable="true"
            :rotatable="true"
            :scalable="true"
            :origin="false"
            :hideDefaultLines="false"
            :hideRotationControls="false"
            :hideDefaultControls="false"
            :keepRatio="isKeepingRatio"
            :renderDirections="['nw', 'n', 'ne', 'w', 'e', 'sw', 's', 'se']"
            :transformOrigin="'50% 50%'"
            :snappable="true"
            :snapCenter="true"
            :snapThreshold="5"
            :verticalGuidelines="[0, canvasConfig.width / 2, canvasConfig.width]"
            :horizontalGuidelines="[0, canvasConfig.height / 2, canvasConfig.height]"
            :elementSnapDirections="{
              top: true,
              right: true,
              bottom: true,
              left: true,
              center: true,
              middle: true
            }"
            :snapDirections="{
              top: true,
              right: true,
              bottom: true,
              left: true,
              center: true,
              middle: true
            }"
            :snapGap="true"
            :isDisplaySnapDigit="true"
            :elementGuidelines="getElementGuidelines()"
            :bounds="{
              left: 0,
              top: 0,
              right: canvasConfig.width,
              bottom: canvasConfig.height
            }"
            :renderMode="'transform'"
            @dragGroupStart="handleGroupDragStart"
            @dragGroup="handleGroupDrag"
            @dragGroupEnd="handleGroupDragEnd"
            @resizeGroupStart="handleGroupResizeStart"
            @resizeGroup="handleGroupResize"
            @resizeGroupEnd="handleGroupResizeEnd"
            @rotateGroupStart="handleGroupRotateStart"
            @rotateGroup="handleGroupRotate"
            @rotateGroupEnd="handleGroupRotateEnd"
          >
            <div 
              class="group-delete-btn"
              :style="{
                position: 'absolute',
                top: '-20px',
                right: '-30px',
                width: '20px',
                height: '20px',
                background: '#ff4d4f',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: 'pointer',
                color: 'white',
                fontSize: '16px',
                boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
                zIndex: 999999
              }"
              @click.stop="handleGroupDelete"
              @mousedown.stop
            >×</div>
          </vue-moveable>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick, h } from 'vue'
import VueMoveable from 'vue3-moveable'
import { useHistory } from '../composables/useHistory'
import GuideLine from './GuideLine.vue'
import { resumeComponents } from '../config/resume-components'

// 导入基础组件
import Rectangle from './shapes/Rectangle.vue'
import Circle from './shapes/Circle.vue'
import Triangle from './shapes/Triangle.vue'
import Line from './shapes/Line.vue'
import Arrow from './shapes/Arrow.vue'
import Star from './shapes/Star.vue'
import Text from './shapes/Text.vue'
import Title from './shapes/Title.vue'
import Icon from './shapes/Icon.vue'
import Avatar from './shapes/Avatar.vue'
import ResumeField from './shapes/ResumeField.vue'

// 注册组件
const components = {
  rectangle: Rectangle,
  circle: Circle,
  triangle: Triangle,
  line: Line,
  arrow: Arrow,
  star: Star,
  text: Text,
  title: Title,
  icon: Icon,
  avatar: Avatar,
  'resume-field': ResumeField
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
  'elements-change',
  'element-add',
  'selected-elements-change',
  'update:canUndo',
  'update:canRedo'
])

// 历史记录管理
const { pushState, undo, redo, canUndo, canRedo } = useHistory()

// 监听状态变化并通知父组件
watch([canUndo, canRedo], ([newCanUndo, newCanRedo]) => {
  emit('update:canUndo', newCanUndo)
  emit('update:canRedo', newCanRedo)
})

// 本地状态
const currentElement = ref(null)
const elementsList = ref([])
const isKeepingRatio = ref(false)
const isOperating = ref(false)  // 添加操作状态标记

// 添加 moveableRef 的声明
const moveableRef = ref(null)

// 添加多选状态
const selectedElements = ref([])

// 添加多选 Moveable 的引用
const multiMoveableRef = ref(null)

// 修改拖拽相关的状态和方法
const isDragging = ref(false)
const dragStartPos = ref(null)
const dragElement = ref(null)

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
  transformOrigin: 'center',
  zIndex: element.zIndex || 1,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center'
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

// 修改元素选中处理函数
const handleElementSelect = (element, event) => {
  if (event.shiftKey) {
    // Shift 点选模式
    const index = selectedElements.value.findIndex(el => el.id === element.id)
    if (index === -1) {
      // 如果当前有单选的元素，先将其添加到选中组
      if (props.selectedElement && props.selectedElement.id !== element.id) {
        selectedElements.value = [props.selectedElement]
      }
      // 添加新元素到选中组
      selectedElements.value.push(element)
      emit('element-select', null)
      emit('selected-elements-change', selectedElements.value)
    } else {
      // 从选中组中移除元素
      selectedElements.value.splice(index, 1)
      if (selectedElements.value.length === 1) {
        emit('element-select', selectedElements.value[0])
        emit('selected-elements-change', [])
      } else if (selectedElements.value.length === 0) {
        emit('element-select', null)
        emit('selected-elements-change', [])
      } else {
        emit('selected-elements-change', selectedElements.value)
      }
    }
  } else {
    // 普通点选模式
    selectedElements.value = []
    emit('element-select', element)
    emit('selected-elements-change', [])
  }
}

// 修改画布点击处理函数
const handleCanvasClick = (e) => {
  if (e.target.closest('.moveable-control-box') || 
      e.target.closest('.canvas-element') ||
      e.target.closest('.group-delete-btn')) {
    return
  }
  selectedElements.value = []
  emit('element-select', null)
  emit('selected-elements-change', [])
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
    element.style.transform = `translate(${currentElement.value.x}px, ${currentElement.value.y}px) rotate(${currentElement.value.rotate}deg)`
  }
  
  updateElement(currentElement.value)
  emit('element-select', currentElement.value)
  pushState(elementsList.value)
  currentElement.value = null
}

// 添加 generateId 函数
const generateId = () => {
  return Date.now() + Math.random().toString(36).substr(2, 9)
}

// 修改 handleDrop 方法
const handleDrop = (e) => {
  e.preventDefault()
  e.stopPropagation()
  
  const canvasRect = e.currentTarget.getBoundingClientRect()
  const x = (e.clientX - canvasRect.left) / props.scale
  const y = (e.clientY - canvasRect.top) / props.scale

  const componentData = e.dataTransfer.getData('text/plain')
  if (!componentData) {
    console.log('没有获取到组件数据')
    return
  }

  try {
    const parsedData = JSON.parse(componentData)
    console.log('解析的拖放数据:', parsedData)

    if (parsedData.type === 'basic-info') {
      // 从 resumeComponents 中获取基本信息字段配置
      const basicInfoConfig = resumeComponents.find(group => group.key === 'basicInfo')
      if (!basicInfoConfig) return

      let currentY = y
      basicInfoConfig.fields.forEach((field, index) => {
        const element = {
          id: generateId(),
          type: 'resume-field',
          x: x,
          y: currentY,
          width: field.width || 200,
          height: field.type === 'textarea' ? (field.height || 100) : 30,
          rotate: 0,
          props: {
            label: field.label,
            dataPath: `basic_info.${field.key}`,
            type: field.type || 'text',
            value: '',
            fontSize: 14,
            color: '#333333',
            labelWidth: 70,
            labelColor: '#666666',
            isPreview: false
          }
        }

        elementsList.value.push(element)
        currentY += element.height + 10
      })

      // 选中第一个元素
      if (elementsList.value.length > 0) {
        emit('element-select', elementsList.value[elementsList.value.length - basicInfoConfig.fields.length])
      }
    } else {
      // 处理其他类型的组件
      const newElement = {
        id: generateId(),
        type: parsedData.type,
        x,
        y,
        width: 100,
        height: 100,
        rotate: 0,
        props: parsedData.props || {}
      }

      // 根据类型调整默认尺寸
      if (parsedData.type === 'icon') {
        newElement.width = 40
        newElement.height = 40
      } else if (parsedData.type === 'text' || parsedData.type === 'title') {
        newElement.width = 200
        newElement.height = 40
      }

      elementsList.value.push(newElement)
      emit('element-select', newElement)
    }

    emit('elements-change', elementsList.value)
    pushState(elementsList.value)
  } catch (error) {
    console.error('拖放错误:', error)
    console.error('原始数据:', componentData)
  }
}

// 添加处理元素值更新的方法
const handleElementValueUpdate = (element, value) => {
  if (!element) return
  
  const updatedElement = {
    ...element,
    props: {
      ...element.props,
      value
    }
  }
  
  // 更新元素列表
  const index = elementsList.value.findIndex(el => el.id === element.id)
  if (index !== -1) {
    elementsList.value[index] = updatedElement
    emit('elements-change', elementsList.value)
  }
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
  // 如果正在输入文本，不处理快捷键
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
    return
  }

  if (e.key === 'Shift') {
    isKeepingRatio.value = true
  }
  
  // 处理删除键
  if (e.key === 'Delete' || e.key === 'Backspace') {
    // 如果有多选组，删除所有选中的元素
    if (selectedElements.value.length > 0) {
      handleGroupDelete()
      return
    }
    // 如果是单选，删除当前选中的元素
    if (props.selectedElement) {
      handleElementDelete(props.selectedElement)
      return
    }
  }
  
  // 如果有选中的元素，处理方向键移动
  if ((props.selectedElement || selectedElements.value.length > 0) && !e.metaKey && !e.ctrlKey && !e.altKey) {
    const step = e.shiftKey ? 10 : 1 // 按住 Shift 时移动 10px，否则移动 1px
    let elements = selectedElements.value.length > 0 ? selectedElements.value : [props.selectedElement]
    let updated = false

    switch (e.key) {
      case 'ArrowUp':
        e.preventDefault()
        elements.forEach(element => {
          const updatedElement = {
            ...element,
            y: Math.max(0, element.y - step)
          }
          updateElement(updatedElement)
        })
        updated = true
        break
      case 'ArrowDown':
        e.preventDefault()
        elements.forEach(element => {
          const updatedElement = {
            ...element,
            y: Math.min(props.canvasConfig.height - element.height, element.y + step)
          }
          updateElement(updatedElement)
        })
        updated = true
        break
      case 'ArrowLeft':
        e.preventDefault()
        elements.forEach(element => {
          const updatedElement = {
            ...element,
            x: Math.max(0, element.x - step)
          }
          updateElement(updatedElement)
        })
        updated = true
        break
      case 'ArrowRight':
        e.preventDefault()
        elements.forEach(element => {
          const updatedElement = {
            ...element,
            x: Math.min(props.canvasConfig.width - element.width, element.x + step)
          }
          updateElement(updatedElement)
        })
        updated = true
        break
    }

    if (updated) {
      emit('elements-change', [...elementsList.value])
      pushState([...elementsList.value])
    }
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
    const domElement = document.querySelector(`[data-id='${updatedElement.id}']`)
    if (domElement) {
      // 更新所有可能的样式属性
      const {
        fontFamily,
        fontSize,
        fontWeight,
        fontStyle,
        textAlign,
        verticalAlign,
        color,
        lineHeight,
        opacity,
        content
      } = updatedElement.props

      // 更新文本内容
      if (content !== undefined) {
        const textContent = domElement.querySelector('.text-content')
        if (textContent) {
          textContent.textContent = content
          // 将样式应用到 text-content 元素上
          Object.assign(textContent.style, {
            fontFamily: fontFamily || 'Arial',
            fontSize: fontSize ? `${fontSize}px` : '14px',
            fontWeight: fontWeight || 'normal',
            fontStyle: fontStyle || 'normal',
            textAlign: textAlign || 'left',
            verticalAlign: verticalAlign || 'top',
            color: color || '#333333',
            lineHeight: lineHeight || '1.5',
            opacity: opacity || '1'
          })
        }
      }

      // 强制重新渲染
      domElement.style.display = 'none'
      domElement.offsetHeight // 触发重排
      domElement.style.display = 'flex'
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
  
  // 直接更新删除按钮的样式
  const deleteBtn = document.querySelector('.element-delete-btn')
  if (deleteBtn) {
    const angle = updatedElement.rotate || 0
    deleteBtn.style.transform = `translate(0, 0) rotate(${angle}deg)`
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
      centerRect: true,
      horizontal: true,
      vertical: true,
      gap: 0,
      bounds: {
        left: el.x,
        top: el.y,
        right: el.x + el.width,
        bottom: el.y + el.height,
        center: el.x + el.width / 2,
        middle: el.y + el.height / 2
      }
    }))
}

// 修改 updateElement 函数
const updateElement = (updatedElement) => {
  const index = elementsList.value.findIndex(el => el.id === updatedElement.id)
  if (index !== -1) {
    elementsList.value[index] = updatedElement
    
    if (props.selectedElement?.id === updatedElement.id) {
      emit('element-select', updatedElement)
    }
    
    const multiSelectIndex = selectedElements.value.findIndex(el => el.id === updatedElement.id)
    if (multiSelectIndex !== -1) {
      selectedElements.value[multiSelectIndex] = updatedElement
      emit('selected-elements-change', [...selectedElements.value])
      
      nextTick(() => {
        if (multiMoveableRef.value) {
          multiMoveableRef.value.updateRect()
          multiMoveableRef.value.updateTarget()
          selectedElements.value.forEach(element => {
            const domElement = document.querySelector(`[data-id='${element.id}']`)
            if (domElement) {
              domElement.style.transform = `translate(${element.x}px, ${element.y}px) rotate(${element.rotate || 0}deg)`
            }
          })
        }
      })
    }
    
    emit('elements-change', [...elementsList.value])
  }
}

// 处理元素删除
const handleElementDelete = (element) => {
  if (!element) return
  
  // 过滤掉被删除的元素
  const updatedElements = elementsList.value.filter(el => el.id !== element.id)
  
  // 更新元素列表
  elementsList.value = updatedElements
  
  // 触发更新事件
  emit('elements-change', updatedElements)
  
  // 清除选中状态
  emit('element-select', null)
  
  // 保存到历史记录
  pushState(updatedElements)
}

// 添加组删除方法
const handleGroupDelete = () => {
  if (selectedElements.value.length === 0) return
  
  // 获取所有选中元素的 ID
  const selectedIds = new Set(selectedElements.value.map(el => el.id))
  
  // 过滤掉被删除的元素
  const updatedElements = elementsList.value.filter(el => !selectedIds.has(el.id))
  
  // 更新元素列表
  elementsList.value = updatedElements
  
  // 清空选中状态
  selectedElements.value = []
  emit('element-select', null)
  
  // 触发更新事件
  emit('elements-change', updatedElements)
  
  // 保存到历史记录
  pushState(updatedElements)
}

// 处理组拖拽
const handleGroupDragStart = ({ events }) => {
  events.forEach((ev, i) => {
    const element = selectedElements.value[i]
    if (!element) return
    element._dragStart = {
      x: element.x,
      y: element.y
    }
  })
  isOperating.value = true
}

const handleGroupDrag = ({ events }) => {
  events.forEach((ev, i) => {
    const element = selectedElements.value[i]
    if (!element || !element._dragStart) return

    const [x, y] = ev.beforeTranslate

    // 确保不超出画布边界
    const boundedX = Math.max(0, Math.min(x, props.canvasConfig.width - element.width))
    const boundedY = Math.max(0, Math.min(y, props.canvasConfig.height - element.height))

    const updatedElement = {
      ...element,
      x: Math.round(boundedX),
      y: Math.round(boundedY)
    }

    // 更新元素位置
    const index = elementsList.value.findIndex(el => el.id === element.id)
    if (index !== -1) {
      elementsList.value[index] = updatedElement
      selectedElements.value[i] = updatedElement

      // 直接更新 DOM 样式
      const domElement = document.querySelector(`[data-id='${element.id}']`)
      if (domElement) {
        domElement.style.transform = `translate(${boundedX}px, ${boundedY}px) rotate(${element.rotate || 0}deg)`
      }
    }
  })

  // 触发更新事件
  emit('elements-change', [...elementsList.value])
}

const handleGroupDragEnd = () => {
  selectedElements.value.forEach(element => {
    delete element._dragStart
  })
  isOperating.value = false
  pushState([...elementsList.value])
}

// 处理组缩放
const handleGroupResizeStart = ({ events }) => {
  events.forEach((ev, i) => {
    const element = selectedElements.value[i]
    if (!element) return
    element._resizeStart = {
      width: element.width,
      height: element.height,
      x: element.x,
      y: element.y
    }
  })
  isOperating.value = true
}

const handleGroupResize = ({ events }) => {
  events.forEach((ev, i) => {
    const element = selectedElements.value[i]
    if (!element || !element._resizeStart) return

    const { width, height } = ev
    const [x, y] = ev.drag.beforeTranslate

    const updatedElement = {
      ...element,
      width: Math.round(width),
      height: Math.round(height),
      x: Math.round(element._resizeStart.x + x),
      y: Math.round(element._resizeStart.y + y)
    }

    // 更新元素尺寸和位置
    const index = elementsList.value.findIndex(el => el.id === element.id)
    if (index !== -1) {
      elementsList.value[index] = updatedElement
      selectedElements.value[i] = updatedElement

      // 直接更新 DOM 样式
      const domElement = document.querySelector(`[data-id='${element.id}']`)
      if (domElement) {
        domElement.style.width = `${updatedElement.width}px`
        domElement.style.height = `${updatedElement.height}px`
        domElement.style.transform = `translate(${updatedElement.x}px, ${updatedElement.y}px) rotate(${element.rotate || 0}deg)`
      }
    }
  })

  // 触发更新事件
  emit('elements-change', [...elementsList.value])
}

const handleGroupResizeEnd = () => {
  selectedElements.value.forEach(element => {
    delete element._resizeStart
  })
  isOperating.value = false
  pushState([...elementsList.value])
}

// 处理组旋转
const handleGroupRotateStart = ({ events }) => {
  events.forEach((ev, i) => {
    const element = selectedElements.value[i]
    if (!element) return
    element._rotateStart = element.rotate || 0
  })
  isOperating.value = true
}

const handleGroupRotate = ({ events }) => {
  events.forEach((ev, i) => {
    const element = selectedElements.value[i]
    if (!element || element._rotateStart === undefined) return

    const rotate = (element._rotateStart + ev.rotate) % 360

    const updatedElement = {
      ...element,
      rotate: Math.round(rotate)
    }

    // 更新元素旋转角度
    const index = elementsList.value.findIndex(el => el.id === element.id)
    if (index !== -1) {
      elementsList.value[index] = updatedElement
      selectedElements.value[i] = updatedElement

      // 直接更新 DOM 样式
      const domElement = document.querySelector(`[data-id='${element.id}']`)
      if (domElement) {
        domElement.style.transform = `translate(${element.x}px, ${element.y}px) rotate(${updatedElement.rotate}deg)`
      }
    }
  })

  // 触发更新事件
  emit('elements-change', [...elementsList.value])
}

const handleGroupRotateEnd = () => {
  selectedElements.value.forEach(element => {
    delete element._rotateStart
  })
  isOperating.value = false
  pushState([...elementsList.value])
}

// 添加对齐和分布方法
// 水平分布到画布
const alignHorizontalToCanvas = () => {
  const elements = selectedElements.value.length > 0 ? selectedElements.value : [props.selectedElement]
  if (!elements || elements.length === 0) return

  elements.forEach(element => {
    const updatedElement = {
      ...element,
      x: (props.canvasConfig.width - element.width) / 2
    }
    updateElement(updatedElement)
  })

  emit('elements-change', [...elementsList.value])
  pushState([...elementsList.value])
}

// 垂直分布到画布
const alignVerticalToCanvas = () => {
  const elements = selectedElements.value.length > 0 ? selectedElements.value : [props.selectedElement]
  if (!elements || elements.length === 0) return

  elements.forEach(element => {
    const updatedElement = {
      ...element,
      y: (props.canvasConfig.height - element.height) / 2
    }
    updateElement(updatedElement)
  })

  emit('elements-change', [...elementsList.value])
  pushState([...elementsList.value])
}

// 左对齐
const alignLeft = () => {
  const elements = selectedElements.value.length > 0 ? selectedElements.value : [props.selectedElement]
  if (!elements || elements.length === 0) return

  const leftMost = 0  // 对齐到画布左边缘
  elements.forEach(element => {
    const updatedElement = {
      ...element,
      x: leftMost
    }
    updateElement(updatedElement)
  })

  emit('elements-change', [...elementsList.value])
  pushState([...elementsList.value])
}

// 水平居中对齐
const alignHorizontalCenter = () => {
  const elements = selectedElements.value.length > 0 ? selectedElements.value : [props.selectedElement]
  if (!elements || elements.length === 0) return

  // 如果只有一个元素，则相对于画布居中
  if (elements.length === 1) {
    const element = elements[0]
    const updatedElement = {
      ...element,
      x: (props.canvasConfig.width - element.width) / 2
    }
    updateElement(updatedElement)
  } else {
    // 多个元素，则相对于选中组的边界框居中
    const leftMost = Math.min(...elements.map(el => el.x))
    const rightMost = Math.max(...elements.map(el => el.x + el.width))
    const groupWidth = rightMost - leftMost
    const groupCenter = leftMost + groupWidth / 2

    elements.forEach(element => {
      const updatedElement = {
        ...element,
        x: groupCenter - element.width / 2
      }
      updateElement(updatedElement)
    })
  }

  emit('elements-change', [...elementsList.value])
  pushState([...elementsList.value])
}

// 右对齐
const alignRight = () => {
  const elements = selectedElements.value.length > 0 ? selectedElements.value : [props.selectedElement]
  if (!elements || elements.length === 0) return

  elements.forEach(element => {
    const updatedElement = {
      ...element,
      x: props.canvasConfig.width - element.width  // 对齐到画布右边缘
    }
    updateElement(updatedElement)
  })

  emit('elements-change', [...elementsList.value])
  pushState([...elementsList.value])
}

// 顶部对齐
const alignTop = () => {
  const elements = selectedElements.value.length > 0 ? selectedElements.value : [props.selectedElement]
  if (!elements || elements.length === 0) return

  const topMost = 0  // 对齐到画布顶部
  elements.forEach(element => {
    const updatedElement = {
      ...element,
      y: topMost
    }
    updateElement(updatedElement)
  })

  emit('elements-change', [...elementsList.value])
  pushState([...elementsList.value])
}

// 垂直居中对齐
const alignVerticalCenter = () => {
  const elements = selectedElements.value.length > 0 ? selectedElements.value : [props.selectedElement]
  if (!elements || elements.length === 0) return

  // 如果只有一个元素，则相对于画布居中
  if (elements.length === 1) {
    const element = elements[0]
    const updatedElement = {
      ...element,
      y: (props.canvasConfig.height - element.height) / 2
    }
    updateElement(updatedElement)
  } else {
    // 多个元素，则相对于选中组的边界框居中
    const topMost = Math.min(...elements.map(el => el.y))
    const bottomMost = Math.max(...elements.map(el => el.y + el.height))
    const groupHeight = bottomMost - topMost
    const groupCenter = topMost + groupHeight / 2

    elements.forEach(element => {
      const updatedElement = {
        ...element,
        y: groupCenter - element.height / 2
      }
      updateElement(updatedElement)
    })
  }

  emit('elements-change', [...elementsList.value])
  pushState([...elementsList.value])
}

// 底部对齐
const alignBottom = () => {
  const elements = selectedElements.value.length > 0 ? selectedElements.value : [props.selectedElement]
  if (!elements || elements.length === 0) return

  elements.forEach(element => {
    const updatedElement = {
      ...element,
      y: props.canvasConfig.height - element.height  // 对齐到画布底部
    }
    updateElement(updatedElement)
  })

  emit('elements-change', [...elementsList.value])
  pushState([...elementsList.value])
}

// 处理元素拖拽开始
const handleElementDragStart = (event, element) => {
  // 如果元素已经被选中，不启用拖拽
  if (element.id === props.selectedElement?.id || selectedElements.value.includes(element)) {
    return
  }
  
  isDragging.value = true
  dragElement.value = element
  dragStartPos.value = {
    x: event.clientX,
    y: event.clientY,
    elementX: element.x,
    elementY: element.y
  }

  // 添加全局事件监听
  window.addEventListener('mousemove', handleMouseMove)
  window.addEventListener('mouseup', handleMouseUp)
}

// 处理鼠标移动
const handleMouseMove = (event) => {
  if (!isDragging.value || !dragStartPos.value || !dragElement.value) return
  
  const dx = event.clientX - dragStartPos.value.x
  const dy = event.clientY - dragStartPos.value.y
  
  const newX = Math.max(0, Math.min(props.canvasConfig.width - dragElement.value.width, 
    dragStartPos.value.elementX + dx / props.scale))
  const newY = Math.max(0, Math.min(props.canvasConfig.height - dragElement.value.height, 
    dragStartPos.value.elementY + dy / props.scale))
  
  // 直接更新 DOM 样式
  const domElement = document.querySelector(`[data-id='${dragElement.value.id}']`)
  if (domElement) {
    domElement.style.transform = `translate(${newX}px, ${newY}px) rotate(${dragElement.value.rotate || 0}deg)`
  }
}

// 处理鼠标松开
const handleMouseUp = (event) => {
  if (!isDragging.value || !dragStartPos.value || !dragElement.value) return
  
  const dx = event.clientX - dragStartPos.value.x
  const dy = event.clientY - dragStartPos.value.y
  
  const newX = Math.max(0, Math.min(props.canvasConfig.width - dragElement.value.width, 
    dragStartPos.value.elementX + dx / props.scale))
  const newY = Math.max(0, Math.min(props.canvasConfig.height - dragElement.value.height, 
    dragStartPos.value.elementY + dy / props.scale))
  
  const updatedElement = {
    ...dragElement.value,
    x: Math.round(newX),
    y: Math.round(newY)
  }
  
  updateElement(updatedElement)
  pushState([...elementsList.value])
  
  // 清理状态和事件监听
  isDragging.value = false
  dragStartPos.value = null
  dragElement.value = null
  window.removeEventListener('mousemove', handleMouseMove)
  window.removeEventListener('mouseup', handleMouseUp)
}

// 组件卸载时清理事件监听
onUnmounted(() => {
  window.removeEventListener('mousemove', handleMouseMove)
  window.removeEventListener('mouseup', handleMouseUp)
})

// 暴露对齐方法
defineExpose({
  alignHorizontalToCanvas,
  alignVerticalToCanvas,
  alignLeft,
  alignHorizontalCenter,
  alignRight,
  alignTop,
  alignVerticalCenter,
  alignBottom,
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
  outline: 2px solid #ff4d4f !important;
}

.element-multi-selected {
  outline: none !important;
}

:deep(.moveable-control-box) {
  --moveable-color: #ff4d4f;
  z-index: 100;
  pointer-events: auto !important;
}

:deep(.moveable-control) {
  width: 8px !important;
  height: 8px !important;
  margin-left: -4px !important;
  margin-top: -4px !important;
  border: 1px solid #fff !important;
  background-color: #ff4d4f !important;
  border-radius: 50% !important;
  pointer-events: auto !important;
}

:deep(.moveable-nw) {
  cursor: nw-resize !important;
}

:deep(.moveable-n) {
  cursor: n-resize !important;
}

:deep(.moveable-ne) {
  cursor: ne-resize !important;
}

:deep(.moveable-w) {
  cursor: w-resize !important;
}

:deep(.moveable-e) {
  cursor: e-resize !important;
}

:deep(.moveable-sw) {
  cursor: sw-resize !important;
}

:deep(.moveable-s) {
  cursor: s-resize !important;
}

:deep(.moveable-se) {
  cursor: se-resize !important;
}

:deep(.moveable-rotation-control) {
  border-radius: 50% !important;
  background-color: #fff !important;
  border: 2px solid #ff4d4f !important;
  width: 16px !important;
  height: 16px !important;
  margin-left: -8px !important;
  margin-top: -8px !important;
  cursor: pointer !important;
  pointer-events: auto !important;
}

:deep(.moveable-origin) {
  display: none !important;
}

:deep(.moveable-line) {
  background: #ff4d4f !important;
  opacity: 0.5;
  display: block !important;
}

:deep(.moveable-direction) {
  pointer-events: auto !important;
  display: block !important;
}

.canvas-element-wrapper {
  position: absolute;
  width: auto;
  height: auto;
  top: 0;
  left: 0;
  transform: translate(var(--x), var(--y)) rotate(var(--rotate, 0deg));
}

.element-wrapper {
  position: absolute;
  transform-origin: center;
  will-change: transform;
  display: flex;
  align-items: center;
  justify-content: center;
  user-select: none;
  cursor: move;  /* 添加移动光标 */
}

.canvas-element {
  width: 100%;
  height: 100%;
  position: relative;
  pointer-events: auto;
}

.element-delete-btn {
  position: absolute;
  width: 20px;
  height: 20px;
  background: #ff4d4f;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: white;
  font-size: 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  z-index: 999999;
  pointer-events: auto;
}

.element-delete-btn:hover {
  background: #ff7875;
  transform: scale(1.1);
}

.element-delete-btn:active {
  background: #ff4d4f;
  transform: scale(1);
}

:deep(.group-moveable .moveable-control-box) {
  --moveable-color: #1890ff;
  border: 1px solid #1890ff !important;
}

:deep(.group-moveable .moveable-line) {
  background: #1890ff !important;
  opacity: 0.5;
  height: 1px !important;
}

:deep(.group-moveable .moveable-control) {
  width: 8px !important;
  height: 8px !important;
  margin-left: -4px !important;
  margin-top: -4px !important;
  border: 1px solid #fff !important;
  background-color: #1890ff !important;
  border-radius: 50% !important;
}

:deep(.group-moveable .moveable-rotation-control) {
  border-color: #1890ff !important;
}

.group-delete-btn {
  pointer-events: auto !important;
}

.group-delete-btn:hover {
  background: #ff7875 !important;
  transform: scale(1.1) !important;
}

.group-delete-btn:active {
  background: #ff4d4f !important;
  transform: scale(1) !important;
}
</style>