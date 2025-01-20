<template>
  <div class="editor-panel">
    <div class="panel-content">
      <!-- 元素属性设置 -->
      <template v-if="element">
        <h3>元素属性</h3>
        <div class="panel-section">
          <h4>位置和大小</h4>
          <div class="form-group">
            <label>位置</label>
            <div class="input-group">
              <input
                type="number"
                :value="element.x"
                @input="updateElementProp('x', $event.target.value)"
                placeholder="X"
              >
              <input
                type="number"
                :value="element.y"
                @input="updateElementProp('y', $event.target.value)"
                placeholder="Y"
              >
            </div>
          </div>
          <div class="form-group">
            <label>尺寸</label>
            <div class="input-group">
              <input
                type="number"
                :value="element.width"
                @input="updateElementProp('width', $event.target.value)"
                placeholder="宽度"
              >
              <input
                type="number"
                :value="element.height"
                @input="updateElementProp('height', $event.target.value)"
                placeholder="高度"
              >
            </div>
          </div>
          <div class="form-group">
            <label>旋转</label>
            <input
              type="range"
              :value="element.rotation"
              @input="updateElementProp('rotation', $event.target.value)"
              min="0"
              max="360"
            >
          </div>
        </div>

        <div class="panel-section">
          <h4>样式</h4>
          <template v-if="element.type === 'shape'">
            <div class="form-group">
              <label>背景色</label>
              <input
                type="color"
                :value="element.backgroundColor"
                @input="updateElementProp('backgroundColor', $event.target.value)"
              >
            </div>
            <div class="form-group">
              <label>边框</label>
              <div class="input-group">
                <input
                  type="number"
                  :value="element.borderWidth"
                  @input="updateElementProp('borderWidth', $event.target.value)"
                  placeholder="边框宽度"
                >
                <select
                  :value="element.borderStyle"
                  @change="updateElementProp('borderStyle', $event.target.value)"
                >
                  <option value="solid">实线</option>
                  <option value="dashed">虚线</option>
                  <option value="dotted">点线</option>
                </select>
                <input
                  type="color"
                  :value="element.borderColor"
                  @input="updateElementProp('borderColor', $event.target.value)"
                >
              </div>
            </div>
          </template>

          <template v-if="element.type === 'text'">
            <div class="form-group">
              <label>文本内容</label>
              <textarea
                :value="element.content"
                @input="updateElementProp('content', $event.target.value)"
                rows="3"
              ></textarea>
            </div>
            <div class="form-group">
              <label>字体</label>
              <div class="input-group">
                <select
                  :value="element.fontFamily"
                  @change="updateElementProp('fontFamily', $event.target.value)"
                >
                  <option value="Arial">Arial</option>
                  <option value="Microsoft YaHei">微软雅黑</option>
                  <option value="SimSun">宋体</option>
                </select>
                <input
                  type="number"
                  :value="element.fontSize"
                  @input="updateElementProp('fontSize', $event.target.value)"
                  min="12"
                  max="72"
                  step="1"
                >
              </div>
            </div>
            <div class="form-group">
              <label>文字颜色</label>
              <input
                type="color"
                :value="element.color"
                @input="updateElementProp('color', $event.target.value)"
              >
            </div>
            <div class="form-group">
              <label>对齐方式</label>
              <div class="button-group">
                <button
                  class="btn"
                  :class="{ active: element.textAlign === 'left' }"
                  @click="updateElementProp('textAlign', 'left')"
                >
                  <AlignTextLeft theme="outline" size="16" />
                </button>
                <button
                  class="btn"
                  :class="{ active: element.textAlign === 'center' }"
                  @click="updateElementProp('textAlign', 'center')"
                >
                  <AlignTextCenter theme="outline" size="16" />
                </button>
                <button
                  class="btn"
                  :class="{ active: element.textAlign === 'right' }"
                  @click="updateElementProp('textAlign', 'right')"
                >
                  <AlignTextRight theme="outline" size="16" />
                </button>
              </div>
            </div>
          </template>
        </div>

        <div class="panel-section">
          <h4>层级</h4>
          <div class="form-group">
            <label>层级</label>
            <input
              type="number"
              :value="element.zIndex"
              @input="updateElementProp('zIndex', $event.target.value)"
              min="1"
              step="1"
            >
          </div>
        </div>
      </template>

      <!-- 画布设置 -->
      <template v-else>
        <h3>画布设置</h3>
        
        <!-- 画布管理 -->
        <div class="panel-section">
          <h4>画布管理</h4>
          <div class="canvas-list">
            <div 
              v-for="canvas in canvasList" 
              :key="canvas.id"
              class="canvas-item"
              :class="{ active: currentCanvasId === canvas.id }"
              @click="$emit('switch-canvas', canvas.id)"
            >
              <div class="canvas-preview" :style="{ backgroundColor: canvas.config.backgroundColor }">
                <div class="canvas-overlay"></div>
              </div>
              <div class="canvas-index">{{ canvas.id }}</div>
              <button 
                v-if="canvas.id !== 1"
                class="btn-icon" 
                @click.stop="$emit('delete-canvas', canvas.id)"
              >
                <Delete theme="outline" size="12" />
              </button>
            </div>
            <button 
              v-if="canvasList.length < 5"
              class="btn-add" 
              @click="$emit('add-canvas')"
            >
              <Plus theme="outline" size="14" />
            </button>
          </div>
        </div>

        <!-- 画布属性 -->
        <div class="panel-section">
          <h4>画布属性</h4>
          
          <!-- 背景设置 -->
          <div class="form-group">
            <div class="form-header">
              <label>背景颜色</label>
              <div class="form-actions">
                <button 
                  class="btn-text"
                  @click="applyToAllCanvas"
                >
                  应用到所有画布
                </button>
              </div>
            </div>
            <div class="color-picker">
              <input 
                type="color" 
                :value="getCurrentCanvas()?.config?.backgroundColor || '#ffffff'"
                @input="updateBackgroundColor($event.target.value)"
              >
              <input 
                type="text"
                :value="getCurrentCanvas()?.config?.backgroundColor || '#ffffff'"
                @input="updateBackgroundColor($event.target.value)"
                placeholder="#FFFFFF"
              >
            </div>
          </div>
        </div>

        <!-- 辅助功能 -->
        <div class="panel-section">
          <h4>辅助功能</h4>
          <div class="switch-list">
            <!-- 网格 -->
            <div class="switch-item">
              <div class="switch-header">
                <div class="switch-text-group">
                  <span class="switch-text">显示网格</span>
                  <button 
                    v-if="getCurrentCanvas()?.config?.showGrid"
                    class="btn-icon"
                    @click="showGridSettings = !showGridSettings"
                  >
                    <Setting theme="outline" size="14" />
                  </button>
                </div>
                <Switch 
                  :model-value="getCurrentCanvas()?.config?.showGrid"
                  @update:model-value="(value) => handleConfigChange('showGrid', value)"
                />
              </div>
              <!-- 网格设置 -->
              <div v-if="getCurrentCanvas()?.config?.showGrid && showGridSettings" class="switch-settings">
                <div class="form-group">
                  <label>网格大小</label>
                  <div class="input-group">
                    <input 
                      type="number"
                      :value="getCurrentCanvas()?.config?.gridSize"
                      @input="(e) => handleConfigChange('gridSize', Number(e.target.value))"
                      min="5"
                      max="50"
                      step="5"
                    >
                    <span class="unit">px</span>
                  </div>
                </div>
                <div class="form-group">
                  <label>网格颜色</label>
                  <div class="color-picker">
                    <input 
                      type="color"
                      :value="getCurrentCanvas()?.config?.gridColor"
                      @input="(e) => handleConfigChange('gridColor', e.target.value)"
                    >
                    <input 
                      type="text"
                      :value="getCurrentCanvas()?.config?.gridColor"
                      @input="(e) => handleConfigChange('gridColor', e.target.value)"
                      placeholder="rgba(0, 0, 0, 0.1)"
                    >
                  </div>
                </div>
              </div>
            </div>

            <!-- 标尺 -->
            <div class="switch-item">
              <div class="switch-header">
                <span class="switch-text">显示标尺</span>
                <Switch 
                  :model-value="getCurrentCanvas()?.config?.showRuler"
                  @update:model-value="(value) => handleConfigChange('showRuler', value)"
                />
              </div>
            </div>

            <!-- 辅助线 -->
            <div class="switch-item">
              <div class="switch-header">
                <span class="switch-text">显示辅助线</span>
                <Switch 
                  :model-value="getCurrentCanvas()?.config?.showGuides"
                  @update:model-value="(value) => handleConfigChange('showGuides', value)"
                />
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { AlignTextLeft, AlignTextCenter, AlignTextRight, Delete, Plus, Setting } from '@icon-park/vue-next'
import Switch from './Switch.vue'

