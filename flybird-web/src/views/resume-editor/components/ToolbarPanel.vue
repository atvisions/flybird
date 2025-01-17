<template>
  <div class="toolbar-panel">
    <v-expansion-panels>
      <!-- 模板列表 -->
      <v-expansion-panel>
        <v-expansion-panel-title>
          <div class="d-flex align-center">
            <v-icon class="mr-2">mdi-file-document-outline</v-icon>
            模板列表
          </div>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <div v-if="loading" class="d-flex justify-center">
            <v-progress-circular indeterminate></v-progress-circular>
          </div>
          <div v-else-if="templates.length === 0" class="text-center pa-4">
            暂无模板
          </div>
          <div v-else class="template-list">
            <v-card
              v-for="template in templates"
              :key="template.id"
              class="mb-4"
              variant="outlined"
            >
              <v-img
                :src="template.thumbnail"
                height="160"
                cover
                class="bg-grey-lighten-2"
              >
                <template v-slot:placeholder>
                  <div class="d-flex align-center justify-center fill-height">
                    <v-icon icon="mdi-image" size="48" color="grey-lighten-1"></v-icon>
                  </div>
                </template>
              </v-img>

              <v-card-title class="text-subtitle-1 font-weight-bold">
                {{ template.name }}
                <v-chip
                  v-if="template.is_vip"
                  color="warning"
                  size="small"
                  class="ml-2"
                >
                  VIP
                </v-chip>
              </v-card-title>

              <v-card-text class="text-body-2">
                {{ template.description }}
              </v-card-text>

              <v-card-actions>
                <v-btn
                  color="primary"
                  variant="text"
                  block
                  @click="handleTemplateSelect(template)"
                >
                  使用此模板
                </v-btn>
              </v-card-actions>
            </v-card>
          </div>
        </v-expansion-panel-text>
      </v-expansion-panel>

      <!-- 设计元素 -->
      <v-expansion-panel>
        <v-expansion-panel-title>
          <div class="d-flex align-center">
            <v-icon class="mr-2">mdi-shape-outline</v-icon>
            设计元素
          </div>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <div class="design-elements">
            <!-- 图片元素 -->
            <div 
              class="design-element"
              draggable="true"
              @dragstart="(e) => handleElementDragStart('image', e)"
            >
              <v-img
                src="/images.jpeg"
                width="60"
                height="60"
                class="rounded"
              ></v-img>
              <div class="element-label">图片</div>
            </div>

            <!-- 矩形 -->
            <div 
              class="design-element"
              draggable="true"
              @dragstart="(e) => handleElementDragStart('rectangle', e)"
            >
              <div class="shape-preview rectangle"></div>
              <div class="element-label">矩形</div>
            </div>

            <!-- 三角形 -->
            <div 
              class="design-element"
              draggable="true"
              @dragstart="(e) => handleElementDragStart('triangle', e)"
            >
              <div class="shape-preview triangle"></div>
              <div class="element-label">三角形</div>
            </div>

            <!-- 圆形 -->
            <div 
              class="design-element"
              draggable="true"
              @dragstart="(e) => handleElementDragStart('circle', e)"
            >
              <div class="shape-preview circle"></div>
              <div class="element-label">圆形</div>
            </div>

            <!-- 文字 -->
            <div 
              class="design-element"
              draggable="true"
              @dragstart="(e) => handleElementDragStart('text', e)"
            >
              <div class="text-preview">
                <v-icon icon="mdi-format-text" size="32" color="primary"></v-icon>
              </div>
              <div class="element-label">文字</div>
            </div>
          </div>
        </v-expansion-panel-text>
      </v-expansion-panel>

      <!-- 布局组件面板 -->
      <v-expansion-panel>
        <v-expansion-panel-title>布局组件</v-expansion-panel-title>
        <v-expansion-panel-text>
          <div class="components-grid">
            <div
              v-for="component in layoutComponents"
              :key="component.id"
              class="component-item"
              draggable="true"
              @dragstart="(e) => handleLayoutDragStart(e, component)"
            >
              <v-icon :icon="component.icon" size="24" class="mb-1"></v-icon>
              <span class="component-name">{{ component.name }}</span>
            </div>
          </div>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useTemplateStore } from '@/stores/template'

const emit = defineEmits(['element-dragstart', 'template-select'])

// 模板相关
const templateStore = useTemplateStore()
const templates = ref([])
const loading = ref(false)

