<template>
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 48 48"
    :style="{ transform: \`scale(\${scale})\` }"
  >
    <g v-if="type === 'phone'">
      <path
        d="M10,20 C10,10 20,10 24,10 C28,10 38,10 38,20 C38,30 28,38 24,38 C20,38 10,30 10,20"
        fill="#FFE5B9"
        stroke="#FF9A5B"
        stroke-width="2"
      />
      <circle cx="24" cy="24" r="8" fill="#FF9A5B" />
      <path
        d="M22,22 L26,26 M26,22 L22,26"
        stroke="#FFE5B9"
        stroke-width="2"
        stroke-linecap="round"
      />
    </g>
    <g v-else-if="type === 'email'">
      <path
        d="M8,16 L24,28 L40,16 L40,36 L8,36 L8,16"
        fill="#B4E6FF"
        stroke="#4A90E2"
        stroke-width="2"
      />
      <path
        d="M8,36 L24,24 L40,36"
        fill="none"
        stroke="#4A90E2"
        stroke-width="2"
      />
    </g>
    <!-- 可以继续添加更多图标类型 -->
  </svg>
</template>

<script setup>
defineProps({
  type: {
    type: String,
    required: true
  },
  size: {
    type: Number,
    default: 48
  },
  scale: {
    type: Number,
    default: 1
  }
})
</script> 