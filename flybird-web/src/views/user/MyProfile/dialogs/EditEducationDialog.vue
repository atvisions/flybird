<template>
  <TransitionRoot appear :show="modelValue" as="template">
    <Dialog as="div" class="relative z-50" @close="handleClose">
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
                <h3 class="text-lg font-medium text-gray-900">
                  {{ initialData ? '编辑教育经历' : '添加教育经历' }}
                </h3>
                <button
                  @click="handleClose"
                  class="p-1 rounded-full hover:bg-gray-100 transition-colors"
                >
                  <XMarkIcon class="w-5 h-5 text-gray-400" />
                </button>
              </DialogTitle>

              <!-- 表单内容 -->
              <form @submit.prevent="handleSubmit" class="p-6">
                <div class="space-y-4">
                  <!-- 第一行：学校和专业 -->
                  <div class="grid grid-cols-2 gap-4">
                    <!-- 学校名称 -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        学校名称
                      </label>
                      <input
                        v-model="formData.school"
                        type="text"
                        class="w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                        placeholder="请输入学校名称"
                        required
                      />
                    </div>

                    <!-- 专业名称 -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        专业名称
                      </label>
                      <input
                        v-model="formData.major"
                        type="text"
                        class="w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                        placeholder="请输入专业名称"
                        required
                      />
                    </div>
                  </div>

                  <!-- 第二行：学历和在读状态 -->
                  <div class="grid grid-cols-2 gap-4">
                    <!-- 学历 -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        学历
                      </label>
                      <Listbox v-model="formData.degree">
                        <div class="relative">
                          <ListboxButton class="relative w-full cursor-pointer rounded-lg bg-white py-2 pl-3 pr-10 text-left border border-gray-300 hover:border-gray-400 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500">
                            <span class="block truncate">{{ getDegreeLabel(formData.degree) || '请选择学历' }}</span>
                            <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                              <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                            </span>
                          </ListboxButton>
                          <transition
                            leave-active-class="transition duration-100 ease-in"
                            leave-from-class="opacity-100"
                            leave-to-class="opacity-0"
                          >
                            <ListboxOptions class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-lg bg-white py-1 text-sm shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                              <ListboxOption
                                v-for="option in degreeOptions"
                                :key="option.value"
                                :value="option.value"
                                v-slot="{ active, selected }"
                                as="template"
                              >
                                <li :class="[
                                  active ? 'bg-blue-50' : 'text-gray-900',
                                  'relative cursor-pointer select-none py-2 pl-3 pr-9'
                                ]">
                                  <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">
                                    {{ option.label }}
                                  </span>
                                  <span v-if="selected" :class="[
                                    'text-blue-600',
                                    'absolute inset-y-0 right-0 flex items-center pr-4'
                                  ]">
                                    <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                  </span>
                                </li>
                              </ListboxOption>
                            </ListboxOptions>
                          </transition>
                        </div>
                      </Listbox>
                    </div>

                    <!-- 在读状态 -->
                    <div class="flex items-center h-full pt-7">
                      <input
                        type="checkbox"
                        v-model="formData.is_current"
                        class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <label class="ml-2 text-sm text-gray-700">
                        目前在读
                      </label>
                    </div>
                  </div>

                  <!-- 第三行：起止时间 -->
                  <div class="grid grid-cols-2 gap-4">
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        入学时间
                      </label>
                      <input
                        v-model="formData.start_date"
                        type="month"
                        placeholder="YYYY-MM"
                        class="w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                        required
                      />
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        毕业时间
                      </label>
                      <input
                        v-model="formData.end_date"
                        type="month"
                        placeholder="YYYY-MM"
                        class="w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                        :min="formData.start_date"
                        :disabled="formData.is_current"
                      />
                    </div>
                  </div>

                  <!-- 第四行：在校经历和成就 -->
                  <div>
                    <!-- 在校经历 -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        在校经历
                      </label>
                      <textarea
                        v-model="formData.description"
                        rows="4"
                        class="w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                        placeholder="请描述在校期间的主要经历"
                      ></textarea>
                    </div>

                    <!-- 在校成就 -->
                    <div class="mt-4">
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        在校成就
                      </label>
                      <textarea
                        v-model="formData.achievements"
                        rows="4"
                        class="w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                        placeholder="请描述在校期间取得的成就"
                      ></textarea>
                    </div>
                  </div>
                </div>

                <!-- 底部按钮 -->
                <div class="mt-6 flex justify-end space-x-3">
                  <button
                    type="button"
                    @click="handleClose"
                    class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
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
  TransitionChild,
  Listbox,
  ListboxButton,
  ListboxOptions,
  ListboxOption
} from '@headlessui/vue'
import { 
  XMarkIcon,
  ChevronUpDownIcon,
  CheckIcon 
} from '@heroicons/vue/24/outline'

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
const formData = ref({
  school: '',      // 学校名称
  major: '',       // 专业名称
  degree: '',      // 学历
  start_date: '',  // 入学时间
  end_date: '',    // 毕业时间
  is_current: false, // 是否在读
  description: '', // 在校经历
  achievements: '' // 在校成就
})

