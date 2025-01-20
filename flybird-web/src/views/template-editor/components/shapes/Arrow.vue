<template>
  <svg 
    :width="width" 
    :height="height" 
    :viewBox="`0 0 ${width} ${height}`"
    xmlns="http://www.w3.org/2000/svg"
    preserveAspectRatio="none"
  >
    <defs>
      <marker
        v-if="startArrow !== 'none'"
        :id="`start-arrow-${id}`"
        :markerWidth="startArrowSize"
        :markerHeight="startArrowSize"
        refX="0"
        refY="5"
        orient="auto"
        markerUnits="strokeWidth"
      >
        <path
          :d="getArrowPath(startArrow)"
          :fill="stroke"
          :stroke="stroke"
          :stroke-width="1"
        />
      </marker>
      <marker
        v-if="endArrow !== 'none'"
        :id="`end-arrow-${id}`"
        :markerWidth="endArrowSize"
        :markerHeight="endArrowSize"
        refX="10"
        refY="5"
        orient="auto"
        markerUnits="strokeWidth"
      >
        <path
          :d="getArrowPath(endArrow)"
          :fill="stroke"
          :stroke="stroke"
          :stroke-width="1"
        />
      </marker>
    </defs>
    <line
      :x1="strokeWidth"
      :y1="height / 2"
      :x2="width - strokeWidth"
      :y2="height / 2"
      :stroke="stroke"
      :stroke-width="strokeWidth"
      :stroke-dasharray="strokeStyle === 'dashed' ? '5,5' : 'none'"
      :stroke-linecap="lineCap"
      :stroke-linejoin="lineJoin"
      :opacity="opacity"
      :marker-start="startArrow !== 'none' ? `url(#start-arrow-${id})` : ''"
      :marker-end="endArrow !== 'none' ? `url(#end-arrow-${id})` : ''"
      vector-effect="non-scaling-stroke"
    />
  </svg>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  id: {
    type: [String, Number],
    required: true
  },
  width: {
    type: Number,
    required: true
  },
  height: {
    type: Number,
    required: true
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
  },
  startArrow: {
    type: String,
    default: 'none'
  },
  endArrow: {
    type: String,
    default: 'arrow'
  },
  startArrowSize: {
    type: Number,
    default: 10
  },
  endArrowSize: {
    type: Number,
    default: 10
  },
  lineCap: {
    type: String,
    default: 'butt'
  },
  lineJoin: {
    type: String,
    default: 'miter'
  }
})

const getArrowPath = (type) => {
  switch (type) {
    case 'arrow':
      return 'M 0 0 L 10 5 L 0 10 z'
    case 'dot':
      return 'M 5,0 A 5,5 0 1,1 5,10 A 5,5 0 1,1 5,0 Z'
    case 'diamond':
      return 'M 0 5 L 5 0 L 10 5 L 5 10 z'
    default:
      return ''
  }
}
</script>

<style scoped>
svg {
  display: block;
  width: 100%;
  height: 100%;
  overflow: visible;
}
</style> 