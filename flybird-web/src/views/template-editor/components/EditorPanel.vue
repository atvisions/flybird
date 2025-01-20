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
        </div>

        <div class="panel-section">
          <h4>样式</h4>
          <!-- 形状通用样式设置 -->
          <template v-if="['rectangle', 'circle', 'triangle', 'star'].includes(element.type)">
            <div class="form-group">
              <label>背景颜色</label>
              <div class="color-picker">
                <input 
                  type="color" 
                  :value="element.props?.fill || '#ffffff'"
                  @input="(e) => updateElementProp('props', {
                    ...element.props,
                    fill: e.target.value
                  })"
                >
                <input 
                  type="text"
                  :value="element.props?.fill || '#ffffff'"
                  @input="(e) => updateElementProp('props', {
                    ...element.props,
                    fill: e.target.value
                  })"
                  placeholder="#FFFFFF"
                >
              </div>
            </div>

            <div class="form-group">
              <label>边框</label>
              <div class="border-settings">
                <div class="input-group">
                  <input
                    type="number"
                    :value="element.props?.strokeWidth || 1"
                    @input="(e) => updateElementProp('props', {
                      ...element.props,
                      strokeWidth: Math.max(0, parseInt(e.target.value) || 0)
                    })"
                    min="0"
                    max="20"
                    placeholder="粗细"
                  >
                  <span class="unit">px</span>
                </div>
                <select
                  :value="element.props?.strokeStyle || 'solid'"
                  @change="(e) => updateElementProp('props', {
                    ...element.props,
                    strokeStyle: e.target.value
                  })"
                >
                  <option value="solid">实线</option>
                  <option value="dashed">虚线</option>
                  <option value="dotted">点线</option>
                </select>
                <div class="color-picker">
                  <input
                    type="color"
                    :value="element.props?.stroke || '#000000'"
                    @input="(e) => updateElementProp('props', {
                      ...element.props,
                      stroke: e.target.value
                    })"
                  >
                  <input 
                    type="text"
                    :value="element.props?.stroke || '#000000'"
                    @input="(e) => updateElementProp('props', {
                      ...element.props,
                      stroke: e.target.value
                    })"
                    placeholder="#000000"
                  >
                </div>
              </div>
            </div>

            <!-- 如果是矩形，显示圆角设置 -->
            <template v-if="element.type === 'rectangle'">
              <div class="form-group">
                <label>圆角</label>
                <div class="radius-control">
                  <input
                    type="range"
                    :value="element.props?.radius || 0"
                    @input="(e) => {
                      const value = Math.min(50, Math.max(0, parseInt(e.target.value) || 0))
                      updateElementProp('props', {
                        ...element.props,
                        radius: value
                      })
                    }"
                    min="0"
                    max="50"
                    step="1"
                  >
                  <div class="input-group">
                    <input 
                      type="number" 
                      min="0"
                      max="50"
                      :value="element.props?.radius || 0"
                      @input="(e) => {
                        const value = Math.min(50, Math.max(0, parseInt(e.target.value) || 0))
                        updateElementProp('props', {
                          ...element.props,
                          radius: value
                        })
                      }"
                    >
                    <span class="unit">px</span>
                  </div>
                </div>
              </div>
            </template>
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
            <div class="z-index-group">
              <div class="z-index-control">
                <button 
                  class="btn-stepper"
                  @click="updateElementProp('zIndex', Math.max(1, (element.zIndex || 1) - 1))"
                >-</button>
                <input
                  type="number"
                  :value="element.zIndex || 1"
                  @input="(e) => updateElementProp('zIndex', Math.max(1, parseInt(e.target.value) || 1))"
                  min="1"
                  step="1"
                >
                <button 
                  class="btn-stepper"
                  @click="updateElementProp('zIndex', (element.zIndex || 1) + 1)"
                >+</button>
              </div>
              <button 
                class="btn-arrow"
                title="置于顶层"
                @click="updateElementProp('zIndex', 9999)"
              >
                <Up theme="filled" size="16" fill="#374151" />
              </button>
              <button 
                class="btn-arrow"
                title="置于底层"
                @click="updateElementProp('zIndex', 1)"
              >
                <Down theme="filled" size="16" fill="#374151" />
              </button>
            </div>
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
import { 
  AlignTextLeft, 
  AlignTextCenter, 
  AlignTextRight, 
  Delete, 
  Plus, 
  Setting,
  Up,
  Down
} from '@icon-park/vue-next'
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
  if (!props.element) return

  // 直接更新属性，保持与画布组件相同的更新逻辑
  emit('update', {
    ...props.element,
    [prop]: value
  })
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
.editor-panel {
  padding: 10px;
  height: 100%;
  overflow-y: auto;
}

.panel-content {
  display: flex;
  flex-direction: column;
}

.panel-section {
  padding: 8px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);
}

h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 12px;
}

