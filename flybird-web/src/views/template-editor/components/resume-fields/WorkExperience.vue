<template>
  <div
    class="work-experience-field"
    draggable="true"
    @dragstart="handleDragStart"
    :class="{ 'is-preview': isPreview }"
  >
    <template v-if="isPreview">
      <div class="preview-content">
        <div class="header">
          <div class="company">{{ previewData.company }}</div>
          <div class="time">{{ previewData.startDate }} - {{ previewData.endDate }}</div>
        </div>
        <div class="info">
          <div class="position">{{ previewData.position }}</div>
          <div class="department" v-if="previewData.department">{{ previewData.department }}</div>
        </div>
        <div class="description" v-if="previewData.description">{{ previewData.description }}</div>
        <div class="achievements" v-if="previewData.achievements">
          <div class="label">工作成就：</div>
          <div class="content">{{ previewData.achievements }}</div>
        </div>
        <div class="technologies" v-if="previewData.technologies">
          <div class="label">技术栈：</div>
          <div class="content">{{ previewData.technologies }}</div>
        </div>
      </div>
    </template>
    <template v-else>
      <div class="field-content">
        <el-icon><Suitcase /></el-icon>
        <span>工作经历</span>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { workExperienceFields } from './config'
import { ElIcon } from 'element-plus'
import { Suitcase } from '@element-plus/icons-vue'

const props = defineProps({
  isPreview: {
    type: Boolean,
    default: false
  },
  data: {
    type: Object,
    default: () => ({})
  }
})

// 预览数据
const previewData = computed(() => ({
  company: props.data.company || '某公司',
  position: props.data.position || '职位名称',
  department: props.data.department || '',
  startDate: props.data.start_date || '2020.01',
  endDate: props.data.end_date || '至今',
  description: props.data.description || '工作描述...',
  achievements: props.data.achievements || '',
  technologies: props.data.technologies || ''
}))

const handleDragStart = (event) => {
  const dragData = {
    type: 'resume-field',
    field: {
      type: 'work-experience',
      label: '工作经历',
      dataPath: 'work_experience[0]',
      fields: [
        {
          type: 'text',
          label: '公司名称',
          key: 'company',
          dataPath: 'work_experience[0].company',
          defaultStyle: {
            fontSize: 16,
            fontWeight: 'bold',
            color: '#333333'
          }
        },
        {
          type: 'text',
          label: '职位名称',
          key: 'position',
          dataPath: 'work_experience[0].position',
          defaultStyle: {
            fontSize: 14,
            color: '#666666'
          }
        },
        {
          type: 'text',
          label: '所在部门',
          key: 'department',
          dataPath: 'work_experience[0].department',
          defaultStyle: {
            fontSize: 14,
            color: '#666666'
          }
        },
        {
          type: 'date',
          label: '开始时间',
          key: 'start_date',
          dataPath: 'work_experience[0].start_date',
          mappingType: 'date',
          defaultStyle: {
            fontSize: 14,
            color: '#666666'
          }
        },
        {
          type: 'date',
          label: '结束时间',
          key: 'end_date',
          dataPath: 'work_experience[0].end_date',
          mappingType: 'date',
          defaultStyle: {
            fontSize: 14,
            color: '#666666'
          }
        },
        {
          type: 'text',
          label: '工作时长',
          key: 'duration',
          dataPath: 'work_experience[0].duration',
          defaultStyle: {
            fontSize: 14,
            color: '#666666'
          }
        },
        {
          type: 'textarea',
          label: '工作描述',
          key: 'description',
          dataPath: 'work_experience[0].description',
          mappingType: 'textarea',
          defaultStyle: {
            fontSize: 14,
            lineHeight: 1.5,
            color: '#666666'
          }
        },
        {
          type: 'textarea',
          label: '工作成就',
          key: 'achievements',
          dataPath: 'work_experience[0].achievements',
          mappingType: 'textarea',
          defaultStyle: {
            fontSize: 14,
            lineHeight: 1.5,
            color: '#666666'
          }
        },
        {
          type: 'textarea',
          label: '技术栈',
          key: 'technologies',
          dataPath: 'work_experience[0].technologies',
          mappingType: 'textarea',
          defaultStyle: {
            fontSize: 14,
            lineHeight: 1.5,
            color: '#666666'
          }
        }
      ]
    }
  }
  event.dataTransfer.setData('text/plain', JSON.stringify(dragData))
}
</script>

<style lang="scss" scoped>
.work-experience-field {
  width: 100%;
  padding: 12px;
  border: 1px dashed #dcdfe6;
  border-radius: 4px;
  cursor: move;
  background-color: #fff;
  transition: all 0.3s;

  &:hover {
    border-color: #409eff;
    background-color: #ecf5ff;
  }

  &.is-preview {
    cursor: default;
    border-style: solid;

    &:hover {
      border-color: #dcdfe6;
      background-color: #fff;
    }
  }

  .field-content {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #606266;

    .el-icon {
      font-size: 16px;
    }
  }

  .preview-content {
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
      
      .company {
        font-size: 16px;
        font-weight: bold;
        color: #303133;
      }
      
      .time {
        font-size: 14px;
        color: #909399;
      }
    }

    .info {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 8px;
      
      .position {
        font-size: 14px;
        color: #606266;
      }
      
      .department {
        font-size: 14px;
        color: #909399;
        &:before {
          content: '|';
          margin-right: 12px;
          color: #dcdfe6;
        }
      }
    }

    .description {
      font-size: 14px;
      color: #606266;
      line-height: 1.6;
      margin-bottom: 8px;
      white-space: pre-line;
    }

    .achievements, .technologies {
      margin-top: 8px;
      
      .label {
        font-size: 14px;
        color: #606266;
        font-weight: 500;
        margin-bottom: 4px;
      }
      
      .content {
        font-size: 14px;
        color: #606266;
        line-height: 1.6;
        white-space: pre-line;
      }
    }
  }
}
</style> 