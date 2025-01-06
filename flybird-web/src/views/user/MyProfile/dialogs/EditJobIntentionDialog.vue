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
            as="div"
            :show="true"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel class="w-full max-w-2xl transform overflow-hidden rounded-xl bg-white text-left align-middle shadow-xl transition-all">
              <!-- 表单内容 -->
              <form @submit.prevent="handleSubmit" class="flex flex-col max-h-[calc(100vh-8rem)]">
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

                <!-- 表单字段区域 - 添加滚动容器 -->
                <div class="flex-1 overflow-y-auto">
                  <div class="p-6 space-y-6 w-full">
                    <!-- 第一行：工作类型和求职状态 -->
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
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
                              class="absolute z-10 mt-1 w-full overflow-auto rounded-lg bg-white py-1 text-sm shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
                              style="min-width: 100%; max-width: none; width: max-content;"
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
                              class="absolute z-10 mt-1 w-full overflow-auto rounded-lg bg-white py-1 text-sm shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
                              style="min-width: 100%; max-width: none; width: max-content;"
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
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
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
                              class="absolute z-10 mt-1 w-full overflow-auto rounded-lg bg-white py-1 text-sm shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
                              style="min-width: 100%; max-width: none; width: max-content;"
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
                        <Listbox v-model="form.expected_city">
                          <div class="relative">
                            <ListboxButton
                              class="relative w-full cursor-pointer rounded-lg bg-white py-2.5 pl-4 pr-10 text-left border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-500"
                            >
                              <span class="block truncate text-sm">
                                {{ form.expected_city || '请选择期望城市' }}
                              </span>
                              <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
                                <ChevronUpDownIcon class="h-5 w-5 text-gray-400" />
                              </span>
                            </ListboxButton>

                            <ListboxOptions
                              class="absolute z-10 mt-1 w-full overflow-auto rounded-lg bg-white py-1 text-sm shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
                              style="min-width: 100%; max-width: none; width: max-content;"
                            >
                              <ListboxOption
                                v-for="city in CITY_OPTIONS"
                                :key="city.value"
                                :value="city.value"
                                v-slot="{ active, selected }"
                              >
                                <li
                                  :class="[
                                    active ? 'bg-blue-50 text-blue-600' : 'text-gray-900',
                                    'relative cursor-pointer select-none py-2.5 pl-4 pr-9'
                                  ]"
                                >
                                  <span :class="[selected ? 'font-medium' : 'font-normal', 'block truncate']">
                                    {{ city.label }}
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

                    <!-- 第三行：期望行业 -->
                    <div class="space-y-1">
                      <label class="block text-sm font-medium text-gray-700">
                        期望行业
                      </label>
                      <div class="relative w-full">
                        <input
                          type="text"
                          v-model="form.industries"
                          placeholder="请输入期望行业，多个行业用逗号分隔"
                          class="w-full rounded-lg border border-gray-300 py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-500"
                          @change="handleIndustriesInput"
                        />
                        <!-- 已选行业标签 -->
                        <div class="mt-2 flex flex-wrap gap-2 w-full">
                          <div
                            v-for="industry in selectedIndustries"
                            :key="industry"
                            class="inline-flex items-center px-2 py-1 text-xs rounded-full bg-blue-50 text-blue-600 space-x-1 whitespace-nowrap"
                          >
                            <span>{{ industry }}</span>
                            <XMarkIcon 
                              class="w-3 h-3 cursor-pointer hover:text-blue-800 shrink-0" 
                              @click="removeIndustry(industry)"
                            />
                          </div>
                        </div>
                        <!-- 热门行业推荐 -->
                        <div class="mt-3 w-full">
                          <div class="flex justify-between items-center mb-2">
                            <div class="text-xs text-gray-500">热门行业：</div>
                            <div class="text-xs text-gray-400">{{ selectedIndustries.length }}/5</div>
                          </div>
                          <div class="flex flex-wrap gap-2 w-full">
                            <button
                              v-for="industry in availableIndustries"
                              :key="industry"
                              type="button"
                              @click="addIndustry(industry)"
                              :disabled="selectedIndustries.length >= 5"
                              :class="[
                                'inline-flex items-center px-2 py-1 text-xs rounded-full border transition-colors whitespace-nowrap',
                                selectedIndustries.length >= 5 
                                  ? 'border-gray-100 text-gray-300 cursor-not-allowed' 
                                  : 'border-gray-200 text-gray-600 hover:bg-gray-50 hover:border-gray-300'
                              ]"
                            >
                              {{ industry }}
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 底部按钮 - 固定在底部 -->
                <div class="flex justify-end space-x-3 px-6 py-4 bg-gray-50 border-t border-gray-200">
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
                    class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
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
import { ref, watch, computed } from 'vue'
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

