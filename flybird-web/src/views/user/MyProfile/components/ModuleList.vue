<!-- src/views/user/MyProfile/components/ModuleList.vue -->
<template>
  <div class="space-y-4">
    <div v-for="module in activeModules" :key="module.type" class="bg-white rounded-lg shadow">
      <div class="flex items-center justify-between px-4 py-3">
        <h3 class="text-base font-medium text-gray-900">{{ module.name }}</h3>
        <div class="flex items-center space-x-2">
          <button
            @click="handleModuleEdit(module.type)"
            class="p-1 hover:bg-gray-100 rounded-full"
          >
            <PencilSquareIcon class="w-5 h-5 text-gray-400" />
          </button>
          <button
            @click="handleRemove(module.type)"
            class="p-1 hover:bg-gray-100 rounded-full"
          >
            <TrashIcon class="w-5 h-5 text-gray-400" />
          </button>
        </div>
      </div>
      
      <div class="px-4 pb-4">
        <!-- 求职意向模块 -->
        <template v-if="module.type === 'job_intention' && module.data">
          <div class="text-gray-600">
            <!-- 求职状态标识 -->
            <div class="flex items-center space-x-2 mb-3">
              <div 
                class="w-2 h-2 rounded-full"
                :class="getJobStatusColor(module.data.job_status)"
              ></div>
              <span class="text-sm font-medium">
                {{ getJobStatusLabel(module.data.job_status) }}
              </span>
            </div>

            <!-- 主要信息卡片 -->
            <div class="bg-gray-50 rounded-lg p-4 space-y-4">
              <!-- 工作类型和薪资 -->
              <div class="flex justify-between items-start">
                <div class="flex items-start space-x-3">
                  <BriefcaseIcon class="w-5 h-5 text-blue-500 mt-0.5" />
                  <div>
                    <div class="text-sm text-gray-500">期望职位</div>
                    <div class="font-medium mt-1">{{ getJobTypeLabel(module.data.job_type) }}</div>
                  </div>
                </div>
                <div class="flex items-start space-x-3">
                  <BanknotesIcon class="w-5 h-5 text-emerald-500 mt-0.5" />
                  <div class="text-right">
                    <div class="text-sm text-gray-500">期望薪资</div>
                    <div class="font-medium mt-1 text-emerald-600">
                      {{ module.data.expected_salary }}
                    </div>
                  </div>
                </div>
              </div>

              <!-- 期望城市 -->
              <div class="flex items-start space-x-3">
                <MapPinIcon class="w-5 h-5 text-red-500 mt-0.5" />
                <div>
                  <div class="text-sm text-gray-500">期望城市</div>
                  <div class="font-medium mt-1">
                    {{ formatCity(module.data.expected_city) }}
                  </div>
                </div>
              </div>

              <!-- 期望行业 -->
              <div v-if="module.data.industries" class="flex items-start space-x-3">
                <BuildingOfficeIcon class="w-5 h-5 text-purple-500 mt-0.5" />
                <div class="flex-1">
                  <div class="text-sm text-gray-500 mb-2">期望行业</div>
                  <div class="flex flex-wrap gap-2">
                    <span 
                      v-for="industry in formatIndustries(module.data.industries)" 
                      :key="industry"
                      class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-purple-50 text-purple-700"
                    >
                      {{ industry }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>

        <!-- 工作经历模块 -->
        <template v-else-if="module.type === 'work_experience' && module.data">
          <div class="relative space-y-0">
            <!-- 时间线 -->
            <div class="absolute left-[0.5625rem] top-3 bottom-3 w-px bg-gray-200"></div>

            <!-- 工作经历列表 -->
            <div 
              v-for="(exp, index) in module.data" 
              :key="index" 
              class="relative pl-12 pb-6"
            >
              <!-- 时间节点 -->
              <div class="absolute left-[0.5625rem] -translate-x-1/2 top-2 w-3 h-3 rounded-full bg-white border-2 border-blue-500"></div>
              
              <!-- 内容卡片 -->
              <div class="bg-gray-50 rounded-lg border border-gray-100 p-4 hover:shadow-sm transition-shadow">
                <!-- 头部信息 -->
                <div class="flex items-center justify-between mb-3">
                  <div class="flex-1">
                    <div class="text-sm text-gray-500">
                      {{ formatDate(exp.start_date) }} - {{ exp.end_date ? formatDate(exp.end_date) : '至今' }}
                    </div>
                    <div class="flex items-center justify-between mt-1.5">
                      <span class="text-base font-medium text-gray-900">{{ exp.company }}</span>
                      <div class="flex items-center space-x-2">
                        <button
                          @click="handleEdit(module.type, exp)"
                          class="p-1 hover:bg-white rounded-full transition-colors"
                        >
                          <PencilSquareIcon class="w-4 h-4 text-gray-400" />
                        </button>
                        <button
                          @click="handleDelete(module.type, exp.id)"
                          class="p-1 hover:bg-white rounded-full transition-colors"
                        >
                          <TrashIcon class="w-4 h-4 text-gray-400" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 职位 -->
                <div class="text-sm font-medium text-blue-600 mb-3">
                  {{ exp.position }}
                </div>

                <!-- 工作内容 -->
                <div class="space-y-2">
                  <div class="flex items-center space-x-2">
                    <DocumentTextIcon class="w-4 h-4 text-gray-400" />
                    <span class="text-sm text-gray-500">工作内容</span>
                  </div>
                  <div class="text-sm leading-relaxed text-gray-600 pl-6">
                    {{ exp.description }}
                  </div>
                </div>

                <!-- 工作成果 -->
                <div v-if="exp.achievements" class="mt-3 space-y-2">
                  <div class="flex items-center space-x-2">
                    <TrophyIcon class="w-4 h-4 text-yellow-500" />
                    <span class="text-sm text-gray-500">工作成果</span>
                  </div>
                  <div class="text-sm leading-relaxed text-gray-600 pl-6">
                    {{ exp.achievements }}
                  </div>
                </div>
              </div>
            </div>

            <!-- 添加按钮 -->
            <div class="relative pl-12">
              <div class="absolute left-[0.5625rem] -translate-x-1/2 top-2 w-3 h-3 rounded-full bg-white border-2 border-gray-300"></div>
              <button
                @click="handleAdd(module.type)"
                class="w-full flex items-center justify-center px-4 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-all"
              >
                <PlusIcon class="w-4 h-4 mr-2" />
                添加工作经历
              </button>
            </div>
          </div>
        </template>

        <!-- 默认显示 -->
        <div v-else-if="!module.data" class="text-center text-gray-400 py-4">
          暂无内容，点击编辑添加
        </div>
        <div v-else class="text-gray-600">
          {{ module.data }}
        </div>
      </div>
    </div>
  </div>

  <!-- 删除确认弹窗 -->
  <TransitionRoot appear :show="showDeleteConfirm" as="template">
    <Dialog as="div" class="relative z-50" @close="showDeleteConfirm = false">
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
            <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-xl bg-white text-left align-middle shadow-xl transition-all">
              <div class="p-6">
                <div class="flex items-start space-x-3">
                  <div class="p-2 bg-red-50 rounded-full flex-shrink-0">
                    <ExclamationTriangleIcon class="w-6 h-6 text-red-600" />
                  </div>
                  <div class="flex-1">
                    <DialogTitle as="h3" class="text-lg font-medium text-gray-900">
                      确认移除板块？
                    </DialogTitle>
                    <p class="mt-2 text-sm text-gray-500">
                      移除板块后，该板块将移至"更多模块"中，您可以随时重新添加。
                    </p>
                  </div>
                </div>
                
                <div class="mt-6 flex justify-end space-x-3">
                  <button
                    type="button"
                    @click="showDeleteConfirm = false"
                    class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
                  >
                    取消
                  </button>
                  <button
                    type="button"
                    @click="confirmRemove"
                    class="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                  >
                    确认移除
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
import { ref, watch } from 'vue'
import { 
  PencilSquareIcon, 
  TrashIcon,
  PlusIcon,
  ExclamationTriangleIcon,
  BriefcaseIcon,
  BanknotesIcon,
  MapPinIcon,
  BuildingOfficeIcon,
  CalendarIcon,
  DocumentTextIcon,
  TrophyIcon
} from '@heroicons/vue/24/outline'
import { ALL_MODULES } from '@/constants'
import JobIntentionContent from './JobIntentionContent.vue'
import WorkExperienceContent from './WorkExperienceContent.vue'
import { JOB_TYPE_OPTIONS, JOB_STATUS_OPTIONS, SALARY_OPTIONS } from '../constants/jobOptions'
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionRoot,
  TransitionChild
} from '@headlessui/vue'

