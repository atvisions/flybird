<template>
  <Text
    v-bind="$props"
    @update:content="$emit('update:content', $event)"
  />
</template>

<script setup>
import Text from './Text.vue'

const props = defineProps({
  content: {
    type: String,
    default: '标题'
  },
  color: {
    type: String,
    default: '#000000'
  },
  fontSize: {
    type: Number,
    default: 24
  },
  fontFamily: {
    type: String,
    default: 'Arial'
  },
  fontWeight: {
    type: [String, Number],
    default: 'bold'
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
    default: 'center'
  },
  lineHeight: {
    type: Number,
    default: 1.2
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

defineEmits(['update:content'])
</script> 