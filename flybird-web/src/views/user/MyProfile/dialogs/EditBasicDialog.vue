<!-- src/views/user/MyProfile/dialogs/EditBasicDialog.vue -->
<template>
  <TransitionRoot appear :show="!!modelValue" as="template">
    <Dialog as="div" class="relative z-50" @close="handleClose">
      <!-- 背景遮罩 -->
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black/25" />
      </TransitionChild>

      <!-- 对话框 -->
      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4 text-center">
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel class="w-full max-w-2xl transform overflow-hidden rounded-xl bg-white text-left align-middle shadow-xl transition-all">
              <!-- 头部 -->
              <DialogTitle as="div" class="flex items-center justify-between px-6 py-4 border-b border-gray-200">
                <h3 class="text-lg font-medium text-gray-900">编辑基本信息</h3>
                <button
                  @click="handleClose"
                  class="rounded-full p-1 hover:bg-gray-100 transition-colors"
                >
                  <XMarkIcon class="w-5 h-5 text-gray-400" />
                </button>
              </DialogTitle>

              <!-- 表单内容 -->
              <div class="px-6 py-4">
                <form @submit.prevent="handleSubmit" class="space-y-4">
                  <!-- 第一行：姓名和性别 -->
                  <div class="grid grid-cols-2 gap-4">
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        姓名<span class="text-red-500">*</span>
                      </label>
                      <input
                        v-model="formData.name"
                        type="text"
                        class="w-full px-3 py-2 border rounded-lg"
                        :class="[
                          formErrors.name 
                            ? 'border-red-300 focus:ring-red-500 focus:border-red-500' 
                            : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500'
                        ]"
                        placeholder="请输入姓名"
                      />
                      <p v-if="formErrors.name" class="mt-1 text-sm text-red-500">
                        {{ formErrors.name }}
                      </p>
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">性别</label>
                      <div class="flex gap-2 w-full">
                        <button
                          v-for="option in genderOptions"
                          :key="option.value"
                          type="button"
                          class="flex items-center justify-center flex-1 px-2 py-2 text-sm font-medium rounded-lg border transition-colors min-w-[60px]"
                          :class="[
                            formData.gender === option.value
                              ? option.value === 'female'
                                ? 'bg-pink-50 text-pink-700 border-pink-200 hover:bg-pink-100'
                                : 'bg-blue-50 text-blue-700 border-blue-200 hover:bg-blue-100'
                              : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                          ]"
                          @click="formData.gender = option.value"
                        >
                          <!-- 男性图标 -->
                          <svg 
                            v-if="option.value === 'male'" 
                            class="w-4 h-4 mr-1" 
                            viewBox="0 0 24 24" 
                            fill="none" 
                            :stroke="formData.gender === 'male' ? 'currentColor' : '#6B7280'"
                          >
                            <circle cx="12" cy="12" r="5" stroke-width="2"/>
                            <path d="M16 8L21 3" stroke-width="2" stroke-linecap="round"/>
                            <path d="M21 3H16M21 3V8" stroke-width="2" stroke-linecap="round"/>
                          </svg>
                          <!-- 女性图标 -->
                          <svg 
                            v-else 
                            class="w-4 h-4 mr-1" 
                            viewBox="0 0 24 24" 
                            fill="none" 
                            :stroke="formData.gender === 'female' ? 'currentColor' : '#6B7280'"
                          >
                            <circle cx="12" cy="10" r="5" stroke-width="2"/>
                            <path d="M12 15V21" stroke-width="2" stroke-linecap="round"/>
                            <path d="M9 18H15" stroke-width="2" stroke-linecap="round"/>
                          </svg>
                          {{ option.label }}
                        </button>
                      </div>
                    </div>
                  </div>

                  <!-- 第二行：出生日期和手机号码 -->
                  <div class="grid grid-cols-2 gap-4">
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">出生日期</label>
                      <input
                        v-model="formData.birth_date"
                        type="date"
                        :max="maxDate"
                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">手机号码</label>
                      <input
                        v-model="formData.phone"
                        type="tel"
                        class="w-full px-3 py-2 border rounded-lg"
                        :class="[
                          formErrors.phone 
                            ? 'border-red-300 focus:ring-red-500 focus:border-red-500' 
                            : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500'
                        ]"
                        placeholder="请输入手机号码"
                      />
                      <p v-if="formErrors.phone" class="mt-1 text-sm text-red-500">
                        {{ formErrors.phone }}
                      </p>
                    </div>
                  </div>

                  <!-- 第三行：邮箱和所在城市 -->
                  <div class="grid grid-cols-2 gap-4">
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">邮箱</label>
                      <input
                        v-model="formData.email"
                        type="email"
                        class="w-full px-3 py-2 border rounded-lg"
                        :class="[
                          formErrors.email 
                            ? 'border-red-300 focus:ring-red-500 focus:border-red-500' 
                            : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500'
                        ]"
                        placeholder="请输入邮箱"
                      />
                      <p v-if="formErrors.email" class="mt-1 text-sm text-red-500">
                        {{ formErrors.email }}
                      </p>
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">所在城市</label>
                      <input
                        v-model="formData.location"
                        type="text"
                        class="w-full px-3 py-2 border rounded-lg"
                        :class="[
                          formErrors.location 
                            ? 'border-red-300 focus:ring-red-500 focus:border-red-500' 
                            : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500'
                        ]"
                        placeholder="请输入所在城市"
                      />
                      <p v-if="formErrors.location" class="mt-1 text-sm text-red-500">
                        {{ formErrors.location }}
                      </p>
                    </div>
                  </div>

                  <!-- 第四行：个人简介（独占一行） -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">个人简介</label>
                    <textarea
                      v-model="formData.personal_summary"
                      rows="4"
                      class="w-full px-3 py-2 border rounded-lg"
                      :class="[
                        formErrors.personal_summary 
                          ? 'border-red-300 focus:ring-red-500 focus:border-red-500' 
                          : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500'
                      ]"
                      placeholder="请输入个人简介（20-100字）"
                    ></textarea>
                    <p v-if="formErrors.personal_summary" class="mt-1 text-sm text-red-500">
                      {{ formErrors.personal_summary }}
                    </p>
                  </div>
                </form>
              </div>

              <!-- 底部按钮 -->
              <div class="px-6 py-4 bg-gray-50 border-t border-gray-200">
                <div class="flex justify-end space-x-3">
                  <button
                    type="button"
                    @click="handleClose"
                    class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
                  >
                    取消
                  </button>
                  <button
                    type="submit"
                    @click="handleSubmit"
                    :disabled="loading"
                    class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {{ loading ? '保存中...' : '保存' }}
                  </button>
                </div>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { ref, watch, reactive, computed } from 'vue'
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionChild,
  TransitionRoot
} from '@headlessui/vue'
import { XMarkIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  modelValue: Boolean,
  initialData: {
    type: Object,
    default: () => ({})
  },
  loading: Boolean
})

