<template>
  <div class="basic-info-fields">
    <div class="field-group">
      <h3>基本信息</h3>
      <div class="fields-container">
        <div
          v-for="field in basicInfoFields"
          :key="field.key"
          class="field-item"
          draggable="true"
          @dragstart="handleDragStart($event, field)"
        >
          <el-tooltip :content="field.label" placement="top">
            <div class="field-content">
              <component
                :is="getFieldComponent(field.type)"
                v-bind="getFieldProps(field)"
                :style="field.defaultStyle"
              />
            </div>
          </el-tooltip>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { basicInfoFields } from './config'
import { ref } from 'vue'
import ResumeAvatar from '../shapes/ResumeAvatar.vue'
import ResumeText from '../shapes/ResumeText.vue'
import ResumeTextarea from '../shapes/ResumeTextarea.vue'

const getFieldComponent = (type) => {
  const componentMap = {
    avatar: ResumeAvatar,
    text: ResumeText,
    textarea: ResumeTextarea
  }
  return componentMap[type]
}

const getFieldProps = (field) => {
  return {
    label: field.label,
    value: '', // 预览时可以传入示例数据
    ...field.defaultStyle
  }
}

const handleDragStart = (event, field) => {
  event.dataTransfer.setData('application/json', JSON.stringify({
    type: 'resume-field',
    fieldType: field.type,
    category: 'basic-info',
    field
  }))
}
</script>

<style scoped>
.basic-info-fields {
  padding: 16px;
}

.field-group {
  margin-bottom: 24px;
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
  background: #f5f7fa;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  padding: 8px;
  cursor: move;
  transition: all 0.3s;
}

.field-item:hover {
  background: #ecf5ff;
  border-color: #409eff;
}

.field-content {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 40px;
}
</style> 