// 获取模板列表
const fetchTemplates = async () => {
  console.log('开始获取模板列表...')
  loading.value = true
  try {
    const response = await templateStore.getTemplates({
      page: 1,
      page_size: 50,
      ordering: '-created_at',
      status: 'pending,approved'  // 获取待审核和已通过的模板
    })
    console.log('获取到的完整响应:', response)
    console.log('响应数据中的results:', response?.data?.results)
    
    if (response?.data?.results) {
      templates.value = response.data.results
      console.log('设置后的模板数据:', templates.value)
      console.log('模板ID列表:', templates.value.map(t => t.id))
    } else {
      console.error('获取模板列表失败: 无数据')
      templates.value = []
    }
  } catch (error) {
    console.error('获取模板列表失败:', error)
    templates.value = []
  } finally {
    loading.value = false
    console.log('模板列表获取完成，当前模板数量:', templates.value.length)
  }
}

// 暴露刷新方法给父组件
defineExpose({
  refreshTemplates: fetchTemplates
})

// 选择模板
const handleTemplateSelect = (template) => {
  console.log('选择模板:', template)
  emit('template-select', template)
}

// 设计元素拖拽开始
const handleElementDragStart = (type, event) => {
  const elementConfig = {
    width: 100,
    height: 100,
    styles: {}
  }
  
  // 根据类型设置默认配置
  switch (type) {
    case 'rectangle':
    case 'circle':
    case 'triangle':
      elementConfig.styles = {
        backgroundColor: '#409EFF'
      }
      break
    case 'text':
      elementConfig.content = '点击编辑文本'
      elementConfig.styles = {
        fontSize: '14px',
        color: '#333333'
      }
      break
    case 'image':
      elementConfig.width = 200
      elementConfig.height = 200
      elementConfig.content = '/images.jpeg'
      break
  }

  event.dataTransfer.setData('element-type', type)
  event.dataTransfer.setData('element-config', JSON.stringify(elementConfig))
  event.dataTransfer.effectAllowed = 'move'
  emit('element-dragstart', type)
}

onMounted(() => {
  fetchTemplates()
})

// 布局组件列表
const layoutComponents = ref([
  {
    id: 'single',
    type: 'layout',
    name: '单栏布局',
    icon: 'mdi-view-stream',
    config: {
      type: 'single',
      columns: 1
    }
  },
  {
    id: 'double',
    type: 'layout',
    name: '双栏布局',
    icon: 'mdi-view-sequential',
    config: {
      type: 'double',
      columns: 2
    }
  }
])

// 处理布局组件拖拽开始
const handleLayoutDragStart = (event, component) => {
  const elementData = {
    type: 'layout',
    config: component.config
  }
  event.dataTransfer.setData('element', JSON.stringify(elementData))
  event.dataTransfer.effectAllowed = 'move'
  emit('element-dragstart', 'layout')
}
</script>

<style scoped>
.toolbar-panel {
  width: 280px;
  height: 100%;
  border-right: 1px solid #e0e0e0;
  background: #ffffff;
  overflow-y: auto;
}

.template-list {
  padding: 12px;
}

.template-list .v-card {
  transition: all 0.3s ease;
}

.template-list .v-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.components-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  padding: 12px;
}

.component-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 12px;
  background: #f5f7fa;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  cursor: move;
  transition: all 0.3s;
}

.component-item:hover {
  background: #ecf5ff;
  border-color: #409eff;
}

.component-name {
  font-size: 12px;
  color: #606266;
  margin-top: 4px;
  text-align: center;
}

.design-elements {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  padding: 12px;
}

.design-element {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: #f5f7fa;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  cursor: move;
  transition: all 0.3s;
}

.design-element:hover {
  background: #ecf5ff;
  border-color: #409eff;
}

.element-label {
  font-size: 12px;
  color: #606266;
  text-align: center;
}

.shape-preview {
  width: 60px;
  height: 60px;
  border: 2px solid #dcdfe6;
}

.shape-preview.rectangle {
  background-color: #409EFF;
}

.shape-preview.circle {
  background-color: #E6A23C;
  border-radius: 50%;
}

.shape-preview.triangle {
  background-color: #67C23A;
  clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
}

.text-preview {
  width: 60px;
  height: 60px;
  border: 2px solid #dcdfe6;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
}
</style> 