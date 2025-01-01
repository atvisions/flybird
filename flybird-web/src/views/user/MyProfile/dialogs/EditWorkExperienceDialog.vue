<template>
  <TransitionRoot appear :show="modelValue" as="div">
    <Dialog as="div" class="relative z-50" @close="handleClose">
      <!-- 背景遮罩 -->
      <TransitionChild
        as="div"
        :show="true"
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
            <DialogPanel 
              class="w-full max-w-2xl transform overflow-hidden rounded-xl bg-white text-left align-middle shadow-xl transition-all"
            >
              <!-- 头部 -->
              <DialogTitle 
                as="div" 
                class="flex items-center justify-between border-b border-gray-200 px-6 py-4"
              >
                <h3 class="text-lg font-medium text-gray-900">
                  {{ initialData.id ? '编辑工作经历' : '添加工作经历' }}
                </h3>
                <button
                  @click="handleClose"
                  class="rounded-full p-1 hover:bg-gray-100 transition-colors"
                >
                  <XMarkIcon class="w-5 h-5 text-gray-400" />
                </button>
              </DialogTitle>

              <!-- 表单内容 -->
              <form @submit.prevent="handleSubmit" class="p-6">
                <div class="space-y-6">
                  <!-- 公司名称 -->
                  <div class="space-y-1">
                    <label class="block text-sm font-medium text-gray-700">公司名称</label>
                    <input
                      v-model="form.company"
                      type="text"
                      placeholder="请输入公司名称"
                      :class="[
                        'w-full rounded-lg border py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10',
                        errors.company ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
                      ]"
                    />
                    <p v-if="errors.company" class="text-sm text-red-500 mt-1">{{ errors.company }}</p>
                  </div>

                  <!-- 所在部门和职位名称 -->
                  <div class="grid grid-cols-2 gap-6">
                    <div class="space-y-1">
                      <label class="block text-sm font-medium text-gray-700">所在部门</label>
                      <input
                        v-model="form.department"
                        type="text"
                        placeholder="请输入所在部门（选填）"
                        :class="[
                          'w-full rounded-lg border py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10',
                          errors.department ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
                        ]"
                      />
                      <p v-if="errors.department" class="text-sm text-red-500 mt-1">{{ errors.department }}</p>
                    </div>

                    <div class="space-y-1">
                      <label class="block text-sm font-medium text-gray-700">职位名称</label>
                      <input
                        v-model="form.position"
                        type="text"
                        placeholder="请输入职位名称"
                        :class="[
                          'w-full rounded-lg border py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10',
                          errors.position ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
                        ]"
                      />
                      <p v-if="errors.position" class="text-sm text-red-500 mt-1">{{ errors.position }}</p>
                    </div>
                  </div>

                  <!-- 在职时间 -->
                  <div class="space-y-2">
                    <label class="block text-sm font-medium text-gray-700">在职时间</label>
                    <div class="flex items-center space-x-4">
                      <div class="relative flex-1">
                        <input
                          v-model="form.start_date"
                          type="date"
                          :class="[
                            'w-full rounded-lg border py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10',
                            errors.start_date ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
                          ]"
                        />
                        <CalendarIcon class="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" />
                      </div>
                      
                      <span v-if="!form.is_current" class="text-gray-500">至</span>
                      
                      <div v-if="!form.is_current" class="relative flex-1">
                        <input
                          v-model="form.end_date"
                          type="date"
                          :class="[
                            'w-full rounded-lg border py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10',
                            errors.end_date ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
                          ]"
                        />
                        <CalendarIcon class="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" />
                      </div>
                    </div>
                    <p v-if="errors.start_date || errors.end_date" class="text-sm text-red-500 mt-1">
                      {{ errors.start_date || errors.end_date }}
                    </p>
                    
                    <label class="inline-flex items-center mt-2">
                      <input
                        type="checkbox"
                        v-model="form.is_current"
                        class="rounded border-gray-300 text-blue-600 focus:ring-blue-500/10"
                      />
                      <span class="ml-2 text-sm text-gray-700">至今</span>
                    </label>
                  </div>

                  <!-- 工作描述 -->
                  <div class="space-y-1">
                    <label class="block text-sm font-medium text-gray-700">工作描述</label>
                    <textarea
                      v-model="form.description"
                      rows="4"
                      placeholder="请详细描述您的工作职责和内容（至少50字）"
                      :class="[
                        'w-full rounded-lg border py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10',
                        errors.description ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
                      ]"
                    ></textarea>
                    <p v-if="errors.description" class="text-sm text-red-500 mt-1">{{ errors.description }}</p>
                  </div>

                  <!-- 工作成就 -->
                  <div class="space-y-1">
                    <label class="block text-sm font-medium text-gray-700">工作成就</label>
                    <textarea
                      v-model="form.achievements"
                      rows="3"
                      placeholder="请描述您在这份工作中取得的成就"
                      class="w-full rounded-lg border border-gray-300 py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-500"
                    ></textarea>
                  </div>

                  <!-- 技术栈 -->
                  <div class="space-y-1">
                    <label class="block text-sm font-medium text-gray-700">技术栈</label>
                    <textarea
                      v-model="form.technologies"
                      rows="2"
                      placeholder="请列出您使用的主要技术栈"
                      class="w-full rounded-lg border border-gray-300 py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-500"
                    ></textarea>
                  </div>

                  <!-- 底部按钮 -->
                  <div class="flex justify-end space-x-3 pt-6">
                    <button
                      type="button"
                      @click="handleClose"
                      class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
                    >
                      取消
                    </button>
                    <button
                      type="submit"
                      :disabled="loading"
                      class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {{ loading ? '保存中...' : '确认' }}
                    </button>
                  </div>
                </div>
              </form>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { ref, watch } from 'vue'
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionRoot,
  TransitionChild
} from '@headlessui/vue'
import { XMarkIcon, CalendarIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  initialData: {
    type: Object,
    default: () => ({})
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'submit'])

