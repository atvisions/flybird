<template>
  <div class="resume-text" :style="textStyle">
    <span v-if="label" class="label">{{ label }}：</span>
    <el-input
      v-model="modelValue"
      :placeholder="placeholder"
      @update:modelValue="handleInput"
    />
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

const props = defineProps({
  value: {
    type: [String, Number],
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
  }
})

const emit = defineEmits(['update:value'])

const modelValue = ref(props.value)

watch(() => props.value, (newVal) => {
  modelValue.value = newVal
})

const textStyle = computed(() => ({
  fontSize: `${props.fontSize}px`,
  fontWeight: props.fontWeight,
  color: props.color
}))

const handleInput = (value) => {
  emit('update:value', value)
}
</script>

<style scoped>
.resume-text {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
}

.label {
  white-space: nowrap;
  color: #666;
}

:deep(.el-input__wrapper) {
  background: transparent;
  box-shadow: none !important;
}

:deep(.el-input__inner) {
  border: none;
  background: transparent;
  padding: 0;
}

:deep(.el-input__inner:focus) {
  box-shadow: none;
}
</style> 