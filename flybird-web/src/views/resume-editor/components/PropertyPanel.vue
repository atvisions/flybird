<template>
  <div class="property-panel">
    <template v-if="selectedElement">
      <div class="panel-header">
        <h3 class="panel-title">{{ panelTitle }}</h3>
      </div>
      
      <div class="panel-content">
        <!-- 圆角设置 -->
        <div class="form-item" v-if="showBorderRadius">
          <label>圆角</label>
          <div class="slider-wrapper">
            <div class="d-flex align-center">
              <v-slider
                v-model="borderRadius"
                :min="0"
                :max="100"
                :step="1"
                hide-details
                class="mr-2"
              ></v-slider>
              <v-text-field
                v-model="borderRadius"
                type="number"
                style="width: 70px"
                density="compact"
                hide-details
                variant="outlined"
              ></v-text-field>
            </div>
          </div>
        </div>

        <!-- 数据绑定 -->
        <div class="form-item" v-if="selectedElement?.type === 'text' || selectedElement?.type === 'image'">
          <label>数据绑定</label>
          <div class="d-flex gap-2">
            <v-select
              v-model="dataBinding"
              :items="filteredDataFields"
              density="compact"
              hide-details
              variant="outlined"
              :placeholder="bindingPlaceholder"
              clearable
              class="flex-grow-1"
              item-title="label"
              item-value="field"
            >
              <template v-slot:item="{ item, props }">
                <v-list-item
                  v-if="item.raw.type === 'group'"
                  :title="item.raw.label"
                  disabled
                  class="text-primary"
                ></v-list-item>
                <v-list-item
                  v-else
                  v-bind="props"
                  :title="item.raw.label"
                  :value="item.raw.field"
                ></v-list-item>
              </template>
            </v-select>
            <v-btn
              variant="outlined"
              density="compact"
              @click="applyDataBinding"
              :disabled="!dataBinding"
            >
              绑定
            </v-btn>
          </div>
          <div class="mt-2 text-caption text-grey">
            {{ bindingTip }}
          </div>
        </div>

        <!-- 背景色设置 -->
        <div class="form-item" v-if="showBackgroundColor">
          <label>背景色</label>
          <v-color-picker
            v-model="backgroundColor"
            hide-inputs
            mode="hex"
            width="100%"
            class="mt-2"
          ></v-color-picker>
        </div>

        <!-- 文字样式设置 -->
        <template v-if="selectedElement?.type === 'text'">
          <div class="form-item">
            <label>文字颜色</label>
            <v-color-picker
              v-model="textColor"
              hide-inputs
              mode="hex"
              width="100%"
              class="mt-2"
            ></v-color-picker>
          </div>

          <div class="form-item">
            <label>字体大小</label>
            <v-slider
              v-model="fontSize"
              :min="12"
              :max="72"
              :step="1"
              hide-details
              class="mr-2"
            >
              <template v-slot:append>
                <v-text-field
                  v-model="fontSize"
                  type="number"
                  style="width: 70px"
                  density="compact"
                  hide-details
                  variant="outlined"
                ></v-text-field>
              </template>
            </v-slider>
          </div>

          <div class="form-item">
            <label>对齐方式</label>
            <div class="d-flex gap-2">
              <v-btn-toggle
                v-model="textAlign"
                density="compact"
                color="primary"
              >
                <v-btn value="left">
                  <v-icon>mdi-format-align-left</v-icon>
                </v-btn>
                <v-btn value="center">
                  <v-icon>mdi-format-align-center</v-icon>
                </v-btn>
                <v-btn value="right">
                  <v-icon>mdi-format-align-right</v-icon>
                </v-btn>
              </v-btn-toggle>
            </div>
          </div>

          <div class="form-item">
            <label>字体粗细</label>
            <v-switch
              v-model="isBold"
              color="primary"
              hide-details
              label="加粗"
              density="compact"
              inset
            ></v-switch>
          </div>

          <div class="form-item">
            <label>字体</label>
            <v-select
              v-model="fontFamily"
              :items="fontFamilies"
              item-title="title"
              item-value="value"
              density="compact"
              hide-details
              variant="outlined"
            ></v-select>
          </div>
        </template>

        <!-- 尺寸信息 -->
        <div class="form-item">
          <label>尺寸</label>
          <div class="size-inputs">
            <v-text-field
              v-model.number="width"
              type="number"
              label="宽度"
              density="compact"
              hide-details
              variant="outlined"
            ></v-text-field>
            <v-text-field
              v-model.number="height"
              type="number"
              label="高度"
              density="compact"
              hide-details
              variant="outlined"
            ></v-text-field>
          </div>
        </div>

        <!-- 层级控制 -->
        <div class="form-item">
          <label>层级</label>
          <div class="d-flex gap-2">
            <v-btn
              variant="outlined"
              density="compact"
              prepend-icon="mdi-arrow-up"
              @click="handleZIndexChange('up')"
            >
              上移一层
            </v-btn>
            <v-btn
              variant="outlined"
              density="compact"
              prepend-icon="mdi-arrow-down"
              @click="handleZIndexChange('down')"
            >
              下移一层
            </v-btn>
          </div>
        </div>
      </div>
    </template>
    
    <div v-else class="empty-state">
      <v-icon icon="mdi-select" size="40" color="grey-lighten-1"></v-icon>
      <p>请选择一个元素</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  selectedElement: {
    type: Object,
    default: null
  },
  dataFields: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update'])

