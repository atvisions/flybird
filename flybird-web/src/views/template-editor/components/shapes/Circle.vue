<template>
  <div 
    class="shape-circle"
    :style="{
      backgroundColor: fill,
      borderColor: stroke,
      borderWidth: `${strokeWidth}px`,
      borderStyle: strokeStyle,
      opacity: opacity
    }"
  ></div>
</template>

<script setup>
defineProps({
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
    default: 1
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
</script>

<style scoped>
.shape-circle {
  position: relative;
  box-sizing: border-box;
  display: block;
  width: var(--width, 100px);
  height: var(--height, 100px);
  border-radius: 50%;
}
</style> 