// 表单数据
const form = ref({
  id: null,
  company: '',
  position: '',
  department: '',
  start_date: null,
  end_date: null,
  is_current: false,
  description: '',
  achievements: '',
  technologies: ''
})

// 监听初始数据变化
watch(() => props.initialData, (newVal) => {
  if (newVal) {
    // 确保所有字段都有默认值
    form.value = {
      id: newVal.id || null,
      company: newVal.company || '',
      position: newVal.position || '',
      department: newVal.department || '',
      start_date: newVal.start_date?.split('T')[0] || null,
      end_date: newVal.end_date?.split('T')[0] || null,
      is_current: newVal.is_current || false,
      description: newVal.description || '',
      achievements: newVal.achievements || '',
      technologies: newVal.technologies || ''
    }
    console.log('Form initialized:', form.value)
  }
}, { immediate: true, deep: true })

const handleClose = () => {
  emit('update:modelValue', false)
}

// 表单验证状态
const errors = ref({
  company: '',
  position: '',
  department: '',
  start_date: '',
  end_date: '',
  description: ''
})

// 验证表单
const validateForm = () => {
  let isValid = true
  errors.value = {
    company: '',
    position: '',
    department: '',
    start_date: '',
    end_date: '',
    description: ''
  }

  // 必填字段验证
  if (!form.value.company?.trim()) {
    errors.value.company = '请输入公司名称'
    isValid = false
  }

  if (!form.value.position?.trim()) {
    errors.value.position = '请输入职位名称'
    isValid = false
  }

  if (!form.value.start_date) {
    errors.value.start_date = '请选择入职时间'
    isValid = false
  }

  if (!form.value.is_current && !form.value.end_date) {
    errors.value.end_date = '请选择离职时间或勾选"至今"'
    isValid = false
  }

  // 工作描述至少50字
  if (!form.value.description?.trim() || form.value.description.length < 50) {
    errors.value.description = '工作描述至少需要50个字符'
    isValid = false
  }

  // 日期逻辑验证
  if (form.value.start_date && form.value.end_date && !form.value.is_current) {
    const startDate = new Date(form.value.start_date)
    const endDate = new Date(form.value.end_date)
    if (endDate < startDate) {
      errors.value.end_date = '离职时间不能早于入职时间'
      isValid = false
    }
  }

  return isValid
}

// 提交处理
const handleSubmit = () => {
  if (!validateForm()) {
    return
  }
  
  console.log('Submitting form:', form.value)
  const formData = {
    ...form.value,
    // 处理日期格式
    start_date: form.value.start_date,
    end_date: form.value.is_current ? null : form.value.end_date,
    // 确保文本字段有值
    department: form.value.department?.trim() || '',
    achievements: form.value.achievements?.trim() || '',
    technologies: form.value.technologies?.trim() || ''
  }
  
  console.log('Formatted form data:', formData)
  emit('submit', formData)
}
</script>

<style scoped>
/* 移动端适配 */
@media (max-width: 640px) {
  .grid {
    @apply grid-cols-1 gap-4;
  }
}

/* 输入框聚焦效果 */
input:focus, textarea:focus {
  @apply ring-2 ring-blue-500/10 border-blue-500;
}

/* 过渡动画 */
.transition-all {
  @apply duration-200;
}

/* 错误状态下的输入框动画 */
.border-red-300 {
  @apply transition-colors duration-200;
}

/* 错误提示文字渐入动画 */
.text-red-500 {
  @apply animate-fade-in;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(-4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.2s ease-out;
}
</style> 