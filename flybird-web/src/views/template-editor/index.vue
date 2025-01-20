<template>
  <div class="template-editor">
    <!-- 顶部工具栏 -->
    <EditorToolbar
      :can-undo="canvasRef?.canUndo()"
      :can-redo="canvasRef?.canRedo()"
      @clear="handleClear"
      @save="handleSave"
      @undo="handleUndo"
      @redo="handleRedo"
    />

    <!-- 主要内容区域 -->
    <div class="editor-content">
      <!-- 左侧面板 -->
      <EditorSidebar />

      <!-- 中间画布区域 -->
      <div class="editor-main">
        <div class="canvas-container">
          <EditorCanvas
            ref="canvasRef"
            :scale="scale"
            :elements="getCurrentCanvas()?.elements || []"
            :canvas-list="templateData.canvases"
            :current-canvas-id="currentCanvasId"
            :canvas-config="getCurrentCanvas()?.config"
            :selected-element="selectedElement"
            @element-select="handleElementSelect"
            @elements-change="updateCanvasElements"
            @switch-canvas="switchCanvas"
            @add-canvas="addCanvas"
            @delete-canvas="removeCanvas"
          />
        </div>
        <div class="editor-footer">
          <span class="canvas-pages">Page {{ currentCanvasId }}/{{ templateData.canvases.length }}</span>
          <div class="footer-content">
            <div class="zoom-control">
              <button class="zoom-btn" @click="handleZoomOut" :disabled="scale <= MIN_SCALE">
                <Minus theme="outline" :size="16" />
              </button>
              <div class="zoom-slider">
                <div class="zoom-track" @mousedown="handleTrackClick">
                  <div class="zoom-progress" :style="{ width: `${((scale - MIN_SCALE) / (MAX_SCALE - MIN_SCALE)) * 100}%` }"></div>
                  <div class="zoom-ticks">
                    <div class="zoom-tick" style="left: 0%"></div>
                    <div class="zoom-tick" style="left: 25%"></div>
                    <div class="zoom-tick zoom-tick-100" style="left: 50%"></div>
                    <div class="zoom-tick" style="left: 75%"></div>
                    <div class="zoom-tick" style="left: 100%"></div>
                  </div>
                  <div 
                    class="zoom-handle" 
                    :style="{ left: `${((scale - MIN_SCALE) / (MAX_SCALE - MIN_SCALE)) * 100}%` }"
                    @mousedown.stop="startDrag"
                  >
                    <div class="zoom-tooltip">{{ Math.round(scale * 100) }}%</div>
                  </div>
                </div>
              </div>
              <button class="zoom-btn" @click="handleZoomIn" :disabled="scale >= MAX_SCALE">
                <Plus theme="outline" :size="16" />
              </button>
            </div>
            <button class="fullscreen-btn" @click="toggleFullscreen" :title="isFullscreen ? '退出全屏' : '全屏'">
              <FullScreen v-if="!isFullscreen" theme="outline" :size="18" />
              <OffScreen v-else theme="outline" :size="18" />
            </button>
          </div>
        </div>
      </div>

      <!-- 右侧属性面板 -->
      <EditorPanel
        :element="selectedElement"
        :canvas-list="templateData.canvases"
        :current-canvas-id="currentCanvasId"
        :canvas-config="getCurrentCanvas()?.config"
        @update="handleElementUpdate"
        @add-canvas="addCanvas"
        @delete-canvas="removeCanvas"
        @switch-canvas="switchCanvas"
        @update-canvas-config="updateCanvasConfig"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Minus, Plus, FullScreen, OffScreen } from '@icon-park/vue-next'
import EditorCanvas from './components/EditorCanvas.vue'
import EditorToolbar from './components/EditorToolbar.vue'
import EditorSidebar from './components/EditorSidebar.vue'
import EditorPanel from './components/EditorPanel.vue'

// 导入组合式函数
import { useZoom } from './composables/useZoom'
import { useCanvas } from './composables/useCanvas'
import { useCanvasConfig } from './composables/useCanvasConfig'

// 画布引用
const canvasRef = ref(null)

// 使用组合式函数
const { scale, MIN_SCALE, MAX_SCALE, SCALE_STEP, handleZoomIn, handleZoomOut, handleZoomChange } = useZoom()
const { 
  templateData,
  currentCanvasId, 
  addCanvas, 
  removeCanvas, 
  switchCanvas, 
  getCurrentCanvas,
  updateCanvasElements,
  updateCanvasConfig,
  A4_CONFIG,
  selectedElement,
  handleElementSelect,
  handleElementUpdate,
  handleClear,
  handleSave
} = useCanvas()

const { canvasConfig } = useCanvasConfig()

const handleTrackClick = (e) => {
  if (e.target.classList.contains('zoom-handle')) return
  
  const slider = e.currentTarget.closest('.zoom-slider')
  const sliderRect = slider.getBoundingClientRect()
  const sliderWidth = sliderRect.width - 20
  const left = Math.max(0, Math.min(sliderWidth, e.clientX - sliderRect.left - 10))
  const percentage = left / sliderWidth
  const newScale = MIN_SCALE + percentage * (MAX_SCALE - MIN_SCALE)
  handleZoomChange(Number(newScale.toFixed(2)))
}

