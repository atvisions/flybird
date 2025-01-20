<template>
  <div class="circle" :style="style"></div>
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
  width: {
    type: Number,
    default: 100
  },
  height: {
    type: Number,
    default: 100
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