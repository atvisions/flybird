<template>
  <div class="resume-textarea" :style="textareaStyle">
    <div v-if="label" class="label">{{ label }}：</div>
    <el-input
      v-model="modelValue"
      type="textarea"
      :rows="rows"
      :placeholder="placeholder"
      resize="none"
      @update:modelValue="handleInput"
    />
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

const props = defineProps({
  value: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: '请输入'
  },
  rows: {
    type: Number,
    default: 3
  },
  fontSize: {
    type: Number,
    default: 14
  },
  fontWeight: {
    type: String,
    default: 'normal'
  },
  color: {
    type: String,
    default: '#333'
  },
  lineHeight: {
    type: Number,
    default: 1.5
  }
})

const emit = defineEmits(['update:value'])

const modelValue = ref(props.value)

watch(() => props.value, (newVal) => {
  modelValue.value = newVal
})

const textareaStyle = computed(() => ({
  fontSize: `${props.fontSize}px`,
  fontWeight: props.fontWeight,
  color: props.color,
  lineHeight: props.lineHeight
}))

const handleInput = (value) => {
  emit('update:value', value)
}
</script>

<style scoped>
.resume-textarea {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

.label {
  color: #666;
}

:deep(.el-textarea__inner) {
  background: transparent;
  border: none;
  padding: 0;
  box-shadow: none !important;
}

:deep(.el-textarea__inner:focus) {
  box-shadow: none;
}
</style> 