<template>
  <div class="editor-toolbar">
    <div class="toolbar-left">
      <button class="btn">
        <Undo theme="outline" size="16" />
      </button>
      <button class="btn">
        <Redo theme="outline" size="16" />
      </button>
    </div>
    <div class="toolbar-right">
      <button class="btn" @click="handleClear">
        <Delete theme="outline" size="16" />
      </button>
      <button class="btn btn-primary" @click="handleSave">
        <Save theme="outline" size="16" />
        <span>保存</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { Undo, Redo, Delete, Save } from '@icon-park/vue-next'

const emit = defineEmits(['clear', 'save'])

const handleClear = () => {
  emit('clear')
}

const handleSave = () => {
  emit('save')
}
</script>

<style scoped>
@import '../styles/editor.css';
@import '../styles/controls.css';
</style> 