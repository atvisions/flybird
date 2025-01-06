<!-- src/views/user/MyProfile/dialogs/EditDialog.vue -->
<template>
    <el-dialog
      v-model="visible"
      :title="dialogTitle"
      width="640px"
      :close-on-click-modal="false"
      @close="handleClose"
    >
        <el-form
            ref="formRef"
            :model="formData"
            :rules="currentRules"
            label-width="100px"
            class="py-4"
        >
        <!-- 根据模块类型选择不同的字段配置 -->
        <template v-if="currentModule?.type === 'job_intention'">
          <template v-for="field in currentModule.formConfig.fields" :key="field.name">
            <!-- 输入框 -->
            <el-form-item
              v-if="field.type === 'input'"
              :label="field.label"
              :prop="field.name"
            >
              <el-input
                v-model="formData[field.name]"
                :placeholder="field.placeholder"
              />
            </el-form-item>

            <!-- 级联选择器 -->
            <el-form-item
              v-else-if="field.type === 'cascader'"
              :label="field.label"
              :prop="field.name"
            >
              <el-cascader
                v-model="formData[field.name]"
                :options="field.options"
                :placeholder="field.placeholder"
                class="w-full"
              />
            </el-form-item>

            <!-- 薪资范围 -->
            <el-form-item
              v-else-if="field.type === 'salary-range'"
              :label="field.label"
            >
              <div class="flex items-center space-x-2">
                <el-input-number
                  v-model="formData[field.name]"
                  :min="0"
                  :max="formData[field.name2] || 999"
                  :placeholder="field.placeholder[0]"
                />
                <span class="text-gray-500">K -</span>
                <el-input-number
                  v-model="formData[field.name2]"
                  :min="formData[field.name] || 0"
                  :placeholder="field.placeholder[1]"
                />
                <span class="text-gray-500">K</span>
              </div>
            </el-form-item>

            <!-- 下拉选择 -->
            <el-form-item
              v-else-if="field.type === 'select'"
              :label="field.label"
              :prop="field.name"
            >
              <el-select
                v-model="formData[field.name]"
                :placeholder="field.placeholder"
                class="w-full"
              >
                <el-option
                  v-for="option in field.options"
                  :key="option.value"
                  :label="option.label"
                  :value="option.value"
                />
              </el-select>
            </el-form-item>
          </template>
        </template>

        <!-- 其他模块的字段 -->
        <template v-else>
          <template v-for="field in currentModule?.formConfig?.fields" :key="field.name">
            <!-- 文本输入框 -->
            <el-form-item
              v-if="field.type === 'text'"
              :label="field.label"
              :prop="field.name"
            >
              <el-input
                v-model="formData[field.name]"
                :placeholder="`请输入${field.label}`"
              />
            </el-form-item>
    
            <!-- 文本域 -->
            <el-form-item
              v-else-if="field.type === 'textarea'"
              :label="field.label"
              :prop="field.name"
            >
              <el-input
                v-model="formData[field.name]"
                type="textarea"
                :rows="4"
                :placeholder="`请输入${field.label}`"
              />
            </el-form-item>
    
            <!-- 日期选择 -->
            <el-form-item
              v-else-if="field.type === 'date'"
              :label="field.label"
              :prop="field.name"
            >
              <el-date-picker
                v-model="formData[field.name]"
                type="date"
                :placeholder="`请选择${field.label}`"
                class="w-full"
              />
            </el-form-item>
    
            <!-- 日期范围 -->
            <el-form-item
              v-else-if="field.type === 'daterange'"
              :label="field.label"
              :prop="field.name"
            >
              <el-date-picker
                v-model="formData[field.name]"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                class="w-full"
              />
            </el-form-item>
    
            <!-- 标签输入 -->
            <el-form-item
              v-else-if="field.type === 'tags'"
              :label="field.label"
              :prop="field.name"
            >
              <el-select
                v-model="formData[field.name]"
                multiple
                filterable
                allow-create
                default-first-option
                :placeholder="`请输入${field.label}`"
                class="w-full"
              />
            </el-form-item>
    
            <!-- 级联选择器 -->
            <el-form-item
              v-else-if="field.type === 'cascader'"
              :label="field.label"
              :prop="field.name"
            >
              <el-cascader
                v-model="formData[field.name]"
                :options="field.options"
                :placeholder="field.placeholder"
                class="w-full"
              />
            </el-form-item>
    
            <!-- 薪资范围 -->
            <el-form-item
              v-else-if="field.type === 'salary-range'"
              :label="field.label"
            >
              <div class="flex items-center space-x-2">
                <el-input-number
                  v-model="formData[field.name]"
                  :min="0"
                  :max="formData[field.name2] || 999"
                  :placeholder="field.placeholder[0]"
                />
                <span class="text-gray-500">K -</span>
                <el-input-number
                  v-model="formData[field.name2]"
                  :min="formData[field.name] || 0"
                  :placeholder="field.placeholder[1]"
                />
                <span class="text-gray-500">K</span>
              </div>
            </el-form-item>
          </template>
        </template>
      </el-form>
  
      <template #footer>
        <div class="flex justify-end space-x-3">
          <el-button @click="handleClose">取消</el-button>
          <el-button 
            type="primary" 
            :loading="loading"
            @click="handleSubmit"
          >
            保存
          </el-button>
        </div>
      </template>
    </el-dialog>
  </template>
  
  <script setup>
  import { ref, computed, watch } from 'vue'
  import { ElMessage } from 'element-plus'
  import { options } from '../constants/options'
  import { validationRules } from '../constants/rules'
  
  const props = defineProps({
    modelValue: Boolean,
    module: {
      type: Object,
      required: true
    },
    initialFormData: {
      type: Object,
      default: () => ({})
    },
    loading: Boolean
  })
  // 创建本地表单数据副本
