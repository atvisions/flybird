<template>
  <button 
    class="switch"
    :class="{ 'switch-checked': modelValue }"
    @click="toggle"
    type="button"
  >
    <div class="switch-handle"></div>
  </button>
</template>

<script setup>
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

const toggle = () => {
  emit('update:modelValue', !props.modelValue)
}
</script>

<style scoped>
.switch {
  position: relative;
  display: inline-block;
  width: 28px;
  height: 16px;
  background-color: rgba(0, 0, 0, 0.25);
  border-radius: 100px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  padding: 0;
}

.switch-checked {
  background-color: #1890ff;
}

.switch-handle {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 12px;
  height: 12px;
  background-color: #fff;
  border-radius: 50%;
  transition: all 0.2s;
}

.switch-checked .switch-handle {
  left: 14px;
}

.switch:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

.switch:active .switch-handle {
  width: 14px;
}

.switch-checked:active .switch-handle {
  left: 12px;
}
</style> 