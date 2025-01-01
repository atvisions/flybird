<template>
  <el-dialog
    :title="initialData?.id ? '编辑作品展示' : '添加作品展示'"
    v-model="dialogVisible"
    width="640px"
    :close-on-click-modal="false"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-width="100px"
      class="space-y-4"
    >
      <el-form-item label="作品名称" prop="name">
        <el-input v-model="formData.name" placeholder="请输入作品名称" />
      </el-form-item>

      <el-form-item label="作品链接" prop="link">
        <el-input v-model="formData.link" placeholder="请输入作品链接" />
      </el-form-item>

      <el-form-item label="作品描述" prop="description">
        <el-input
          v-model="formData.description"
          type="textarea"
          :rows="4"
          placeholder="请描述作品的主要内容、特点等"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="flex justify-end space-x-3">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="loading">
          确认
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  modelValue: Boolean,
  initialData: Object,
  loading: Boolean
})

const emit = defineEmits(['update:modelValue', 'submit'])

const dialogVisible = ref(false)
const formRef = ref(null)

const formData = ref({
  name: '',
  link: '',
  description: ''
})

const rules = {
  name: [{ required: true, message: '请输入作品名称', trigger: 'blur' }],
  link: [{ required: true, message: '请输入作品链接', trigger: 'blur' }],
  description: [{ required: true, message: '请输入作品描述', trigger: 'blur' }]
}

watch(() => props.modelValue, (val) => {
  dialogVisible.value = val
})

watch(dialogVisible, (val) => {
  emit('update:modelValue', val)
  if (!val) {
    formRef.value?.resetFields()
  }
})

watch(() => props.initialData, (val) => {
  if (val) {
    formData.value = { ...val }
  } else {
    formData.value = {
      name: '',
      link: '',
      description: ''
    }
  }
}, { immediate: true })

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    const submitData = {
      ...formData.value
    }
    
    if (props.initialData?.id) {
      submitData.id = props.initialData.id
    }
    
    emit('submit', submitData)
  } catch (error) {
    console.error('表单验证失败:', error)
    ElMessage.error('请检查表单填写是否正确')
  }
}
</script> 