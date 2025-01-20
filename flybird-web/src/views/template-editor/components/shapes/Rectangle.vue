<template>
  <div class="rectangle" :style="style"></div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  fill: {
    type: String,
    default: '#ffffff'
  },
  stroke: {
    type: String,
    default: '#000000'
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
  },
  rotation: {
    type: Number,
    default: 0
  },
  radius: {
    type: Number,
    default: 0
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