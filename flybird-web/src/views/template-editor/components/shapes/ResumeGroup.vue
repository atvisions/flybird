<template>
  <div class="resume-group">
    <div class="group-header">
      <div class="group-title">{{ label }}</div>
    </div>
    <div class="group-content">
      <template v-if="isArray">
        <div class="array-item" v-for="(item, index) in defaultData" :key="index">
          <div v-for="(field, key) in fields" :key="key" class="field-item">
            <div class="field-label">{{ field.label }}</div>
            <ResumeField
              :content="item[key] || '暂无数据'"
              :width="200"
              :height="24"
              :fontSize="13"
              :color="'#333'"
              :lineHeight="1.5"
              :contentEditable="false"
            />
          </div>
        </div>
      </template>
      <template v-else>
        <div v-for="(field, key) in fields" :key="key" class="field-item">
          <div class="field-label">{{ field.label }}</div>
          <ResumeField
            :content="defaultData[key] || '暂无数据'"
            :width="200"
            :height="24"
            :fontSize="13"
            :color="'#333'"
            :lineHeight="1.5"
            :contentEditable="false"
          />
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import ResumeField from './ResumeField.vue'

defineProps({
  label: {
    type: String,
    required: true
  },
  fields: {
    type: Object,
    required: true
  },
  isArray: {
    type: Boolean,
    default: false
  },
  defaultData: {
    type: [Object, Array],
    default: () => ({})
  }
})
</script>

<style scoped>
.resume-group {
  width: 100%;
  height: 100%;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.group-header {
  padding: 12px 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.group-title {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.group-content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.array-item {
  padding: 12px;
  background: #f8fafc;
  border-radius: 6px;
  margin-bottom: 12px;
}

.array-item:last-child {
  margin-bottom: 0;
}

.field-item {
  margin-bottom: 12px;
}

.field-item:last-child {
  margin-bottom: 0;
}

.field-label {
  font-size: 12px;
  color: #666;
  margin-bottom: 4px;
}

.field-value {
  font-size: 13px;
  color: #333;
  line-height: 1.5;
}
</style> 