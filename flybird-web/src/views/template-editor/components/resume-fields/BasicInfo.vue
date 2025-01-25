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
  console.log('【BasicInfo】生成字段属性:', {
    field,
    label: field.label,
    dataPath: field.dataPath,
    type: field.type
  })
  
  return {
    label: field.label,
    value: field.defaultValue || '', // 预览时的示例数据
    dataPath: field.dataPath, // 直接使用配置中的 dataPath
    mappingType: field.type, // 添加映射类型
    ...field.defaultStyle
  }
}

const handleDragStart = (event, field) => {
  // 根据字段类型设置特定属性
  const getFieldSpecificProps = (fieldType) => {
    switch (fieldType) {
      case 'avatar':
        return {
          defaultStyle: {
            objectFit: 'cover',
            borderRadius: '50%'
          },
          width: 100,
          height: 100
        }
      case 'textarea':
        return {
          defaultStyle: {
            whiteSpace: 'pre-wrap',
            wordBreak: 'break-word',
            minHeight: '60px',
            padding: '8px'
          },
          width: 300,
          height: 100
        }
      default:
        return {
          defaultStyle: {
            fontSize: field.key === 'name' ? '24px' : '14px',
            fontWeight: field.key === 'name' ? 'bold' : 'normal',
            lineHeight: '1.5'
          },
          width: 200,
          height: 30
        }
    }
  }

  const specificProps = getFieldSpecificProps(field.type)
  
  // 获取字段的映射类型
  const getMappingType = (key) => {
    switch (key) {
      case 'birth_date':
        return 'birth_date'
      case 'location':
        return 'location'
      case 'personal_summary':
        return 'personal_summary'
      case 'avatar':
        return 'avatar'
      default:
        return field.type
    }
  }

  const mappingType = getMappingType(field.key)
  
  console.log('【BasicInfo】开始拖拽字段:', {
    field,
    specificProps,
    dataPath: field.dataPath,
    mappingType
  })
  
  const fieldData = {
    type: 'resume-field',
    component: 'basic_info',
    fieldType: field.type,
    category: 'basic-info',
    field: {
      ...field,
      dataPath: field.dataPath,
      mappingType,
      label: field.label,
      key: field.key,
      defaultStyle: {
        ...field.defaultStyle,
        ...specificProps.defaultStyle
      }
    },
    width: specificProps.width,
    height: specificProps.height,
    props: {
      label: field.label,
      value: '',
      key: field.key,
      dataPath: field.dataPath,
      mappingType,
      defaultStyle: {
        ...field.defaultStyle,
        ...specificProps.defaultStyle
      }
    }
  }
  
  console.log('【BasicInfo】生成的字段数据:', fieldData)
  event.dataTransfer.setData('application/json', JSON.stringify(fieldData))
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