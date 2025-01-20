<template>
  <div 
    class="shape-triangle"
    :style="{
      width: 'var(--width, 100px)',
      height: 'var(--height, 100px)',
      position: 'relative'
    }"
  >
    <div 
      class="triangle-fill"
      :style="{
        borderWidth: `calc(var(--height, 100px) / 2) calc(var(--width, 100px) / 2)`,
        borderColor: `${fill} transparent transparent ${fill}`,
        opacity: opacity
      }"
    ></div>
    <div 
      v-if="strokeWidth > 0"
      class="triangle-stroke"
      :style="{
        borderWidth: `calc((var(--height, 100px) + ${2 * strokeWidth}px) / 2) calc((var(--width, 100px) + ${2 * strokeWidth}px) / 2)`,
        borderColor: `${stroke} transparent transparent ${stroke}`,
        top: `-${strokeWidth}px`,
        left: `-${strokeWidth}px`,
        opacity: opacity
      }"
    ></div>
  </div>
</template>

<script setup>
defineProps({
  fill: {
    type: String,
    default: '#ffffff'
  },
  stroke: {
    type: String,
    default: '#000000'
  },
  strokeWidth: {
    type: Number,
    default: 1
  },
  strokeStyle: {
    type: String,
    default: 'solid'
  },
  opacity: {
    type: Number,
    default: 1
  }
})
</script>

<style scoped>
.shape-triangle {
  box-sizing: border-box;
}

.triangle-fill {
  position: absolute;
  width: 0;
  height: 0;
  border-style: solid;
  box-sizing: border-box;
}

.triangle-stroke {
  position: absolute;
  width: 0;
  height: 0;
  border-style: solid;
  box-sizing: border-box;
  pointer-events: none;
  z-index: -1;
}
</style> 