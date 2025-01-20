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
                @input="(e) => updateElementProp('x', e.target.value)"
                placeholder="X"
                step="1"
                min="0"
              >
              <input
                type="number"
                :value="element.y"
                @input="(e) => updateElementProp('y', e.target.value)"
                placeholder="Y"
                step="1"
                min="0"
              >
            </div>
          </div>
          <div class="form-group">
            <label>尺寸</label>
            <div class="input-group">
              <input
                type="number"
                :value="element.width"
                @input="(e) => updateElementProp('width', e.target.value)"
                placeholder="宽度"
                step="1"
                min="1"
              >
              <input
                type="number"
                :value="element.height"
                @input="(e) => updateElementProp('height', e.target.value)"
                placeholder="高度"
                step="1"
                min="1"
              >
            </div>
          </div>
          <div class="form-group">
            <label>旋转</label>
            <div class="rotate-control">
              <input
                type="range"
                :value="element.rotate || 0"
                @input="(e) => {
                  const value = Math.round(parseFloat(e.target.value) || 0)
                  updateElementProp('rotate', value)
                }"
                min="0"
                max="360"
                step="1"
              >
              <div class="input-group">
                <input
                  type="number"
                  :value="element.rotate || 0"
                  @input="(e) => {
                    const value = Math.round(parseFloat(e.target.value) || 0)
                    updateElementProp('rotate', value)
                  }"
                  placeholder="角度"
                  step="1"
                  min="0"
                  max="360"
                >
                <span class="unit">°</span>
              </div>
            </div>
          </div>
        </div>

        <div class="panel-section">
          <h4>样式</h4>
          <!-- 形状通用样式设置 -->
          <template v-if="['rectangle', 'circle', 'triangle', 'star'].includes(element.type)">
            <div class="form-group">
              <label>背景颜色</label>
              <div class="color-settings">
                <div class="color-type-switch">
                  <button 
                    :class="{ active: !isGradient }"
                    @click="isGradient = false"
                  >
                    纯色
                  </button>
                  <button 
                    :class="{ active: isGradient }"
                    @click="isGradient = true"
                  >
                    渐变
                  </button>
                </div>
                <div v-if="!isGradient" class="color-picker">
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
                  <button 
                    class="btn-save-color" 
                    title="添加到颜色变量"
                    @click="addColorVar(element.props?.fill)"
                  >
                    <Plus theme="outline" size="14" />
                  </button>
                </div>
                <div class="gradient-settings" v-else>
                  <div class="gradient-header">
                    <select v-model="gradientType">
                      <option value="linear">线性渐变</option>
                      <option value="radial">径向渐变</option>
                    </select>
                    <select v-if="gradientType === 'linear'" v-model="gradientDirection">
                      <option value="to right">从左到右</option>
                      <option value="to bottom">从上到下</option>
                      <option value="to bottom right">对角线</option>
                    </select>
                  </div>
                  <div class="gradient-preview">
                    <div 
                      class="gradient-bar"
                      :style="{ background: previewGradient }"
                      @click="addGradientStop"
                    >
                      <div 
                        v-for="(stop, index) in gradientStops" 
                        :key="index"
                        class="gradient-stop"
                        :style="{ 
                          left: `${stop.position}%`,
                          backgroundColor: stop.color
                        }"
                        @mousedown="startDragging(index, $event)"
                      >
                        <div class="gradient-stop-color">
                          <input 
                            type="color" 
                            :value="stop.color"
                            @input="(e) => updateGradientStop(index, e.target.value)"
                          >
                        </div>
                      </div>
                    </div>
                    <button 
                      class="btn-save-gradient" 
                      title="添加到颜色变量"
                      @click="addColorVar(element.props?.fill)"
                    >
                      <Plus theme="outline" size="14" />
                    </button>
                  </div>
                </div>
                <div class="color-blocks" v-if="colorVars.length > 0">
                  <div 
                    v-for="(color, index) in colorVars" 
                    :key="index"
                    class="color-block"
                  >
                    <div 
                      class="color-preview"
                      :style="{ background: color }"
                      :title="color"
                      @click="updateElementProp('props', {
                        ...element.props,
                        fill: color
                      })"
                    ></div>
                    <button 
                      class="btn-delete-color"
                      @click="removeColorVar(index)"
                    >
                      <Delete theme="outline" size="12" />
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label>边框</label>
              <div class="border-settings">
                <div class="input-group">
                  <input
                    type="number"
                    :value="element.props?.strokeWidth || 0"
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

          <!-- 箭头和线条的样式设置 -->
          <template v-if="['arrow', 'line'].includes(element.type)">
            <div class="form-group">
              <label>线条样式</label>
              <div class="border-settings">
                <div class="input-group">
                  <input
                    type="number"
                    :value="element.props?.strokeWidth || 2"
                    @input="(e) => updateElementProp('props', {
                      ...element.props,
                      strokeWidth: Math.max(1, parseInt(e.target.value) || 1)
                    })"
                    min="1"
                    max="20"
                    placeholder="线宽"
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
                </select>
                <div class="color-picker">
                  <input
                    type="color"
                    :value="element.props?.stroke || '#096dd9'"
                    @input="(e) => updateElementProp('props', {
                      ...element.props,
                      stroke: e.target.value
                    })"
                  >
                  <input 
                    type="text"
                    :value="element.props?.stroke || '#096dd9'"
                    @input="(e) => updateElementProp('props', {
                      ...element.props,
                      stroke: e.target.value
                    })"
                    placeholder="#096dd9"
                  >
                </div>
              </div>
            </div>

            <div class="form-group">
              <label>线条端点</label>
              <div class="input-group">
                <select
                  :value="element.props?.lineCap || 'butt'"
                  @change="(e) => updateElementProp('props', {
                    ...element.props,
                    lineCap: e.target.value
                  })"
                >
                  <option value="butt">方形</option>
                  <option value="round">圆形</option>
                  <option value="square">延伸方形</option>
                </select>
                <select
                  :value="element.props?.lineJoin || 'miter'"
                  @change="(e) => updateElementProp('props', {
                    ...element.props,
                    lineJoin: e.target.value
                  })"
                >
                  <option value="miter">尖角</option>
                  <option value="round">圆角</option>
                  <option value="bevel">斜角</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label>箭头样式</label>
              <div class="arrow-settings">
                <div class="input-group">
                  <select
                    :value="element.props?.startArrow || 'none'"
                    @change="(e) => updateElementProp('props', {
                      ...element.props,
                      startArrow: e.target.value
                    })"
                  >
                    <option value="none">无箭头</option>
                    <option value="arrow">箭头</option>
                    <option value="dot">圆点</option>
                    <option value="diamond">菱形</option>
                  </select>
                  <input
                    type="number"
                    :value="element.props?.startArrowSize || 10"
                    @input="(e) => updateElementProp('props', {
                      ...element.props,
                      startArrowSize: Math.max(5, parseInt(e.target.value) || 10)
                    })"
                    min="5"
                    max="20"
                    placeholder="起点大小"
                  >
                </div>
                <div class="input-group">
                  <select
                    :value="element.props?.endArrow || 'none'"
                    @change="(e) => updateElementProp('props', {
                      ...element.props,
                      endArrow: e.target.value
                    })"
                  >
                    <option value="none">无箭头</option>
                    <option value="arrow">箭头</option>
                    <option value="dot">圆点</option>
                    <option value="diamond">菱形</option>
                  </select>
                  <input
                    type="number"
                    :value="element.props?.endArrowSize || 10"
                    @input="(e) => updateElementProp('props', {
                      ...element.props,
                      endArrowSize: Math.max(5, parseInt(e.target.value) || 10)
                    })"
                    min="5"
                    max="20"
                    placeholder="终点大小"
                  >
                </div>
              </div>
            </div>

            <div class="form-group">
              <label>透明度</label>
              <div class="opacity-control">
                <input
                  type="range"
                  :value="element.props?.opacity || 1"
                  @input="(e) => updateElementProp('props', {
                    ...element.props,
                    opacity: parseFloat(e.target.value)
                  })"
                  min="0"
                  max="1"
                  step="0.1"
                >
                <div class="input-group">
                  <input
                    type="number"
                    :value="element.props?.opacity || 1"
                    @input="(e) => updateElementProp('props', {
                      ...element.props,
                      opacity: Math.min(1, Math.max(0, parseFloat(e.target.value) || 0))
                    })"
                    min="0"
                    max="1"
                    step="0.1"
                  >
                </div>
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
              <div v-if="showGridSettings" class="switch-settings">
                <div class="form-group">
                  <label>网格大小</label>
                  <div class="input-group">
                    <input 
                      type="number"
                      :value="getCurrentCanvas()?.config?.gridSize"
                      @input="(e) => handleConfigChange('gridSize', Math.max(5, Math.min(50, Number(e.target.value))))"
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
                <div class="switch-text-group">
                  <span class="switch-text">显示标尺</span>
                  <button 
                    class="btn-icon"
                    @click="showRulerSettings = !showRulerSettings"
                  >
                    <Setting theme="outline" size="14" />
                  </button>
                </div>
                <Switch 
                  :model-value="getCurrentCanvas()?.config?.showRuler"
                  @update:model-value="(value) => handleConfigChange('showRuler', value)"
                />
              </div>
              <!-- 标尺设置 -->
              <div v-if="showRulerSettings" class="switch-settings">
                <div class="form-group">
                  <label>标尺颜色</label>
                  <div class="color-picker">
                    <input 
                      type="color"
                      :value="getCurrentCanvas()?.config?.rulerColor || '#999999'"
                      @input="(e) => handleConfigChange('rulerColor', e.target.value)"
                    >
                    <input 
                      type="text"
                      :value="getCurrentCanvas()?.config?.rulerColor || '#999999'"
                      @input="(e) => handleConfigChange('rulerColor', e.target.value)"
                      placeholder="#999999"
                    >
                  </div>
                </div>
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
import { ref, computed, watch } from 'vue'
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