const localFormData = ref({...props.formData})

// 监听 formData 变化
watch(() => props.formData, (newVal) => {
  localFormData.value = {...newVal}
}, { deep: true })
  const emit = defineEmits(['update:modelValue', 'submit', 'cancel'])
  // 创建本地表单数据
const formData = ref({...props.initialFormData})

// 监听初始数据变化
watch(() => props.initialFormData, (newVal) => {
  formData.value = {...newVal}
}, { deep: true })
  const formRef = ref(null)
  const visible = computed({
    get: () => props.modelValue,
    set: (val) => emit('update:modelValue', val)
  })
  
  const currentModule = computed(() => {
    return props.module
  })
  const dialogTitle = computed(() => {
    if (!props.module) return ''
    return `编辑${props.module.name}`
  })
  
  const currentRules = computed(() => {
    if (!props.module) return {}
    
    // 获取模块对应的验证规则
    const moduleRules = validationRules[props.module.type]
    if (!moduleRules) return {}

    // 如果是求职意向模块，直接返回规则
    if (props.module.type === 'job_intention') {
      return moduleRules
    }

    // 其他模块的处理逻辑...
    return moduleRules
  })
  
  const getOptions = (fieldKey) => {
    return options[fieldKey] || []
  }
  
  const handleSubmit = async () => {
    if (!formRef.value) return
    
    try {
      await formRef.value.validate()
      // 如果是求职意向模块，进行数据格式化
      if (props.module.type === 'job_intention') {
        const formattedData = {
          job_type: formData.value.job_type || '',
          job_status: formData.value.job_status || 'open',
          expected_salary: formData.value.expected_salary || '',
          expected_city: formData.value.expected_city || '',
          industries: formData.value.industries || ''
        }
        emit('submit', formattedData)
      } else {
        emit('submit', formData.value)
      }
    } catch (error) {
      console.error('表单验证失败:', error)
      ElMessage.error('请完善必填信息')
    }
  }
  
  const handleClose = () => {
    emit('cancel')
  }
  
  // 监听弹窗关闭，重置表单
  watch(visible, (val) => {
    if (!val && formRef.value) {
      formRef.value.resetFields()
    }
  })
  </script>