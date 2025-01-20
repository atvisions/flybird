<template>
  <div class="editor-toolbar">
    <div class="toolbar-group">
      <button 
        class="toolbar-button" 
        :disabled="!canUndo"
        @click="handleUndo"
      >
        <i class="iconfont icon-undo"></i>
        <span>撤销</span>
      </button>
      <button 
        class="toolbar-button" 
        :disabled="!canRedo"
        @click="handleRedo"
      >
        <i class="iconfont icon-redo"></i>
        <span>重做</span>
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

const props = defineProps({
  canUndo: {
    type: Boolean,
    default: false
  },
  canRedo: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['clear', 'save', 'undo', 'redo'])

const handleClear = () => {
  emit('clear')
}

const handleSave = () => {
  emit('save')
}

const handleUndo = () => {
  emit('undo')
}

const handleRedo = () => {
  emit('redo')
}
</script>

<style scoped>
@import '../styles/editor.css';
@import '../styles/controls.css';

.editor-toolbar {
  height: 48px;
  padding: 0 16px;
  background-color: #fff;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  gap: 16px;
}

.toolbar-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.toolbar-button {
  height: 32px;
  padding: 0 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  background: #fff;
  color: #333;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: all 0.3s;
}

.toolbar-button:hover:not(:disabled) {
  color: #1890ff;
  border-color: #1890ff;
}

.toolbar-button:disabled {
  cursor: not-allowed;
  color: #d9d9d9;
  background: #f5f5f5;
}

.iconfont {
  font-size: 14px;
}
</style> 