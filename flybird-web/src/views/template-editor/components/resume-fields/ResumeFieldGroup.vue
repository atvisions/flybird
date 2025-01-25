<template>
  <div class="resume-field-group">
    <div 
      class="group-header" 
      @click="toggleExpand"
      :draggable="props.groupKey === 'basicInfo'"
      @dragstart="props.groupKey === 'basicInfo' ? handleDragStart($event) : null"
    >
      <el-icon :class="{ 'is-expand': isExpanded }">
        <ArrowRight />
      </el-icon>
      <span class="group-title">{{ title }}</span>
    </div>
    <div v-show="isExpanded" class="group-content">
      <div
        v-for="field in fields"
        :key="field.key"
        class="field-item"
        draggable="true"
        @dragstart="handleFieldDragStart($event, field)"
      >
        <el-tooltip :content="field.label" placement="right">
          <div class="field-preview">
            <component
              :is="getFieldComponent(field.type)"
              v-bind="getFieldProps(field)"
            />
          </div>
        </el-tooltip>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ArrowRight } from '@element-plus/icons-vue'
import ResumeAvatar from '../shapes/ResumeAvatar.vue'
import ResumeText from '../shapes/ResumeText.vue'
import ResumeTextarea from '../shapes/ResumeTextarea.vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  fields: {
    type: Array,
    required: true
  },
  groupKey: {
    type: String,
    required: true
  }
})

const isExpanded = ref(true)

const toggleExpand = () => {
  isExpanded.value = !isExpanded.value
}

const getFieldComponent = (type) => {
  const componentMap = {
    avatar: ResumeAvatar,
    text: ResumeText,
    textarea: ResumeTextarea
  }
  return componentMap[type] || ResumeText
}

const getFieldProps = (field) => {
  return {
    label: field.label,
    value: '', // 预览时可以传入示例数据
    ...field.defaultStyle
  }
}

// 处理基本信息组的拖拽
const handleDragStart = (event) => {
  const dragData = {
    type: 'basic-info',
    props: {
      fields: props.fields.map(field => ({
        type: field.type || 'text',
        label: field.label,
        key: field.key,
        dataPath: field.dataPath,
        width: field.width || 200,
        height: field.height || 30,
        defaultStyle: field.defaultStyle || {}
      }))
    }
  }
  event.dataTransfer.setData('text/plain', JSON.stringify(dragData))
}

// 处理单个字段的拖拽
const handleFieldDragStart = (event, field) => {
  const dragData = {
    type: 'resume-field',
    props: {
      type: field.type,
      label: field.label,
      dataPath: `basic_info.${field.key}`,
      value: '',
      isPreview: false,
      width: field.type === 'avatar' ? 100 : (field.width || 200),
      height: field.type === 'avatar' ? 100 : (field.height || 30),
      ...field.defaultStyle
    }
  }
  event.dataTransfer.setData('text/plain', JSON.stringify(dragData))
}
</script>

<style scoped>
.resume-field-group {
  border-radius: 4px;
  margin-bottom: 8px;
  background: #fff;
}

.group-header {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  cursor: pointer;
  user-select: none;
}

.group-header:hover {
  background: #f5f7fa;
}

.group-title {
  margin-left: 8px;
  font-size: 14px;
  color: #333;
}

.is-expand {
  transform: rotate(90deg);
}

.group-content {
  padding: 0 16px 16px;
}

.field-item {
  margin-bottom: 8px;
  cursor: move;
}

.field-item:last-child {
  margin-bottom: 0;
}

.field-preview {
  padding: 8px;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  background: #f5f7fa;
  transition: all 0.3s;
}

.field-preview:hover {
  background: #ecf5ff;
  border-color: #409eff;
}

:deep(.el-icon) {
  transition: transform 0.3s;
}
</style> 