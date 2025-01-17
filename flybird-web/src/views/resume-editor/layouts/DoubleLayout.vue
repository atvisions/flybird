<template>
  <div class="double-layout">
    <div class="layout-columns" :style="layoutStyles">
      <!-- 左列 -->
      <div class="layout-column"
        :class="{ 'drag-over': isDragOverLeft }"
        @dragenter="handleDragEnter($event, 'left')"
        @dragleave="handleDragLeave($event, 'left')"
        @dragover="handleDragOver"
        @drop="e => handleDrop(e, 'left')">
        <div v-if="!leftComponents.length" class="column-placeholder">
          <v-icon size="32" color="rgba(0,0,0,0.2)">mdi-plus</v-icon>
          <div class="text-body-2 text-medium-emphasis mt-2">拖拽组件到此处</div>
        </div>
        <template v-else>
          <div v-for="component in leftComponents" 
            :key="component.id"
            class="component-item">
            <div class="component-header">
              <span class="component-name">{{ component.name }}</span>
              <div class="component-actions">
                <v-btn
                  icon="mdi-delete"
                  size="small"
                  color="error"
                  variant="text"
                  @click="removeComponent(component, 'left')"
                ></v-btn>
              </div>
            </div>
            <component
              :is="getComponentByType(component.type)"
              :config="component.config"
              @update:config="config => updateComponentConfig(component.id, config, 'left')"
            ></component>
          </div>
        </template>
      </div>

      <!-- 右列 -->
      <div class="layout-column"
        :class="{ 'drag-over': isDragOverRight }"
        @dragenter="handleDragEnter($event, 'right')"
        @dragleave="handleDragLeave($event, 'right')"
        @dragover="handleDragOver"
        @drop="e => handleDrop(e, 'right')">
        <div v-if="!rightComponents.length" class="column-placeholder">
          <v-icon size="32" color="rgba(0,0,0,0.2)">mdi-plus</v-icon>
          <div class="text-body-2 text-medium-emphasis mt-2">拖拽组件到此处</div>
        </div>
        <template v-else>
          <div v-for="component in rightComponents" 
            :key="component.id"
            class="component-item">
            <div class="component-header">
              <span class="component-name">{{ component.name }}</span>
              <div class="component-actions">
                <v-btn
                  icon="mdi-delete"
                  size="small"
                  color="error"
                  variant="text"
                  @click="removeComponent(component, 'right')"
                ></v-btn>
              </div>
            </div>
            <component
              :is="getComponentByType(component.type)"
              :config="component.config"
              @update:config="config => updateComponentConfig(component.id, config, 'right')"
            ></component>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useComponents } from '../composables/useComponents'

const props = defineProps({
  config: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:config'])

const leftComponents = ref(props.config.leftComponents || [])
const rightComponents = ref(props.config.rightComponents || [])
const isDragOverLeft = ref(false)
const isDragOverRight = ref(false)

const { getComponentByType } = useComponents()

// 计算布局样式
const layoutStyles = computed(() => ({
  backgroundColor: props.config.styles?.backgroundColor || '#f5f7fa',
  borderColor: props.config.styles?.borderColor || '#e4e7ed',
  padding: props.config.styles?.padding || '16px',
  borderRadius: props.config.styles?.borderRadius || '8px',
  ...props.config.styles
}))

// 监听配置变化
watch(() => props.config, (newConfig) => {
  leftComponents.value = newConfig.leftComponents || []
  rightComponents.value = newConfig.rightComponents || []
}, { deep: true })

// 处理拖拽进入
const handleDragEnter = (event, column) => {
  event.preventDefault()
  if (column === 'left') {
    isDragOverLeft.value = true
  } else {
    isDragOverRight.value = true
  }
}

// 处理拖拽离开
const handleDragLeave = (event, column) => {
  event.preventDefault()
  if (column === 'left') {
    isDragOverLeft.value = false
  } else {
    isDragOverRight.value = false
  }
}

// 处理拖拽悬停
const handleDragOver = (event) => {
  event.preventDefault()
}

// 处理组件放置
const handleDrop = (event, column) => {
  event.preventDefault()
  if (column === 'left') {
    isDragOverLeft.value = false
  } else {
    isDragOverRight.value = false
  }
  
  const componentData = event.dataTransfer.getData('application/json')
  if (componentData) {
    try {
      const component = JSON.parse(componentData)
      if (component.type !== 'layout') {
        addComponent(component, column)
      }
    } catch (error) {
      console.error('解析组件数据失败:', error)
    }
  }
}

// 添加组件
const addComponent = (component, column) => {
  const newComponent = {
    id: Date.now(),
    type: component.type,
    name: component.name,
    config: component.config || {}
  }
  if (column === 'left') {
    leftComponents.value.push(newComponent)
  } else {
    rightComponents.value.push(newComponent)
  }
  updateConfig()
}

// 移除组件
const removeComponent = (component, column) => {
  const components = column === 'left' ? leftComponents : rightComponents
  const index = components.value.findIndex(c => c.id === component.id)
  if (index > -1) {
    components.value.splice(index, 1)
    updateConfig()
  }
}

// 更新组件配置
const updateComponentConfig = (componentId, config, column) => {
  const components = column === 'left' ? leftComponents : rightComponents
  const component = components.value.find(c => c.id === componentId)
  if (component) {
    component.config = config
    updateConfig()
  }
}

// 更新配置
const updateConfig = () => {
  emit('update:config', {
    ...props.config,
    leftComponents: leftComponents.value,
    rightComponents: rightComponents.value
  })
}
</script>

<style scoped>
.double-layout {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  padding: 20px;
}

.layout-columns {
  display: flex;
  gap: 20px;
  height: 100%;
  border: 2px dashed;
  transition: all 0.3s;
}

.layout-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  transition: all 0.3s;
}

.layout-column.drag-over {
  background-color: #ecf5ff !important;
  border-color: #409eff !important;
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