// 属性状态
const borderRadius = ref(0)
const backgroundColor = ref('#409EFF')
const width = ref(200)
const height = ref(200)

// 文字相关状态
const textColor = ref('#333333')
const fontSize = ref(16)
const textAlign = ref('left')
const isBold = ref(false)
const fontFamily = ref('Microsoft YaHei')

// 字体选项
const fontFamilies = [
  { title: '微软雅黑', value: '"Microsoft YaHei", "PingFang SC", "Hiragino Sans GB"' },
  { title: '宋体', value: 'SimSun, "Songti SC"' },
  { title: '黑体', value: 'SimHei, "Heiti SC"' },
  { title: '楷体', value: 'KaiTi, "Kaiti SC"' },
  { title: '仿宋', value: 'FangSong, "STFangsong"' },
  { title: 'Arial', value: 'Arial, "Helvetica Neue", Helvetica' },
  { title: 'Times New Roman', value: '"Times New Roman", Times, serif' },
  { title: '思源黑体', value: '"Source Han Sans CN", "Noto Sans CJK SC"' }
]

const dataBinding = ref('')

// 计算属性
const panelTitle = computed(() => {
  if (!props.selectedElement) return ''
  switch (props.selectedElement.type) {
    case 'image':
      return '图片属性'
    case 'shape':
      return '形状属性'
    default:
      return '元素属性'
  }
})

const showBorderRadius = computed(() => {
  return props.selectedElement?.type === 'image' || 
         (props.selectedElement?.type === 'shape' && props.selectedElement?.shapeType !== 'triangle')
})

const showBackgroundColor = computed(() => {
  return props.selectedElement?.type === 'shape'
})

// 将数据字段按组分类
const groupedDataFields = computed(() => {
  const groups = {}
  props.dataFields.forEach(field => {
    if (!groups[field.group]) {
      groups[field.group] = []
    }
    groups[field.group].push(field)
  })

  const result = []
  Object.keys(groups).forEach(group => {
    // 添加组标题
    result.push({
      type: 'group',
      label: group,
      field: null
    })
    // 添加组内字段
    result.push(...groups[group])
  })

  return result
})

// 监听选中元素变化
watch(() => props.selectedElement, (newElement) => {
  if (newElement) {
    // 更新圆角值
    borderRadius.value = parseInt(newElement.styles?.borderRadius || 0)
    // 更新背景色
    backgroundColor.value = newElement.styles?.backgroundColor || '#409EFF'
    // 更新尺寸
    width.value = newElement.width
    height.value = newElement.height
    // 更新文字样式
    if (newElement.type === 'text') {
      textColor.value = newElement.styles?.color || '#333333'
      fontSize.value = parseInt(newElement.styles?.fontSize) || 16
      textAlign.value = newElement.styles?.textAlign || 'left'
      isBold.value = newElement.styles?.fontWeight === 'bold'
      fontFamily.value = newElement.styles?.fontFamily || 'Microsoft YaHei'
    }
  }
}, { immediate: true })

// 监听圆角变化
watch(borderRadius, (newValue) => {
  handleStyleChange('borderRadius', `${newValue}px`)
})

// 监听背景色变化
watch(backgroundColor, (newValue) => {
  handleStyleChange('backgroundColor', newValue)
})

