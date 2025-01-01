<template>
  <el-dialog
    :title="initialData?.id ? '编辑语言能力' : '添加语言能力'"
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
      <el-form-item label="语言名称" prop="name">
        <el-input v-model="formData.name" placeholder="请输入语言名称" />
      </el-form-item>

      <el-form-item label="掌握程度" prop="level">
        <el-select v-model="formData.level" placeholder="请选择掌握程度">
          <el-option
            v-for="item in levelOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="补充说明" prop="description">
        <el-input
          v-model="formData.description"
          type="textarea"
          :rows="4"
          placeholder="可补充语言证书、使用经验等信息"
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

const levelOptions = [
  { value: 'native', label: '母语' },
  { value: 'fluent', label: '流利' },
  { value: 'professional', label: '商务熟练' },
  { value: 'intermediate', label: '中等' },
  { value: 'basic', label: '基础' }
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
  name: '',
  level: '',
  description: ''
})

const rules = {
  name: [{ required: true, message: '请输入语言名称', trigger: 'blur' }],
  level: [{ required: true, message: '请选择掌握程度', trigger: 'change' }],
  description: [{ required: true, message: '请输入补充说明', trigger: 'blur' }]
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
      level: '',
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