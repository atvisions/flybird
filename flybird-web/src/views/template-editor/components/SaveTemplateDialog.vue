<!-- SaveTemplateDialog.vue -->
<template>
  <el-dialog
    :title="isEdit ? '保存模板' : '创建模板'"
    v-model="dialogVisible"
    width="500px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-width="80px"
      class="save-form"
    >
      <el-form-item label="名称" prop="name">
        <el-input v-model="formData.name" placeholder="请输入模板名称" />
      </el-form-item>

      <el-form-item label="分类" prop="category">
        <el-select v-model="formData.category" placeholder="请选择分类" class="w-full">
          <el-option
            v-for="item in categories"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="描述" prop="description">
        <el-input
          v-model="formData.description"
          type="textarea"
          :rows="3"
          placeholder="请输入模板描述"
        />
      </el-form-item>

      <el-form-item label="关键词" prop="keywords">
        <el-input
          v-model="formData.keywords"
          placeholder="请输入关键词，多个关键词用逗号分隔"
        />
      </el-form-item>

      <el-form-item label="公开" prop="is_public">
        <el-switch v-model="formData.is_public" />
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="loading">
          {{ isEdit ? '保存' : '创建' }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { categoryApi } from '../api'
import { showToast } from '@/components/ToastMessage'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  defaultData: {
    type: Object,
    default: () => ({
      name: '',
      description: '',
      category: '',
      keywords: '',
      is_public: true
    })
  },
  isEdit: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:visible', 'save'])

// 表单引用
const formRef = ref(null)
const loading = ref(false)
const categories = ref([])

// 对话框可见性
const dialogVisible = ref(props.visible)

// 监听 visible 属性变化
watch(() => props.visible, (newVal) => {
  dialogVisible.value = newVal
})

// 监听对话框可见性变化
watch(dialogVisible, (newVal) => {
  emit('update:visible', newVal)
})

// 表单数据
const formData = ref({
  name: '',
  description: '',
  category: '',
  keywords: '',
  is_public: true
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入模板名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择分类', trigger: 'change' }
  ]
}

// 获取分类列表
const loadCategories = async () => {
  try {
    const res = await categoryApi.getList()
    categories.value = Array.isArray(res) ? res : []
  } catch (error) {
    console.error('获取分类列表失败:', error)
    showToast('获取分类列表失败', 'error')
  }
}

// 处理关闭
const handleClose = () => {
  dialogVisible.value = false
  formRef.value?.resetFields()
}

// 处理提交
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true
    
    // 处理关键词
    const keywords = formData.value.keywords
      .split(',')
      .map(k => k.trim())
      .filter(k => k)
    
    // 提交数据
    emit('save', {
      ...formData.value,
      keywords
    })
    
    // 重置表单
    formRef.value.resetFields()
  } catch (error) {
    console.error('表单验证失败:', error)
  } finally {
    loading.value = false
  }
}

// 监听默认数据变化
watch(() => props.defaultData, (newData) => {
  if (newData) {
    formData.value = { ...newData }
  }
}, { immediate: true })

// 组件挂载时加载分类列表
onMounted(() => {
  loadCategories()
})
</script>

<style scoped>
.save-form {
  padding: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px;
}

.w-full {
  width: 100%;
}
</style> 