const props = defineProps({
  element: {
    type: Object,
    default: null
  },
  canvasList: {
    type: Array,
    required: true
  },
  currentCanvasId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits([
  'update',
  'add-canvas',
  'delete-canvas',
  'switch-canvas',
  'update-canvas-config'
])

// 获取当前画布
const getCurrentCanvas = () => {
  return props.canvasList.find(canvas => canvas.id === props.currentCanvasId)
}

// 更新元素属性
const updateElementProp = (prop, value) => {
  if (props.element) {
    emit('update', {
      ...props.element,
      [prop]: value
    })
  }
}

// 更新画布配置
const handleConfigChange = (key, value) => {
  console.log('EditorPanel handleConfigChange:', key, value)
  const currentCanvas = getCurrentCanvas()
  if (currentCanvas) {
    emit('update-canvas-config', { [key]: value }, false)
  }
}

// 更新背景颜色
const updateBackgroundColor = (color) => {
  handleConfigChange('backgroundColor', color)
}

// 应用到所有画布
const applyToAllCanvas = () => {
  const currentCanvas = getCurrentCanvas()
  if (currentCanvas?.config?.backgroundColor) {
    emit('update-canvas-config', { backgroundColor: currentCanvas.config.backgroundColor }, true)
  }
}

// 控制网格设置的显示/隐藏
const showGridSettings = ref(false)

// 计算文字颜色（根据背景色自动调整）
const getContrastColor = (backgroundColor) => {
  // 移除可能的空格和#号
  const hex = backgroundColor.replace(/\s/g, '').replace('#', '')
  
  // 转换为RGB
  const r = parseInt(hex.substring(0, 2), 16)
  const g = parseInt(hex.substring(2, 4), 16)
  const b = parseInt(hex.substring(4, 6), 16)
  
  // 计算亮度
  const brightness = (r * 299 + g * 587 + b * 114) / 1000
  
  // 根据亮度返回黑色或白色
  return brightness > 128 ? '#333333' : '#ffffff'
}
</script>

<style scoped>
.canvas-list {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 8px 0;
}

.canvas-pages {
  font-size: 13px;
  color: #666;
}

.canvas-items {
  display: flex;
  gap: 6px;
}

.canvas-item {
  width: 40px;
  height: 55px;
  position: relative;
  background-color: #fff;
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  overflow: hidden;
  box-shadow: 
    0 1px 2px rgba(0, 0, 0, 0.04),
    0 2px 4px rgba(0, 0, 0, 0.02);
}

.canvas-item:hover {
  transform: translateY(-1px);
  box-shadow: 
    0 2px 4px rgba(0, 0, 0, 0.06),
    0 4px 8px rgba(0, 0, 0, 0.04);
}

.canvas-item.active {
  border-color: #1890ff;
  box-shadow: 
    0 0 0 2px rgba(24, 144, 255, 0.2),
    0 2px 4px rgba(0, 0, 0, 0.04);
}

.canvas-preview {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 5px;
  transition: all 0.3s;
  overflow: hidden;
}

.canvas-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    to bottom,
    rgba(255, 255, 255, 0.1),
    rgba(0, 0, 0, 0.05)
  );
  pointer-events: none;
  z-index: 1;
}

