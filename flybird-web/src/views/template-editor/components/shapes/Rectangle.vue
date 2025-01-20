<template>
  <div 
    class="shape-rectangle"
    :style="{
      backgroundColor: fill,
      borderColor: stroke,
      borderWidth: `${strokeWidth}px`,
      borderStyle: strokeStyle,
      opacity: opacity,
      transform: `rotate(${rotation || 0}deg)`,
      transformOrigin: 'center center',
      borderRadius: typeof radius === 'number' ? `${radius}px` : '0'
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
  },
  rotation: {
    type: Number,
    default: 0
  },
  radius: {
    type: [Number, String],
    default: 0
  }
})
</script>

<style scoped>
.shape-rectangle {
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  display: block;
  position: relative;
  transition: border-radius 0.2s;
}
</style> 