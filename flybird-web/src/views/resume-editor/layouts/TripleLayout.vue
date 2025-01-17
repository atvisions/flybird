<template>
  <div class="triple-layout">
    <div class="layout-columns">
      <!-- 左列 -->
      <div class="layout-column"
        @dragenter="handleDragEnter"
        @dragleave="handleDragLeave"
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
            {{ component.name }}
          </div>
        </template>
      </div>

      <!-- 中间列 -->
      <div class="layout-column"
        @dragenter="handleDragEnter"
        @dragleave="handleDragLeave"
        @dragover="handleDragOver"
        @drop="e => handleDrop(e, 'middle')">
        <div v-if="!middleComponents.length" class="column-placeholder">
          <v-icon size="32" color="rgba(0,0,0,0.2)">mdi-plus</v-icon>
          <div class="text-body-2 text-medium-emphasis mt-2">拖拽组件到此处</div>
        </div>
        <template v-else>
          <div v-for="component in middleComponents" 
            :key="component.id"
            class="component-item">
            {{ component.name }}
          </div>
        </template>
      </div>

      <!-- 右列 -->
      <div class="layout-column"
        @dragenter="handleDragEnter"
        @dragleave="handleDragLeave"
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
            {{ component.name }}
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  config: {
    type: Object,
    default: () => ({
      layout: 'triple',
      columns: 3,
      columnWidth: ['33.33%', '33.33%', '33.33%']
    })
  }
})

const leftComponents = ref([])
const middleComponents = ref([])
const rightComponents = ref([])

const handleDragEnter = (event) => {
  event.preventDefault()
  event.target.classList.add('drag-over')
}

const handleDragLeave = (event) => {
  event.preventDefault()
  event.target.classList.remove('drag-over')
}

const handleDragOver = (event) => {
  event.preventDefault()
}

const handleDrop = (event, column) => {
  event.preventDefault()
  event.target.classList.remove('drag-over')
  
  const componentData = event.dataTransfer.getData('application/json')
  if (componentData) {
    try {
      const component = JSON.parse(componentData)
      if (column === 'left') {
        leftComponents.value.push(component)
      } else if (column === 'middle') {
        middleComponents.value.push(component)
      } else {
        rightComponents.value.push(component)
      }
    } catch (error) {
      console.error('解析组件数据失败:', error)
    }
  }
}
</script>

<style scoped>
.triple-layout {
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
}

.layout-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
  border: 2px dashed #e4e7ed;
  border-radius: 8px;
  padding: 16px;
  transition: all 0.3s;
  gap: 12px;
}

.layout-column.drag-over {
  background-color: #ecf5ff;
  border-color: #409eff;
}

.column-placeholder {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 120px;
  color: rgba(0, 0, 0, 0.4);
  background-color: white;
  border-radius: 6px;
  transition: all 0.3s;
}

.component-item {
  padding: 16px;
  background-color: white;
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  transition: all 0.3s;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
}

.component-item:hover {
  border-color: #409eff;
  box-shadow: 0 2px 12px rgba(64, 158, 255, 0.1);
}
</style> 