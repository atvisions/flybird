<template>
  <div
    class="design-element"
    :class="{ 'is-selected': isSelected }"
    :style="elementStyle"
    @click.stop="$emit('select', element)"
    ref="elementRef"
  >
    <!-- 图片元素 -->
    <v-img
      v-if="element.type === 'image'"
      :src="element.content"
      :width="element.width"
      :height="element.height"
      :style="element.styles"
      cover
    />

    <!-- 文字元素 -->
    <div
      v-else-if="element.type === 'text'"
      class="text-element"
      :class="{ 'has-binding': element.dataBinding }"
      :style="{
        width: `${element.width}px`,
        height: `${element.height}px`,
        color: element.styles.color,
        fontSize: element.styles.fontSize,
        fontWeight: element.styles.fontWeight,
        textAlign: element.styles.textAlign,
        fontFamily: `${element.styles.fontFamily}, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif`
      }"
      @dblclick="startTextEdit"
    >
      <div v-if="!isEditing" class="text-content">
        {{ element.content }}
        <div v-if="element.dataBinding" class="binding-indicator">
          <v-icon size="small" color="primary">mdi-link-variant</v-icon>
          <span class="binding-label">{{ element.dataBinding.label }}</span>
        </div>
      </div>
      <textarea
        v-else
        v-model="editingText"
        class="text-editor"
        @blur="finishTextEdit"
        @keydown.enter="finishTextEdit"
        @contextmenu.prevent="showContextMenu"
        ref="textEditorRef"
        :style="{
          color: element.styles.color,
          fontSize: element.styles.fontSize,
          fontWeight: element.styles.fontWeight,
          textAlign: element.styles.textAlign,
          fontFamily: `${element.styles.fontFamily}, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif`,
          width: '100%',
          height: '100%'
        }"
      ></textarea>

      <!-- 右键菜单 -->
      <v-menu
        v-model="showMenu"
        :position-x="menuX"
        :position-y="menuY"
        absolute
        offset-y
      >
        <v-list>
          <v-list-subheader>插入数据字段</v-list-subheader>
          <v-list-item
            v-for="field in dataFields"
            :key="field.field"
            @click="insertField(field)"
            :title="field.label"
          >
            <template v-slot:prepend>
              <v-icon size="small">mdi-link-variant</v-icon>
            </template>
          </v-list-item>
        </v-list>
      </v-menu>
    </div>

    <!-- 形状元素 -->
    <div
      v-else-if="element.type === 'shape'"
      class="shape-element"
      :class="element.shapeType"
      :style="{
        width: `${element.width}px`,
        height: `${element.height}px`,
        ...element.styles
      }"
    ></div>

    <!-- 选中时显示的控制点 -->
    <template v-if="isSelected">
      <!-- 旋转控制点 -->
      <div class="rotate-handle" @mousedown.stop="startRotate"></div>
      
      <!-- 缩放控制点 -->
      <div 
        v-for="(handle, index) in resizeHandles" 
        :key="index"
        class="resize-handle"
        :class="handle.class"
        @mousedown.stop="startResize($event, handle.cursor)"
      ></div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'