h4 {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 10px;
}

.form-group {
  margin-bottom: 12px;
}

.form-group:last-child {
  margin-bottom: 0;
}

label {
  display: block;
  font-size: 13px;
  color: #4b5563;
  margin-bottom: 8px;
}

.input-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.input-group input[type="number"],
.input-group input[type="text"],
.input-group select {
  flex: 1;
  height: 32px;
  padding: 0 12px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 13px;
  color: #374151;
  background-color: #fff;
  transition: all 0.2s;
}

.input-group input[type="number"]:hover,
.input-group input[type="text"]:hover,
.input-group select:hover {
  border-color: #a5b4fc;
}

.input-group input[type="number"]:focus,
.input-group input[type="text"]:focus,
.input-group select:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.1);
  outline: none;
}

.color-picker {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
}

.color-picker input[type="color"] {
  width: 36px;
  height: 36px;
  padding: 2px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  cursor: pointer;
  background-color: #fff;
  transition: all 0.2s;
}

.color-picker input[type="text"] {
  flex: 1;
  height: 36px;
  padding: 0 12px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 13px;
  color: #374151;
}

.border-settings {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.button-group {
  display: flex;
  gap: 8px;
}

.btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  background-color: #fff;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.btn:hover {
  border-color: #a5b4fc;
  color: #4f46e5;
}

.btn.active {
  background-color: #4f46e5;
  border-color: #4f46e5;
  color: #fff;
}

.unit {
  color: #6b7280;
  font-size: 13px;
}

input[type="range"] {
  width: 100%;
  height: 4px;
  background: #e5e7eb;
  border-radius: 2px;
  outline: none;
  -webkit-appearance: none;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  background: #fff;
  border: 2px solid #4f46e5;
  border-radius: 50%;
  cursor: pointer;
}

textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 13px;
  color: #374151;
  resize: vertical;
  min-height: 80px;
}

textarea:hover {
  border-color: #a5b4fc;
}

textarea:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.1);
  outline: none;
}

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

.border-settings {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.border-settings .input-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.border-settings select {
  height: 32px;
  padding: 0 8px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  background-color: #fff;
  cursor: pointer;
}

.border-settings select:hover {
  border-color: #40a9ff;
}

.border-settings select:focus {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
  outline: none;
}

.color-picker {
  display: flex;
  align-items: center;
  gap: 8px;
}

.color-picker input[type="color"] {
  width: 32px;
  height: 32px;
  padding: 2px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  cursor: pointer;
  background-color: #fff;
}

.color-picker input[type="color"]:hover {
  border-color: #40a9ff;
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

.color-picker input[type="text"]:hover {
  border-color: #40a9ff;
}

.color-picker input[type="text"]:focus {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
  outline: none;
}

.input-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.input-group input[type="number"] {
  width: 60px;
  height: 32px;
  padding: 0 8px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 14px;
  color: #333;
}

.input-group input[type="number"]:hover {
  border-color: #40a9ff;
}

.input-group input[type="number"]:focus {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
  outline: none;
}

.unit {
  color: #999;
  font-size: 14px;
}

.radius-control {
  display: flex;
  align-items: center;
  gap: 12px;
}

.radius-control input[type="range"] {
  flex: 1;
  height: 4px;
  background: #e5e7eb;
  border-radius: 2px;
  outline: none;
  -webkit-appearance: none;
}

.radius-control input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  background: #fff;
  border: 2px solid #4f46e5;
  border-radius: 50%;
  cursor: pointer;
}

.radius-control .input-group {
  width: 80px;
  flex-shrink: 0;
}

.radius-control .input-group input[type="number"] {
  width: 100%;
}

.z-index-group {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
}

.z-index-control {
  flex: 1;
  display: flex;
  align-items: center;
  height: 32px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  overflow: hidden;
}

.z-index-control input[type="number"] {
  flex: 1;
  height: 100%;
  border: none;
  text-align: center;
  font-size: 14px;
  color: #374151;
  padding: 0;
  -moz-appearance: textfield;
  min-width: 40px;
}

.z-index-control input[type="number"]::-webkit-outer-spin-button,
.z-index-control input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.btn-stepper {
  width: 32px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f9fafb;
  border: none;
  color: #374151;
  font-size: 16px;
  font-weight: normal;
  cursor: pointer;
  transition: all 0.2s;
  padding: 0;
  line-height: 1;
}

.btn-stepper:hover {
  background: #f3f4f6;
  color: #4f46e5;
}

.btn-stepper:active {
  background: #e5e7eb;
}

.btn-arrow {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s;
  padding: 0;
}

.btn-arrow:hover {
  background: #f3f4f6;
  border-color: #a5b4fc;
  color: #4f46e5;
}

.btn-arrow:active {
  background: #e5e7eb;
}

.btn-arrow svg {
  width: 16px;
  height: 16px;
}
</style> 