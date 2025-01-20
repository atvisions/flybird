<template>
  <div class="triangle-wrapper">
    <svg 
      :width="width" 
      :height="height" 
      :viewBox="`0 0 ${width} ${height}`"
      xmlns="http://www.w3.org/2000/svg"
      preserveAspectRatio="none"
    >
      <path
        :d="getPath"
        :fill="fill"
        :stroke="stroke"
        :stroke-width="strokeWidth"
        :stroke-dasharray="strokeStyle === 'dashed' ? '5,5' : 'none'"
        :opacity="opacity"
        vector-effect="non-scaling-stroke"
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
    default: 2
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

const getPath = computed(() => {
  // 创建直角等腰三角形的路径
  return `M 0 ${props.height} L ${props.width} ${props.height} L 0 0 Z`
})
</script>

<style scoped>
.triangle-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

svg {
  width: 100%;
  height: 100%;
  display: block;
  overflow: visible;
}

path {
  vector-effect: non-scaling-stroke;
}
</style> 