const props = defineProps({
  element: {
    type: Object,
    required: true
  },
  isSelected: {
    type: Boolean,
    default: false
  },
  scale: {
    type: Number,
    default: 1
  },
  dataFields: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['select', 'update'])

// DOM 引用
const elementRef = ref(null)

// 元素样式
const elementStyle = computed(() => ({
  transform: `translate(${props.element.x}px, ${props.element.y}px) rotate(${props.element.rotation || 0}deg)`,
  position: 'absolute',
  cursor: props.isSelected ? 'move' : 'pointer',
  userSelect: 'none',
  zIndex: props.element.styles?.zIndex || 0
}))

// 缩放控制点配置
const resizeHandles = [
  { class: 'nw', cursor: 'nw-resize' },
  { class: 'n', cursor: 'n-resize' },
  { class: 'ne', cursor: 'ne-resize' },
  { class: 'w', cursor: 'w-resize' },
  { class: 'e', cursor: 'e-resize' },
  { class: 'sw', cursor: 'sw-resize' },
  { class: 's', cursor: 's-resize' },
  { class: 'se', cursor: 'se-resize' }
]

// 拖拽相关状态
let startX = 0
let startY = 0
let startWidth = 0
let startHeight = 0
let startRotation = 0
let isDragging = false
let isResizing = false
let isRotating = false
let currentHandle = null

// 开始移动
const startDrag = (e) => {
  if (!props.isSelected || isResizing || isRotating) return
  
  isDragging = true
  startX = e.clientX - props.element.x
  startY = e.clientY - props.element.y
  
  document.addEventListener('mousemove', handleDrag)
  document.addEventListener('mouseup', stopDrag)
}

// 处理移动
const handleDrag = (e) => {
  if (!isDragging) return
  
  const newX = e.clientX - startX
  const newY = e.clientY - startY
  
  emit('update', {
    ...props.element,
    x: newX,
    y: newY
  })
}

// 停止移动
const stopDrag = () => {
  isDragging = false
  document.removeEventListener('mousemove', handleDrag)
  document.removeEventListener('mouseup', stopDrag)
}

// 开始缩放
const startResize = (e, cursor) => {
  e.stopPropagation()
  isResizing = true
  currentHandle = cursor
  
  startX = e.clientX
  startY = e.clientY
  startWidth = props.element.width
  startHeight = props.element.height
  
  document.addEventListener('mousemove', handleResize)
  document.addEventListener('mouseup', stopResize)
}

// 处理缩放
const handleResize = (e) => {
  if (!isResizing) return
  
  const dx = (e.clientX - startX) / props.scale
  const dy = (e.clientY - startY) / props.scale
  
  let newWidth = startWidth
  let newHeight = startHeight
  
  switch (currentHandle) {
    case 'e-resize':
      newWidth = startWidth + dx
      break
    case 'w-resize':
      newWidth = startWidth - dx
      break
    case 's-resize':
      newHeight = startHeight + dy
      break
    case 'n-resize':
      newHeight = startHeight - dy
      break
    case 'se-resize':
      newWidth = startWidth + dx
      newHeight = startHeight + dy
      break
    case 'sw-resize':
      newWidth = startWidth - dx
      newHeight = startHeight + dy
      break
    case 'ne-resize':
      newWidth = startWidth + dx
      newHeight = startHeight - dy
      break
    case 'nw-resize':
      newWidth = startWidth - dx
      newHeight = startHeight - dy
      break
  }
  
  // 确保尺寸不小于最小值
  newWidth = Math.max(20, newWidth)
  newHeight = Math.max(20, newHeight)
  
  emit('update', {
    ...props.element,
    width: newWidth,
    height: newHeight
  })
}

// 停止缩放
const stopResize = () => {
  isResizing = false
  currentHandle = null
  document.removeEventListener('mousemove', handleResize)
  document.removeEventListener('mouseup', stopResize)
}

// 开始旋转
const startRotate = (e) => {
  e.stopPropagation()
  isRotating = true
  
  const rect = elementRef.value.getBoundingClientRect()
  const centerX = rect.left + rect.width / 2
  const centerY = rect.top + rect.height / 2
  startRotation = Math.atan2(e.clientY - centerY, e.clientX - centerX)
  
  document.addEventListener('mousemove', handleRotate)
  document.addEventListener('mouseup', stopRotate)
}

// 处理旋转
const handleRotate = (e) => {
  if (!isRotating || !elementRef.value) return
  
  const rect = elementRef.value.getBoundingClientRect()
  const centerX = rect.left + rect.width / 2
  const centerY = rect.top + rect.height / 2
  
  const angle = Math.atan2(e.clientY - centerY, e.clientX - centerX)
  let rotation = (angle - startRotation) * (180 / Math.PI)
  
  // 将旋转角度限制在0-360度之间
  rotation = (rotation + 360) % 360
  
  emit('update', {
    ...props.element,
    rotation
  })
}

// 停止旋转
const stopRotate = () => {
  isRotating = false
  document.removeEventListener('mousemove', handleRotate)
  document.removeEventListener('mouseup', stopRotate)
}

const isEditing = ref(false)
const editingText = ref('')
const textEditorRef = ref(null)

// 开始文字编辑
const startTextEdit = (e) => {
  if (props.element.type !== 'text') return
  e.stopPropagation()
  isEditing.value = true
  editingText.value = props.element.content
  nextTick(() => {
    if (textEditorRef.value) {
      textEditorRef.value.focus()
    }
  })
}

// 完成文字编辑
const finishTextEdit = () => {
  if (!isEditing.value) return
  isEditing.value = false
  emit('update', {
    ...props.element,
    content: editingText.value
  })
}

// 右键菜单状态
const showMenu = ref(false)
const menuX = ref(0)
const menuY = ref(0)

// 显示右键菜单
const showContextMenu = (event) => {
  event.preventDefault()
  menuX.value = event.clientX
  menuY.value = event.clientY
  showMenu.value = true
}

// 插入字段
const insertField = (field) => {
  const textarea = textEditorRef.value
  const start = textarea.selectionStart
  const end = textarea.selectionEnd
  const fieldText = `{{${field.field}}}`
  
  editingText.value = 
    editingText.value.substring(0, start) +
    fieldText +
    editingText.value.substring(end)

  // 更新元素
  emit('update', {
    ...props.element,
    content: editingText.value,
    dataBinding: {
      field: field.field,
      label: field.label
    }
  })

  // 关闭菜单
  showMenu.value = false
}

// 添加事件监听
onMounted(() => {
  if (elementRef.value) {
    elementRef.value.addEventListener('mousedown', startDrag)
  }
})

onUnmounted(() => {
  if (elementRef.value) {
    elementRef.value.removeEventListener('mousedown', startDrag)
  }
  // 清理所有可能的事件监听
  document.removeEventListener('mousemove', handleDrag)
  document.removeEventListener('mouseup', stopDrag)
  document.removeEventListener('mousemove', handleResize)
  document.removeEventListener('mouseup', stopResize)
  document.removeEventListener('mousemove', handleRotate)
  document.removeEventListener('mouseup', stopRotate)
})
</script>

<style scoped>
.design-element {
  position: absolute;
  touch-action: none;
}

.is-selected {
  outline: 1px solid #409eff;
}

.resize-handle {
  position: absolute;
  width: 8px;
  height: 8px;
  background: #fff;
  border: 1px solid #409eff;
  border-radius: 50%;
}

.rotate-handle {
  position: absolute;
  width: 8px;
  height: 8px;
  background: #fff;
  border: 1px solid #409eff;
  border-radius: 50%;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  cursor: pointer;
}

/* 缩放控制点位置 */
.nw { top: -4px; left: -4px; cursor: nw-resize; }
.n { top: -4px; left: 50%; transform: translateX(-50%); cursor: n-resize; }
.ne { top: -4px; right: -4px; cursor: ne-resize; }
.w { top: 50%; left: -4px; transform: translateY(-50%); cursor: w-resize; }
.e { top: 50%; right: -4px; transform: translateY(-50%); cursor: e-resize; }
.sw { bottom: -4px; left: -4px; cursor: sw-resize; }
.s { bottom: -4px; left: 50%; transform: translateX(-50%); cursor: s-resize; }
.se { bottom: -4px; right: -4px; cursor: se-resize; }

/* 形状元素样式 */
.shape-element {
  width: 100%;
  height: 100%;
}

.shape-element.triangle {
  clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
}

.text-element {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  overflow: hidden;
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.5;
}

.text-content {
  width: 100%;
  height: 100%;
  padding: 4px;
  margin: 0;
}

.text-editor {
  border: none;
  outline: none;
  background: transparent;
  resize: none;
  padding: 4px;
  margin: 0;
  line-height: 1.5;
}

.text-element.has-binding {
  position: relative;
}

.binding-indicator {
  position: absolute;
  top: -18px;
  left: 0;
  font-size: 12px;
  color: #409eff;
  display: flex;
  align-items: center;
  gap: 4px;
  background: rgba(255, 255, 255, 0.9);
  padding: 2px 4px;
  border-radius: 4px;
  border: 1px solid #409eff;
  pointer-events: none;
}

.binding-label {
  font-size: 12px;
  color: #409eff;
}
</style> 