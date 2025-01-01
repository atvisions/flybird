<template>
  <TransitionRoot appear :show="modelValue" as="template">
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
              <DialogTitle 
                as="div" 
                class="flex items-center justify-between border-b border-gray-200 px-6 py-4"
              >
                <h3 class="text-lg font-medium text-gray-900">编辑求职意向</h3>
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
                  <!-- 第一行：工作类型和求职状态 -->
                  <div class="grid grid-cols-2 gap-6">
                    <!-- 工作类型 -->
                    <div class="space-y-1">
                      <label class="block text-sm font-medium text-gray-700">
                        工作类型
                      </label>
                      <Listbox v-model="form.job_type">
                        <div class="relative">
                          <ListboxButton
                            class="relative w-full cursor-pointer rounded-lg bg-white py-2.5 pl-4 pr-10 text-left border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-500"
                          >
                            <span class="block truncate text-sm">
                              {{ getJobTypeLabel(form.job_type) }}
                            </span>
                            <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
                              <ChevronUpDownIcon class="h-5 w-5 text-gray-400" />
                            </span>
                          </ListboxButton>

                          <ListboxOptions
                            class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-lg bg-white py-1 text-sm shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
                          >
                            <ListboxOption
                              v-for="option in JOB_TYPE_OPTIONS"
                              :key="option.value"
                              :value="option.value"
                              v-slot="{ active, selected }"
                            >
                              <li
                                :class="[
                                  active ? 'bg-blue-50 text-blue-600' : 'text-gray-900',
                                  'relative cursor-pointer select-none py-2.5 pl-4 pr-9'
                                ]"
                              >
                                <span :class="[selected ? 'font-medium' : 'font-normal', 'block truncate']">
                                  {{ option.label }}
                                </span>
                                <span
                                  v-if="selected"
                                  :class="[
                                    active ? 'text-blue-600' : 'text-blue-500',
                                    'absolute inset-y-0 right-0 flex items-center pr-3'
                                  ]"
                                >
                                  <CheckIcon class="h-5 w-5" />
                                </span>
                              </li>
                            </ListboxOption>
                          </ListboxOptions>
                        </div>
                      </Listbox>
                    </div>

                    <!-- 求职状态 -->
                    <div class="space-y-1">
                      <label class="block text-sm font-medium text-gray-700">
                        求职状态
                      </label>
                      <Listbox v-model="form.job_status">
                        <div class="relative">
                          <ListboxButton
                            class="relative w-full cursor-pointer rounded-lg bg-white py-2.5 pl-4 pr-10 text-left border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-500"
                          >
                            <span class="block truncate text-sm">
                              {{ getJobStatusLabel(form.job_status) }}
                            </span>
                            <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
                              <ChevronUpDownIcon class="h-5 w-5 text-gray-400" />
                            </span>
                          </ListboxButton>

                          <ListboxOptions
                            class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-lg bg-white py-1 text-sm shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
                          >
                            <ListboxOption
                              v-for="option in JOB_STATUS_OPTIONS"
                              :key="option.value"
                              :value="option.value"
                              v-slot="{ active, selected }"
                            >
                              <li
                                :class="[
                                  active ? 'bg-blue-50 text-blue-600' : 'text-gray-900',
                                  'relative cursor-pointer select-none py-2.5 pl-4 pr-9'
                                ]"
                              >
                                <span :class="[selected ? 'font-medium' : 'font-normal', 'block truncate']">
                                  {{ option.label }}
                                </span>
                                <span
                                  v-if="selected"
                                  :class="[
                                    active ? 'text-blue-600' : 'text-blue-500',
                                    'absolute inset-y-0 right-0 flex items-center pr-3'
                                  ]"
                                >
                                  <CheckIcon class="h-5 w-5" />
                                </span>
                              </li>
                            </ListboxOption>
                          </ListboxOptions>
                        </div>
                      </Listbox>
                    </div>
                  </div>

                  <!-- 第二行：期望薪资和期望城市 -->
                  <div class="grid grid-cols-2 gap-6">
                    <!-- 期望薪资 -->
                    <div class="space-y-1">
                      <label class="block text-sm font-medium text-gray-700">
                        期望薪资
                      </label>
                      <Listbox v-model="form.expected_salary">
                        <div class="relative">
                          <ListboxButton
                            class="relative w-full cursor-pointer rounded-lg bg-white py-2.5 pl-4 pr-10 text-left border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-500"
                          >
                            <span class="block truncate text-sm">
                              {{ getSalaryLabel(form.expected_salary) }}
                            </span>
                            <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
                              <ChevronUpDownIcon class="h-5 w-5 text-gray-400" />
                            </span>
                          </ListboxButton>

                          <ListboxOptions
                            class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-lg bg-white py-1 text-sm shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
                          >
                            <ListboxOption
                              v-for="option in SALARY_OPTIONS"
                              :key="option.value"
                              :value="option.value"
                              v-slot="{ active, selected }"
                            >
                              <li
                                :class="[
                                  active ? 'bg-blue-50 text-blue-600' : 'text-gray-900',
                                  'relative cursor-pointer select-none py-2.5 pl-4 pr-9'
                                ]"
                              >
                                <span :class="[selected ? 'font-medium' : 'font-normal', 'block truncate']">
                                  {{ option.label }}
                                </span>
                                <span
                                  v-if="selected"
                                  :class="[
                                    active ? 'text-blue-600' : 'text-blue-500',
                                    'absolute inset-y-0 right-0 flex items-center pr-3'
                                  ]"
                                >
                                  <CheckIcon class="h-5 w-5" />
                                </span>
                              </li>
                            </ListboxOption>
                          </ListboxOptions>
                        </div>
                      </Listbox>
                    </div>

                    <!-- 期望城市 -->
                    <div class="space-y-1">
                      <label class="block text-sm font-medium text-gray-700">
                        期望城市
                      </label>
                      <input
                        type="text"
                        v-model="form.expected_city"
                        placeholder="请输入期望城市，多个城市用逗号分隔"
                        class="w-full rounded-lg border border-gray-300 py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-500"
                      />
                    </div>
                  </div>

                  <!-- 第三行：期望行业 -->
                  <div class="space-y-1">
                    <label class="block text-sm font-medium text-gray-700">
                      期望行业
                    </label>
                    <div class="relative">
                      <input
                        type="text"
                        v-model="form.industries"
                        placeholder="请输入期望行业，多个行业用逗号分隔"
                        class="w-full rounded-lg border border-gray-300 py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-500"
                      />
                    </div>
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
  Listbox,
  ListboxButton,
  ListboxOptions,
  ListboxOption,
  TransitionRoot,
  TransitionChild
} from '@headlessui/vue'
import {
  XMarkIcon,
  ChevronUpDownIcon,
  CheckIcon
} from '@heroicons/vue/24/outline'

