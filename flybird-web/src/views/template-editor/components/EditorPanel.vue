<template>
  <div class="editor-panel">
    <!-- 多选状态下的操作面板 -->
    <div v-if="selectedElements && selectedElements.length > 1" class="multi-select-panel">
      <div class="panel-section">
        <div class="section-title">多选操作</div>
        <div class="align-group">
          <div class="group-title">对齐方式</div>
          <div class="button-group">
            <button class="btn-icon" @click="alignElements('left')" title="左对齐">
              <AlignLeft theme="outline" size="16" fill="#374151" />
            </button>
            <button class="btn-icon" @click="alignElements('center')" title="垂直居中">
              <AlignTextCenter theme="outline" size="16" fill="#374151" />
            </button>
            <button class="btn-icon" @click="alignElements('right')" title="右对齐">
              <AlignRight theme="outline" size="16" fill="#374151" />
            </button>
            <button class="btn-icon" @click="alignElements('top')" title="顶部对齐">
              <AlignTop theme="outline" size="16" fill="#374151" />
            </button>
            <button class="btn-icon" @click="alignElements('middle')" title="水平居中">
              <AlignTextMiddle theme="outline" size="16" fill="#374151" />
            </button>
            <button class="btn-icon" @click="alignElements('bottom')" title="底部对齐">
              <AlignBottom theme="outline" size="16" fill="#374151" />
            </button>
          </div>
        </div>
        
        <div class="distribute-group">
          <div class="group-title">分布方式</div>
          <div class="button-group">
            <button class="btn-icon" @click="distributeElements('horizontal')" title="水平分布">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="1" y="4" width="2" height="8" fill="#374151"/>
                <rect x="7" y="4" width="2" height="8" fill="#374151"/>
                <rect x="13" y="4" width="2" height="8" fill="#374151"/>
              </svg>
            </button>
            <button class="btn-icon" @click="distributeElements('vertical')" title="垂直分布">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="4" y="1" width="8" height="2" fill="#374151"/>
                <rect x="4" y="7" width="8" height="2" fill="#374151"/>
                <rect x="4" y="13" width="8" height="2" fill="#374151"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 原有的单选面板 -->
    <template v-else>
      <div class="panel-content">
        <!-- 元素属性设置 -->
        <template v-if="element">
          <h3>元素属性</h3>
          <div class="panel-section">
            <h4>基础属性</h4>
            <div class="form-group">
              <div class="input-group">
                <div class="input-item">
                  <label>X</label>
                  <input
                    type="number"
                    :value="element.x"
                    @input="(e) => updateElementProp('x', parseInt(e.target.value))"
                    placeholder="X坐标"
                  >
                </div>
                <div class="input-item">
                  <label>Y</label>
                  <input
                    type="number"
                    :value="element.y"
                    @input="(e) => updateElementProp('y', parseInt(e.target.value))"
                    placeholder="Y坐标"
                  >
                </div>
                <div class="input-item">
                  <label>宽</label>
                  <input
                    type="number"
                    :value="element.width"
                    @input="(e) => updateElementProp('width', parseInt(e.target.value))"
                    placeholder="宽度"
                  >
                </div>
                <div class="input-item">
                  <label>高</label>
                  <input
                    type="number"
                    :value="element.height"
                    @input="(e) => updateElementProp('height', parseInt(e.target.value))"
                    placeholder="高度"
                  >
                </div>
              </div>
            </div>
            <div class="form-group">
              <label>旋转</label>
              <div class="rotate-control">
                <input
                  type="range"
                  :value="element.rotate || 0"
                  @input="(e) => updateElementProp('rotate', parseInt(e.target.value))"
                  min="0"
                  max="360"
                  step="1"
                >
                <input
                  type="number"
                  :value="element.rotate || 0"
                  @input="(e) => updateElementProp('rotate', parseInt(e.target.value))"
                  min="0"
                  max="360"
                  step="1"
                  style="width: 70px"
                >
              </div>
            </div>
            <div class="form-group">
              <label>透明度</label>
              <div class="opacity-control">
                <input
                  type="range"
                  :value="element.props?.opacity || 1"
                  @input="(e) => handleElementPropChange('opacity', parseFloat(e.target.value))"
                  min="0"
                  max="1"
                  step="0.1"
                >
                <input
                  type="number"
                  :value="element.props?.opacity || 1"
                  @input="(e) => handleElementPropChange('opacity', Math.min(1, Math.max(0, parseFloat(e.target.value) || 0)))"
                  min="0"
                  max="1"
                  step="0.1"
                  style="width: 70px"
                >
              </div>
            </div>
            <!-- 标题样式设置 -->
            <template v-if="element?.type === 'h3' || element?.type === 'h4'">
              <!-- 字体大小 -->
              <div class="form-group">
                <label>字体大小</label>
                <div class="input-group">
                  <input 
                    type="number" 
                    :value="element.props?.fontSize"
                    @input="(e) => handleElementPropChange('fontSize', Number(e.target.value))"
                    min="12"
                    max="72"
                    step="1"
                    :disabled="false"
                  >
                  <span class="unit">px</span>
                </div>
              </div>

              <!-- 文本对齐 -->
              <div class="form-group">
                <label>水平对齐</label>
                <div class="button-group">
                  <button 
                    class="btn-icon" 
                    :class="{ active: element.props?.textAlign === 'left' }"
                    @click="() => handleElementPropChange('textAlign', 'left')"
                    title="左对齐"
                  >
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <rect x="2" y="4" width="8" height="1.5" :fill="element.props?.textAlign === 'left' ? '#1890ff' : '#333'" />
                      <rect x="2" y="7.25" width="12" height="1.5" :fill="element.props?.textAlign === 'left' ? '#1890ff' : '#333'" />
                      <rect x="2" y="10.5" width="8" height="1.5" :fill="element.props?.textAlign === 'left' ? '#1890ff' : '#333'" />
                    </svg>
                  </button>
                  <button 
                    class="btn-icon" 
                    :class="{ active: element.props?.textAlign === 'center' }"
                    @click="() => handleElementPropChange('textAlign', 'center')"
                    title="居中对齐"
                  >
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <rect x="4" y="4" width="8" height="1.5" :fill="element.props?.textAlign === 'center' ? '#1890ff' : '#333'" />
                      <rect x="2" y="7.25" width="12" height="1.5" :fill="element.props?.textAlign === 'center' ? '#1890ff' : '#333'" />
                      <rect x="4" y="10.5" width="8" height="1.5" :fill="element.props?.textAlign === 'center' ? '#1890ff' : '#333'" />
                    </svg>
                  </button>
                  <button 
                    class="btn-icon" 
                    :class="{ active: element.props?.textAlign === 'right' }"
                    @click="() => handleElementPropChange('textAlign', 'right')"
                    title="右对齐"
                  >
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <rect x="6" y="4" width="8" height="1.5" :fill="element.props?.textAlign === 'right' ? '#1890ff' : '#333'" />
                      <rect x="2" y="7.25" width="12" height="1.5" :fill="element.props?.textAlign === 'right' ? '#1890ff' : '#333'" />
                      <rect x="6" y="10.5" width="8" height="1.5" :fill="element.props?.textAlign === 'right' ? '#1890ff' : '#333'" />
                    </svg>
                  </button>
                </div>
              </div>

              <!-- 垂直对齐 -->
              <div class="form-group">
                <label>垂直对齐</label>
                <div class="button-group">
                  <button 
                    class="btn-icon" 
                    :class="{ active: element.props?.verticalAlign === 'top' }"
                    @click="() => handleElementPropChange('verticalAlign', 'top')"
                    title="顶部对齐"
                  >
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <rect x="2" y="2" width="12" height="1.5" :fill="element.props?.verticalAlign === 'top' ? '#1890ff' : '#333'" />
                      <rect x="4" y="5" width="8" height="1.5" :fill="element.props?.verticalAlign === 'top' ? '#1890ff' : '#333'" />
                      <rect x="4" y="8" width="8" height="1.5" :fill="element.props?.verticalAlign === 'top' ? '#1890ff' : '#333'" />
                    </svg>
                  </button>
                  <button 
                    class="btn-icon" 
                    :class="{ active: element.props?.verticalAlign === 'middle' }"
                    @click="() => handleElementPropChange('verticalAlign', 'middle')"
                    title="垂直居中"
                  >
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <rect x="4" y="4" width="8" height="1.5" :fill="element.props?.verticalAlign === 'middle' ? '#1890ff' : '#333'" />
                      <rect x="2" y="7.25" width="12" height="1.5" :fill="element.props?.verticalAlign === 'middle' ? '#1890ff' : '#333'" />
                      <rect x="4" y="10.5" width="8" height="1.5" :fill="element.props?.verticalAlign === 'middle' ? '#1890ff' : '#333'" />
                    </svg>
                  </button>
                  <button 
                    class="btn-icon" 
                    :class="{ active: element.props?.verticalAlign === 'bottom' }"
                    @click="() => handleElementPropChange('verticalAlign', 'bottom')"
                    title="底部对齐"
                  >
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <rect x="4" y="7" width="8" height="1.5" :fill="element.props?.verticalAlign === 'bottom' ? '#1890ff' : '#333'" />
                      <rect x="4" y="10" width="8" height="1.5" :fill="element.props?.verticalAlign === 'bottom' ? '#1890ff' : '#333'" />
                      <rect x="2" y="13" width="12" height="1.5" :fill="element.props?.verticalAlign === 'bottom' ? '#1890ff' : '#333'" />
                    </svg>
                  </button>
                </div>
              </div>

              <!-- 字体颜色 -->
              <div class="form-group">
                <label>字体颜色</label>
                <ColorPicker
                  :model-value="element.props?.color"
                  @update:model-value="(color) => handleElementPropChange('color', color)"
                />
              </div>

              <!-- 填充颜色 -->
              <div class="form-group">
                <label>填充颜色</label>
                <ColorPicker
                  :model-value="element.props?.fill"
                  @update:model-value="(color) => handleElementPropChange('fill', color)"
                />
              </div>

              <!-- 行高 -->
              <div class="form-group">
                <label>行高</label>
                <div class="input-group">
                  <input 
                    type="number" 
                    :value="element.props?.lineHeight"
                    @input="(e) => handleElementPropChange('lineHeight', Number(e.target.value))"
                    min="1"
                    max="3"
                    step="0.1"
                  >
                </div>
              </div>
            </template>
          </div>

          <!-- 添加对齐操作区域 -->
          <div class="panel-section">
            <h4>对齐方式</h4>
            <div class="form-group">
              <div class="align-controls">
                <!-- 画布对齐 -->
                <div class="align-group">
                  <label>画布对齐</label>
                  <div class="button-group">
                    <button 
                      class="btn-icon" 
                      title="水平居中到画布"
                      @click="$emit('align-horizontal-to-canvas')"
                    >
                      <AlignTextCenter theme="outline" size="16" fill="#374151" />
                    </button>
                    <button 
                      class="btn-icon" 
                      title="垂直居中到画布"
                      @click="$emit('align-vertical-to-canvas')"
                    >
                      <AlignTextMiddle theme="outline" size="16" fill="#374151" />
                    </button>
                  </div>
                </div>
                
                <!-- 水平对齐 -->
                <div class="align-group">
                  <label>水平对齐</label>
                  <div class="button-group">
                    <button 
                      class="btn-icon" 
                      title="左对齐"
                      @click="$emit('align-left')"
                    >
                      <AlignLeft theme="outline" size="16" fill="#374151" />
                    </button>
                    <button 
                      class="btn-icon" 
                      title="水平居中"
                      @click="$emit('align-horizontal-center')"
                    >
                      <AlignTextCenter theme="outline" size="16" fill="#374151" />
                    </button>
                    <button 
                      class="btn-icon" 
                      title="右对齐"
                      @click="$emit('align-right')"
                    >
                      <AlignRight theme="outline" size="16" fill="#374151" />
                    </button>
                  </div>
                </div>
                
                <!-- 垂直对齐 -->
                <div class="align-group">
                  <label>垂直对齐</label>
                  <div class="button-group">
                    <button 
                      class="btn-icon" 
                      title="顶部对齐"
                      @click="$emit('align-top')"
                    >
                      <AlignTop theme="outline" size="16" fill="#374151" />
                    </button>
                    <button 
                      class="btn-icon" 
                      title="垂直居中"
                      @click="$emit('align-vertical-center')"
                    >
                      <AlignTextMiddle theme="outline" size="16" fill="#374151" />
                    </button>
                    <button 
                      class="btn-icon" 
                      title="底部对齐"
                      @click="$emit('align-bottom')"
                    >
                      <AlignBottom theme="outline" size="16" fill="#374151" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="panel-section">
            <h4>样式</h4>
            <!-- 形状通用样式设置 -->
            <template v-if="['rectangle', 'circle', 'triangle', 'star'].includes(element.type)">
              <div class="form-group">
                <label>填充颜色</label>
                <ColorPicker
                  :model-value="element.props?.fill"
                  @update:model-value="(color) => handleElementPropChange('fill', color)"
                />
              </div>

              <div class="form-group">
                <label>边框</label>
                <div class="border-settings">
                  <div class="border-style-wrapper">
                    <div class="border-style-group">
                      <button 
                        class="btn-icon" 
                        :class="{ active: element.props?.strokeStyle === 'solid' }"
                        @click="() => handleElementPropChange('strokeStyle', 'solid')"
                        title="实线"
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <rect x="2" y="7.5" width="12" height="1.5" :fill="element.props?.strokeStyle === 'solid' ? '#1890ff' : '#333'" />
                        </svg>
                      </button>
                      <button 
                        class="btn-icon" 
                        :class="{ active: element.props?.strokeStyle === 'dashed' }"
                        @click="() => handleElementPropChange('strokeStyle', 'dashed')"
                        title="虚线"
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <rect x="2" y="7.5" width="3" height="1.5" :fill="element.props?.strokeStyle === 'dashed' ? '#1890ff' : '#333'" />
                          <rect x="6.5" y="7.5" width="3" height="1.5" :fill="element.props?.strokeStyle === 'dashed' ? '#1890ff' : '#333'" />
                          <rect x="11" y="7.5" width="3" height="1.5" :fill="element.props?.strokeStyle === 'dashed' ? '#1890ff' : '#333'" />
                        </svg>
                      </button>
                      <button 
                        class="btn-icon" 
                        :class="{ active: element.props?.strokeStyle === 'dotted' }"
                        @click="() => handleElementPropChange('strokeStyle', 'dotted')"
                        title="点线"
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <rect x="2" y="7.5" width="1.5" height="1.5" :fill="element.props?.strokeStyle === 'dotted' ? '#1890ff' : '#333'" />
                          <rect x="5.5" y="7.5" width="1.5" height="1.5" :fill="element.props?.strokeStyle === 'dotted' ? '#1890ff' : '#333'" />
                          <rect x="9" y="7.5" width="1.5" height="1.5" :fill="element.props?.strokeStyle === 'dotted' ? '#1890ff' : '#333'" />
                          <rect x="12.5" y="7.5" width="1.5" height="1.5" :fill="element.props?.strokeStyle === 'dotted' ? '#1890ff' : '#333'" />
                        </svg>
                      </button>
                    </div>
                    <input
                      type="number"
                      :value="element.props?.strokeWidth || 0"
                      @input="(e) => handleElementPropChange('strokeWidth', Math.max(0, parseInt(e.target.value) || 0))"
                      min="0"
                      max="20"
                      placeholder="线宽"
                    >
                  </div>
                  <div class="border-color">
                    <label>边框颜色</label>
                    <ColorPicker
                      :model-value="element.props?.stroke"
                      @update:model-value="(color) => handleElementPropChange('stroke', color)"
                    />
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
                      @input="(e) => handleElementPropChange('radius', Math.min(50, Math.max(0, parseInt(e.target.value) || 0)))"
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
                        @input="(e) => handleElementPropChange('radius', Math.min(50, Math.max(0, parseInt(e.target.value) || 0)))"
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
                  <div class="button-group">
                    <button 
                      class="btn-icon" 
                      :class="{ active: element.props?.strokeStyle === 'solid' }"
                      @click="() => updateElementProp('props', {
                        ...element.props,
                        strokeStyle: 'solid'
                      })"
                    >
                      <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect x="2" y="7.5" width="12" height="1.5" :fill="element.props?.strokeStyle === 'solid' ? '#1890ff' : '#333'" />
                      </svg>
                    </button>
                    <button 
                      class="btn-icon" 
                      :class="{ active: element.props?.strokeStyle === 'dashed' }"
                      @click="() => updateElementProp('props', {
                        ...element.props,
                        strokeStyle: 'dashed'
                      })"
                    >
                      <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect x="2" y="7.5" width="3" height="1.5" :fill="element.props?.strokeStyle === 'dashed' ? '#1890ff' : '#333'" />
                        <rect x="6.5" y="7.5" width="3" height="1.5" :fill="element.props?.strokeStyle === 'dashed' ? '#1890ff' : '#333'" />
                        <rect x="11" y="7.5" width="3" height="1.5" :fill="element.props?.strokeStyle === 'dashed' ? '#1890ff' : '#333'" />
                      </svg>
                    </button>
                  </div>
                  <div class="border-color">
                    <label>边框颜色</label>
                    <ColorPicker
                      :model-value="element.props.stroke"
                      @update:model-value="(color) => handleElementPropChange('stroke', color)"
                    />
                  </div>
                </div>
              </div>

              <div class="form-group">
                <label>线条端点</label>
                <div class="line-cap-settings">
                  <div class="select-group">
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
            </template>

            <!-- 文本属性 -->
            <template v-if="element?.type === 'text' || element?.type === 'title' || element?.type === 'resume-field'">
              <!-- 文本内容 -->
              <div class="form-group" v-if="element?.type !== 'resume-field'">
                <label>文本内容</label>
                <textarea
                  :value="element.props?.content"
                  @input="(e) => handleElementPropChange('content', e.target.value)"
                  rows="3"
                  placeholder="请输入文本内容"
                ></textarea>
              </div>
              
              <!-- 字体设置 -->
              <div class="form-group">
                <div class="font-settings">
                  <div class="font-row">
                    <select
                      :value="element.props?.fontFamily"
                      @change="(e) => handleElementPropChange('fontFamily', e.target.value)"
                      class="font-select"
                    >
                      <option value="Arial">Arial</option>
                      <option value="Helvetica">Helvetica</option>
                      <option value="Times New Roman">Times New Roman</option>
                      <option value="Microsoft YaHei">微软雅黑</option>
                      <option value="SimSun">宋体</option>
                      <option value="SimHei">黑体</option>
                      <option value="KaiTi">楷体</option>
                    </select>
                    <div class="font-size">
                      <input 
                        type="number" 
                        :value="element.props?.fontSize"
                        @input="(e) => handleElementPropChange('fontSize', Number(e.target.value))"
                        min="12"
                        max="72"
                        step="1"
                      >
                    </div>
                  </div>
                  <div class="font-style-row">
                    <div class="button-group">
                      <button 
                        class="btn-icon" 
                        :class="{ active: element.props?.fontWeight === 'bold' }"
                        @click="() => handleElementPropChange('fontWeight', element.props?.fontWeight === 'bold' ? 'normal' : 'bold')"
                        title="粗体"
                      >
                        <strong>B</strong>
                      </button>
                      <button 
                        class="btn-icon" 
                        :class="{ active: element.props?.fontStyle === 'italic' }"
                        @click="() => handleElementPropChange('fontStyle', element.props?.fontStyle === 'italic' ? 'normal' : 'italic')"
                        title="斜体"
                      >
                        <em>I</em>
                      </button>
                    </div>
                    <!-- 水平对齐 -->
                    <div class="button-group">
                      <button 
                        class="btn-icon" 
                        :class="{ active: element.props?.textAlign === 'left' }"
                        @click="() => handleElementPropChange('textAlign', 'left')"
                        title="左对齐"
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <rect x="2" y="4" width="8" height="1.5" :fill="element.props?.textAlign === 'left' ? '#1890ff' : '#333'" />
                          <rect x="2" y="7.25" width="12" height="1.5" :fill="element.props?.textAlign === 'left' ? '#1890ff' : '#333'" />
                          <rect x="2" y="10.5" width="8" height="1.5" :fill="element.props?.textAlign === 'left' ? '#1890ff' : '#333'" />
                        </svg>
                      </button>
                      <button 
                        class="btn-icon" 
                        :class="{ active: element.props?.textAlign === 'center' }"
                        @click="() => handleElementPropChange('textAlign', 'center')"
                        title="居中对齐"
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <rect x="4" y="4" width="8" height="1.5" :fill="element.props?.textAlign === 'center' ? '#1890ff' : '#333'" />
                          <rect x="2" y="7.25" width="12" height="1.5" :fill="element.props?.textAlign === 'center' ? '#1890ff' : '#333'" />
                          <rect x="4" y="10.5" width="8" height="1.5" :fill="element.props?.textAlign === 'center' ? '#1890ff' : '#333'" />
                        </svg>
                      </button>
                      <button 
                        class="btn-icon" 
                        :class="{ active: element.props?.textAlign === 'right' }"
                        @click="() => handleElementPropChange('textAlign', 'right')"
                        title="右对齐"
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <rect x="6" y="4" width="8" height="1.5" :fill="element.props?.textAlign === 'right' ? '#1890ff' : '#333'" />
                          <rect x="2" y="7.25" width="12" height="1.5" :fill="element.props?.textAlign === 'right' ? '#1890ff' : '#333'" />
                          <rect x="6" y="10.5" width="8" height="1.5" :fill="element.props?.textAlign === 'right' ? '#1890ff' : '#333'" />
                        </svg>
                      </button>
                    </div>
                    <!-- 垂直对齐 -->
                    <div class="button-group">
                      <button 
                        class="btn-icon" 
                        :class="{ active: element.props?.verticalAlign === 'top' }"
                        @click="() => handleElementPropChange('verticalAlign', 'top')"
                        title="顶部对齐"
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <rect x="2" y="2" width="12" height="1.5" :fill="element.props?.verticalAlign === 'top' ? '#1890ff' : '#333'" />
                          <rect x="4" y="5" width="8" height="1.5" :fill="element.props?.verticalAlign === 'top' ? '#1890ff' : '#333'" />
                          <rect x="4" y="8" width="8" height="1.5" :fill="element.props?.verticalAlign === 'top' ? '#1890ff' : '#333'" />
                        </svg>
                      </button>
                      <button 
                        class="btn-icon" 
                        :class="{ active: element.props?.verticalAlign === 'middle' }"
                        @click="() => handleElementPropChange('verticalAlign', 'middle')"
                        title="垂直居中"
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <rect x="4" y="4" width="8" height="1.5" :fill="element.props?.verticalAlign === 'middle' ? '#1890ff' : '#333'" />
                          <rect x="2" y="7.25" width="12" height="1.5" :fill="element.props?.verticalAlign === 'middle' ? '#1890ff' : '#333'" />
                          <rect x="4" y="10.5" width="8" height="1.5" :fill="element.props?.verticalAlign === 'middle' ? '#1890ff' : '#333'" />
                        </svg>
                      </button>
                      <button 
                        class="btn-icon" 
                        :class="{ active: element.props?.verticalAlign === 'bottom' }"
                        @click="() => handleElementPropChange('verticalAlign', 'bottom')"
                        title="底部对齐"
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <rect x="4" y="7" width="8" height="1.5" :fill="element.props?.verticalAlign === 'bottom' ? '#1890ff' : '#333'" />
                          <rect x="4" y="10" width="8" height="1.5" :fill="element.props?.verticalAlign === 'bottom' ? '#1890ff' : '#333'" />
                          <rect x="2" y="13" width="12" height="1.5" :fill="element.props?.verticalAlign === 'bottom' ? '#1890ff' : '#333'" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 字体颜色 -->
              <div class="form-group">
                <label>字体颜色</label>
                <ColorPicker
                  :model-value="element.props?.color"
                  @update:model-value="(color) => handleElementPropChange('color', color)"
                />
              </div>

              <!-- 行高 -->
              <div class="form-group">
                <label>行高</label>
                <div class="input-group">
                  <input 
                    type="number" 
                    :value="element.props?.lineHeight"
                    @input="(e) => handleElementPropChange('lineHeight', Number(e.target.value))"
                    min="1"
                    max="3"
                    step="0.1"
                  >
                </div>
              </div>
            </template>

            <!-- 图标样式设置 -->
            <template v-if="element?.type === 'icon'">
              <div class="form-group">
                <label>图标颜色</label>
                <ColorPicker
                  :model-value="element.props?.fill"
                  @update:model-value="(color) => handleElementPropChange('fill', color)"
                />
              </div>

              <div class="form-group">
                <label>边框</label>
                <div class="border-settings">
                  <div class="border-style-wrapper">
                    <div class="border-style-group">
                      <button 
                        class="btn-icon" 
                        :class="{ active: element.props?.strokeStyle === 'solid' }"
                        @click="() => handleElementPropChange('strokeStyle', 'solid')"
                        title="实线"
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <rect x="2" y="7.5" width="12" height="1.5" :fill="element.props?.strokeStyle === 'solid' ? '#1890ff' : '#333'" />
                        </svg>
                      </button>
                      <button 
                        class="btn-icon" 
                        :class="{ active: element.props?.strokeStyle === 'dashed' }"
                        @click="() => handleElementPropChange('strokeStyle', 'dashed')"
                        title="虚线"
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <rect x="2" y="7.5" width="3" height="1.5" :fill="element.props?.strokeStyle === 'dashed' ? '#1890ff' : '#333'" />
                          <rect x="6.5" y="7.5" width="3" height="1.5" :fill="element.props?.strokeStyle === 'dashed' ? '#1890ff' : '#333'" />
                          <rect x="11" y="7.5" width="3" height="1.5" :fill="element.props?.strokeStyle === 'dashed' ? '#1890ff' : '#333'" />
                        </svg>
                      </button>
                      <button 
                        class="btn-icon" 
                        :class="{ active: element.props?.strokeStyle === 'dotted' }"
                        @click="() => handleElementPropChange('strokeStyle', 'dotted')"
                        title="点线"
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <rect x="2" y="7.5" width="1.5" height="1.5" :fill="element.props?.strokeStyle === 'dotted' ? '#1890ff' : '#333'" />
                          <rect x="5.5" y="7.5" width="1.5" height="1.5" :fill="element.props?.strokeStyle === 'dotted' ? '#1890ff' : '#333'" />
                          <rect x="9" y="7.5" width="1.5" height="1.5" :fill="element.props?.strokeStyle === 'dotted' ? '#1890ff' : '#333'" />
                          <rect x="12.5" y="7.5" width="1.5" height="1.5" :fill="element.props?.strokeStyle === 'dotted' ? '#1890ff' : '#333'" />
                        </svg>
                      </button>
                    </div>
                    <input
                      type="number"
                      :value="element.props?.strokeWidth || 0"
                      @input="(e) => handleElementPropChange('strokeWidth', Math.max(0, parseInt(e.target.value) || 0))"
                      min="0"
                      max="20"
                      placeholder="线宽"
                    >
                  </div>
                  <div class="border-color">
                    <label>边框颜色</label>
                    <ColorPicker
                      :model-value="element.props?.stroke"
                      @update:model-value="(color) => handleElementPropChange('stroke', color)"
                    />
                  </div>
                </div>
              </div>
            </template>

            <!-- 头像样式设置 -->
            <template v-if="element?.type === 'avatar'">
              <div class="form-group">
                <div class="avatar-settings">
                  <div class="avatar-row">
                    <div class="form-item">
                      <label>头像索引</label>
                      <div class="input-group">
                        <input 
                          type="number" 
                          :value="element.props?.avatarIndex || 1"
                          @input="(e) => handleElementPropChange('avatarIndex', Math.min(10, Math.max(1, parseInt(e.target.value) || 1)))"
                          min="1"
                          max="10"
                          step="1"
                        >
                      </div>
                    </div>
                    <div class="form-item">
                      <label>边框宽度</label>
                      <div class="input-group">
                        <input 
                          type="number" 
                          :value="element.props?.borderWidth || 0"
                          @input="(e) => handleElementPropChange('borderWidth', Math.max(0, parseInt(e.target.value) || 0))"
                          min="0"
                          max="10"
                          step="1"
                        >
                        <span class="unit">px</span>
                      </div>
                    </div>
                  </div>
                  <div class="form-item">
                    <label>圆角度</label>
                    <div class="radius-control">
                      <input
                        type="range"
                        :value="element.props?.borderRadius || 50"
                        @input="(e) => handleElementPropChange('borderRadius', Math.min(50, Math.max(0, parseInt(e.target.value) || 0)))"
                        min="0"
                        max="50"
                        step="1"
                      >
                      <div class="input-group">
                        <input 
                          type="number" 
                          min="0"
                          max="50"
                          :value="element.props?.borderRadius || 50"
                          @input="(e) => handleElementPropChange('borderRadius', Math.min(50, Math.max(0, parseInt(e.target.value) || 0)))"
                        >
                        <span class="unit">%</span>
                      </div>
                    </div>
                  </div>
                  <div class="form-item">
                    <label>边框颜色</label>
                    <ColorPicker
                      :model-value="element.props?.borderColor"
                      @update:model-value="(color) => handleElementPropChange('borderColor', color)"
                    />
                  </div>
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
                    @click="handleElementPropChange('zIndex', Math.max(1, (element.zIndex || 1) - 1))"
                  >-</button>
                  <input
                    type="number"
                    :value="element.zIndex || 1"
                    @input="(e) => handleElementPropChange('zIndex', Math.max(1, parseInt(e.target.value) || 1))"
                    min="1"
                    step="1"
                  >
                  <button 
                    class="btn-stepper"
                    @click="handleElementPropChange('zIndex', (element.zIndex || 1) + 1)"
                  >+</button>
                </div>
                <button 
                  class="btn-arrow"
                  title="置于顶层"
                  @click="handleElementPropChange('zIndex', 9999)"
                >
                  <Up theme="filled" size="16" fill="#374151" />
                </button>
                <button 
                  class="btn-arrow"
                  title="置于底层"
                  @click="handleElementPropChange('zIndex', 1)"
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
                v-for="(canvas, index) in canvasList" 
                :key="canvas.id"
                class="canvas-item"
                :class="{ active: currentCanvasId === canvas.id }"
                @click="$emit('switch-canvas', canvas.id)"
              >
                <div class="canvas-preview" :style="{ backgroundColor: canvas.config?.backgroundColor || '#ffffff' }">
                  <div class="canvas-overlay"></div>
                </div>
                <div class="canvas-index">{{ index + 1 }}</div>
                <button 
                  v-if="canvasList.length > 1 && index > 0"
                  class="btn-delete" 
                  @click.stop="handleDeleteCanvas(canvas.id)"
                >
                  <Delete theme="outline" size="12" />
                </button>
              </div>
              <button 
                v-if="canvasList.length < 5"
                class="btn-add" 
                @click="handleAddCanvas"
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
              <ColorPicker
                :model-value="getCurrentCanvas()?.config?.backgroundColor || '#ffffff'"
                @update:model-value="updateBackgroundColor"
              />
            </div>
          </div>

          <!-- 辅助功能 -->
          <div class="panel-section">
            <h4>辅助功能</h4>
            <div class="switch-list">
              <!-- 网格 -->
              <div class="switch-item">
                <div class="switch-header">
                  <span class="switch-text">显示网格</span>
                  <Switch 
                    :model-value="getCurrentCanvas()?.config?.showGrid"
                    @update:model-value="(value) => handleConfigChange('showGrid', value)"
                  />
                </div>
              </div>

              <!-- 辅助线 -->
              <div class="switch-item">
                <div class="switch-header">
                  <span class="switch-text">显示辅助线</span>
                  <Switch 
                    :model-value="getCurrentCanvas()?.config?.showGuideLine"
                    @update:model-value="(value) => handleConfigChange('showGuideLine', value)"
                  />
                </div>
              </div>
            </div>
          </div>
        </template>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { 
  Delete, 
  Plus, 
  Setting,
  Up,
  Down,
  AlignHorizontalCenter,
  AlignVerticalCenter,
  AlignLeft,
  AlignRight,
  AlignTop,
  AlignBottom,
  AlignTextCenter,
  AlignTextMiddle,
  DistributeHorizontal,
  DistributeVertical
} from '@icon-park/vue-next'
import Switch from './Switch.vue'
import ColorPicker from './ColorPicker.vue'
import { showToast } from '@/utils/toast'

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
  selectedElements: {
    type: Array,
    default: () => []
  },
  isEditable: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits([
  'update',
  'add-canvas',
  'delete-canvas',
  'switch-canvas',
  'update-canvas-config',
  'align-horizontal-to-canvas',
  'align-vertical-to-canvas',
  'align-left',
  'align-horizontal-center',
  'align-right',
  'align-top',
  'align-vertical-center',
  'align-bottom',
  'align-elements',
  'distribute-elements',
  'spacing-change'
])

