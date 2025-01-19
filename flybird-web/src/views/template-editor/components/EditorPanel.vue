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
              <div class="canvas-info">
                <span class="canvas-name">{{ canvas.id }}</span>
                <button 
                  v-if="canvas.id !== 1"
                  class="btn-icon" 
                  @click.stop="$emit('delete-canvas', canvas.id)"
                >
                  <Delete theme="outline" size="12" />
                </button>
              </div>
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
          
          <!-- 缩放控制 -->
          <div class="zoom-control">
            <span class="canvas-pages">{{ currentCanvasId }}/{{ canvasList.length }}</span>
            <div class="zoom-buttons">
              <!-- 缩放按钮 -->
            </div>
          </div>
          
          <!-- 背景设置 -->
          <div class="form-group">
            <label>背景颜色</label>
            <input 
              type="color" 
              :value="canvasConfig.backgroundColor"
              @input="updateCanvasConfig('backgroundColor', $event.target.value)"
            >
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
                    v-if="canvasConfig.showGrid"
                    class="btn-icon"
                    @click="showGridSettings = !showGridSettings"
                  >
                    <Setting theme="outline" size="14" />
                  </button>
                </div>
                <Switch 
                  :checked="canvasConfig.showGrid"
                  @change="updateCanvasConfig('showGrid', $event)"
                />
              </div>
              <!-- 网格设置 -->
              <div v-if="canvasConfig.showGrid && showGridSettings" class="switch-settings">
                <div class="form-group">
                  <label>网格大小</label>
                  <div class="input-group">
                    <input 
                      type="number"
                      :value="canvasConfig.gridSize"
                      @input="updateCanvasConfig('gridSize', Number($event.target.value))"
                      min="5"
                      max="50"
                    >
                    <span class="unit">px</span>
                  </div>
                </div>
                <div class="form-group">
                  <label>网格颜色</label>
                  <input 
                    type="color"
                    :value="canvasConfig.gridColor"
                    @input="updateCanvasConfig('gridColor', $event.target.value)"
                  >
                </div>
              </div>
            </div>

            <!-- 标尺 -->
            <div class="switch-item">
              <div class="switch-header">
                <span class="switch-text">显示标尺</span>
                <Switch 
                  :checked="canvasConfig.showRuler"
                  @change="updateCanvasConfig('showRuler', $event)"
                />
              </div>
            </div>

            <!-- 辅助线 -->
            <div class="switch-item">
              <div class="switch-header">
                <span class="switch-text">显示辅助线</span>
                <Switch 
                  :checked="canvasConfig.showGuides"
                  @change="updateCanvasConfig('showGuides', $event)"
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
import { ref } from 'vue'
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
  },
  canvasConfig: {
    type: Object,
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
const updateCanvasConfig = (key, value) => {
  const newConfig = {
    ...props.canvasConfig,
    [key]: value
  }
  emit('update-canvas-config', newConfig)
}

// 控制网格设置的显示/隐藏
const showGridSettings = ref(false)
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
  border: 1px solid #e8e8e8;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.canvas-item.active {
  border-color: #1890ff;
}

.canvas-info {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.canvas-name {
  font-size: 14px;
  color: #666;
}

.btn-icon {
  position: absolute;
  top: 2px;
  right: 2px;
  padding: 2px;
  border: none;
  background: none;
  color: #999;
  cursor: pointer;
  opacity: 0;
  z-index: 2;
}

.canvas-item:hover .btn-icon {
  opacity: 1;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
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
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.canvas-pages {
  font-size: 13px;
  color: #666;
}

.zoom-buttons {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style> 