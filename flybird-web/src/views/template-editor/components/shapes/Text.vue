<template>
  <div 
    class="text-element"
    :style="{
      width: `${width}px`,
      height: `${height}px`,
      color: props.color || '#000000',
      fontSize: `${props.fontSize || 14}px`,
      fontFamily: props.fontFamily ? `${props.fontFamily}, var(--font-sans)` : 'var(--font-sans)',
      fontWeight: props.fontWeight || 'normal',
      fontStyle: props.fontStyle || 'normal',
      lineHeight: props.lineHeight || 1.5,
      opacity: props.opacity || 1,
      padding: '4px',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center'
    }"
  >
    <div 
      class="text-content" 
      :contenteditable="isEditable"
      @input="handleInput"
      @blur="handleBlur"
      @mousedown.stop
      @dblclick="handleDoubleClick"
      :style="{
        textAlign: props.textAlign || 'left',
        width: '100%',
        fontFamily: 'inherit',
        fontWeight: 'inherit',
        fontStyle: 'inherit',
        alignSelf: props.verticalAlign === 'top' ? 'flex-start' : props.verticalAlign === 'bottom' ? 'flex-end' : 'center',
        justifySelf: props.textAlign === 'left' ? 'flex-start' : props.textAlign === 'right' ? 'flex-end' : 'center',
        pointerEvents: isEditing ? 'auto' : 'none'
      }"
    >{{ props.content || '请输入文本' }}</div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  width: {
    type: Number,
    required: true
  },
  height: {
    type: Number,
    required: true
  },
  content: {
    type: String,
    default: '请输入文本'
  },
  textAlign: {
    type: String,
    default: 'left'
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
  fontStyle: {
    type: String,
    default: 'normal'
  },
  lineHeight: {
    type: Number,
    default: 1.5
  },
  opacity: {
    type: Number,
    default: 1
  },
  contentEditable: {
    type: Boolean,
    default: true
  },
  verticalAlign: {
    type: String,
    default: 'center'
  }
})

const emit = defineEmits(['update'])

const isEditable = computed(() => props.contentEditable)

const isEditing = ref(false)

const handleInput = (e) => {
  if (!props.contentEditable) return
  const updatedProps = {
    content: e.target.textContent,
    textAlign: props.textAlign,
    color: props.color,
    fontSize: props.fontSize,
    fontFamily: props.fontFamily,
    fontWeight: props.fontWeight,
    fontStyle: props.fontStyle,
    lineHeight: props.lineHeight,
    opacity: props.opacity,
    verticalAlign: props.verticalAlign
  }
  emit('update', { props: updatedProps })
}

const handleDoubleClick = (e) => {
  e.stopPropagation()
  isEditing.value = true
}

const handleBlur = (e) => {
  if (!props.contentEditable) return
  isEditing.value = false
  const updatedProps = {
    content: e.target.textContent,
    textAlign: props.textAlign,
    color: props.color,
    fontSize: props.fontSize,
    fontFamily: props.fontFamily,
    fontWeight: props.fontWeight,
    fontStyle: props.fontStyle,
    lineHeight: props.lineHeight,
    opacity: props.opacity,
    verticalAlign: props.verticalAlign
  }
  emit('update', { props: updatedProps })
}
</script>

<style scoped>
.text-element {
  box-sizing: border-box;
  overflow: hidden;
  word-break: break-word;
  user-select: none;
}

.text-content {
  outline: none;
  user-select: text;
  width: 100%;
  min-height: 1em;
}

.text-content:focus {
  outline: none;
}

.text-content[contenteditable="false"] {
  user-select: none;
  cursor: default;
}
</style> 