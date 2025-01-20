<template>
  <div class="star" :style="style">
    <svg 
      :width="width" 
      :height="height" 
      :viewBox="`0 0 ${width} ${height}`"
      :style="{
        opacity: opacity || 1
      }"
    >
      <path 
        :d="getStarPath()" 
        :fill="fill || '#1890ff'"
        :stroke="stroke || '#096dd9'"
        :stroke-width="strokeWidth || 0"
      />
    </svg>
  </div>
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
  opacity: {
    type: Number,
    default: 1
  }
})

const getStarPath = () => {
  const centerX = props.width / 2
  const centerY = props.height / 2
  const outerRadius = Math.min(props.width, props.height) / 2
  const innerRadius = outerRadius * 0.382
  const points = []
  
  for (let i = 0; i < 10; i++) {
    const radius = i % 2 === 0 ? outerRadius : innerRadius
    const angle = (i * Math.PI) / 5 - Math.PI / 2
    points.push([
      centerX + radius * Math.cos(angle),
      centerY + radius * Math.sin(angle)
    ])
  }
  
  return `M ${points[0][0]},${points[0][1]} ${points.slice(1).map(p => `L ${p[0]},${p[1]}`).join(' ')} Z`
}

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