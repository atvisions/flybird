<template>
  <div 
    class="avatar-element"
    :style="{
      width: `${width}px`,
      height: `${height}px`,
      opacity: props.opacity || 1,
      borderWidth: `${props.borderWidth || 0}px`,
      borderStyle: props.borderWidth ? 'solid' : 'none',
      borderColor: props.borderColor || '#e5e7eb',
      borderRadius: `${props.borderRadius || 50}%`
    }"
  >
    <img :src="avatarSrc" class="avatar-image" :style="{ borderRadius: `${props.borderRadius || 50}%` }" />
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
  content: {
    type: String,
    default: '{{avatar}}'
  },
  opacity: {
    type: Number,
    default: 1
  },
  avatarIndex: {
    type: Number,
    default: 1
  },
  borderWidth: {
    type: Number,
    default: 0
  },
  borderColor: {
    type: String,
    default: '#e5e7eb'
  },
  borderRadius: {
    type: Number,
    default: 50
  }
})

const avatarSrc = computed(() => {
  const index = String(props.avatarIndex || 1).padStart(2, '0')
  return `/face/face-${index}.png`
})

defineEmits(['update'])
</script>

<style scoped>
.avatar-element {
  box-sizing: border-box;
  overflow: hidden;
  user-select: none;
  background: white;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style> 