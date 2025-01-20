<template>
  <SketchRule
    :width="width"
    :height="height"
    :scale="scale"
    :startX="startX"
    :startY="startY"
    :shadow="shadow"
    :cornerActive="true"
    :thick="20"
    :palette="{
      bgColor: '#f5f5f5',         // 背景色
      longfgColor: rulerColor,    // 长刻度颜色
      shortfgColor: rulerColor,   // 短刻度颜色
      fontColor: rulerColor,      // 字体颜色
      shadowColor: '#E8E8E8',     // 阴影颜色
      lineColor: '#E8E8E8',       // 线条颜色
      borderColor: '#e5e7eb',     // 边框颜色
      cornerActiveColor: '#DADADC' // 角落激活颜色
    }"
    @onCornerClick="handleCornerClick"
  />
</template>

<script setup>
import { computed } from 'vue'
import SketchRule from 'vue3-ruler-tool'

const props = defineProps({
  width: {
    type: Number,
    required: true
  },
  height: {
    type: Number,
    required: true
  },
  scale: {
    type: Number,
    default: 1
  },
  offset: {
    type: Object,
    default: () => ({ x: 0, y: 0 })
  },
  rulerColor: {
    type: String,
    default: '#999999'
  }
})

// 计算标尺起始位置
const startX = computed(() => -props.offset.x)
const startY = computed(() => -props.offset.y)

// 标尺配置
const shadow = computed(() => ({
  x: 0,
  y: 0,
  width: props.width,
  height: props.height
}))

// 处理角落点击
const handleCornerClick = () => {
  // 可以在这里添加角落点击的处理逻辑
}
</script>

<style>
:deep(.sketch-ruler) {
  z-index: 10;
  pointer-events: none;
}
</style> 