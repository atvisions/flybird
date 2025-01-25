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
  if (!formData.value) return
  
  await formData.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const submitData = {
          name: formData.value.name.trim(),
          category: Number(formData.value.category),
          description: formData.value.description.trim(),
          is_public: formData.value.is_public,
          keywords: formData.value.keywords ? formData.value.keywords.split(',').filter(Boolean) : [],
          status: props.mode === 'draft' ? 0 : 2
        }
        
        if (props.template) {
          await templateApi.update(props.template.id, submitData)
        } else {
          await templateApi.create(submitData)
        }
        
        ElMessage.success('保存成功')
        dialogVisible.value = false
        emit('success')
      } catch (error) {
        ElMessage.error('保存失败')
      } finally {
        loading.value = false
      }
    }
  })
}

const handleDialogClose = () => {
  formData.value?.resetFields()
  dialogVisible.value = false
}
</script> 