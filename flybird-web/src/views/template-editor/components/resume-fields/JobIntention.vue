<template>
  <div class="job-intention-fields">
    <div class="field-group">
      <div class="field-item"
        v-for="field in jobIntentionFields"
        :key="field.key"
        draggable="true"
        @dragstart="handleDragStart($event, field)"
        @dragend="handleDragEnd"
      >
        <div class="field-preview">
          <div class="field-label">{{ field.label }}</div>
          <div class="field-value">{{ getPreviewValue(field) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { jobIntentionFields } from './config'

const emit = defineEmits(['select-field'])

// 获取预览值
const getPreviewValue = (field) => {
  switch (field.key) {
    case 'job_type':
      return '全职'
    case 'job_status':
      return '在职找工作'
    case 'expected_salary':
      return '15k-20k'
    case 'expected_city':
      return '北京'
    case 'industries':
      return 'IT互联网'
    default:
      return '点击编辑'
  }
}

// 处理拖拽开始
const handleDragStart = (event, field) => {
  event.dataTransfer.effectAllowed = 'copy'
  event.dataTransfer.dropEffect = 'copy'
  
  const componentData = {
    type: 'resume-field',
    component: field.type,
    label: field.label,
    props: {
      ...field,
      isPreview: false
    }
  }
  
  event.dataTransfer.setData('text/plain', JSON.stringify(componentData))
  event.target.classList.add('dragging')
}

const handleDragEnd = (event) => {
  event.target.classList.remove('dragging')
}
</script>

<style scoped>
.job-intention-fields {
  padding: 12px;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field-item {
  padding: 8px;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  cursor: grab;
  transition: all 0.2s;
}

.field-item:hover {
  border-color: #1890ff;
  box-shadow: 0 2px 6px rgba(24, 144, 255, 0.1);
  transform: translateY(-1px);
}

.field-item.dragging {
  opacity: 0.5;
  cursor: grabbing;
}

.field-preview {
  display: flex;
  align-items: center;
  gap: 8px;
}

.field-label {
  font-size: 13px;
  color: #666;
  min-width: 70px;
}

.field-value {
  font-size: 13px;
  color: #333;
  flex: 1;
}
</style> 