// 渐变相关状态
const isGradient = ref(false)
const gradientType = ref('linear')
const gradientDirection = ref('to right')
const gradientStops = ref([
  { color: '#4f46e5', position: 0 },
  { color: '#1890ff', position: 100 }
])

// 渐变预览
const previewGradient = computed(() => {
  const stops = gradientStops.value
    .sort((a, b) => a.position - b.position)
    .map(stop => `${stop.color} ${stop.position}%`)
    .join(', ')
    
  return gradientType.value === 'linear'
    ? `linear-gradient(to right, ${stops})`
    : `linear-gradient(to right, ${stops})`
})

// 拖拽相关状态
const isDragging = ref(false)
const draggedStopIndex = ref(-1)

// 开始拖拽
const startDragging = (index, event) => {
  isDragging.value = true
  draggedStopIndex.value = index
  
  const handleMouseMove = (e) => {
    if (!isDragging.value) return
    
    const bar = event.target.parentElement
    const rect = bar.getBoundingClientRect()
    const position = Math.min(100, Math.max(0, 
      ((e.clientX - rect.left) / rect.width) * 100
    ))
    
    gradientStops.value[draggedStopIndex.value].position = Math.round(position)
    updateGradientBackground()
  }
  
  const handleMouseUp = () => {
    isDragging.value = false
    draggedStopIndex.value = -1
    document.removeEventListener('mousemove', handleMouseMove)
    document.removeEventListener('mouseup', handleMouseUp)
  }
  
  document.addEventListener('mousemove', handleMouseMove)
  document.addEventListener('mouseup', handleMouseUp)
}