const emit = defineEmits(['update:modelValue', 'submit'])

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入姓名' },
    { 
      validator: (value) => {
        if (!value) return true
        if (value.length < 2 || value.length > 20) {
          return '姓名长度需要在2-20个字符之间'
        }
        const nameRegex = /^[\u4e00-\u9fa5a-zA-Z\s]+$/
        if (!nameRegex.test(value)) {
          return '姓名只能包含中文或英文字符'
        }
        return true
      }
    }
  ],
  phone: [
    { 
      validator: (value) => {
        if (!value) return true // 选填
        // 中国大陆手机号格式验证
        const phoneRegex = /^1[3-9]\d{9}$/
        if (!phoneRegex.test(value)) {
          return '请输入正确的手机号码格式'
        }
        return true
      }
    }
  ],
  personal_summary: [
    {
      validator: (value) => {
        if (!value) return true // 选填
        const length = value.trim().length
        if (length < 20 || length > 100) {
          return '个人简介需要在20-100个字符之间'
        }
        return true
      }
    }
  ],
  location: [
    {
      validator: (value) => {
        if (!value) return true // 选填
        // 城市名称验证：2-20个字符，只允许中文、英文和空格
        if (value.length < 2 || value.length > 20) {
          return '城市名称长度需要在2-20个字符之间'
        }
        const cityRegex = /^[\u4e00-\u9fa5a-zA-Z\s]+$/
        if (!cityRegex.test(value)) {
          return '城市名称只能包含中文或英文字符'
        }
        return true
      }
    }
  ],
  email: [
    {
      validator: (value) => {
        if (!value) return true // 选填
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        if (!emailRegex.test(value)) {
          return '请输入正确的邮箱格式'
        }
        return true
      }
    }
  ]
}