// 监听尺寸变化
watch([width, height], () => {
  handleSizeChange()
})

// 监听文字颜色变化
watch(textColor, (newValue) => {
  handleStyleChange('color', newValue)
})

// 监听字体大小变化
watch(fontSize, (newValue) => {
  handleStyleChange('fontSize', `${newValue}px`)
})

// 监听对齐方式变化
watch(textAlign, (newValue) => {
  handleStyleChange('textAlign', newValue)
})

// 监听字体粗细变化
watch(isBold, (newValue) => {
  handleStyleChange('fontWeight', newValue ? 'bold' : 'normal')
})

// 监听字体变化
watch(fontFamily, (newValue) => {
  handleStyleChange('fontFamily', newValue)
})

// 计算属性
const bindingPlaceholder = computed(() => {
  return props.selectedElement?.type === 'image' 
    ? '选择要绑定的图片字段' 
    : '选择要绑定的字段'
})

const bindingTip = computed(() => {
  return props.selectedElement?.type === 'image'
    ? '提示：绑定后图片将自动替换为用户的对应图片'
    : '提示：绑定后的文本将显示为 {{字段名}}，用户使用模板时会自动替换为对应的数据'
})

// 根据元素类型过滤数据字段
const filteredDataFields = computed(() => {
  const groups = {}
  props.dataFields.forEach(field => {
    // 根据元素类型过滤字段
    if (props.selectedElement?.type === 'image' && field.type !== 'image') {
      return
    }
    if (props.selectedElement?.type === 'text' && field.type !== 'text') {
      return
    }
    
    if (!groups[field.group]) {
      groups[field.group] = []
    }
    groups[field.group].push(field)
  })

  const result = []
  Object.keys(groups).forEach(group => {
    // 只添加有字段的组
    if (groups[group].length > 0) {
      // 添加组标题
      result.push({
        type: 'group',
        label: group,
        field: null
      })
      // 添加组内字段
      result.push(...groups[group])
    }
  })

  return result
})

// 应用数据绑定
const applyDataBinding = () => {
  if (!props.selectedElement || !dataBinding.value) return
  
  const field = props.dataFields.find(f => f.field === dataBinding.value)
  if (!field) return

  if (props.selectedElement.type === 'image') {
    emit('update', {
      ...props.selectedElement,
      dataBinding: {
        field: dataBinding.value,
        label: field.label
      }
    })
  } else if (props.selectedElement.type === 'text') {
    emit('update', {
      ...props.selectedElement,
      content: `{{${dataBinding.value}}}`,
      dataBinding: {
        field: dataBinding.value,
        label: field.label
      }
    })
  }

  // 清空选择
  dataBinding.value = ''
}

// 监听选中元素变化时，重置数据绑定选择
watch(() => props.selectedElement, () => {
  dataBinding.value = ''
}, { immediate: true })

// 处理样式变化
const handleStyleChange = (property, value) => {
  if (!props.selectedElement) return
  
  emit('update', {
    ...props.selectedElement,
    styles: {
      ...props.selectedElement.styles,
      [property]: value
    }
  })
}

// 处理尺寸变化
const handleSizeChange = () => {
  if (!props.selectedElement) return
  
  emit('update', {
    ...props.selectedElement,
    width: width.value,
    height: height.value
  })
}

// 处理层级变化
const handleZIndexChange = (direction) => {
  if (!props.selectedElement) return
  
  const currentZIndex = parseInt(props.selectedElement.styles?.zIndex || 0)
  const newZIndex = direction === 'up' ? currentZIndex + 1 : currentZIndex - 1
  
  emit('update', {
    ...props.selectedElement,
    styles: {
      ...props.selectedElement.styles,
      zIndex: newZIndex
    }
  })
}
</script>

<style scoped>
.property-panel {
  width: 300px;
  height: 100%;
  border-left: 1px solid #e0e0e0;
  background: #ffffff;
  display: flex;
  flex-direction: column;
}

.panel-header {
  padding: 16px;
  border-bottom: 1px solid #e0e0e0;
}

.panel-title {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin: 0;
}

.panel-content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.form-item {
  margin-bottom: 20px;
}

.form-item label {
  display: block;
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
}

.slider-wrapper {
  padding: 0 8px;
}

.size-inputs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #909399;
  gap: 12px;
}

.empty-state p {
  font-size: 14px;
  margin: 0;
}
</style> 