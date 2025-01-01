<template>
  <el-dialog
    :title="initialData?.id ? '编辑证书奖项' : '添加证书奖项'"
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
      <el-form-item label="证书名称" prop="name">
        <el-input v-model="formData.name" placeholder="请输入证书或奖项名称" />
      </el-form-item>

      <el-form-item label="获得时间" prop="date">
        <el-date-picker
          v-model="formData.date"
          type="month"
          placeholder="选择获得时间"
          format="YYYY.MM"
          value-format="YYYY-MM"
        />
      </el-form-item>

      <el-form-item label="证书描述" prop="description">
        <el-input
          v-model="formData.description"
          type="textarea"
          :rows="4"
          placeholder="请描述证书或奖项的相关信息"
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
  date: '',
  description: ''
})

const rules = {
  name: [{ required: true, message: '请输入证书名称', trigger: 'blur' }],
  date: [{ required: true, message: '请选择获得时间', trigger: 'change' }],
  description: [{ required: true, message: '请输入证书描述', trigger: 'blur' }]
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
      date: '',
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