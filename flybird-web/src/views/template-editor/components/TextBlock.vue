<template>
  <div 
    class="text-block"
    :class="{ 'is-selected': selected }"
    :style="{
      left: `${x}px`,
      top: `${y}px`,
      width: `${width}px`,
      minHeight: `${height}px`,
      color,
      fontSize: `${fontSize}px`,
      fontFamily,
      fontWeight,
      textAlign,
      transform: `rotate(${rotation}deg)`,
      zIndex
    }"
    @click="$emit('select')"
  >
    {{ content }}
  </div>
</template>

<script setup>
defineProps({
  x: {
    type: Number,
    default: 0
  },
  y: {
    type: Number,
    default: 0
  },
  width: {
    type: Number,
    default: 200
  },
  height: {
    type: Number,
    default: 100
  },
  content: {
    type: String,
    default: '双击编辑文本'
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
    type: [String, Number],
    default: 'normal'
  },
  textAlign: {
    type: String,
    default: 'left'
  },
  rotation: {
    type: Number,
    default: 0
  },
  zIndex: {
    type: Number,
    default: 1
  },
  selected: {
    type: Boolean,
    default: false
  }
})

defineEmits(['select', 'update'])
</script>

<style scoped>
.text-block {
  position: absolute;
  user-select: none;
  cursor: move;
  word-break: break-all;
  line-height: 1.5;
}

.text-block.is-selected {
  outline: 2px solid #1890ff;
}
</style> 