// 选项常量
const JOB_TYPE_OPTIONS = [
  { value: 'full_time', label: '全职' },
  { value: 'part_time', label: '兼职' },
  { value: 'internship', label: '实习' },
  { value: 'freelance', label: '自由职业' }
]

const JOB_STATUS_OPTIONS = [
  { value: 'actively_looking', label: '积极找工作' },
  { value: 'open_to_offers', label: '考虑机会' },
  { value: 'not_looking', label: '暂不找工作' }
]

const SALARY_OPTIONS = [
  { value: '0-5', label: '5K以下' },
  { value: '5-10', label: '5-10K' },
  { value: '10-15', label: '10-15K' },
  { value: '15-20', label: '15-20K' },
  { value: '20-30', label: '20-30K' },
  { value: '30-50', label: '30-50K' },
  { value: '50-100', label: '50-100K' },
  { value: '100+', label: '100K以上' }
]

const props = defineProps({
  modelValue: Boolean,
  initialData: {
    type: Object,
    default: () => ({})
  },
  loading: Boolean
})

const emit = defineEmits(['update:modelValue', 'submit'])

// 表单数据
const form = ref({
  job_type: '',           
  job_status: '',         
  expected_salary: '',    
  expected_city: '',      
  industries: '',         // 改为字符串类型,因为后端接收的是逗号分隔的字符串
})

// 修改 watch 逻辑
watch(() => props.initialData, (newVal) => {
  console.log('【EditJobIntentionDialog】初始数据变化:', newVal)
  
  if (newVal) {
    // 处理 industries 数据,确保是字符串格式
    const industries = Array.isArray(newVal.industries) 
      ? newVal.industries.join(',')
      : newVal.industries || ''

    // 处理 expected_city 数据,确保是字符串格式  
    const expected_city = Array.isArray(newVal.expected_city)
      ? newVal.expected_city.join(',')
      : newVal.expected_city || ''

    console.log('【EditJobIntentionDialog】处理后的数据:', {
      原始数据: newVal,
      处理后城市: expected_city,
      处理后行业: industries
    })

    form.value = {
      ...newVal,
      industries,
      expected_city,
      // 确保所有必需字段都有默认值
      job_type: newVal.job_type || '',
      job_status: newVal.job_status || '',
      expected_salary: newVal.expected_salary || ''
    }

    console.log('【EditJobIntentionDialog】表单数据:', form.value)
  }
}, { immediate: true, deep: true })

const handleClose = () => {
  emit('update:modelValue', false)
}

const handleSubmit = () => {
  console.log('【EditJobIntentionDialog】提交前表单数据:', form.value)
  
  // 提交前处理数据格式
  const formData = {
    ...form.value,
    // 确保 industries 和 expected_city 是字符串格式
    industries: form.value.industries?.split(',').filter(Boolean).join(',') || '',
    expected_city: form.value.expected_city?.split(',').filter(Boolean).join(',') || ''
  }
  
  console.log('【EditJobIntentionDialog】提交的数据:', formData)
  emit('submit', formData)
}

// 标签获取方法
const getJobTypeLabel = (value) => {
  const option = JOB_TYPE_OPTIONS.find(opt => opt.value === value)
  return option ? option.label : '请选择工作类型'
}

const getJobStatusLabel = (value) => {
  const option = JOB_STATUS_OPTIONS.find(opt => opt.value === value)
  return option ? option.label : '请选择求职状态'
}

const getSalaryLabel = (value) => {
  const option = SALARY_OPTIONS.find(opt => opt.value === value)
  return option ? option.label : '请选择期望薪资'
}
</script>

<style scoped>
/* 添加一些过渡动画 */
.transition-all {
  @apply duration-200;
}

/* 输入框聚焦效果 */
input:focus, select:focus {
  @apply ring-2 ring-blue-500/10 border-blue-500;
}

/* 下拉选项悬停效果 */
.hover\:bg-blue-50:hover {
  @apply bg-blue-50 text-blue-600;
}
</style> 