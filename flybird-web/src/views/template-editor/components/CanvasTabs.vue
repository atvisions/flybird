<template>
  <div class="canvas-tabs">
    <div class="tab-list">
      <div
        v-for="canvas in canvasList"
        :key="canvas.id"
        class="tab-item"
        :class="{ active: currentCanvasId === canvas.id }"
        @click="handleTabClick(canvas.id)"
      >
        <span class="tab-name">{{ canvas.name }}</span>
        <button 
          v-if="canvasList.length > 1"
          class="tab-close"
          @click.stop="handleRemoveCanvas(canvas.id)"
        >
          <Close theme="outline" size="12" />
        </button>
      </div>
    </div>
    <button 
      class="btn btn-add"
      @click="handleAddCanvas"
      :disabled="canvasList.length >= 5"
    >
      <Plus theme="outline" size="16" />
    </button>
  </div>
</template>

<script setup>
import { Close, Plus } from '@icon-park/vue-next'

const props = defineProps({
  canvasList: {
    type: Array,
    required: true
  },
  currentCanvasId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['switch', 'add', 'remove'])

const handleTabClick = (id) => {
  emit('switch', id)
}

const handleAddCanvas = () => {
  emit('add')
}

const handleRemoveCanvas = (id) => {
  if (confirm('确定要删除该画布吗？此操作不可恢复')) {
    emit('remove', id)
  }
}
</script>

<style scoped>
.canvas-tabs {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-bottom: 1px solid #f0f0f0;
  background-color: #fff;
}

.tab-list {
  display: flex;
  gap: 4px;
  flex: 1;
  overflow-x: auto;
  padding-bottom: 4px;
}

.tab-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 4px;
  background-color: #f5f5f5;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
}

.tab-item:hover {
  background-color: #e8e8e8;
}

.tab-item.active {
  background-color: #e6f4ff;
  color: #1890ff;
}

.tab-name {
  font-size: 14px;
}

.tab-close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  padding: 0;
  border: none;
  background: none;
  border-radius: 50%;
  cursor: pointer;
  opacity: 0.5;
  transition: all 0.2s;
}

.tab-close:hover {
  opacity: 1;
  background-color: rgba(0, 0, 0, 0.05);
}

.btn-add {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-add:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style> 