<template>
  <Text
    class="resume-field"
    :width="width"
    :height="height" 
    :content="content"
    :textAlign="textAlign"
    :color="color"
    :fontSize="fontSize"
    :fontFamily="fontFamily"
    :lineHeight="lineHeight"
    :opacity="opacity"
    :contentEditable="false"
    @update="handleUpdate"
  />
</template>

<script setup>
import Text from './Text.vue'

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
    default: ''
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

const handleUpdate = (data) => {
  // 过滤掉 content 更新,只允许样式更新
  const { content: _, ...styleProps } = data.props
  emit('update', { props: styleProps })
}
</script>

<style scoped>
.resume-field {
  box-sizing: border-box;
  overflow: hidden;
  word-break: break-word;
  user-select: none;
}
</style> 