<template>
  <div
    ref="fieldRef"
    class="resume-textarea"
    :class="{ selected: isSelected }"
    :style="textareaStyle"
    @mousedown="handleMouseDown"
    @click="handleClick"
  >
    <div v-if="label" class="textarea-label" :style="labelStyle">{{ label }}：</div>
    <div class="textarea-content" :style="contentStyle">
      {{ value || `[${label}]` }}
    </div>
    <div v-if="isSelected" class="resize-handles">
      <div class="resize-handle top-left" @mousedown.stop="startResize('top-left')"></div>
      <div class="resize-handle top-right" @mousedown.stop="startResize('top-right')"></div>
      <div class="resize-handle bottom-left" @mousedown.stop="startResize('bottom-left')"></div>
      <div class="resize-handle bottom-right" @mousedown.stop="startResize('bottom-right')"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'

const props = defineProps({
  value: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    required: true
  },
  selected: {
    type: Boolean,
    default: false
  },
  width: {
    type: Number,
    required: true
  },
  height: {
    type: Number,
    required: true
  },
  fontSize: {
    type: Number,
    default: 14
  },
  fontWeight: {
    type: Number,
    default: 400
  },
  color: {
    type: String,
    default: '#333333'
  },
  lineHeight: {
    type: Number,
    default: 1.5
  },
  labelColor: {
    type: String,
    default: '#666666'
  }
})

const emit = defineEmits(['update:selected', 'update'])

const fieldRef = ref(null)
const isSelected = computed(() => props.selected)
const isResizing = ref(false)
const resizeStartPos = ref({ x: 0, y: 0 })
const resizeStartSize = ref({ width: 0, height: 0 })
const currentResizeHandle = ref(null)

const isDragging = ref(false)
const dragStartPos = ref(null)

const textareaStyle = computed(() => ({
  width: `${props.width}px`,
  height: `${props.height}px`,
  fontSize: `${props.fontSize}px`,
  fontWeight: props.fontWeight,
  color: props.color,
  lineHeight: props.lineHeight
}))

const labelStyle = computed(() => ({
  color: props.labelColor,
  fontSize: `${props.fontSize}px`,
  fontWeight: 500
}))

const contentStyle = computed(() => ({
  fontSize: `${props.fontSize}px`,
  fontWeight: props.fontWeight,
  color: props.color,
  lineHeight: props.lineHeight
}))

const handleClick = (event) => {
  event.stopPropagation()
  event.preventDefault()
  emit('update:selected', true)
}

const handleMouseDown = (event) => {
  event.stopPropagation()
  event.preventDefault()
  
  if (event.target.closest('.resize-handle')) return
  
  isDragging.value = true
  dragStartPos.value = {
    x: event.clientX,
    y: event.clientY
  }
  
  window.addEventListener('mousemove', handleMouseMove)
  window.addEventListener('mouseup', handleMouseUp)
  
  emit('update:selected', true)
}

const handleMouseMove = (event) => {
  if (!isDragging.value || !dragStartPos.value) return
  
  const dx = event.clientX - dragStartPos.value.x
  const dy = event.clientY - dragStartPos.value.y
  
  emit('update', {
    props: {
      x: dx,
      y: dy
    }
  })
}

const handleMouseUp = () => {
  isDragging.value = false
  dragStartPos.value = null
  
  window.removeEventListener('mousemove', handleMouseMove)
  window.removeEventListener('mouseup', handleMouseUp)
}

const startResize = (handle) => {
  isResizing.value = true
  currentResizeHandle.value = handle
  
  const rect = fieldRef.value.getBoundingClientRect()
  resizeStartPos.value = {
    x: rect.right,
    y: rect.bottom
  }
  resizeStartSize.value = {
    width: props.width,
    height: props.height
  }
  
  window.addEventListener('mousemove', handleResize)
  window.addEventListener('mouseup', stopResize)
}

const handleResize = (event) => {
  if (!isResizing.value) return
  
  const dx = event.clientX - resizeStartPos.value.x
  const dy = event.clientY - resizeStartPos.value.y
  
  let newWidth = resizeStartSize.value.width
  let newHeight = resizeStartSize.value.height
  
  switch (currentResizeHandle.value) {
    case 'top-left':
      newWidth = Math.max(100, resizeStartSize.value.width - dx)
      newHeight = Math.max(60, resizeStartSize.value.height - dy)
      break
    case 'top-right':
      newWidth = Math.max(100, resizeStartSize.value.width + dx)
      newHeight = Math.max(60, resizeStartSize.value.height - dy)
      break
    case 'bottom-left':
      newWidth = Math.max(100, resizeStartSize.value.width - dx)
      newHeight = Math.max(60, resizeStartSize.value.height + dy)
      break
    case 'bottom-right':
      newWidth = Math.max(100, resizeStartSize.value.width + dx)
      newHeight = Math.max(60, resizeStartSize.value.height + dy)
      break
  }
  
  emit('update', {
    props: {
      width: newWidth,
      height: newHeight
    }
  })
}

const stopResize = () => {
  isResizing.value = false
  currentResizeHandle.value = null
  window.removeEventListener('mousemove', handleResize)
  window.removeEventListener('mouseup', stopResize)
}

onUnmounted(() => {
  window.removeEventListener('mousemove', handleMouseMove)
  window.removeEventListener('mouseup', handleMouseUp)
  window.removeEventListener('mousemove', handleResize)
  window.removeEventListener('mouseup', stopResize)
})
</script>

<style scoped>
.resume-textarea {
  position: absolute;
  user-select: none;
  cursor: move;
  box-sizing: border-box;
  min-width: 100px;
  min-height: 60px;
  display: flex;
  flex-direction: column;
  border: 2px solid transparent;
  transition: border-color 0.2s;
  padding: 8px;
  background: #fafafa;
  border-radius: 4px;
}

.resume-textarea.selected {
  border: 2px solid #409eff;
  z-index: 1;
}

.resume-textarea:hover {
  border-color: #409eff;
}

.textarea-label {
  flex-shrink: 0;
  margin-bottom: 8px;
}

.textarea-content {
  flex: 1;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-word;
  background: #fff;
  padding: 8px;
  border-radius: 4px;
  max-height: 100%;
}

.resize-handles {
  position: absolute;
  top: -4px;
  left: -4px;
  right: -4px;
  bottom: -4px;
  pointer-events: none;
  z-index: 2;
}

.resize-handle {
  position: absolute;
  width: 8px;
  height: 8px;
  background: #fff;
  border: 1px solid #409eff;
  pointer-events: auto;
  cursor: pointer;
  border-radius: 50%;
  z-index: 3;
}

.top-left {
  top: -4px;
  left: -4px;
  cursor: nw-resize;
}

.top-right {
  top: -4px;
  right: -4px;
  cursor: ne-resize;
}

.bottom-left {
  bottom: -4px;
  left: -4px;
  cursor: sw-resize;
}

.bottom-right {
  bottom: -4px;
  right: -4px;
  cursor: se-resize;
}
</style> 