// 获取当前画布
const getCurrentCanvas = () => {
  const canvas = props.canvasList.find(canvas => canvas.id === props.currentCanvasId)
  return canvas || null
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
    if (prop === 'width' || prop === 'height') {
      finalValue = Math.max(1, parseInt(value) || 1)
    } else if (prop === 'rotate') {
      finalValue = Math.min(360, Math.max(0, parseInt(value) || 0))
    } else {
      finalValue = Math.max(0, parseInt(value) || 0)
    }
  }

  // 创建更新后的元素对象
  const updatedElement = {
    ...props.element,
    [prop]: finalValue
  }

  // 触发更新事件
  emit('update', updatedElement)
  
  // 立即触发选中事件，强制更新当前选中的元素
  emit('element-select', updatedElement)
}

// 更新画布配置
const handleConfigChange = (key, value) => {
  const currentCanvas = getCurrentCanvas()
  if (currentCanvas) {
    const config = {}
    config[key] = value
    emit('update-canvas-config', {
      canvasId: currentCanvas.id,
      config,
      applyToAll: false
    })
  }
}

// 更新背景颜色
const updateBackgroundColor = (color) => {
  handleConfigChange('backgroundColor', color)
}

// 应用到所有画布
const applyToAllCanvas = () => {
  const currentCanvas = getCurrentCanvas()
  if (currentCanvas) {
    emit('update-canvas-config', {
      canvasId: currentCanvas.id,
      config: {
        backgroundColor: currentCanvas.config?.backgroundColor,
        showGrid: currentCanvas.config?.showGrid,
        showGuideLine: currentCanvas.config?.showGuideLine
      },
      applyToAll: true
    })
  }
}

