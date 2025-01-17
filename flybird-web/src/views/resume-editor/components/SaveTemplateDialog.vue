<template>
  <v-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    max-width="600"
    persistent
  >
    <v-card>
      <v-card-title class="text-h5">保存为模板</v-card-title>
      <v-card-text>
        <v-form ref="form" v-model="valid">
          <v-text-field
            v-model="formData.name"
            label="模板名称"
            :rules="[v => !!v || '请输入模板名称']"
            required
            validate-on="input"
          ></v-text-field>

          <v-select
            v-if="categories.length > 0"
            v-model="formData.category"
            :items="categories"
            item-title="name"
            item-value="id"
            label="选择分类"
            :rules="[v => !!v || '请选择分类']"
            required
            validate-on="input"
          ></v-select>

          <v-file-input
            v-model="formData.thumbnail"
            label="缩略图"
            accept="image/*"
            :rules="[
              v => !!v || '请上传缩略图',
              v => !v || !v.length || v[0].size < 2000000 || '图片大小不能超过2MB'
            ]"
            required
            validate-on="input"
            @change="handleFileChange"
            show-size
            prepend-icon="mdi-camera"
          ></v-file-input>

          <v-textarea
            v-model="formData.description"
            label="模板描述"
            :rules="[v => !!v || '请输入模板描述']"
            required
            validate-on="input"
          ></v-textarea>

          <v-switch
            v-model="formData.is_vip"
            label="VIP模板"
            color="primary"
          ></v-switch>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn 
          color="grey-darken-1" 
          variant="text" 
          @click="$emit('update:modelValue', false)"
        >
          取消
        </v-btn>
        <v-btn
          color="primary"
          variant="text"
          :loading="loading"
          :disabled="!valid"
          @click="handleSave"
        >
          保存
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useTemplateStore } from '@/stores/template'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'save'])

// 表单数据
const form = ref(null)
const valid = ref(false)
const loading = ref(false)
const formData = ref({
  name: '',
  category: null,
  thumbnail: null,
  description: '',
  is_vip: false
})

// 模板分类
const templateStore = useTemplateStore()
const categories = ref([])

// 获取分类数据
const fetchCategories = async () => {
  try {
    loading.value = true
    const response = await templateStore.getCategories()
    console.log('获取到的分类数据:', response)
    // 从response.data.results中获取分类列表
    if (response?.data?.results) {
      categories.value = response.data.results
      console.log('设置的分类数据:', categories.value)
    } else {
      console.error('获取分类失败: 无数据')
      categories.value = []
    }
  } catch (error) {
    console.error('获取分类出错:', error)
    categories.value = []
  } finally {
    loading.value = false
  }
}

// 监听对话框显示状态
watch(() => props.modelValue, async (val) => {
  if (val) {
    // 每次打开对话框时都重新获取分类
    await fetchCategories()
  }
  if (!val) {
    // 重置表单
    form.value?.reset()
    formData.value = {
      name: '',
      category: null,
      thumbnail: null,
      description: '',
      is_vip: false
    }
    valid.value = false
  }
})

// 处理文件变化
const handleFileChange = async (files) => {
  if (files && files.length > 0) {
    const file = files[0]
    if (file.size > 2000000) {
      formData.value.thumbnail = null
      return
    }
  }
  await validateForm()
}

// 手动验证表单
const validateForm = async () => {
  if (form.value) {
    const { valid: isValid } = await form.value.validate()
    valid.value = isValid
  }
}

// 监听表单数据变化
watch(formData, async () => {
  await validateForm()
}, { deep: true })

// 保存模板
const handleSave = async () => {
  await validateForm()
  if (!valid.value) return

  loading.value = true
  try {
    // 检查必填字段
    if (!formData.value.category) {
      throw new Error('请选择分类')
    }
    if (!formData.value.thumbnail) {
      throw new Error('请上传缩略图')
    }

    // 转换布尔值为字符串
    const data = {
      ...formData.value,
      is_vip: formData.value.is_vip.toString()
    }
    emit('save', data)
  } catch (error) {
    console.error('保存失败:', error)
    throw error
  } finally {
    loading.value = false
  }
}

// 初始化时获取分类数据
onMounted(() => {
  if (props.modelValue) {
    fetchCategories()
  }
})
</script> 