const props = defineProps({
  activeModules: {
    type: Array,
    required: true
  },
  inactiveModules: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['remove', 'edit', 'edit-item', 'remove-item'])

// 获取模块显示名称
const getModuleName = (type) => {
  return ALL_MODULES[type] || type
}

// 删除确认相关
const showDeleteConfirm = ref(false)
const moduleToDelete = ref(null)

// 处理移除按钮点击
const handleRemove = (moduleType) => {
  console.log('准备移除模块:', moduleType)
  moduleToDelete.value = moduleType
  showDeleteConfirm.value = true
}

// 确认移除
const confirmRemove = () => {
  if (moduleToDelete.value) {
    console.log('确认移除模块:', moduleToDelete.value)
    emit('remove', moduleToDelete.value)
    showDeleteConfirm.value = false
    moduleToDelete.value = null
  }
}

// 监听模块变化
watch(() => props.activeModules, (newModules) => {
  console.log('ModuleList - 活动模块更新:', {
    active: newModules,
    inactive: props.inactiveModules,
    activeCount: newModules.length,
    inactiveCount: props.inactiveModules?.length
  })
}, { deep: true })

// 格式化薪资显示
const formatSalary = (salary) => {
  if (!salary) return '未设置'
  const [min, max] = salary.split('-')
  if (min && max) {
    return `${min}-${max}K/月`
  }
  return `${salary}K/月`
}

// 获取到岗时间显示
const getArrivalTime = (time) => {
  const timeMap = {
    'immediately': '随时到岗',
    'within_1_week': '1周内',
    'within_1_month': '1个月内',
    'within_3_months': '3个月内',
    'negotiable': '待商议'
  }
  return timeMap[time] || '未设置'
}

// 获取工作性质显示
const getJobNature = (nature) => {
  const natureMap = {
    'full_time': '全职',
    'part_time': '兼职',
    'internship': '实习',
    'freelance': '自由职业'
  }
  return natureMap[nature] || '未设置'
}

// 获取工作类型显示
const getWorkType = (type) => {
  const typeMap = {
    'office': '办公室工作',
    'remote': '远程工作',
    'hybrid': '混合办公',
    'flexible': '灵活办公'
  }
  return typeMap[type] || '未设置'
}

// 获取求职状态显示
const getJobStatus = (status) => {
  const statusMap = {
    'actively_looking': '积极找工作',
    'open_to_offers': '考虑机会',
    'not_looking': '暂不找工作'
  }
  return statusMap[status] || '未设置'
}

// 获取求职状态颜色
const getJobStatusColor = (status) => {
  const colorMap = {
    'actively_looking': 'bg-green-500',      // 积极找工作
    'open_to_offers': 'bg-yellow-500',       // 考虑机会
    'not_looking': 'bg-gray-500'             // 暂不找工作
  }
  return colorMap[status] || 'bg-gray-300'
}

// 获取工作类型标签
const getJobTypeLabel = (value) => {
  const typeMap = {
    'full_time': '全职',
    'part_time': '兼职',
    'internship': '实习',
    'freelance': '自由职业'
  }
  return typeMap[value] || '未设置'
}

// 获取求职状态标签
const getJobStatusLabel = (value) => {
  const statusMap = {
    'actively_looking': '积极找工作',
    'open_to_offers': '考虑机会',
    'not_looking': '暂不找工作'
  }
  return statusMap[value] || '未设置'
}

// 获取薪资标签
const getSalaryLabel = (value) => {
  const option = SALARY_OPTIONS.find(opt => opt.value === value)
  return option ? option.label : '未设置'
}

// 格式化城市显示
const formatCity = (city) => {
  if (!city) return '未设置'
  return city.split(',').join('、')
}

// 格式化行业显示
const formatIndustries = (industries) => {
  if (!industries) return []
  return typeof industries === 'string' ? industries.split(',') : industries
}

// 格式化日期显示
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}`
}

// 添加事件处理方法
const handleEdit = (type, item) => {
  console.log('ModuleList handleEdit:', type, item)
  if (type === 'job_intention') {
    // 找到求职意向模块的数据
    const jobModule = props.activeModules.find(m => m.type === 'job_intention')
    emit('edit-item', type, jobModule?.data)
  } else {
    emit('edit-item', type, item)
  }
}

// 处理顶部编辑按钮点击
const handleModuleEdit = (type) => {
  console.log('ModuleList handleModuleEdit:', type)
  const module = props.activeModules.find(m => m.type === type)
  emit('edit', type, module?.data)
}

const handleDelete = (type, itemId) => {
  emit('remove-item', type, itemId)
}

const handleAdd = (type) => {
  emit('edit', type)
}
</script>

<style scoped>
.delete-confirm-dialog :deep(.el-dialog__body) {
  @apply p-0;
}

/* 移动端适配 */
@media (max-width: 640px) {
  .delete-confirm-dialog {
    margin: 0 !important;
  }
  
  .p-6 {
    @apply p-4;
  }
}

/* 添加渐变效果 */
.bg-gray-50 {
  background: linear-gradient(to right, #f9fafb, #f3f4f6);
}

/* 悬停效果 */
.hover\:bg-gray-200:hover {
  @apply bg-gray-200 transition-colors duration-200;
}

/* 优化卡片样式 */
.border-gray-100 {
  border-color: rgba(229, 231, 235, 0.5);
}

/* 优化阴影效果 */
.hover\:shadow-sm:hover {
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

/* 优化文本行高 */
.leading-relaxed {
  line-height: 1.625;
}

/* 优化按钮悬停效果 */
button:hover .text-gray-400 {
  @apply text-gray-500 transition-colors;
}

/* 优化时间线节点效果 */
.border-blue-500 {
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

/* 优化卡片阴影效果 */
.hover\:shadow-sm:hover {
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
}

/* 优化文本行高 */
.leading-relaxed {
  line-height: 1.625;
}

/* 时间线渐变效果 */
.bg-gray-200 {
  background: linear-gradient(180deg, 
    transparent 0%,
    #e5e7eb 10%,
    #e5e7eb 90%,
    transparent 100%
  );
}
</style>