// 控制网格设置的显示/隐藏
const showGridSettings = ref(false)

// 颜色变量列表 - 使用 localStorage 持久化存储
const colorVars = ref(JSON.parse(localStorage.getItem('colorVars') || '[]'))

// 添加颜色变量
const addColorVar = (color) => {
  if (!color) return
  if (!colorVars.value.includes(color)) {
    colorVars.value.push(color)
    // 保存到 localStorage
    localStorage.setItem('colorVars', JSON.stringify(colorVars.value))
  }
}

// 删除颜色变量
const removeColorVar = (index) => {
  colorVars.value.splice(index, 1)
  // 保存到 localStorage
  localStorage.setItem('colorVars', JSON.stringify(colorVars.value))
}

// 监听画布ID变化，重置网格设置面板
watch(() => props.currentCanvasId, () => {
  showGridSettings.value = false
})

// 控制标尺设置的显示/隐藏
const showRulerSettings = ref(false)

// 更新文本属性
const handleElementPropChange = (prop, value) => {
  if (!props.element) return

  // 创建更新后的元素对象
  const updatedElement = {
    ...props.element,
    props: {
      ...props.element.props,
      [prop]: value
    }
  }

  // 如果是 zIndex 属性，直接更新到元素根级别
  if (prop === 'zIndex') {
    updatedElement.zIndex = value
    delete updatedElement.props.zIndex
  }

  // 触发更新事件
  emit('update', updatedElement)
  
  // 立即触发选中事件，强制更新当前选中的元素
  emit('element-select', updatedElement)
}

