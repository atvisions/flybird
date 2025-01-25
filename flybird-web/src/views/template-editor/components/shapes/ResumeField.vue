<template>
  <div
    ref="fieldRef"
    class="resume-field"
    :class="{ selected: isSelected }"
    :style="fieldStyle"
    @click="handleClick"
  >
    <template v-if="type === 'avatar'">
      <div class="avatar-field">
        <img 
          v-if="value" 
          :src="value" 
          :style="{ borderRadius: '50%' }"
          draggable="false"
        />
        <div 
          v-else 
          class="avatar-placeholder" 
          style="border-radius: 50%"
          draggable="false"
        >
          <el-icon :size="40"><Avatar /></el-icon>
          <div class="avatar-text">头像</div>
        </div>
      </div>
    </template>
    <template v-else>
      <div class="field-content" :style="contentStyle">
        {{ isPreview ? value || `[${label}]` : `[${label}]` }}
      </div>
    </template>
    <div v-if="isSelected" class="resize-handles">
      <div class="resize-handle top-left" @mousedown.stop="startResize('top-left')"></div>
      <div class="resize-handle top-right" @mousedown.stop="startResize('top-right')"></div>
      <div class="resize-handle bottom-left" @mousedown.stop="startResize('bottom-left')"></div>
      <div class="resize-handle bottom-right" @mousedown.stop="startResize('bottom-right')"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import ResumeAvatar from './ResumeAvatar.vue'
import ResumeText from './ResumeText.vue'
import ResumeTextarea from './ResumeTextarea.vue'
import { Avatar } from '@element-plus/icons-vue'