const startDrag = (e) => {
  e.preventDefault()
  
  const handle = e.target
  const slider = handle.closest('.zoom-slider')
  const sliderRect = slider.getBoundingClientRect()
  const sliderWidth = sliderRect.width - 20  // 减去左右padding
  
  const updatePosition = (clientX) => {
    const left = Math.max(0, Math.min(sliderWidth, clientX - sliderRect.left - 10))  // 10是左padding
    const percentage = left / sliderWidth
    const newScale = MIN_SCALE + percentage * (MAX_SCALE - MIN_SCALE)
    handleZoomChange(Number(newScale.toFixed(2)))
  }
  
  const handleDrag = (e) => {
    e.preventDefault()
    updatePosition(e.clientX)
  }
  
  const stopDrag = () => {
    document.removeEventListener('mousemove', handleDrag)
    document.removeEventListener('mouseup', stopDrag)
    document.body.style.cursor = ''
    document.body.style.userSelect = ''
  }
  
  document.body.style.cursor = 'grabbing'
  document.body.style.userSelect = 'none'
  
  document.addEventListener('mousemove', handleDrag)
  document.addEventListener('mouseup', stopDrag)
}

// 全屏状态
const isFullscreen = ref(false)

// 切换全屏
const toggleFullscreen = () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen()
    isFullscreen.value = true
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen()
      isFullscreen.value = false
    }
  }
}

// 监听全屏变化
onMounted(() => {
  document.addEventListener('fullscreenchange', () => {
    isFullscreen.value = !!document.fullscreenElement
  })
})

onUnmounted(() => {
  document.removeEventListener('fullscreenchange', () => {
    isFullscreen.value = !!document.fullscreenElement
  })
})

// 处理元素更新
const handleElementsChange = (newElements) => {
  // Implementation needed
}

// 处理撤销
const handleUndo = () => {
  canvasRef.value?.handleUndo()
}

// 处理重做
const handleRedo = () => {
  canvasRef.value?.handleRedo()
}
</script>

<style>
@import './styles/editor.css';
@import './styles/drag.css';
</style>

<style scoped>
@import './styles/editor.css';

.editor-footer {
  padding: 8px 24px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  display: flex;
  align-items: center;
  background: #fff;
  box-shadow: 0 -1px 2px rgba(0, 0, 0, 0.02);
}

.canvas-pages {
  font-size: 13px;
  color: #666;
  margin-right: auto;
  font-weight: 500;
}

.footer-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.zoom-control {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(to bottom, #fafafa, #f5f5f5);
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 8px;
  padding: 4px;
  box-shadow: 
    0 1px 2px rgba(0, 0, 0, 0.04),
    inset 0 1px 1px rgba(255, 255, 255, 0.9);
}

.zoom-slider {
  width: 140px;
  height: 28px;
  position: relative;
  display: flex;
  align-items: center;
  padding: 0 10px;
}

.zoom-track {
  width: 100%;
  height: 4px;
  background: #e8e8e8;
  border-radius: 2px;
  position: relative;
}

.zoom-progress {
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  background: #1890ff;
  border-radius: 2px;
}

.zoom-handle {
  position: absolute;
  top: 50%;
  width: 16px;
  height: 16px;
  margin-top: -8px;
  margin-left: -8px;
  background: white;
  border: 2px solid #1890ff;
  border-radius: 50%;
  cursor: grab;
  transition: transform 0.2s;
  z-index: 10;
}

.zoom-handle:hover {
  transform: scale(1.1);
}

.zoom-handle:active {
  cursor: grabbing;
  transform: scale(1.1);
}

.zoom-ticks {
  position: absolute;
  left: 0;
  right: 0;
  top: 50%;
  margin-top: -3px;
  height: 6px;
  pointer-events: none;
}

.zoom-tick {
  position: absolute;
  width: 2px;
  height: 6px;
  background: #e8e8e8;
  margin-left: -1px;
}

.zoom-tick-100 {
  height: 8px;
  margin-top: -1px;
  background: #d9d9d9;
}

.zoom-tooltip {
  position: absolute;
  top: -25px;
  left: 50%;
  transform: translateX(-50%);
  background: #1890ff;
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
  white-space: nowrap;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.2s;
}

.zoom-handle:hover .zoom-tooltip {
  opacity: 1;
}

.zoom-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: none;
  background: transparent;
  color: #666;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 6px;
}

.zoom-btn:hover:not(:disabled) {
  color: #1890ff;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 
    0 2px 6px rgba(24, 144, 255, 0.1),
    inset 0 1px 1px rgba(255, 255, 255, 1);
}

.zoom-btn:active:not(:disabled) {
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 
    0 1px 2px rgba(24, 144, 255, 0.1),
    inset 0 1px 1px rgba(255, 255, 255, 1);
}

.zoom-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.fullscreen-btn {
  position: absolute;
  right: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
  border-radius: 6px;
}

.fullscreen-btn:hover {
  color: #1890ff;
  background: rgba(24, 144, 255, 0.1);
}

.fullscreen-btn:active {
  background: rgba(24, 144, 255, 0.2);
}
</style> 