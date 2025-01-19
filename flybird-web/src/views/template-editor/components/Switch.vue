<template>
  <button 
    class="switch"
    :class="{ checked: checked }"
    type="button"
    role="switch"
    :aria-checked="checked"
    @click="$emit('change', !checked)"
  >
    <span class="switch-handle"></span>
  </button>
</template>

<script setup>
defineProps({
  checked: {
    type: Boolean,
    default: false
  }
})

defineEmits(['change'])
</script>

<style scoped>
.switch {
  position: relative;
  display: inline-flex;
  align-items: center;
  width: 36px;
  height: 20px;
  padding: 0;
  border: none;
  border-radius: 10px;
  background-color: #bfbfbf;
  cursor: pointer;
  transition: all 0.2s;
}

.switch.checked {
  background-color: #1890ff;
}

.switch-handle {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.2s;
}

.switch.checked .switch-handle {
  left: 18px;
}

.switch:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

.switch:active .switch-handle {
  width: 20px;
}

.switch.checked:active .switch-handle {
  left: 14px;
}
</style> 