<template>
  <div class="star" :style="style">
    <svg width="100%" height="100%" viewBox="0 0 100 100" preserveAspectRatio="none">
      <path 
        :d="starPath" 
        :fill="fill"
        :stroke="stroke"
        :stroke-width="strokeWidth"
        :stroke-dasharray="strokeStyle === 'dashed' ? '5,5' : ''"
      />
    </svg>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  points: {
    type: Number,
    default: 5
  },
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

const starPath = computed(() => {
  const points = props.points
  const outerRadius = 50
  const innerRadius = outerRadius * 0.382 // 黄金比例
  let path = ''
  
  for (let i = 0; i < points * 2; i++) {
    const radius = i % 2 === 0 ? outerRadius : innerRadius
    const angle = (i * Math.PI) / points
    const x = 50 + radius * Math.sin(angle)
    const y = 50 - radius * Math.cos(angle)
    path += (i === 0 ? 'M' : 'L') + x + ',' + y
  }
  
  return path + 'Z'
})

const style = computed(() => ({
  width: '100%',
  height: '100%',
  position: 'relative',
  boxSizing: 'border-box'
}))
</script>

<style scoped>
.star {
  display: block;
}

.star svg {
  display: block;
}
</style> 