const isContentDisabled = computed(() => {
  return props.element?.type === 'resume-field';
});

const isStyleDisabled = computed(() => {
  return false; // 样式属性永远不禁用
});

// 对齐操作
const alignElement = (alignment) => {
  emit('align', alignment)
}

// 添加多选相关的属性
const spacing = ref(10)

// 添加多选相关的方法
const alignElements = (direction) => {
  emit('align-elements', {
    elements: props.selectedElements,
    direction
  })
}

const distributeElements = (direction) => {
  emit('distribute-elements', {
    elements: props.selectedElements,
    direction
  })
}

const handleSpacingChange = () => {
  emit('spacing-change', {
    elements: props.selectedElements,
    spacing: spacing.value
  })
}

// 添加画布
const handleAddCanvas = () => {
  if (!props.isEditable) return  // 添加编辑权限检查
  
  if (props.canvasList.length >= 5) {
    showToast('最多只能添加5个画布', 'warning')
    return
  }
  
  // 找到最小的未使用的索引
  const usedIndexes = props.canvasList.map(canvas => canvas.page_index)
  let newIndex = 0
  while (usedIndexes.includes(newIndex)) {
    newIndex++
  }
  
  // 创建新画布的默认配置
  const newCanvas = {
    id: Date.now(),
    config: {
      width: 794,
      height: 1123,
      showGuideLine: true,
      backgroundColor: '#ffffff',
      showGrid: true,
      gridSize: 10,
      gridColor: 'rgba(0, 0, 0, 0.15)'
    },
    elements: [],
    page_index: newIndex
  }
  
  // 触发添加画布事件
  emit('add-canvas', newCanvas)
}

