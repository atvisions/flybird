<template>
  <div class="job-intention-fields">
    <div 
      class="field-group"
      draggable="true"
      @dragstart="handleDragStart"
    >
      <h3>求职意向</h3>
      <div class="fields-container">
        <div
          v-for="field in jobIntentionFields"
          :key="field.key"
          class="field-item"
        >
          <div class="field-content">
            {{ field.label }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { jobIntentionFields } from './config'
import { ref } from 'vue'

const handleDragStart = (event) => {
  const dragData = {
    type: 'job-intention',
    component: 'jobIntention',
    field: {
      key: 'job_intention',
      label: '求职意向',
      type: 'group',
      fields: jobIntentionFields
    }
  }
  
  console.log('求职意向拖拽数据:', dragData)
  event.dataTransfer.setData('text/plain', JSON.stringify(dragData))
}
</script>

<style scoped>
.job-intention-fields {
  padding: 16px;
}

.field-group {
  margin-bottom: 24px;
  background: #f5f7fa;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 16px;
  cursor: move;
  transition: all 0.3s;
}

.field-group:hover {
  background: #ecf5ff;
  border-color: #409eff;
}

.field-group h3 {
  font-size: 16px;
  margin-bottom: 16px;
  color: #333;
}

.fields-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 12px;
}

.field-item {
  background: white;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  padding: 8px;
}

.field-content {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 40px;
}
</style> 