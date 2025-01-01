<template>
  <el-dialog
    :title="initialData?.id ? '编辑社交主页' : '添加社交主页'"
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
      <el-form-item label="平台名称" prop="platform">
        <el-select v-model="formData.platform" placeholder="请选择平台">
          <el-option
            v-for="item in platformOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="用户名" prop="username">
        <el-input v-model="formData.username" placeholder="请输入用户名" />
      </el-form-item>

      <el-form-item label="主页链接" prop="url">
        <el-input v-model="formData.url" placeholder="请输入主页链接" />
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

const platformOptions = [
  { value: 'github', label: 'GitHub' },
  { value: 'linkedin', label: 'LinkedIn' },
  { value: 'twitter', label: 'Twitter' },
  { value: 'website', label: '个人网站' },
  { value: 'other', label: '其他' }
]

const props = defineProps({
  modelValue: Boolean,
  initialData: Object,
  loading: Boolean
})

const emit = defineEmits(['update:modelValue', 'submit'])

const dialogVisible = ref(false)
const formRef = ref(null)

const formData = ref({
  platform: '',
  username: '',
  url: ''
})

const rules = {
  platform: [{ required: true, message: '请选择平台', trigger: 'change' }],
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  url: [{ required: true, message: '请输入主页链接', trigger: 'blur' }]
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
      platform: '',
      username: '',
      url: ''
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