<template>
  <div class="color-picker-wrapper" @click.stop>
    <div class="color-preview" @click="togglePopup">
      <div class="color-preview-row">
        <div class="color-block" :style="{ backgroundColor: modelValue }"></div>
        <input
          type="text"
          :value="modelValue"
          @input="handleColorInput"
          placeholder="#000000"
        >
      </div>
    </div>
    
    <!-- 遮罩层 -->
    <div v-if="showPopup" class="color-picker-overlay" @click="closePopup"></div>
    
    <!-- 弹出面板 -->
    <div v-if="showPopup" class="color-popup">
      <div class="popup-header">
        <h3>选择颜色</h3>
        <button class="btn-close" @click="closePopup">×</button>
      </div>
      
      <div class="popup-content">
        <!-- 颜色选择器 -->
        <div class="color-selector">
          <div class="color-preview"></div>
          <input
            type="color"
            :value="modelValue"
            @input="handleColorInput"
          >
        </div>
        
        <!-- 最近使用的颜色 -->
        <div class="recent-colors">
          <div class="section-title">最近使用</div>
          <div class="color-grid">
            <div
              v-for="color in recentColors"
              :key="color"
              class="color-item"
              :style="{ backgroundColor: color }"
              @click="selectColor(color)"
            ></div>
          </div>
        </div>
        
        <!-- 保存的颜色 -->
        <div class="saved-colors">
          <div class="section-header">
            <div class="section-title">已保存</div>
            <button 
              class="btn-save"
              @click="saveCurrentColor"
              :disabled="savedColors.includes(modelValue)"
            >
              保存当前颜色
            </button>
          </div>
          <div class="color-grid">
            <div
              v-for="color in savedColors"
              :key="color"
              class="color-item"
              :style="{ backgroundColor: color }"
              @click="selectColor(color)"
            >
              <button 
                class="btn-delete"
                @click.stop="deleteColor(color)"
              >×</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: '#000000'
  }
})

const emit = defineEmits(['update:model-value'])

// 状态
const showPopup = ref(false)
const recentColors = ref([])
const savedColors = ref([])

// 从 localStorage 加载保存的颜色
onMounted(() => {
  const saved = localStorage.getItem('savedColors')
  if (saved) {
    savedColors.value = JSON.parse(saved)
  }
  
  const recent = localStorage.getItem('recentColors')
  if (recent) {
    recentColors.value = JSON.parse(recent)
  }
  
  // 添加点击事件监听
  document.addEventListener('click', handleClickOutside)
})

// 移除事件监听
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// 处理颜色输入
const handleColorInput = (e) => {
  const color = e.target.value
  emit('update:model-value', color)
  addRecentColor(color)
}

// 选择颜色
const selectColor = (color) => {
  emit('update:model-value', color)
  addRecentColor(color)
}

// 添加到最近使用
const addRecentColor = (color) => {
  if (!recentColors.value.includes(color)) {
    recentColors.value.unshift(color)
    if (recentColors.value.length > 8) {
      recentColors.value.pop()
    }
    localStorage.setItem('recentColors', JSON.stringify(recentColors.value))
  }
}

// 保存当前颜色
const saveCurrentColor = () => {
  if (!savedColors.value.includes(props.modelValue)) {
    savedColors.value.push(props.modelValue)
    localStorage.setItem('savedColors', JSON.stringify(savedColors.value))
  }
}

// 删除保存的颜色
const deleteColor = (color) => {
  const index = savedColors.value.indexOf(color)
  if (index > -1) {
    savedColors.value.splice(index, 1)
    localStorage.setItem('savedColors', JSON.stringify(savedColors.value))
  }
}

// 切换弹窗
const togglePopup = () => {
  showPopup.value = !showPopup.value
}

// 关闭弹窗
const closePopup = () => {
  showPopup.value = false
}

// 点击外部关闭
const handleClickOutside = (event) => {
  const wrapper = document.querySelector('.color-picker-wrapper')
  if (showPopup.value && wrapper && !wrapper.contains(event.target)) {
    closePopup()
  }
}
</script>

<style scoped>
.color-picker-wrapper {
  position: relative;
  width: 100%;
}

.color-preview {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
  cursor: pointer;
}

.color-preview-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.color-block {
  width: 32px;
  height: 32px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  background-color: #fff;
  transition: transform 0.2s;
}

.color-block:hover {
  transform: scale(1.05);
}

.color-preview input {
  flex: 1;
  min-width: 80px;
  height: 32px;
  padding: 0 8px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  font-size: 13px;
  color: #374151;
}

.color-picker-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.2);
  z-index: 999;
}

.color-popup {
  position: absolute;
  bottom: calc(100% + 4px);
  left: -14px;
  width: 280px;
  background: white;
  border-radius: 6px;
  box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
}

.popup-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  border-bottom: 1px solid #e5e7eb;
}

.popup-header h3 {
  margin: 0;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
}

.btn-close {
  width: 20px;
  height: 20px;
  border: none;
  background: none;
  font-size: 16px;
  color: #9ca3af;
  cursor: pointer;
  transition: color 0.2s;
}

.btn-close:hover {
  color: #374151;
}

.popup-content {
  padding: 12px;
}

.color-selector {
  margin-bottom: 12px;
  position: relative;
}

.color-selector input {
  width: 100%;
  height: 36px;
  padding: 0;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  cursor: pointer;
  opacity: 0;
  position: absolute;
  top: 0;
  left: 0;
}

.color-selector .color-preview {
  width: 100%;
  height: 36px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  background: v-bind('modelValue');
}

.section-title {
  font-size: 12px;
  font-weight: 500;
  color: #4b5563;
  margin-bottom: 6px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 6px;
}

.btn-save {
  padding: 3px 6px;
  border: 1px solid #e5e7eb;
  border-radius: 3px;
  background: white;
  font-size: 12px;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-save:hover {
  border-color: #1890ff;
  color: #1890ff;
  background: #f0f7ff;
}

.btn-save:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.color-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 6px;
  margin-bottom: 12px;
}

.color-item {
  position: relative;
  width: 100%;
  padding-bottom: 100%;
  border: 1px solid #e5e7eb;
  border-radius: 3px;
  cursor: pointer;
  transition: transform 0.2s;
}

.color-item:hover {
  transform: scale(1.05);
}

.color-item:hover .btn-delete {
  opacity: 1;
}

.btn-delete {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 14px;
  height: 14px;
  border: none;
  border-radius: 50%;
  background: #ef4444;
  color: white;
  font-size: 10px;
  line-height: 1;
  opacity: 0;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-delete:hover {
  background: #dc2626;
  transform: scale(1.1);
}

.recent-colors,
.saved-colors {
  margin-top: 12px;
}
</style> 