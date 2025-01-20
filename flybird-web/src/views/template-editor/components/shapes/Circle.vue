<template>
  <div 
    class="shape-circle"
    :style="{
      width: `${width}px`,
      height: `${height}px`,
      backgroundColor: props.fill || '#1890ff',
      borderColor: props.stroke || '#096dd9',
      borderWidth: `${props.strokeWidth || 0}px`,
      borderStyle: props.strokeStyle || 'solid',
      borderRadius: '50%',
      opacity: props.opacity || 1
    }"
  ></div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  width: {
    type: Number,
    required: true
  },
  height: {
    type: Number,
    required: true
  },
  fill: {
    type: String,
    default: '#1890ff'
  },
  stroke: {
    type: String,
    default: '#096dd9'
  },
  strokeWidth: {
    type: Number,
    default: 0
  },
  strokeStyle: {
    type: String,
    default: 'solid'
  },
  opacity: {
    type: Number,
    default: 1
  }
})

const style = computed(() => ({
  width: '100%',
  height: '100%',
  background: props.fill,
  border: props.strokeWidth ? `${props.strokeWidth}px ${props.strokeStyle} ${props.stroke}` : 'none',
  borderRadius: '50%',
  boxSizing: 'border-box'
}))
</script>

<style scoped>
.circle {
  display: block;
  position: relative;
}
</style> 