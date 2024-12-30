<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    :width="dialogWidth"
    :fullscreen="isMobile"
    :close-on-click-modal="false"
    :show-close="false"
    @close="handleClose"
    class="edit-dialog"
    destroy-on-close
  >
    <div class="dialog-container">
      <!-- Header -->
      <div class="dialog-header">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium text-gray-900">编辑求职意向</h3>
          <!-- 移动端显示关闭按钮 -->
          <button
            v-if="isMobile"
            @click="handleClose"
            class="text-gray-400 hover:text-gray-500"
          >
            <XMarkIcon class="h-6 w-6" />
          </button>
        </div>
      </div>

      <!-- Body -->
      <div class="dialog-body p-4">
        <el-form
          ref="formRef"
          :model="form"
          :disabled="loading"
        >
          <form @submit.prevent="handleSubmit" class="space-y-4 sm:space-y-5">
            <!-- 两列布局 -->
            <div class="grid grid-cols-2 gap-4">
              <!-- 工作类型 -->
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700">工作类型</label>
                <el-form-item prop="job_type" class="mb-0">
                  <Listbox v-model="form.job_type">
                    <div class="relative w-full">
                      <ListboxButton class="relative w-full cursor-default rounded-md border border-gray-300 bg-gray-50 py-2 pl-3 pr-10 text-left shadow-sm focus:border-gray-900 focus:outline-none focus:ring-1 focus:ring-gray-900/10 sm:text-sm">
                        <span class="block truncate">{{ getJobTypeLabel(form.job_type) }}</span>
                        <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                          <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                        </span>
                      </ListboxButton>

                      <transition
                        leave-active-class="transition ease-in duration-100"
                        leave-from-class="opacity-100"
                        leave-to-class="opacity-0"
                      >
                        <ListboxOptions class="absolute z-10 mt-1 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                          <ListboxOption
                            v-for="option in JOB_TYPE_OPTIONS"
                            :key="option.value"
                            :value="option.value"
                            v-slot="{ active, selected }"
                          >
                            <div :class="[
                              active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                              'relative cursor-default select-none py-2 pl-3 pr-9'
                            ]">
                              <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">
                                {{ option.label }}
                              </span>
                              <span v-if="selected" :class="[active ? 'text-gray-900' : 'text-gray-600', 'absolute inset-y-0 right-0 flex items-center pr-4']">
                                <CheckIcon class="h-5 w-5" aria-hidden="true" />
                              </span>
                            </div>
                          </ListboxOption>
                        </ListboxOptions>
                      </transition>
                    </div>
                  </Listbox>
                </el-form-item>
              </div>

              <!-- 求职状态 -->
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700">求职状态</label>
                <el-form-item prop="job_status" class="mb-0">
                  <Listbox v-model="form.job_status">
                    <div class="relative w-full">
                      <ListboxButton class="relative w-full cursor-default rounded-md border border-gray-300 bg-gray-50 py-2 pl-3 pr-10 text-left shadow-sm focus:border-gray-900 focus:outline-none focus:ring-1 focus:ring-gray-900/10 sm:text-sm">
                        <span class="block truncate">{{ getJobStatusLabel(form.job_status) }}</span>
                        <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                          <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                        </span>
                      </ListboxButton>

                      <transition
                        leave-active-class="transition ease-in duration-100"
                        leave-from-class="opacity-100"
                        leave-to-class="opacity-0"
                      >
                        <ListboxOptions class="absolute z-10 mt-1 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                          <ListboxOption
                            v-for="option in LOCAL_JOB_STATUS_OPTIONS"
                            :key="option.value"
                            :value="option.value"
                            v-slot="{ active, selected }"
                          >
                            <div :class="[
                              active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                              'relative cursor-default select-none py-2 pl-3 pr-9'
                            ]">
                              <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">
                                {{ option.label }}
                              </span>
                              <span v-if="selected" :class="[active ? 'text-gray-900' : 'text-gray-600', 'absolute inset-y-0 right-0 flex items-center pr-4']">
                                <CheckIcon class="h-5 w-5" aria-hidden="true" />
                              </span>
                            </div>
                          </ListboxOption>
                        </ListboxOptions>
                      </transition>
                    </div>
                  </Listbox>
                </el-form-item>
              </div>

              <!-- 期望薪资 -->
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700">期望薪资</label>
                <el-form-item prop="expected_salary" class="mb-0">
                  <Listbox v-model="form.expected_salary">
                    <div class="relative w-full">
                      <ListboxButton class="relative w-full cursor-default rounded-md border border-gray-300 bg-gray-50 py-2 pl-3 pr-10 text-left shadow-sm focus:border-gray-900 focus:outline-none focus:ring-1 focus:ring-gray-900/10 sm:text-sm">
                        <span class="block truncate">{{ getSalaryLabel(form.expected_salary) }}</span>
                        <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                          <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                        </span>
                      </ListboxButton>

                      <transition
                        leave-active-class="transition ease-in duration-100"
                        leave-from-class="opacity-100"
                        leave-to-class="opacity-0"
                      >
                        <ListboxOptions class="absolute z-10 mt-1 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                          <ListboxOption
                            v-for="option in SALARY_OPTIONS"
                            :key="option.value"
                            :value="option.value"
                            v-slot="{ active, selected }"
                          >
                            <div :class="[
                              active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                              'relative cursor-default select-none py-2 pl-3 pr-9'
                            ]">
                              <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">
                                {{ option.label }}
                              </span>
                              <span v-if="selected" :class="[active ? 'text-gray-900' : 'text-gray-600', 'absolute inset-y-0 right-0 flex items-center pr-4']">
                                <CheckIcon class="h-5 w-5" aria-hidden="true" />
                              </span>
                            </div>
                          </ListboxOption>
                        </ListboxOptions>
                      </transition>
                    </div>
                  </Listbox>
                </el-form-item>
              </div>

              <!-- 期望城市 -->
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700">期望城市</label>
                <el-form-item prop="expected_city" class="mb-0">
                  <input
                    v-model="form.expected_city"
                    type="text"
                    placeholder="请输入期望城市，多个城市用逗号分隔"
                    class="block w-full rounded-md border-gray-300 bg-gray-50 py-2 px-3 shadow-sm focus:border-gray-900 focus:ring-1 focus:ring-gray-900/10 sm:text-sm"
                  />
                </el-form-item>
              </div>
            </div>

            <!-- 期望行业 -->
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700">期望行业</label>
              <el-form-item prop="industries" class="mb-0">
                <input
                  v-model="form.industries"
                  type="text"
                  placeholder="请输入期望行业，多个行业用逗号分隔"
                  class="block w-full rounded-md border-gray-300 bg-gray-50 py-2 px-3 shadow-sm focus:border-gray-900 focus:ring-1 focus:ring-gray-900/10 sm:text-sm"
                />
              </el-form-item>
            </div>
          </form>
        </el-form>
      </div>

      <!-- Footer -->
      <div class="dialog-footer">
        <div class="flex justify-end space-x-3">
          <button
            type="button"
            @click="handleClose"
            class="rounded-md border border-gray-300 bg-white px-3 sm:px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-900/10"
          >
            取消
          </button>
          <button
            type="button"
            @click="handleSubmit"
            :disabled="loading"
            class="rounded-md border border-transparent bg-gray-900 px-3 sm:px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-900/10 disabled:opacity-50"
          >
            {{ loading ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from '@headlessui/vue'
import { CheckIcon, ChevronUpDownIcon } from '@heroicons/vue/20/solid'
import { JOB_TYPE_OPTIONS, JOB_STATUS_OPTIONS, SALARY_OPTIONS } from '../constants/jobOptions'
import { INDUSTRY_CATEGORIES } from '../constants/industryOptions'
import { useWindowSize } from '@vueuse/core'
import { ElMessage } from 'element-plus'
import { XMarkIcon } from '@heroicons/vue/24/outline'

// 添加调试日志
console.log('求职状态选项:', JOB_STATUS_OPTIONS)

const props = defineProps({
  modelValue: Boolean,
  initialData: {
    type: Object,
    default: () => ({})
  },
  loading: Boolean
})

const emit = defineEmits(['update:modelValue', 'submit'])

// 表单引用
const formRef = ref(null)

// 常用城市列表
const commonCities = [
  '北京',
  '上海',
  '广州',
  '深圳',
  '杭州',
  '南京',
  '成都',
  '武汉',
  '西安',
  '苏州',
  '天津',
  '重庆'
]

// 城市选择
const selectedCities = ref([])

// 表单数据
const form = ref({
  job_type: '',
  job_status: '',
  expected_salary: '',
  expected_city: '',
  industries: []
})

// 处理城市变化
const handleCityChange = (value) => {
  form.value.expected_city = value.join('-')
}

// 监听初始数据变化
watch(() => props.initialData, (newVal) => {
  if (newVal) {
    // 转换旧的状态值到新的状态值
    const convertOldStatus = (oldStatus) => {
      const statusMap = {
        'open': 'unemployed_looking',
        'closed': 'employed_not_looking'
      }
      return statusMap[oldStatus] || oldStatus
    }

    const formData = {
      ...form.value,
      ...newVal,
      job_status: convertOldStatus(newVal.job_status),
      // 将破折号分隔的城市转换为逗号分隔
      expected_city: newVal.expected_city ? newVal.expected_city.split('-').join(',') : ''
    }
    
    form.value = formData
    console.log('更新后的表单数据:', form.value)
  }
}, { immediate: true })

// 表单验证规则
const rules = {
  job_type: [{ required: true, message: '请选择工作类型', trigger: 'change' }],
  job_status: [{ required: true, message: '请选择求职状态', trigger: 'change' }]
}

// 对话框可见性
const dialogVisible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    console.log('表单验证通过')
    
    // 处理行业数据
    const formData = { ...form.value }
    
    // 确保使用新的状态值
    const statusMap = {
      'open': 'unemployed_looking',
      'closed': 'employed_not_looking'
    }
    formData.job_status = statusMap[formData.job_status] || formData.job_status
    
    // 将逗号分隔的城市转换为破折号分隔（后端存储格式）
    if (formData.expected_city) {
      formData.expected_city = formData.expected_city.split(',').map(city => city.trim()).join('-')
    }
    
    if (Array.isArray(formData.industries)) {
      formData.industries = formData.industries.join(',')
    }
    
    console.log('提交的数据:', formData)
    emit('submit', formData)
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}

// 临时定义选项用于测试
const LOCAL_JOB_STATUS_OPTIONS = [
  { value: 'unemployed_looking', label: '离职-找工作' },
  { value: 'employed_not_looking', label: '在职-暂不考虑' },
  { value: 'employed_looking', label: '在职-看机会' },
  { value: 'student_internship', label: '在校-找实习' },
  { value: 'fresh_graduate', label: '应届生' }
]

const { width } = useWindowSize()
const isMobile = computed(() => width.value < 640)

// 根据屏幕宽度设置弹窗宽度
const dialogWidth = computed(() => {
  if (isMobile.value) return '100%'
  if (width.value < 1024) return '80%'
  return '640px'
})

// 处理关闭对话框
const handleClose = () => {
  dialogVisible.value = false
}

// 获取工作类型标签
const getJobTypeLabel = (value) => {
  const option = JOB_TYPE_OPTIONS.find(opt => opt.value === value)
  return option ? option.label : '请选择工作类型'
}

// 获取求职状态标签
const getJobStatusLabel = (value) => {
  const option = LOCAL_JOB_STATUS_OPTIONS.find(opt => opt.value === value)
  return option ? option.label : '请选择求职状态'
}

// 获取薪资标签
const getSalaryLabel = (value) => {
  const option = SALARY_OPTIONS.find(opt => opt.value === value)
  return option ? option.label : '请选择期望薪资'
}
</script>

<style>
.edit-dialog {
  @apply max-h-screen flex flex-col;
}

.edit-dialog :deep(.el-dialog__body) {
  @apply flex-1 overflow-y-auto;
}

.edit-dialog :deep(.el-dialog__footer) {
  @apply sticky bottom-0 bg-gray-50 z-10;
}

/* 移动端样式 */
@media (max-width: 640px) {
  .edit-dialog {
    margin: 0 !important;
  }

  .edit-dialog :deep(.el-dialog__body) {
    @apply p-0;
    height: calc(100vh - 120px);
    overflow-y: auto;
  }

  /* 调整表单布局 */
  .dialog-body {
    @apply px-4;  /* 添加左右内边距 */
  }

  /* 在移动端时所有输入框占满整行 */
  .grid {
    @apply grid-cols-1 gap-3;
  }

  /* 调整输入框在移动端的大小和间距 */
  input, select, textarea {
    @apply text-base py-3;  /* 增加高度使触摸更容易 */
  }

  /* 调整标签和输入框的间距 */
  .space-y-2 {
    @apply space-y-1.5;
  }

  /* 调整表单项之间的间距 */
  .space-y-4 {
    @apply space-y-3;
  }

  /* 确保底部按钮有足够的大小和间距 */
  .dialog-footer button {
    @apply py-2.5 px-4 text-base;
  }

  /* 调整下拉选项在移动端的显示 */
  .listbox-button {
    @apply py-3;  /* 增加高度便于触摸 */
  }

  .listbox-options {
    @apply max-h-60;  /* 限制最大高度 */
  }

  /* 调整选项的触摸区域 */
  .listbox-option {
    @apply py-3;
  }
}

/* 桌面端样式 */
@media (min-width: 641px) {
  .edit-dialog :deep(.el-dialog__body) {
    @apply p-0;
    max-height: calc(80vh - 120px);
    overflow-y: auto;
  }

  /* 桌面端保持原有的间距 */
  .dialog-body {
    @apply px-6;
  }
}

/* 通用样式 */
.dialog-header {
  @apply px-6 pt-4 pb-0 border-b border-gray-200;
}

.dialog-footer {
  @apply px-6 py-4 bg-gray-50 border-t border-gray-200;
}

/* 输入框聚焦时的样式 */
input:focus, textarea:focus {
  @apply ring-2 ring-gray-900/10 border-gray-900;
}

/* 禁用状态的样式 */
input:disabled, textarea:disabled {
  @apply bg-gray-100 cursor-not-allowed;
}
</style> 