<!-- SaveTemplateDialog.vue -->
<template>
  <el-dialog
    v-model="dialogVisible"
    :title="dialogTitle"
    width="500px"
    :close-on-click-modal="false"
  >
    <el-form :model="form" label-width="80px">
      <template v-if="type === 'template'">
        <el-form-item label="模板名称" required>
          <el-input v-model:modelValue="form.name" placeholder="请输入模板名称" />
        </el-form-item>
        <el-form-item label="模板分类" required>
          <el-select v-model:modelValue="form.category" placeholder="请选择分类">
            <el-option
              v-for="item in categories"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="模板描述">
          <el-input
            v-model:modelValue="form.description"
            type="textarea"
            rows="3"
            placeholder="请输入模板描述"
          />
        </el-form-item>
        <el-form-item label="是否公开">
          <el-switch v-model:modelValue="form.is_public" />
        </el-form-item>
      </template>
      
      <template v-else>
        <el-form-item label="简历名称" required>
          <el-input v-model:modelValue="form.name" placeholder="请输入简历名称" />
        </el-form-item>
        <el-form-item label="简历描述">
          <el-input
            v-model:modelValue="form.description"
            type="textarea"
            rows="3"
            placeholder="请输入简历描述"
          />
        </el-form-item>
      </template>
    </el-form>
    
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleConfirm">{{ confirmButtonText }}</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { categoryApi } from '@/api/category'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  mode: {
    type: String,
    default: 'draft'
  },
  type: {
    type: String,
    default: 'template'
  },
  templateData: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:visible', 'save'])

const dialogVisible = ref(false)
const categories = ref([])
const form = ref({
  name: '',
  category: '',
  description: '',
  is_public: false
})

// 对话框标题
const dialogTitle = computed(() => {
  if (props.type === 'template') {
    return props.mode === 'draft' ? '保存模板草稿' : '提交模板审核'
  } else {
    return props.mode === 'draft' ? '保存简历草稿' : '发布简历'
  }
})

// 确认按钮文本
const confirmButtonText = computed(() => {
  if (props.type === 'template') {
    return props.mode === 'draft' ? '保存草稿' : '提交审核'
  } else {
    return props.mode === 'draft' ? '保存草稿' : '发布'
  }
})

// 加载分类列表
const loadCategories = async () => {
  try {
    const res = await categoryApi.getList()
    categories.value = Array.isArray(res) ? res : []
  } catch (error) {
    console.error('获取分类列表失败:', error)
  }
}

// 监听弹窗显示和模板数据变化
watch([() => props.visible, () => props.templateData], ([visible, templateData]) => {
  dialogVisible.value = visible
  if (visible) {
    // 打开弹窗时，加载当前模板数据
    if (props.type === 'template') {
      loadCategories()
      // 填充表单数据
      form.value = {
        name: templateData.name || '',
        category: templateData.category || '',
        description: templateData.description || '',
        is_public: templateData.is_public || false
      }
    }
  }
})

watch(() => dialogVisible.value, (val) => {
  emit('update:visible', val)
  if (!val) {
    // 关闭时重置表单
    form.value = {
      name: '',
      category: '',
      description: '',
      is_public: false
    }
  }
})

const handleCancel = () => {
  dialogVisible.value = false
}

const handleConfirm = () => {
  if (!form.value.name) {
    ElMessage.warning(`请输入${props.type === 'template' ? '模板' : '简历'}名称`)
    return
  }
  
  if (props.type === 'template' && !form.value.category) {
    ElMessage.warning('请选择模板分类')
    return
  }
  
  emit('save', form.value)
  dialogVisible.value = false
}
</script>

<style scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style> 