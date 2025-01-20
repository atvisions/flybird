<template>
  <div v-if="showGuideLine" class="guide-line-container">
    <!-- 水平辅助线 -->
    <div 
      v-for="line in horizontalLines"
      :key="line.id"
      class="guide-line horizontal"
      :style="{ top: line.position + 'px' }"
      @mousedown.prevent="startDragH($event, line)"
      @dblclick="deleteLine(line)"
    >
      <!-- 位置显示 -->
      <div class="guide-line-info" :style="{ left: infoPosition.x + 'px' }">
        {{ Math.round(line.position) }}px
      </div>
    </div>

    <!-- 垂直辅助线 -->
    <div 
      v-for="line in verticalLines"
      :key="line.id"
      class="guide-line vertical"
      :style="{ left: line.position + 'px' }"
      @mousedown.prevent="startDragV($event, line)"
      @dblclick="deleteLine(line)"
    >
      <!-- 位置显示 -->
      <div class="guide-line-info" :style="{ top: infoPosition.y + 'px' }">
        {{ Math.round(line.position) }}px
      </div>
    </div>

    <!-- 辅助线创建区域 -->
    <div class="guide-line-rulers">
      <!-- 顶部标尺区域 - 用于创建水平辅助线 -->
      <div 
        class="ruler-area top"
        @mousedown.prevent="startCreateH"
      ></div>
      <!-- 左侧标尺区域 - 用于创建垂直辅助线 -->
      <div 
        class="ruler-area left"
        @mousedown.prevent="startCreateV"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'

const props = defineProps({
  width: {
    type: Number,
    required: true
  },
  height: {
    type: Number,
    required: true
  },
  snapThreshold: {
    type: Number,
    default: 5
  },
  snapTargets: {
    type: Array,
    default: () => []
  },
  showGuideLine: {
    type: Boolean,
    default: true
  }
})

// 辅助线数据
const horizontalLines = ref([])
const verticalLines = ref([])

// 拖动状态
let isDragging = false
let currentLine = null
let startY = 0
let startX = 0

// 信息显示位置
const infoPosition = ref({ x: 0, y: 0 })

// 开始创建新的水平辅助线
const startCreateH = (e) => {
  const newLine = {
    id: Date.now(),
    position: e.clientY,
    type: 'horizontal'
  }
  horizontalLines.value.push(newLine)
  startDragH(e, newLine)
}

// 开始创建新的垂直辅助线
const startCreateV = (e) => {
  const newLine = {
    id: Date.now(),
    position: e.clientX,
    type: 'vertical'
  }
  verticalLines.value.push(newLine)
  startDragV(e, newLine)
}

// 删除辅助线
const deleteLine = (line) => {
  if (line.type === 'horizontal') {
    horizontalLines.value = horizontalLines.value.filter(l => l.id !== line.id)
  } else {
    verticalLines.value = verticalLines.value.filter(l => l.id !== line.id)
  }
}

// 开始拖动
const startDragH = (e, line) => {
  isDragging = true
  currentLine = line
  startY = e.clientY - line.position
  document.addEventListener('mousemove', onDragH)
  document.addEventListener('mouseup', stopDrag)
}

const startDragV = (e, line) => {
  isDragging = true
  currentLine = line
  startX = e.clientX - line.position
  document.addEventListener('mousemove', onDragV)
  document.addEventListener('mouseup', stopDrag)
}

// 检查吸附
const checkSnap = (position, type) => {
  for (const target of props.snapTargets) {
    const targetPos = type === 'horizontal' ? target.y : target.x
    const diff = Math.abs(position - targetPos)
    
    if (diff <= props.snapThreshold) {
      return targetPos
    }
  }
  return position
}

// 更新信息显示位置
const updateInfoPosition = (e) => {
  infoPosition.value = {
    x: e.clientX,
    y: e.clientY
  }
}

// 拖动中
const onDragH = (e) => {
  if (!isDragging || !currentLine) return
  
  const newPosition = e.clientY - startY
  const snappedPosition = checkSnap(newPosition, 'horizontal')
  
  // 更新当前拖动的辅助线位置
  horizontalLines.value = horizontalLines.value.map(line => {
    if (line.id === currentLine.id) {
      return { ...line, position: snappedPosition }
    }
    return line
  })
  
  updateInfoPosition(e)
}

const onDragV = (e) => {
  if (!isDragging || !currentLine) return
  
  const newPosition = e.clientX - startX
  const snappedPosition = checkSnap(newPosition, 'vertical')
  
  // 更新当前拖动的辅助线位置
  verticalLines.value = verticalLines.value.map(line => {
    if (line.id === currentLine.id) {
      return { ...line, position: snappedPosition }
    }
    return line
  })
  
  updateInfoPosition(e)
}

// 停止拖动
const stopDrag = () => {
  isDragging = false
  currentLine = null
  document.removeEventListener('mousemove', onDragH)
  document.removeEventListener('mousemove', onDragV)
  document.removeEventListener('mouseup', stopDrag)
}

// 组件卸载时清理
onUnmounted(() => {
  document.removeEventListener('mousemove', onDragH)
  document.removeEventListener('mousemove', onDragV)
  document.removeEventListener('mouseup', stopDrag)
})
</script>

<style scoped>
.guide-line-container {
  position: absolute;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  z-index: 3;
  pointer-events: none;
}

.guide-line {
  position: absolute;
  background-color: #1890ff;
  opacity: 0.5;
  pointer-events: auto;
  z-index: 2;
  transition: opacity 0.2s;
}

.guide-line:hover {
  opacity: 0.8;
}

.guide-line.horizontal {
  left: 0;
  width: 100%;
  height: 1px;
  cursor: ns-resize;
}

.guide-line.vertical {
  top: 0;
  width: 1px;
  height: 100%;
  cursor: ew-resize;
}

.guide-line-info {
  position: absolute;
  background-color: #1890ff;
  color: white;
  padding: 2px 6px;
  border-radius: 2px;
  font-size: 12px;
  white-space: nowrap;
  pointer-events: none;
  transform: translate(-50%, -100%);
  z-index: 3;
}

.guide-line-rulers {
  position: absolute;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
}

.ruler-area {
  position: absolute;
  background-color: #f5f5f5;
  pointer-events: auto;
  cursor: pointer;
  transition: background-color 0.2s;
}

.ruler-area:hover {
  background-color: #e6e6e6;
}

.ruler-area.top {
  left: 20px;
  top: 0;
  right: 0;
  height: 20px;
  cursor: ns-resize;
  border-bottom: 1px solid #e5e7eb;
}

.ruler-area.left {
  left: 0;
  top: 20px;
  width: 20px;
  bottom: 0;
  cursor: ew-resize;
  border-right: 1px solid #e5e7eb;
}
</style> 