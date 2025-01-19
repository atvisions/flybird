<template>
  <div class="editor-canvas">
    <!-- 画布区域 -->
    <div class="canvas-list">
      <!-- 画布项 -->
      <div 
        v-for="canvas in currentCanvas"
        :key="canvas.id"
        class="canvas-item"
      >
        <div 
          class="canvas-scale-container"
          :style="{ transform: `scale(${scale})` }"
        >
          <!-- 拖拽提示区域 -->
          <div 
            class="drop-area"
            :class="{ 'is-dragging': isDragging }"
            @dragenter.prevent="handleDragEnter"
            @dragleave.prevent="handleDragLeave"
            @dragover.prevent="handleDragOver"
            @drop.prevent="handleDrop"
          >
            <div v-if="elements.length === 0" class="empty-tip">
              <p>从左侧拖拽组件到这里</p>
            </div>
          </div>

          <div 
            class="canvas-content"
            :style="{
              backgroundColor: canvasConfig?.backgroundColor || '#ffffff'
            }"
            @mousedown.self="handleCanvasClick"
          >
            <!-- 网格背景 -->
            <div 
              v-if="canvasConfig?.showGrid"
              class="canvas-grid"
              :style="{
                backgroundSize: `${canvasConfig?.gridSize || 20}px ${canvasConfig?.gridSize || 20}px`,
                backgroundImage: `linear-gradient(to right, ${canvasConfig?.gridColor || 'rgba(0, 0, 0, 0.05)'} 1px, transparent 1px),
                  linear-gradient(to bottom, ${canvasConfig?.gridColor || 'rgba(0, 0, 0, 0.05)'} 1px, transparent 1px)`
              }"
            ></div>

            <!-- 标尺 -->
            <div 
              v-if="canvasConfig?.showRuler"
              class="canvas-ruler"
            >
              <!-- 水平标尺 -->
              <div class="ruler ruler-h"></div>
              <!-- 垂直标尺 -->
              <div class="ruler ruler-v"></div>
              <!-- 标尺交叉点 -->
              <div class="ruler-corner"></div>
            </div>

            <!-- 元素列表 -->
            <template v-for="element in elements" :key="element.id">
              <component
                :is="getElementComponent(element.type)"
                v-bind="element"
                :selected="selectedId === element.id"
                @select="handleSelect(element)"
                @update="handleUpdate"
              />
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import BaseShape from './BaseShape.vue'
import TextBlock from './TextBlock.vue'

const props = defineProps({
  scale: {
    type: Number,
    default: 1
  },
  elements: {
    type: Array,
    default: () => []
  },
  canvasList: {
    type: Array,
    required: true
  },
  currentCanvasId: {
    type: Number,
    required: true
  },
  canvasConfig: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['element-select', 'elements-change'])

// 当前选中的元素ID
const selectedId = ref(null)

// 根据类型获取对应的组件
const getElementComponent = (type) => {
  const componentMap = {
    'shape': BaseShape,
    'text': TextBlock
  }
  return componentMap[type]
}

// 选择元素
const handleSelect = (element) => {
  selectedId.value = element.id
  emit('element-select', element)
}

// 点击画布空白处取消选中
const handleCanvasClick = (e) => {
  // 如果点击的是画布本身（而不是其中的元素），则取消选中
  if (e.target.classList.contains('canvas-content')) {
    selectedId.value = null
    emit('element-select', null)
  }
}

// 更新元素
const handleUpdate = (updatedElement) => {
  const newElements = props.elements.map(el => 
    el.id === updatedElement.id ? updatedElement : el
  )
  emit('elements-change', newElements)
}

// 处理拖放
const handleDrop = (event) => {
  event.preventDefault()
  event.stopPropagation()
  isDragging.value = false
  
  try {
    // 获取拖拽数据
    const dragData = JSON.parse(event.dataTransfer.getData('text/plain'))
    console.log('Drop data:', dragData)
    
    // 获取相对于画布的位置
    const rect = event.currentTarget.getBoundingClientRect()
    const x = (event.clientX - rect.left) / props.scale
    const y = (event.clientY - rect.top) / props.scale

    // 创建新元素
    const newElement = {
      id: Date.now(),
      type: dragData.type,
      subType: dragData.subType,
      x,
      y,
      width: dragData.defaultConfig.width,
      height: dragData.defaultConfig.height,
      backgroundColor: dragData.defaultConfig.backgroundColor,
      borderColor: dragData.defaultConfig.borderColor,
      borderWidth: dragData.defaultConfig.borderWidth,
      borderStyle: dragData.defaultConfig.borderStyle,
      rotation: dragData.defaultConfig.rotation
    }

    console.log('New element:', newElement)

    // 添加到元素列表
    const newElements = [...props.elements, newElement]
    emit('elements-change', newElements)
    
    // 选中新添加的元素
    handleSelect(newElement)
  } catch (error) {
    console.error('Failed to handle drop:', error)
  }
}

// 拖拽状态
const isDragging = ref(false)

// 拖拽相关事件
const handleDragEnter = (e) => {
  e.preventDefault()
  e.stopPropagation()
  isDragging.value = true
}

const handleDragLeave = (e) => {
  e.preventDefault()
  e.stopPropagation()
  if (e.target === e.currentTarget) {
    isDragging.value = false
  }
}

const handleDragOver = (e) => {
  e.preventDefault()
  e.stopPropagation()
  e.dataTransfer.dropEffect = 'copy'
}

// 当前显示的画布
const currentCanvas = computed(() => {
  return props.canvasList.filter(canvas => canvas.id === props.currentCanvasId)
})
</script>

<style scoped>
.editor-canvas {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #e5e5e5;
}

.canvas-list {
  flex: 1;
  overflow: auto;
  background-color: #f0f0f0;
  padding: 0 40px;
}

.canvas-item {
  flex-shrink: 0;
  display: flex;
  justify-content: center;
  margin: 40px auto;
}

.canvas-scale-container {
  width: 794px; /* A4 纸张宽度 */
  height: 1123px; /* A4 纸张高度 */
  position: relative;
  transform-origin: top center;
}

.canvas-content {
  width: 100%;
  height: 100%;
  background-color: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: visible;
}

.drop-area {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  pointer-events: none;
  transition: all 0.2s;
}

.drop-area.is-dragging {
  background-color: rgba(24, 144, 255, 0.1);
  border: 2px dashed #1890ff;
  pointer-events: auto;
  z-index: 999;
}

.empty-tip {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-size: 14px;
  pointer-events: none;
  z-index: 1;
}

/* 网格和标尺样式 */
.canvas-grid,
.canvas-ruler {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 1;
}

/* 元素层级管理 */
.canvas-content > * {
  position: relative;
}

.base-shape {
  z-index: 100;
}

.base-shape.selected {
  z-index: 101;
}

.empty-tip {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-size: 14px;
  pointer-events: none;
  z-index: 1;
}
</style> 