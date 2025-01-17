<template>
  <div class="single-layout">
    <div class="layout-column"
      :class="{ 'drag-over': isDragOver }"
      :style="layoutStyles"
      @dragenter="handleDragEnter"
      @dragleave="handleDragLeave"
      @dragover="handleDragOver"
      @drop="handleDrop">
      
      <draggable
        v-model="components"
        :group="{ name: 'components', pull: true, put: true }"
        item-key="id"
        class="component-list"
        :class="{ 'empty': !components.length }"
        @change="handleComponentChange"
      >
        <template #item="{ element }">
          <div class="component-item">
            <div class="component-header">
              <span class="component-name">{{ element.name }}</span>
              <div class="component-actions">
                <v-btn
                  icon="mdi-delete"
                  size="small"
                  color="error"
                  variant="text"
                  @click="removeComponent(element)"
                ></v-btn>
              </div>
            </div>
            <component
              :is="getComponentByType(element.type)"
              :config="element.config"
              @update:config="config => updateComponentConfig(element.id, config)"
            ></component>
          </div>
        </template>

        <template #header>
          <div v-if="!components.length" class="column-placeholder">
            <v-icon size="32" color="rgba(0,0,0,0.2)">mdi-plus</v-icon>
            <div class="text-body-2 text-medium-emphasis mt-2">拖拽组件到此处</div>
          </div>
        </template>
      </draggable>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import draggable from 'vuedraggable'
import { useComponents } from '../composables/useComponents'

const props = defineProps({
  config: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:config'])

const isDragOver = ref(false)
const components = ref(props.config.components || [])

const { getComponentByType } = useComponents()

// 计算布局样式
const layoutStyles = computed(() => {
  const styles = props.config.styles || {}
  const theme = styles.colors || {}
  const spacing = styles.spacing || {}
  const typography = styles.typography?.body || {}
  
  return {
    // 颜色
    backgroundColor: theme.background || '#f5f7fa',
    color: theme.text || '#2c3e50',
    borderColor: theme.border || '#e4e7ed',
    
    // 间距
    padding: spacing.padding || '16px',
    margin: spacing.margin || '0',
    gap: props.config.gap || spacing.gap || '16px',
    
    // 字体
    fontFamily: typography.font || 'Arial',
    fontSize: typography.size || '14px',
    fontWeight: typography.weight || 'normal',
    
    // 其他样式
    borderRadius: styles.borderRadius || '8px',
    ...styles
  }
})

// 监听配置变化
watch(() => props.config, (newConfig) => {
  components.value = newConfig.components || []
}, { deep: true })

// 处理拖拽进入
const handleDragEnter = (event) => {
  event.preventDefault()
  isDragOver.value = true
}

// 处理拖拽离开
const handleDragLeave = (event) => {
  event.preventDefault()
  isDragOver.value = false
}

// 处理拖拽悬停
const handleDragOver = (event) => {
  event.preventDefault()
}

// 处理组件放置
const handleDrop = (event) => {
  event.preventDefault()
  isDragOver.value = false
  
  const componentData = event.dataTransfer.getData('application/json')
  if (componentData) {
    try {
      const component = JSON.parse(componentData)
      if (component.type !== 'layout') {
        addComponent(component)
      }
    } catch (error) {
      console.error('解析组件数据失败:', error)
    }
  }
}

// 添加组件
const addComponent = (component) => {
  const newComponent = {
    id: Date.now(),
    type: component.type,
    name: component.name,
    config: component.config || {}
  }
  components.value.push(newComponent)
  updateConfig()
}

// 移除组件
const removeComponent = (component) => {
  const index = components.value.findIndex(c => c.id === component.id)
  if (index > -1) {
    components.value.splice(index, 1)
    updateConfig()
  }
}

// 更新组件配置
const updateComponentConfig = (componentId, config) => {
  const component = components.value.find(c => c.id === componentId)
  if (component) {
    component.config = config
    updateConfig()
  }
}

// 处理组件变化
const handleComponentChange = (event) => {
  updateConfig()
}

// 更新配置
const updateConfig = () => {
  emit('update:config', {
    ...props.config,
    components: components.value
  })
}
</script>

<style scoped>
.single-layout {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  padding: 20px;
}

.layout-column {
  height: 100%;
  display: flex;
  flex-direction: column;
  border: 2px dashed;
  transition: all 0.3s;
  gap: 12px;
}

.layout-column.drag-over {
  background-color: #ecf5ff !important;
  border-color: #409eff !important;
}

.component-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 120px;
}

.component-list.empty {
  height: 100%;
}

.column-placeholder {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 120px;
  background-color: #ffffff;
  border-radius: 6px;
  color: rgba(0, 0, 0, 0.4);
  transition: all 0.3s;
}

.component-item {
  background-color: #ffffff;
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  overflow: hidden;
  transition: all 0.3s;
}

.component-item:hover {
  border-color: #409eff;
  box-shadow: 0 2px 12px rgba(64, 158, 255, 0.1);
}

.component-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  background-color: #f5f7fa;
  border-bottom: 1px solid #e4e7ed;
}

.component-name {
  font-size: 14px;
  color: #606266;
}

.component-actions {
  display: flex;
  gap: 4px;
}
</style> 