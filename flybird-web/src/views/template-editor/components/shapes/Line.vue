<template>
  <div class="shape-line">
    <svg 
      width="100%" 
      height="100%" 
      viewBox="0 0 100 100" 
      preserveAspectRatio="none"
    >
      <line 
        x1="0" 
        y1="50" 
        x2="100" 
        y2="50"
        :stroke="stroke"
        :stroke-width="strokeWidth"
        :stroke-dasharray="strokeStyle === 'dashed' ? '5,5' : ''"
        :opacity="opacity"
      />
    </svg>
  </div>
</template>

<script setup>
defineProps({
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
.shape-line {
  width: 100%;
  height: 100%;
}
</style> 