<template>
  <el-dialog
    :title="initialData?.id ? '编辑专业技能' : '添加专业技能'"
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
      <el-form-item label="技能名称" prop="name">
        <el-input v-model="formData.name" placeholder="请输入技能名称" />
      </el-form-item>

      <el-form-item label="技能描述" prop="description">
        <el-input
          v-model="formData.description"
          type="textarea"
          :rows="4"
          placeholder="请描述你的技能水平、经验等"
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
  initialData: {
    type: Object,
    default: () => ({
      name: '',  // 提供默认值
      level: '',
      description: ''
    })
  },
  loading: Boolean
})

const emit = defineEmits(['update:modelValue', 'submit'])

const dialogVisible = ref(false)
const formRef = ref(null)

// 表单数据
const formData = ref({
  name: '',
  level: '',
  description: ''
})

// 监听初始数据变化
watch(() => props.initialData, (val) => {
  if (val) {
    formData.value = {
      name: val.name || '',  // 确保有默认值
      level: val.level || '',
      description: val.description || ''
    }
  } else {
    formData.value = {
      name: '',
      level: '',
      description: ''
    }
  }
}, { immediate: true })

// ... 其他代码
</script> 