// 删除画布
const handleDeleteCanvas = (canvasId) => {
  if (!props.isEditable) return  // 添加编辑权限检查
  
  if (props.canvasList.length <= 1) {
    showToast('至少保留一个画布', 'warning')
    return
  }
  
  // 触发删除画布事件
  emit('delete-canvas', canvasId)
}
</script>

<style scoped>
.editor-panel {
  width: 320px;
  padding: 10px;
  height: 100%;
  overflow-y: auto;
  background-color: #f5f5f5;
  border-radius: 8px;
  flex-shrink: 0;  /* 防止面板被压缩 */
}

.panel-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.panel-section {
  padding: 16px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);
}

h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

h4 {
  font-size: 13px;
  font-weight: 500;
  color: #4b5563;
  margin-bottom: 8px;
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
  gap: 8px;
}

.input-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
  min-width: 0; /* 防止子元素溢出 */
}

.input-item label {
  font-size: 12px;
  color: #666;
  margin-bottom: 0;
}

.input-item input {
  width: 100%;
  height: 32px;
  padding: 0 4px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  font-size: 13px;
  color: #374151;
  text-align: center;
}

/* 基础属性中的输入框特殊样式 */
.panel-section:first-of-type .input-group .input-item input {
  padding: 0 2px;
  width: 60px;
}

