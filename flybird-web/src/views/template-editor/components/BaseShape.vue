<template>
  <div 
    class="base-shape"
    :class="{ selected }"
    :style="shapeStyle"
    @mousedown.stop="handleMouseDown"
  >
    <div 
      class="shape-content" 
      :data-subtype="subType"
      :style="{
        ...contentStyle,
        '--border-color': borderColor
      }"
    ></div>
    <!-- 调整大小的手柄 -->
    <template v-if="selected">
      <div class="resize-handle tl" data-direction="tl" @mousedown.stop="handleResizeStart"></div>
      <div class="resize-handle tr" data-direction="tr" @mousedown.stop="handleResizeStart"></div>
      <div class="resize-handle bl" data-direction="bl" @mousedown.stop="handleResizeStart"></div>
      <div class="resize-handle br" data-direction="br" @mousedown.stop="handleResizeStart"></div>
    </template>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { SHAPE_TYPES } from '../constants/components'

const props = defineProps({
  id: {
    type: [String, Number],
    required: true
  },
  subType: {
    type: String,
    required: true
  },
  x: {
    type: Number,
    default: 0
  },
  y: {
    type: Number,
    default: 0
  },
  width: {
    type: Number,
    default: 100
  },
  height: {
    type: Number,
    default: 100
  },
  rotation: {
    type: Number,
    default: 0
  },
  backgroundColor: {
    type: String,
    default: '#ffffff'
  },
  borderColor: {
    type: String,
    default: '#000000'
  },
  borderWidth: {
    type: Number,
    default: 1
  },
  borderStyle: {
    type: String,
    default: 'solid'
  },
  selected: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['select', 'update'])

// 拖拽状态
const isDragging = ref(false)
const startX = ref(0)
const startY = ref(0)
const startWidth = ref(0)
const startHeight = ref(0)
const isResizing = ref(false)
const resizeDirection = ref('')

// 基础样式
const baseStyle = computed(() => ({
  transform: `translate(${props.x}px, ${props.y}px) rotate(${props.rotation}deg)`,
  width: `${props.width}px`,
  height: `${props.height}px`,
  backgroundColor: props.backgroundColor,
  borderColor: props.borderColor,
  borderWidth: `${props.borderWidth}px`,
  borderStyle: props.borderStyle,
  cursor: isDragging.value ? 'grabbing' : 'grab'
}))

// 形状特定样式
const contentStyle = computed(() => {
  const style = {
    width: '100%',
    height: '100%'
  }

  switch (props.subType) {
    case 'circle':
      return {
        ...style,
        borderRadius: '50%',
        backgroundColor: props.backgroundColor,
        border: `${props.borderWidth}px ${props.borderStyle} ${props.borderColor}`
      }
    case 'rectangle':
      return {
        ...style,
        backgroundColor: props.backgroundColor,
        border: `${props.borderWidth}px ${props.borderStyle} ${props.borderColor}`
      }
    case 'triangle':
      return {
        ...style,
        clipPath: 'polygon(50% 0%, 0% 100%, 100% 100%)',
        backgroundColor: props.backgroundColor,
        border: 'none'
      }
    case 'arrow':
      return {
        ...style,
        backgroundColor: props.backgroundColor,
        clipPath: 'polygon(0% 30%, 70% 30%, 70% 0%, 100% 50%, 70% 100%, 70% 70%, 0% 70%)'
      }
    case 'star':
      return {
        ...style,
        clipPath: 'polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%)',
        backgroundColor: props.backgroundColor,
        border: 'none'
      }
    default:
      return style
  }
})

// 形状样式
const shapeStyle = computed(() => ({
  position: 'absolute',
  transform: `translate(${props.x}px, ${props.y}px) rotate(${props.rotation}deg)`,
  width: `${props.width}px`,
  height: `${props.height}px`,
  userSelect: 'none',
  boxSizing: 'border-box',
  cursor: isDragging.value ? 'grabbing' : 'grab',
  zIndex: props.selected ? 101 : 100
}))

// 开始拖拽
const handleMouseDown = (e) => {
  if (e.target.classList.contains('resize-handle')) {
    return
  }
  
  isDragging.value = true
  startX.value = e.clientX
  startY.value = e.clientY

  // 添加事件监听
  document.addEventListener('mousemove', handleMouseMove)
  document.addEventListener('mouseup', handleMouseUp)

  emit('select')
}

// 拖拽移动
const handleMouseMove = (e) => {
  if (!isDragging.value && !isResizing.value) return

  e.preventDefault()
  e.stopPropagation()

  const scaleContainer = e.target.closest('.canvas-scale-container')
  const scale = scaleContainer ? parseFloat(scaleContainer.style.transform.match(/scale\(([\d.]+)\)/)[1]) : 1

  if (isDragging.value) {
    const deltaX = (e.clientX - startX.value) / scale
    const deltaY = (e.clientY - startY.value) / scale
    
    startX.value = e.clientX
    startY.value = e.clientY

    emit('update', {
      ...props,
      x: props.x + deltaX,
      y: props.y + deltaY
    })
  } else if (isResizing.value) {
    const deltaX = (e.clientX - startX.value) / scale
    const deltaY = (e.clientY - startY.value) / scale
    let newWidth = startWidth.value
    let newHeight = startHeight.value

    switch (resizeDirection.value) {
      case 'br':
        newWidth += deltaX
        newHeight += deltaY
        break
      case 'bl':
        newWidth -= deltaX
        newHeight += deltaY
        break
      case 'tr':
        newWidth += deltaX
        newHeight -= deltaY
        break
      case 'tl':
        newWidth -= deltaX
        newHeight -= deltaY
        break
    }

    // 最小尺寸限制
    newWidth = Math.max(20, newWidth)
    newHeight = Math.max(20, newHeight)

    startX.value = e.clientX
    startY.value = e.clientY

    emit('update', {
      ...props,
      width: newWidth,
      height: newHeight
    })
  }
}

// 结束拖拽
const handleMouseUp = () => {
  isDragging.value = false
  isResizing.value = false
  document.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseup', handleMouseUp)
}

// 开始调整大小
const handleResizeStart = (e) => {
  e.stopPropagation()
  isResizing.value = true
  resizeDirection.value = e.target.dataset.direction
  startX.value = e.clientX
  startY.value = e.clientY
  startWidth.value = props.width
  startHeight.value = props.height

  document.addEventListener('mousemove', handleMouseMove)
  document.addEventListener('mouseup', handleMouseUp)
}
</script>

<style scoped>
.base-shape {
  position: absolute;
  box-sizing: border-box;
  z-index: 100;
  user-select: none;
  transform-origin: center center;
  will-change: transform;
  pointer-events: auto;
}

.base-shape.selected {
  z-index: 101;
}

.base-shape.selected .shape-content {
  outline: 2px solid #1890ff;
  outline-offset: 2px;
}

.shape-content {
  position: relative;
  width: 100%;
  height: 100%;
  pointer-events: auto;
  transition: all 0.2s;
}

/* 调整大小的手柄样式 */
.resize-handle {
  position: absolute;
  width: 8px;
  height: 8px;
  background-color: #fff;
  border: 1px solid #1890ff;
  border-radius: 50%;
  z-index: 102;
  pointer-events: auto;
}

.resize-handle.tl {
  top: -4px;
  left: -4px;
  cursor: nw-resize;
}

.resize-handle.tr {
  top: -4px;
  right: -4px;
  cursor: ne-resize;
}

.resize-handle.bl {
  bottom: -4px;
  left: -4px;
  cursor: sw-resize;
}

.resize-handle.br {
  bottom: -4px;
  right: -4px;
  cursor: se-resize;
}
</style> 