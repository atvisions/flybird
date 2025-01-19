<template>
  <div class="canvas-navigator">
    <div class="thumbnail-list">
      <div
        v-for="canvas in canvasList"
        :key="canvas.id"
        class="thumbnail-item"
        :class="{ active: currentCanvasId === canvas.id }"
        @click="$emit('switch', canvas.id)"
      >
        <!-- 缩略图预览 -->
        <div class="thumbnail-preview">
          <div class="thumbnail-page"></div>
        </div>
        <span class="thumbnail-label">{{ canvas.name }}</span>
      </div>

      <!-- 添加按钮 -->
      <button 
        v-if="canvasList.length < 5"
        class="add-button"
        @click="$emit('add')"
      >
        <Plus theme="outline" size="24" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { Plus } from '@icon-park/vue-next'

defineProps({
  canvasList: {
    type: Array,
    required: true
  },
  currentCanvasId: {
    type: Number,
    required: true
  }
})

defineEmits(['switch', 'add'])
</script>

<style scoped>
.canvas-navigator {
  padding: 16px 0;
  border-top: 1px solid #f0f0f0;
}

.thumbnail-list {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 0 24px;
  overflow-x: auto;
}

.thumbnail-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.thumbnail-preview {
  width: 60px;
  height: 85px;
  padding: 4px;
  border: 1px solid #e8e8e8;
  border-radius: 4px;
  transition: all 0.2s;
}

.thumbnail-page {
  width: 100%;
  height: 100%;
  background-color: #fff;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.thumbnail-item.active .thumbnail-preview {
  border-color: #1890ff;
  background-color: #e6f7ff;
}

.thumbnail-label {
  font-size: 12px;
  color: #666;
}

.thumbnail-item.active .thumbnail-label {
  color: #1890ff;
}

.add-button {
  width: 60px;
  height: 85px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px dashed #d9d9d9;
  border-radius: 4px;
  background: none;
  color: #999;
  cursor: pointer;
  transition: all 0.2s;
}

.add-button:hover {
  color: #1890ff;
  border-color: #1890ff;
  background-color: #e6f7ff;
}
</style> 