<template>
  <div 
    class="shape-rectangle"
    :style="{
      width: `${width}px`,
      height: `${height}px`,
      backgroundColor: props.fill || '#1890ff',
      borderColor: props.stroke || '#096dd9',
      borderWidth: `${props.strokeWidth || 0}px`,
      borderStyle: props.strokeStyle || 'solid',
      borderRadius: `${props.radius || 0}px`,
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
  radius: {
    type: Number,
    default: 0
  },
  opacity: {
    type: Number,
    default: 1
  }
})

const style = computed(() => ({
  background: props.fill,
  border: props.strokeWidth ? `${props.strokeWidth}px ${props.strokeStyle} ${props.stroke}` : 'none',
  borderRadius: props.radius ? `${props.radius}px` : '0'
}))
</script>

<style scoped>
.rectangle {
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  display: block;
  position: relative;
  transition: border-radius 0.2s;
}
</style> 