// 添加渐变色停止点
const addGradientStop = (event) => {
  if (gradientStops.value.length >= 5) return
  
  const bar = event.currentTarget
  const rect = bar.getBoundingClientRect()
  const position = Math.min(100, Math.max(0, 
    ((event.clientX - rect.left) / rect.width) * 100
  ))
  
  // 找到最近的两个停止点
  const stops = gradientStops.value.sort((a, b) => a.position - b.position)
  let color = '#ffffff'
  
  for (let i = 0; i < stops.length - 1; i++) {
    if (position >= stops[i].position && position <= stops[i + 1].position) {
      const ratio = (position - stops[i].position) / (stops[i + 1].position - stops[i].position)
      color = interpolateColor(stops[i].color, stops[i + 1].color, ratio)
      break
    }
  }
  
  gradientStops.value.push({ color, position: Math.round(position) })
  updateGradientBackground()
}

// 颜色插值
const interpolateColor = (color1, color2, ratio) => {
  const r1 = parseInt(color1.slice(1, 3), 16)
  const g1 = parseInt(color1.slice(3, 5), 16)
  const b1 = parseInt(color1.slice(5, 7), 16)
  
  const r2 = parseInt(color2.slice(1, 3), 16)
  const g2 = parseInt(color2.slice(3, 5), 16)
  const b2 = parseInt(color2.slice(5, 7), 16)
  
  const r = Math.round(r1 + (r2 - r1) * ratio)
  const g = Math.round(g1 + (g2 - g1) * ratio)
  const b = Math.round(b1 + (b2 - b1) * ratio)
  
  return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`
}

// 更新渐变色停止点
const updateGradientStop = (index, color) => {
  gradientStops.value[index].color = color
  updateGradientBackground()
}

// 更新渐变背景
const updateGradientBackground = () => {
  const stops = gradientStops.value
    .sort((a, b) => a.position - b.position)
    .map(stop => `${stop.color} ${stop.position}%`)
    .join(', ')
    
  const gradient = gradientType.value === 'linear'
    ? `linear-gradient(${gradientDirection.value}, ${stops})`
    : `radial-gradient(circle at center, ${stops})`
    
  updateElementProp('props', {
    ...props.element.props,
    fill: gradient
  })
}

// 监听渐变类型和方向变化
watch([gradientType, gradientDirection], () => {
  if (isGradient.value) {
    updateGradientBackground()
  }
})

// 监听 element 变化，初始化渐变状态
watch(() => props.element, (newElement) => {
  if (newElement?.props?.fill) {
    // 检查是否是渐变色
    const isGradientFill = newElement.props.fill.includes('gradient')
    isGradient.value = isGradientFill
    
    if (isGradientFill) {
      // 解析渐变色
      const fill = newElement.props.fill
      if (fill.includes('linear-gradient')) {
        gradientType.value = 'linear'
        // 解析方向
        const directionMatch = fill.match(/linear-gradient\((.*?),/)
        if (directionMatch) {
          gradientDirection.value = directionMatch[1].trim()
        }
      } else {
        gradientType.value = 'radial'
      }
      
      // 解析颜色停止点
      const colorStops = fill.match(/(#[0-9a-f]{6}|rgb\([^)]+\))\s*(\d+%)/gi)
      if (colorStops) {
        gradientStops.value = colorStops.map(stop => {
          const [color, position] = stop.split(/\s+/)
          return {
            color,
            position: parseInt(position)
          }
        })
      }
    }
  }
}, { immediate: true })

// 更新元素属性
const updateElementProp = (prop, value) => {
  if (!props.element) return

  // 处理数值类型的属性
  const numericProps = ['x', 'y', 'width', 'height', 'rotate', 'zIndex']
  let finalValue = value

  if (numericProps.includes(prop)) {
    // 对于宽度和高度，只保留最小值限制
    if (prop === 'width' || prop === 'height') {
      finalValue = Math.max(1, parseInt(value) || 1)
    } else if (prop === 'rotate') {
      // 旋转角度限制在 0-360 之间
      finalValue = Math.min(360, Math.max(0, parseInt(value) || 0))
    } else {
      // 其他数值属性保持大于等于0
      finalValue = Math.max(0, parseInt(value) || 0)
    }
  }

  // 如果是 props 对象中的属性
  if (prop === 'props') {
    emit('update', {
      ...props.element,
      props: {
        ...props.element.props,
        ...value
      }
    })
    return
  }

  // 更新其他属性
  emit('update', {
    ...props.element,
    [prop]: finalValue
  })
}

// 更新画布配置
const handleConfigChange = (key, value) => {
  const currentCanvas = getCurrentCanvas()
  if (currentCanvas?.config) {
    const newConfig = { [key]: value }
    console.log('更新画布配置:', key, value) // 添加日志
    emit('update-canvas-config', newConfig)
  }
}

// 更新背景颜色
const updateBackgroundColor = (color) => {
  handleConfigChange('backgroundColor', color)
}

// 应用到所有画布
const applyToAllCanvas = () => {
  const currentCanvas = getCurrentCanvas()
  if (currentCanvas?.config) {
    const config = {
      backgroundColor: currentCanvas.config.backgroundColor,
      showGrid: currentCanvas.config.showGrid,
      gridSize: currentCanvas.config.gridSize,
      gridColor: currentCanvas.config.gridColor
    }
    console.log('应用到所有画布:', config) // 添加日志
    emit('update-canvas-config', config, true)
  }
}

// 控制网格设置的显示/隐藏
const showGridSettings = ref(false)

// 颜色变量列表 - 只存储颜色值
const colorVars = ref([])

// 添加颜色变量
const addColorVar = (color) => {
  if (!color) return
  if (!colorVars.value.includes(color)) {
    colorVars.value.push(color)
  }
}

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

// 删除颜色变量
const removeColorVar = (index) => {
  colorVars.value.splice(index, 1)
}

// 监听画布ID变化，重置网格设置面板
watch(() => props.currentCanvasId, () => {
  showGridSettings.value = false
})

// 控制标尺设置的显示/隐藏
const showRulerSettings = ref(false)
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
}

.color-picker input[type="text"] {
  flex: 1;
  min-width: 120px;
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

/* 删除或注释掉通用的 input[type="range"] 样式 */
/* input[type="range"] {
  width: 100%;
  height: 4px;
  background: #e8e8e8;
  border-radius: 2px;
  outline: none;
  -webkit-appearance: none;
  margin: 0;
  padding: 6px 0;
  cursor: pointer;
} */

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

.rotate-control {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 32px;
}

.rotate-control input[type="range"] {
  flex: 1;
  width: 100%;
  height: 4px;
  background: #e5e7eb;
  border-radius: 2px;
  outline: none;
  -webkit-appearance: none;
  margin: 0;
  padding: 0;
  cursor: pointer;
  position: relative;
  top: 2px;
}

.rotate-control input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  background: #fff;
  border: 2px solid #4f46e5;
  border-radius: 50%;
  cursor: pointer;
  position: relative;
  top: 0px;
}

.rotate-control input[type="range"]::-webkit-slider-thumb:hover {
  transform: scale(1.1);
}

.rotate-control .input-group {
  width: 80px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  
}

.rotate-control .input-group input {
  width: 50px;
  text-align: right;
}

.color-settings {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.color-picker {
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-save-color {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 32px;
  max-width: 32px;
  min-height: 32px;
  max-height: 32px;
  border: 1px solid #cacaca;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
  margin-left: 0px;
  background-color: #fefefe;
  flex-shrink: 0;
}

.btn-save-color:hover {
  border-color: #4f46e5;
  color: #4f46e5;
}

.color-blocks {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 8px;
}

.color-block {
  position: relative;
  width: 24px;
  height: 24px;
}

.color-preview {
  width: 100%;
  height: 100%;
  border-radius: 4px;
  cursor: pointer;
  border: 1px solid #e5e7eb;
  transition: transform 0.2s;
}

.color-preview:hover {
  transform: scale(1.1);
}

.btn-delete-color {
  position: absolute;
  top: -6px;
  right: -6px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #fff;
  border: 1px solid #e5e7eb;
  color: #666;
  padding: 2px;
  cursor: pointer;
  display: none;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.btn-delete-color:hover {
  background: #ff4d4f;
  border-color: #ff4d4f;
  color: #fff;
}

.color-block:hover .btn-delete-color {
  display: flex;
}

.gradient-settings {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 12px;
}

.gradient-header {
  display: flex;
  gap: 8px;
}

.gradient-header select {
  flex: 1;
  height: 32px;
  padding: 0 8px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  background-color: #fff;
  font-size: 13px;
  color: #374151;
}

.gradient-preview {
  position: relative;
  padding: 16px 0;
  display: flex;
  gap: 8px;
  align-items: center;
}

.gradient-bar {
  position: relative;
  flex: 1;
  height: 24px;
  border-radius: 4px;
  background: #fff;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.gradient-stop {
  position: absolute;
  top: -6px;
  width: 16px;
  height: 16px;
  margin-left: -8px;
  background: #fff;
  border: 2px solid #fff;
  border-radius: 50%;
  cursor: move;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.12);
  z-index: 1;
}

.gradient-stop:hover {
  transform: scale(1.1);
}

.gradient-stop-color {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  overflow: hidden;
}

.gradient-stop-color input[type="color"] {
  width: 200%;
  height: 200%;
  margin: -50%;
  padding: 0;
  border: none;
  cursor: pointer;
}

.btn-add-stop {
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  height: 24px;
  padding: 0 12px;
  border: none;
  background: #fff;
  color: #6b7280;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
  border-radius: 12px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.btn-add-stop:hover {
  color: #4f46e5;
  background: #f9fafb;
}

.color-type-switch {
  display: flex;
  gap: 1px;
  background-color: #e5e7eb;
  padding: 2px;
  border-radius: 6px;
  margin-bottom: 12px;
}

.color-type-switch button {
  flex: 1;
  height: 28px;
  border: none;
  background-color: #fff;
  color: #6b7280;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.color-type-switch button:first-child {
  border-radius: 4px 0 0 4px;
}

.color-type-switch button:last-child {
  border-radius: 0 4px 4px 0;
}

.color-type-switch button.active {
  background-color: #4f46e5;
  color: #fff;
}

.btn-save-gradient {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 32px;
  max-width: 32px;
  min-height: 32px;
  max-height: 32px;
  border: 1px solid #cacaca;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
  background-color: #fefefe;
  flex-shrink: 0;
}

.btn-save-gradient:hover {
  border-color: #4f46e5;
  color: #4f46e5;
}

.arrow-settings {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 12px;
}

.arrow-settings .input-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.arrow-settings select {
  flex: 1;
  height: 32px;
  padding: 0 8px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  background-color: #fff;
  font-size: 13px;
  color: #374151;
}

.opacity-control {
  display: flex;
  align-items: center;
  gap: 8px;
}

.opacity-control input[type="range"] {
  flex: 1;
  width: 100%;
  height: 4px;
  background: #e5e7eb;
  border-radius: 2px;
  outline: none;
  -webkit-appearance: none;
  margin: 0;
  padding: 6px 0;
  cursor: pointer;
}

.opacity-control input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  background: #fff;
  border: 2px solid #4f46e5;
  border-radius: 50%;
  cursor: pointer;
}

.opacity-control input[type="range"]::-webkit-slider-thumb:hover {
  transform: scale(1.1);
}

.opacity-control .input-group {
  width: 80px;
  flex-shrink: 0;
}

.opacity-control .input-group input[type="number"] {
  width: 100%;
}
</style> 