// 添加热门城市选项
const CITY_OPTIONS = [
  { value: '北京', label: '北京' },
  { value: '上海', label: '上海' },
  { value: '广州', label: '广州' },
  { value: '深圳', label: '深圳' },
  { value: '杭州', label: '杭州' },
  { value: '成都', label: '成都' },
  { value: '武汉', label: '武汉' },
  { value: '西安', label: '西安' },
  { value: '南京', label: '南京' },
  { value: '苏州', label: '苏州' }
]

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
  job_type: '',           
  job_status: '',         
  expected_salary: '',    
  expected_city: '',      // 改为单选
  industries: ''
})

// 修改 watch 逻辑
watch(() => props.initialData, (newVal) => {

  
  if (newVal) {
    // 处理 industries 数据,确保是字符串格式
    const industries = Array.isArray(newVal.industries) 
      ? newVal.industries.join(',')
      : newVal.industries || ''

    // 处理 expected_city 数据,确保是字符串格式  
    const expected_city = Array.isArray(newVal.expected_city)
      ? newVal.expected_city.join(',')
      : newVal.expected_city || ''


    form.value = {
      ...newVal,
      industries,
      expected_city,
      // 确保所有必需字段都有默认值
      job_type: newVal.job_type || '',
      job_status: newVal.job_status || '',
      expected_salary: newVal.expected_salary || ''
    }

   
  }
}, { immediate: true, deep: true })

const handleClose = () => {
  emit('update:modelValue', false)
}

const handleSubmit = () => {
  
  
  // 提交前处理数据格式
  const formData = {
    ...form.value,
    // 确保 industries 和 expected_city 是字符串格式
    industries: form.value.industries?.split(',').filter(Boolean).join(',') || '',
    expected_city: form.value.expected_city?.split(',').filter(Boolean).join(',') || ''
  }
  
 
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

// 添加热门行业选项
const HOT_INDUSTRIES = [
  '互联网',
  '人工智能',
  '大数据',
  '云计算',
  '金融科技',
  '电子商务',
  '教育科技',
  '医疗健康',
  '新能源',
  '物联网'
]

// 计算已选择的行业
const selectedIndustries = computed(() => {
  return form.value.industries?.split(',').filter(Boolean) || []
})

// 计算可选的热门行业（排除已选择的）
const availableIndustries = computed(() => {
  return HOT_INDUSTRIES.filter(industry => !selectedIndustries.value.includes(industry))
})

// 添加行业
const addIndustry = (industry) => {
  const industries = selectedIndustries.value
  if (!industries.includes(industry) && industries.length < 5) {
    form.value.industries = [...industries, industry].join(',')
  }
}

// 移除行业
const removeIndustry = (industry) => {
  const industries = selectedIndustries.value
  form.value.industries = industries.filter(i => i !== industry).join(',')
}

// 修改输入框的 change 事件处理
const handleIndustriesInput = (event) => {
  const value = event.target.value
  const industries = value.split(',').filter(Boolean)
  if (industries.length > 5) {
    // 只保留前5个行业
    form.value.industries = industries.slice(0, 5).join(',')
  }
}
</script>

<style scoped>
/* PC 端固定宽度 */
.max-w-2xl {
  max-width: 42rem !important;
  width: 42rem !important;
}

/* 移动端适配 */
@media (max-width: 640px) {
  .max-w-2xl {
    max-width: 100% !important;
    width: 100% !important;
  }
  
  .grid {
    @apply grid-cols-1 gap-4;
  }
}

/* 输入框聚焦效果 */
input:focus, select:focus {
  @apply ring-2 ring-blue-500/10 border-blue-500;
}

/* 下拉选项悬停效果 */
.hover\:bg-blue-50:hover {
  @apply bg-blue-50 text-blue-600;
}

/* 过渡动画 */
.transition-all {
  @apply duration-200;
}
</style> 