.panel-section:first-of-type .input-group {
  gap: 4px;
  flex-wrap: nowrap;
  justify-content: space-between;
}

.input-item input:hover {
  border-color: #40a9ff;
}

.input-item input:focus {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.1);
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

.color-picker input[type="color"]:hover {
  border-color: #40a9ff;
}

.color-picker input[type="color"]:focus {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.1);
  outline: none;
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

.color-picker input[type="text"]:hover {
  border-color: #40a9ff;
}

.color-picker input[type="text"]:focus {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.1);
  outline: none;
}

.border-settings {
  width: 100%;
  display: flex !important;
  flex-direction: column !important;
  gap: 8px;
}

.border-style-wrapper {
  display: inline-flex !important;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  background: #f5f5f5;
  padding: 2px 2px 2px 2px;
  border-radius: 6px;
  width: 100% !important;
}

.border-style-group {
  display: flex;
  gap: 2px;
}

.border-style-wrapper input {
  width: 50px;
  height: 28px;
  padding: 0 4px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  font-size: 13px;
  color: #374151;
  text-align: center;
  background: white;
}

.border-color {
  width: 100%;
  margin-top: 4px;
}

.btn-icon {
  width: 32px;
  height: 28px;
  padding: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
  border-radius: 4px;
}

.btn-icon:hover {
  background-color: #f3f4f6;
}

