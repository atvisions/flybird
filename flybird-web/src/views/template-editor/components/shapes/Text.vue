<template>
  <div 
    class="shape-text"
    :style="{
      color,
      fontSize: `${fontSize}px`,
      fontFamily,
      fontWeight,
      fontStyle: italic ? 'italic' : 'normal',
      textDecoration: underline ? 'underline' : 'none',
      textAlign,
      opacity,
      lineHeight: `${lineHeight}em`
    }"
    :contenteditable="editable"
    @blur="handleBlur"
  >{{ content }}</div>
</template>

<script setup>
const props = defineProps({
  content: {
    type: String,
    default: '文本'
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
  italic: {
    type: Boolean,
    default: false
  },
  underline: {
    type: Boolean,
    default: false
  },
  textAlign: {
    type: String,
    default: 'left'
  },
  lineHeight: {
    type: Number,
    default: 1.5
  },
  opacity: {
    type: Number,
    default: 1
  },
  editable: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:content'])

const handleBlur = (e) => {
  emit('update:content', e.target.textContent)
}
</script>

<style scoped>
.shape-text {
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  white-space: pre-wrap;
  word-break: break-word;
  outline: none;
  cursor: text;
}

.shape-text:focus {
  outline: none;
}
</style> 