<template>
  <div class="dialog-overlay" v-if="modelValue" @click="handleClose">
    <div class="dialog-content" @click.stop>
      <div class="dialog-header">
        <h3 class="dialog-title">保存模板</h3>
        <button class="close-button" @click="handleClose">&times;</button>
      </div>
      
      <div class="dialog-body">
        <div class="form-group">
          <label>模板名称</label>
          <input v-model="formData.name" type="text" class="form-input" placeholder="请输入模板名称">
        </div>
        
        <div class="form-group">
          <label>分类</label>
          <select v-model="formData.category" class="form-input">
            <option value="">请选择分类</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </div>
        
        <div class="form-group">
          <label>描述</label>
          <textarea v-model="formData.description" class="form-input" rows="3" placeholder="请输入模板描述"></textarea>
        </div>
        
        <div class="form-group">
          <label class="checkbox-label">
            <input type="checkbox" v-model="formData.is_public">
            <span>公开模板</span>
          </label>
        </div>
      </div>
      
      <div class="dialog-footer">
        <button class="btn btn-cancel" @click="handleClose">取消</button>
        <button class="btn btn-confirm" @click="handleConfirm">保存</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, watch } from 'vue'
import { categoryApi } from '@/api/category'

const props = defineProps({
  modelValue: Boolean,
  template: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue', 'confirm'])

const categories = ref([])
const formData = ref({
  name: '',
  category: '',
  description: '',
  is_public: false
})

// 加载分类数据
const loadCategories = async () => {
  try {
    const res = await categoryApi.getList()
    categories.value = Array.isArray(res) ? res : []
  } catch (error) {
    console.error('获取分类列表失败:', error)
  }
}

// 监听模板数据变化
watch(() => props.template, (newVal) => {
  if (newVal) {
    formData.value = {
      name: newVal.name || '',
      category: newVal.category || '',
      description: newVal.description || '',
      is_public: newVal.is_public || false
    }
  } else {
    // 如果没有模板数据，重置表单
    formData.value = {
      name: '',
      category: '',
      description: '',
      is_public: false
    }
  }
}, { immediate: true, deep: true })

// 处理关闭
const handleClose = () => {
  emit('update:modelValue', false)
}

// 处理确认
const handleConfirm = () => {
  emit('confirm', {
    ...props.template,
    ...formData.value
  })
  handleClose()
}

// 组件挂载时加载分类
loadCategories()
</script>

<style scoped>
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialog-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
}

.dialog-header {
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dialog-title {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.close-button {
  border: none;
  background: none;
  font-size: 20px;
  color: #999;
  cursor: pointer;
}

.dialog-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #333;
}

.form-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 14px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.dialog-footer {
  padding: 16px 20px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.btn {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  font-size: 14px;
  cursor: pointer;
}

.btn-cancel {
  background: #f5f5f5;
  color: #666;
}

.btn-confirm {
  background: #1890ff;
  color: white;
}
</style> 