.btn-icon.active {
  color: #1890ff;
  background-color: white;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.btn-icon.active :deep(svg) {
  fill: #1890ff !important;
}

.unit {
  color: #6b7280;
  font-size: 13px;
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
  width: 36px;
  height: 36px;
  padding: 2px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  cursor: pointer;
  background-color: #fff;
}

.color-picker input[type="color"]:hover {
  border-color: #40a9ff;
}

.color-picker input[type="color"]:focus {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.1);
  outline: none;
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

.color-picker input[type="text"]:hover {
  border-color: #40a9ff;
}

.color-picker input[type="text"]:focus {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.1);
  outline: none;
}

.input-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.input-group input[type="number"] {
  width: 70px;
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
  margin-left: 4px;
  color: #999;
  font-size: 12px;
}

.radius-control {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 32px;
}

.radius-control input[type="range"] {
  flex: 1;
  height: 4px;
  -webkit-appearance: none;
  background: #e5e7eb;
  border-radius: 2px;
  outline: none;
}

.radius-control input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  background: white;
  border: 2px solid #1890ff;
  border-radius: 50%;
  cursor: pointer;
  margin-top: 0px;
}

.radius-control input[type="range"]::-moz-range-thumb {
  width: 16px;
  height: 16px;
  background: white;
  border: 2px solid #1890ff;
  border-radius: 50%;
  cursor: pointer;
}

.radius-control input[type="range"]::-ms-thumb {
  width: 16px;
  height: 16px;
  background: white;
  border: 2px solid #1890ff;
  border-radius: 50%;
  cursor: pointer;
}

.radius-control input[type="number"] {
  width: 70px;
  text-align: center;
  height: 32px;
  padding: 0 8px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  font-size: 13px;
  color: #374151;
}

.radius-control input[type="number"]:hover {
  border-color: #40a9ff;
}

.radius-control input[type="number"]:focus {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.1);
  outline: none;
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
}

.rotate-control input[type="range"] {
  flex: 1;
  height: 4px;
  -webkit-appearance: none;
  background: #e5e7eb;
  border-radius: 2px;
  outline: none;
}

.rotate-control input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  background: white;
  border: 2px solid #1890ff;
  border-radius: 50%;
  cursor: pointer;
  margin-top: 0px;
}

.rotate-control input[type="range"]::-moz-range-thumb {
  width: 16px;
  height: 16px;
  background: white;
  border: 2px solid #1890ff;
  border-radius: 50%;
  cursor: pointer;
}

.rotate-control input[type="range"]::-ms-thumb {
  width: 16px;
  height: 16px;
  background: white;
  border: 2px solid #1890ff;
  border-radius: 50%;
  cursor: pointer;
}

.rotate-control input[type="number"] {
  width: 70px;
  text-align: center;
}

.color-settings {
  display: flex;
  flex-direction: column;
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
  height: 4px;
  -webkit-appearance: none;
  background: #e5e7eb;
  border-radius: 2px;
  outline: none;
}

.opacity-control input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  background: white;
  border: 2px solid #1890ff;
  border-radius: 50%;
  cursor: pointer;
  margin-top: 0px;
}

