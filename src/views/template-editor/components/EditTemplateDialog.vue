<template>
  <!-- No changes to template section -->
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  mode: {
    type: String,
    default: 'draft'
  }
})

const emit = defineEmits(['confirm'])

const formData = ref({
  name: '',
  category: '',
  description: '',
  is_public: false,
  keywords: []
})

const loading = ref(false)

const handleConfirm = async () => {
  // 表单验证
  if (!formData.value.name?.trim()) {
    ElMessage.warning('请输入模板名称')
    return
  }
  if (!formData.value.category) {
    ElMessage.warning('请选择分类')
    return
  }
  if (!formData.value.description?.trim()) {
    ElMessage.warning('请输入模板描述')
    return
  }
  if (formData.value.description.length < 10) {
    ElMessage.warning('描述至少需要10个字符')
    return
  }

  try {
    loading.value = true
    const submitData = {
      name: formData.value.name.trim(),
      category: formData.value.category,
      description: formData.value.description.trim(),
      is_public: formData.value.is_public,
      keywords: formData.value.keywords ? formData.value.keywords.split(',').filter(Boolean) : [],
      status: props.mode === 'draft' ? 0 : 2
    }
    console.log('提交的表单数据:', submitData)
    emit('confirm', submitData)
  } finally {
    loading.value = false
  }
}
</script> 