// 监听初始数据变化
watch(() => props.initialData, (newData) => {
  
  if (newData) {
    formData.value = {
      ...newData,
      start_date: newData.start_date?.slice(0, 7) || '',
      end_date: newData.end_date?.slice(0, 7) || '',
      is_current: !!newData.is_current,
      description: newData.description || '',  // 确保字段名一致
      achievements: newData.achievements || '' // 确保字段名一致
    }
    
  } else {
    formData.value = {
      school: '',
      major: '',
      degree: '',
      start_date: '',
      end_date: '',
      is_current: false,
      description: '',  // 确保字段名一致
      achievements: '' // 确保字段名一致
    }
  }
}, { immediate: true })

// 监听在读状态变化
watch(() => formData.value.is_current, (newVal) => {
  if (newVal) {
    formData.value.end_date = ''  // 在读时清空毕业时间
  }
})

// 处理关闭
const handleClose = () => {
  emit('update:modelValue', false)
}

// 处理提交
const handleSubmit = () => {
  // 处理日期格式
  const formatDate = (dateStr) => {
    if (!dateStr) return null
    return `${dateStr}-01`  // 添加日期，转换为 YYYY-MM-DD 格式
  }

  // 分别处理两个字段
  const description = (formData.value.description || '').trim()
  const achievements = (formData.value.achievements || '').trim()

  console.log('【教育经历】表单字段检查:', {
    原始description: formData.value.description,
    处理后description: description,
    原始achievements: formData.value.achievements,
    处理后achievements: achievements
  })

  // 构建提交数据
  const submitData = {
    id: props.initialData?.id,
    school: formData.value.school.trim(),
    major: formData.value.major.trim(),
    degree: formData.value.degree,
    start_date: formatDate(formData.value.start_date),
    end_date: formData.value.is_current ? null : formatDate(formData.value.end_date),
    is_current: formData.value.is_current,
    description,      // 使用处理后的值
    achievements      // 使用处理后的值
  }

  console.log('【教育经历】最终提交数据:', {
    完整数据: submitData,
    description字段: submitData.description,
    achievements字段: submitData.achievements
  })

  emit('submit', submitData)
}

// 学历选项
const degreeOptions = [
  { value: 'high_school', label: '高中' },
  { value: 'junior_college', label: '大专' },
  { value: 'bachelor', label: '本科' },
  { value: 'master', label: '硕士' },
  { value: 'doctor', label: '博士' },
  { value: 'other', label: '其他' }
]

// 获取学历显示文本
const getDegreeLabel = (value) => {
  const option = degreeOptions.find(opt => opt.value === value)
  return option ? option.label : ''
}
</script>

<style scoped>
/* 移动端适配 */
@media (max-width: 640px) {
  .p-6 {
    @apply p-4;
  }
}

/* 输入框样式优化 */
input[type="month"] {
  @apply appearance-none;
}

/* 禁用状态样式 */
.disabled\:opacity-50:disabled {
  opacity: 0.5;
}

.disabled\:cursor-not-allowed:disabled {
  cursor: not-allowed;
}
</style> 