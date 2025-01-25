<template>
  <div 
    class="resume-text canvas-element"
    :style="textStyle"
  >
    <div 
      class="text-content"
      :style="contentStyle"
    >
      {{ value || `[${label}]` }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  value: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    default: ''
  },
  width: {
    type: Number,
    default: 200
  },
  height: {
    type: Number,
    default: 40
  },
  textAlign: {
    type: String,
    default: 'left'
  },
  verticalAlign: {
    type: String,
    default: 'middle'
  },
  opacity: {
    type: Number,
    default: 1
  },
  color: {
    type: String,
    default: '#000000'
  },
  fontSize: {
    type: Number,
    default: 14
  },
  fontFamily: {
    type: String,
    default: 'Arial'
  },
  fontWeight: {
    type: String,
    default: 'normal'
  },
  fontStyle: {
    type: String,
    default: 'normal'
  },
  lineHeight: {
    type: Number,
    default: 1.5
  },
  labelColor: {
    type: String,
    default: '#666666'
  },
  dataPath: {
    type: String,
    required: true
  },
  zIndex: {
    type: Number,
    default: 1
  }
})

const textStyle = computed(() => ({
  width: '100%',
  height: '100%',
  display: 'flex',
  alignItems: props.verticalAlign === 'top' ? 'flex-start' : 
             props.verticalAlign === 'bottom' ? 'flex-end' : 'center',
  opacity: props.opacity,
  color: props.color,
  fontSize: `${props.fontSize}px`,
  fontFamily: props.fontFamily,
  fontWeight: props.fontWeight,
  fontStyle: props.fontStyle,
  lineHeight: props.lineHeight,
  padding: '4px',
  boxSizing: 'border-box',
  zIndex: props.zIndex
}))

const labelStyle = computed(() => ({
  color: props.labelColor,
  fontSize: `${props.fontSize}px`,
  fontWeight: 500,
  flexShrink: 0
}))

const contentStyle = computed(() => ({
  width: '100%',
  display: 'block',
  textAlign: props.textAlign
}))
</script>

<style scoped>
.resume-text {
  box-sizing: border-box;
  overflow: hidden;
  word-break: break-word;
  user-select: none;
  position: relative;
}

.text-content {
  outline: none;
  width: 100%;
  min-height: 1em;
  overflow: visible;
  white-space: pre-wrap;
  word-break: break-word;
}

.text-label {
  margin-right: 4px;
  white-space: pre-wrap;
}

.text-value {
  flex: 1;
  overflow: visible;
  white-space: pre-wrap;
  word-break: break-word;
}
</style> 