// 表单错误信息
const formErrors = ref({})

const formData = ref({
  name: '',
  gender: '',
  birth_date: '',
  phone: '',
  email: '',
  location: '',
  personal_summary: ''
})

// 监听初始数据变化
watch(() => props.initialData, (newData) => {
  if (newData) {
    formData.value = { ...newData }
  }
}, { immediate: true })

const handleClose = () => {
  emit('update:modelValue', false)
}

// 验证表单
const validateForm = () => {
  formErrors.value = {}
  let isValid = true

  Object.entries(rules).forEach(([field, fieldRules]) => {
    const value = formData.value[field]
    
    for (const rule of fieldRules) {
      if (rule.required && !value) {
        formErrors.value[field] = rule.message
        isValid = false
        break
      }
      
      if (rule.validator) {
        const validationResult = rule.validator(value, formData.value)
        if (typeof validationResult === 'string') {
          formErrors.value[field] = validationResult
          isValid = false
          break
        }
      }
    }
  })

  return isValid
}

const handleSubmit = async () => {
  try {
    if (!validateForm()) {
      return
    }
    
    // 构建提交数据
    const submitData = {
      name: formData.value.name,
      gender: formData.value.gender,
      birth_date: formData.value.birth_date,
      phone: formData.value.phone,
      email: formData.value.email,
      location: formData.value.location,
      personal_summary: formData.value.personal_summary
    }
    
    // 如果有 ID，添加到提交数据中
    if (props.initialData?.id) {
      submitData.id = props.initialData.id
    }
    
    emit('submit', submitData)
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}

// 性别选项
const genderOptions = [
  { value: 'male', label: '男' },
  { value: 'female', label: '女' }
]

// 添加实时验证函数
const validateEmail = () => {
  const emailRules = rules.email
  const value = formData.value.email
  
  formErrors.value.email = undefined // 清除之前的错误
  
  for (const rule of emailRules) {
    if (rule.validator) {
      const validationResult = rule.validator(value)
      if (typeof validationResult === 'string') {
        formErrors.value.email = validationResult
        break
      }
    }
  }
}

// 监听邮箱值的变化
watch(() => formData.value.email, () => {
  validateEmail()
})

// 添加最大日期计算
const maxDate = computed(() => {
  const today = new Date()
  return today.toISOString().split('T')[0]  // 格式化为 YYYY-MM-DD
})
</script>

<style scoped>
:deep(.el-select) {
  width: 100%;
}

:deep(.el-input__wrapper) {
  background-color: white;
  border-radius: 0.5rem;
}

:deep(.el-select .el-input__wrapper) {
  box-shadow: 0 0 0 1px #d1d5db;
  padding: 0.5rem 0.75rem;
}

:deep(.el-select .el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #3b82f6;
}

:deep(.el-select .el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 2px #3b82f680, 0 0 0 1px #3b82f6 !important;
}
</style>