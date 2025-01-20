<template>
  <div class="shape-arrow">
    <svg 
      width="100%" 
      height="100%" 
      viewBox="0 0 100 100" 
      preserveAspectRatio="none"
    >
      <defs>
        <marker
          :id="markerId"
          viewBox="0 0 10 10"
          refX="9"
          refY="5"
          markerWidth="6"
          markerHeight="6"
          orient="auto"
        >
          <path 
            d="M 0 0 L 10 5 L 0 10 z" 
            :fill="stroke"
            :opacity="opacity"
          />
        </marker>
      </defs>
      <line 
        x1="0" 
        y1="50" 
        x2="100" 
        y2="50"
        :stroke="stroke"
        :stroke-width="strokeWidth"
        :stroke-dasharray="strokeStyle === 'dashed' ? '5,5' : ''"
        :opacity="opacity"
        :marker-end="`url(#${markerId})`"
      />
    </svg>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
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

// 生成唯一的marker ID，避免多个箭头组件的marker冲突
const markerId = computed(() => `arrow-marker-${Math.random().toString(36).substr(2, 9)}`)
</script>

<style scoped>
.shape-arrow {
  width: 100%;
  height: 100%;
}
</style> 