const props = defineProps({
  type: {
    type: String,
    default: 'text'
  },
  label: {
    type: String,
    required: true
  },
  value: {
    type: String,
    default: ''
  },
  dataPath: {
    type: String,
    default: ''
  },
  mappingType: {
    type: String,
    default: ''
  },
  selected: {
    type: Boolean,
    default: false
  },
  position: {
    type: Object,
    default: () => ({ x: 0, y: 0 })
  },
  size: {
    type: Object,
    default: () => ({ width: 'auto', height: 'auto' })
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
  borderRadius: {
    type: String,
    default: '0'
  },
  isPreview: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:selected', 'update:position', 'update:size', 'update:value'])

const fieldRef = ref(null)
const isSelected = computed(() => props.selected)
const isResizing = ref(false)
const resizeStartPos = ref({ x: 0, y: 0 })
const resizeStartSize = ref({ width: 0, height: 0 })
const currentResizeHandle = ref(null)

const isDragging = ref(false)
const dragStartPos = ref(null)

const fieldStyle = computed(() => {
  if (props.type === 'avatar') {
    return {
      position: 'absolute',
      width: '100px',
      height: '100px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      overflow: 'hidden'
    }
  }
  return {
    position: 'absolute',
    width: '100%',
    height: '100%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-start',
    overflow: 'hidden'
  }
})

const contentStyle = computed(() => ({
  fontSize: `${props.fontSize}px`,
  fontWeight: props.fontWeight,
  color: props.color,
  lineHeight: props.lineHeight,
  width: '100%',
  height: '100%',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'flex-start',
  whiteSpace: props.type === 'textarea' ? 'pre-wrap' : 'nowrap',
  overflow: 'hidden',
  textOverflow: 'ellipsis'
}))

const getFieldComponent = (type) => {
  const componentMap = {
    avatar: ResumeAvatar,
    text: ResumeText,
    textarea: ResumeTextarea
  }
  return componentMap[type] || ResumeText
}

const componentProps = computed(() => {
  const baseProps = {
    label: props.label,
    value: props.value,
    fontSize: props.fontSize,
    fontWeight: props.fontWeight,
    color: props.color,
    lineHeight: props.lineHeight
  }

  if (props.type === 'avatar') {
    return {
      ...baseProps,
      size: Math.min(parseInt(props.size.width), parseInt(props.size.height)) || 100,
      borderRadius: props.borderRadius || '50%'
    }
  }

  return baseProps
})

const handleClick = (event) => {
  event.stopPropagation()
  emit('update:selected', true)
}

const handleMouseDown = (event) => {
  if (event.button !== 0) return // 只处理左键点击
  
  isDragging.value = true
  dragStartPos.value = {
    x: event.clientX,
    y: event.clientY,
    elementX: props.position.x,
    elementY: props.position.y
  }

  document.addEventListener('mousemove', handleMouseMove)
  document.addEventListener('mouseup', handleMouseUp)
}

const handleMouseMove = (event) => {
  if (!isDragging.value || !dragStartPos.value) return

  const dx = event.clientX - dragStartPos.value.x
  const dy = event.clientY - dragStartPos.value.y

  emit('update:position', {
    x: dragStartPos.value.elementX + dx,
    y: dragStartPos.value.elementY + dy
  })
}

const handleMouseUp = () => {
  isDragging.value = false
  dragStartPos.value = null
  document.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseup', handleMouseUp)
}

const handleValueUpdate = (newValue) => {
  emit('update:value', newValue)
}

const startResize = (handle) => {
  isResizing.value = true
  currentResizeHandle.value = handle
  const { clientX, clientY } = event
  resizeStartPos.value = { x: clientX, y: clientY }
  resizeStartSize.value = { ...props.size }
  
  document.addEventListener('mousemove', handleResize)
  document.addEventListener('mouseup', stopResize)
}

const handleResize = (event) => {
  if (!isResizing.value) return
  
  const dx = event.clientX - resizeStartPos.value.x
  const dy = event.clientY - resizeStartPos.value.y
  
  let newWidth = resizeStartSize.value.width
  let newHeight = resizeStartSize.value.height
  
  switch (currentResizeHandle.value) {
    case 'top-left':
      newWidth = resizeStartSize.value.width - dx
      newHeight = resizeStartSize.value.height - dy
      break
    case 'top-right':
      newWidth = resizeStartSize.value.width + dx
      newHeight = resizeStartSize.value.height - dy
      break
    case 'bottom-left':
      newWidth = resizeStartSize.value.width - dx
      newHeight = resizeStartSize.value.height + dy
      break
    case 'bottom-right':
      newWidth = resizeStartSize.value.width + dx
      newHeight = resizeStartSize.value.height + dy
      break
  }
  
  emit('update:size', {
    width: Math.max(50, newWidth),
    height: Math.max(50, newHeight)
  })
}

const stopResize = () => {
  isResizing.value = false
  currentResizeHandle.value = null
  document.removeEventListener('mousemove', handleResize)
  document.removeEventListener('mouseup', stopResize)
}

onUnmounted(() => {
  document.removeEventListener('mousemove', handleResize)
  document.removeEventListener('mouseup', stopResize)
  document.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseup', handleMouseUp)
})
</script>

<style scoped>
.resume-field {
  position: absolute;
  user-select: none;
  cursor: move;
  border: 1px solid transparent;
  box-sizing: border-box;
}

.resume-field.selected {
  border-color: #409eff;
}

.resize-handles {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.resize-handle {
  position: absolute;
  width: 8px;
  height: 8px;
  background: #fff;
  border: 1px solid #409eff;
  pointer-events: auto;
  cursor: pointer;
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

.avatar-field {
  width: 100px !important;
  height: 100px !important;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: #f5f7fa;
  border: 2px dashed #dcdfe6;
  box-sizing: border-box;
  border-radius: 50%;
}

.avatar-field img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  color: #909399;
}

.avatar-text {
  margin-top: 8px;
  font-size: 14px;
}

.field-content {
  position: relative;
  padding: 4px 8px;
  border: 1px dashed #dcdfe6;
  border-radius: 4px;
  background: rgba(64, 158, 255, 0.1);
  cursor: move;
  transition: all 0.3s;
}

.field-content:hover {
  border-color: #409eff;
  background: rgba(64, 158, 255, 0.2);
}
</style> 