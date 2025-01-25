<template>
  <div class="resume-group" :style="containerStyle">
    <div class="group-header">
      <div class="group-title">{{ title }}</div>
    </div>
    <div class="group-content">
      <div v-for="field in fields" :key="field.key" class="field-item">
        <ResumeField
          :type="field.type"
          :label="field.label"
          :data-path="field.dataPath"
          :mapping-type="field.mappingType"
          :mapping-options="field.mappingOptions"
          :width="field.width || 200"
          :height="field.height || 30"
          :default-style="field.defaultStyle"
          :is-preview="false"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import ResumeField from './ResumeField.vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  fields: {
    type: Array,
    required: true
  },
  width: {
    type: Number,
    default: 400
  },
  height: {
    type: Number,
    default: 300
  }
})

const containerStyle = computed(() => ({
  width: `${props.width}px`,
  minHeight: `${props.height}px`
}))
</script>

<style scoped>
.resume-group {
  background: white;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.group-header {
  margin-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 12px;
}

.group-title {
  font-size: 18px;
  font-weight: 500;
  color: #333;
  margin: 0;
}

.group-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field-item {
  min-height: 30px;
}
</style> 