.canvas-index {
  position: absolute;
  bottom: 4px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 11px;
  color: #666;
  background: rgba(255, 255, 255, 0.9);
  padding: 1px 6px;
  border-radius: 10px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  z-index: 2;
}

.btn-icon {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 16px;
  height: 16px;
  padding: 2px;
  border: none;
  background: rgba(255, 255, 255, 0.9);
  color: #666;
  cursor: pointer;
  opacity: 0;
  z-index: 3;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-icon:hover {
  background: #fff;
  color: #ff4d4f;
  transform: scale(1.1);
}

.canvas-item:hover .btn-icon {
  opacity: 1;
}

/* 继承现有的样式 */
@import '../styles/panel.css';
@import '../styles/controls.css';

.switch-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.switch-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.switch-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 0;
}

.switch-text {
  font-size: 13px;
  color: #666;
}

.switch-controls {
  display: flex;
  align-items: center;
  gap: 4px;
}

.switch-settings {
  margin-left: 0;
  margin-top: 8px;
  padding: 8px;
  background-color: #fafafa;
  border-radius: 4px;
}

.unit {
  color: #999;
  margin-left: 4px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.section-header h4 {
  margin: 0;
}

.switch-text-group {
  display: flex;
  align-items: center;
  gap: 4px;
}

.switch-text {
  font-size: 13px;
  color: #666;
}

.btn-add {
  width: 40px;
  height: 55px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px dashed #d9d9d9;
  background: none;
  color: #999;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.2s;
}

.btn-add:hover {
  color: #1890ff;
  border-color: #1890ff;
  background-color: #e6f7ff;
}

.zoom-control {
  display: none;
}

.form-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.form-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-text {
  padding: 4px 8px;
  border: none;
  background: none;
  color: #666;
  font-size: 12px;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.3s;
}

.btn-text:hover {
  color: #1890ff;
  background: rgba(24, 144, 255, 0.1);
}

.color-picker {
  display: flex;
  align-items: center;
  gap: 8px;
}

.color-picker input[type="color"] {
  width: 32px;
  height: 32px;
  padding: 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.color-picker input[type="text"] {
  flex: 1;
  height: 32px;
  padding: 0 8px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 14px;
  color: #333;
}
</style> 