<template>
  <div 
    class="text-element"
    :style="{
      width: `${width}px`,
      height: `${height}px`,
      color: props.color || '#000000',
      fontSize: `${props.fontSize || 14}px`,
      fontFamily: props.fontFamily || 'Arial',
      lineHeight: props.lineHeight || 1.5,
      opacity: props.opacity || 1,
      padding: '4px'
    }"
  >
    <div 
      class="text-content" 
      contenteditable="true"
      @input="handleInput"
      @blur="handleBlur"
      :style="{
        textAlign: props.textAlign || 'left',
        width: '100%',
        height: '100%'
      }"
    >{{ props.content || '请输入文本' }}</div>
  </div>
</template>

<script setup>
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
  lineHeight: {
    type: Number,
    default: 1.5
  },
  opacity: {
    type: Number,
    default: 1
  }
})

const emit = defineEmits(['update'])

const handleInput = (e) => {
  emit('update', {
    props: {
      textAlign: props.textAlign,
      color: props.color,
      fontSize: props.fontSize,
      fontFamily: props.fontFamily,
      lineHeight: props.lineHeight,
      opacity: props.opacity,
      content: e.target.textContent
    }
  })
}

const handleBlur = (e) => {
  emit('update', {
    props: {
      textAlign: props.textAlign,
      color: props.color,
      fontSize: props.fontSize,
      fontFamily: props.fontFamily,
      lineHeight: props.lineHeight,
      opacity: props.opacity,
      content: e.target.textContent
    }
  })
}
</script>

<style scoped>
.text-element {
  box-sizing: border-box;
  overflow: hidden;
  word-break: break-word;
  user-select: none;
  background: white;
}

.text-content {
  outline: none;
  user-select: text;
  width: 100%;
  height: 100%;
}

.text-content:focus {
  outline: none;
}
</style> 