.opacity-control input[type="range"]::-moz-range-thumb {
  width: 16px;
  height: 16px;
  background: white;
  border: 2px solid #1890ff;
  border-radius: 50%;
  cursor: pointer;
}

.opacity-control input[type="range"]::-ms-thumb {
  width: 16px;
  height: 16px;
  background: white;
  border: 2px solid #1890ff;
  border-radius: 50%;
  cursor: pointer;
}

.opacity-control input[type="number"] {
  width: 70px;
  text-align: center;
}

.opacity-control input[type="number"]:hover {
  border-color: #40a9ff;
}

.opacity-control input[type="number"]:focus {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.1);
  outline: none;
}

.switch-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.switch-item:last-child {
  margin-bottom: 0;
}

.switch-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.switch-text {
  font-size: 13px;
  color: #4b5563;
}

:deep(.switch-component) {
  transform: scale(1.2);
  margin-left: 8px;
}

/* 确保开关按钮的点击区域足够大 */
:deep(.switch-component label) {
  min-width: 44px;
  min-height: 22px;
}

.line-cap-settings {
  padding: 8px;
  background: #fafafa;
  border-radius: 6px;
}

.select-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.select-group select {
  height: 32px;
  padding: 0 8px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  background-color: #fff;
  font-size: 13px;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s;
}

.select-group select:hover {
  border-color: #40a9ff;
}

.select-group select:focus {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.1);
  outline: none;
}

.select-group select option {
  padding: 8px;
}

.shadow-settings {
  padding: 8px;
  background: #fafafa;
  border-radius: 6px;
}

.shadow-row {
  margin-bottom: 8px;
}

.shadow-row:last-child {
  margin-bottom: 0;
}

.shadow-row .input-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.shadow-row .input-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.shadow-row .input-item label {
  font-size: 12px;
  color: #666;
  margin-bottom: 0;
}

.shadow-row .input-item input {
  width: 100%;
  height: 32px;
  padding: 0 8px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  font-size: 13px;
  color: #374151;
}

.shadow-row .input-item input[type="color"] {
  padding: 2px 4px;
}

.disabled {
  background-color: #f5f5f5 !important;
  cursor: not-allowed !important;
  color: #999 !important;
  border-color: #d9d9d9 !important;
}

.disabled:hover {
  border-color: #d9d9d9 !important;
}

.btn-icon.disabled {
  opacity: 0.5;
  pointer-events: none;
}

input[type="color"].disabled {
  opacity: 0.6;
}

.color-picker input[type="text"].disabled {
  background-color: #f5f5f5;
}

textarea.disabled:hover {
  border-color: #e5e7eb;
}

.font-settings {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.font-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.font-select {
  flex: 1;
  height: 32px;
  padding: 0 8px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  background-color: #fff;
  font-size: 13px;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s;
}

.font-size {
  width: 60px;
  flex-shrink: 0;
}

.font-size input {
  width: 100%;
  height: 32px;
  padding: 0 4px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  font-size: 13px;
  color: #374151;
  text-align: center;
  background: white;
}

.font-size input:hover {
  border-color: #40a9ff;
}

.font-size input:focus {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.1);
  outline: none;
}

.font-style-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.font-style-row .button-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.font-style-row .button-group button {
  width: 24px;
  height: 24px;
  padding: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
  border-radius: 4px;
}

.font-style-row .button-group button:hover {
  background-color: #f3f4f6;
}

.font-style-row .button-group button.active {
  color: #1890ff;
  background-color: white;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.font-style-row .button-group button.active :deep(svg) {
  fill: #1890ff !important;
}

.avatar-settings {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.avatar-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.form-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.form-item label {
  font-size: 13px;
  color: #4b5563;
}

.form-item .input-group {
  display: flex;
  align-items: center;
  gap: 4px;
}

.form-item input[type="number"] {
  width: 100%;
  height: 32px;
  padding: 0 8px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  font-size: 13px;
  color: #374151;
  background: white;
}

.form-item input[type="number"]:hover {
  border-color: #40a9ff;
}

.form-item input[type="number"]:focus {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.1);
  outline: none;
}

/* 添加对齐控制样式 */
.align-controls {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 6px;
}

.align-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.align-group label {
  font-size: 13px;
  color: #4b5563;
  margin-bottom: 0;
}

.align-group .button-group {
  display: flex;
  gap: 8px;
  background: #f5f5f5;
  padding: 4px;
  border-radius: 6px;
}

.align-group .button-group .btn-icon {
  flex: 1;
  height: 32px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  transition: all 0.2s;
}

.align-group .button-group .btn-icon:hover {
  border-color: #1890ff;
  background: #f0f5ff;
}

.align-group .button-group .btn-icon:hover :deep(svg) {
  fill: #1890ff;
}

.align-group .button-group .btn-icon:active {
  background: #e6f4ff;
}

.multi-select-panel {
  padding: 16px;
}

.panel-section {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 14px;
  font-weight: 500;
  color: #1f2937;
  margin-bottom: 16px;
}

.group-title {
  font-size: 13px;
  color: #4b5563;
  margin-bottom: 8px;
}

.spacing-group {
  margin-top: 16px;
}

.spacing-group .input-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.spacing-group input {
  width: 80px;
  height: 32px;
  padding: 0 8px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  font-size: 13px;
}

.spacing-group .unit {
  font-size: 13px;
  color: #6b7280;
}

.distribute-group {
  margin-top: 16px;
}

.distribute-group .button-group {
  display: flex;
  gap: 8px;
}

/* 按钮样式优化 */
.btn-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-icon:hover {
  border-color: #1890ff;
  background: #f0f5ff;
}

.btn-icon:hover svg {
  fill: #1890ff;
}

.btn-icon:active {
  background: #e6f4ff;
}

.btn-icon svg {
  width: 16px;
  height: 16px;
  fill: #4b5563;
  transition: all 0.2s;
}

.btn-delete {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 18px;
  height: 18px;
  padding: 0;
  border: none;
  border-radius: 50%;
  background: #fff;
  color: #999;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 0;
  transform: scale(0.8);
  transition: all 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.canvas-item:hover .btn-delete {
  opacity: 1;
  transform: scale(1);
}

.btn-delete:hover {
  background: #ff4d4f;
  color: #fff;
}

.btn-delete:active {
  transform: scale(0.9);
}
</style> 