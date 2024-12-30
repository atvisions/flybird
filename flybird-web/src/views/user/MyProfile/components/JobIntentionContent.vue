<template>
  <div class="p-4">
    <!-- 主要信息 -->
    <div class="grid grid-cols-2 gap-4">
      <!-- 工作类型 -->
      <div class="bg-gray-50 rounded-lg p-3 transition-all hover:bg-gray-100">
        <div class="flex items-start space-x-3">
          <div class="p-2 bg-blue-50 rounded-lg">
            <BriefcaseIcon class="w-5 h-5 text-blue-600" />
          </div>
          <div>
            <span class="text-sm font-medium text-gray-500">工作类型</span>
            <div class="mt-1 text-gray-900">{{ getJobTypeLabel(data?.job_type) }}</div>
          </div>
        </div>
      </div>

      <!-- 求职状态 -->
      <div class="bg-gray-50 rounded-lg p-3 transition-all hover:bg-gray-100">
        <div class="flex items-start space-x-3">
          <div class="p-2 bg-green-50 rounded-lg">
            <UserCircleIcon class="w-5 h-5 text-green-600" />
          </div>
          <div>
            <span class="text-sm font-medium text-gray-500">求职状态</span>
            <div class="mt-1 text-gray-900">{{ getJobStatusLabel(data?.job_status) }}</div>
          </div>
        </div>
      </div>

      <!-- 期望薪资 -->
      <div class="bg-gray-50 rounded-lg p-3 transition-all hover:bg-gray-100">
        <div class="flex items-start space-x-3">
          <div class="p-2 bg-purple-50 rounded-lg">
            <CurrencyYenIcon class="w-5 h-5 text-purple-600" />
          </div>
          <div>
            <span class="text-sm font-medium text-gray-500">期望薪资</span>
            <div class="mt-1 text-gray-900">{{ getSalaryLabel(data?.expected_salary) }}</div>
          </div>
        </div>
      </div>

      <!-- 期望城市 -->
      <div class="bg-gray-50 rounded-lg p-3 transition-all hover:bg-gray-100">
        <div class="flex items-start space-x-3">
          <div class="p-2 bg-orange-50 rounded-lg">
            <MapPinIcon class="w-5 h-5 text-orange-600" />
          </div>
          <div>
            <span class="text-sm font-medium text-gray-500">期望城市</span>
            <div class="mt-1 text-gray-900">{{ formatCity(data?.expected_city) }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 期望行业 -->
    <div class="mt-4 bg-gray-50 rounded-lg p-3 transition-all hover:bg-gray-100">
      <div class="flex items-start space-x-3">
        <div class="p-2 bg-indigo-50 rounded-lg">
          <BuildingOfficeIcon class="w-5 h-5 text-indigo-600" />
        </div>
        <div>
          <span class="text-sm font-medium text-gray-500">期望行业</span>
          <div class="mt-1 text-gray-900">{{ formatIndustries(data?.industries) }}</div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="!data" class="flex flex-col items-center justify-center py-8">
      <DocumentPlusIcon class="w-12 h-12 text-gray-300" />
      <p class="mt-2 text-gray-400">暂无求职意向，点击编辑按钮添加</p>
    </div>
  </div>
</template>

<script setup>
import { JOB_TYPE_OPTIONS, JOB_STATUS_OPTIONS, SALARY_OPTIONS } from '../constants/jobOptions'
import { 
  BriefcaseIcon,
  UserCircleIcon,
  CurrencyYenIcon,
  MapPinIcon,
  BuildingOfficeIcon,
  DocumentPlusIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  data: {
    type: Object,
    default: null
  }
})

// 获取工作类型标签
const getJobTypeLabel = (value) => {
  const option = JOB_TYPE_OPTIONS.find(opt => opt.value === value)
  return option ? option.label : '未设置'
}

// 获取求职状态标签
const getJobStatusLabel = (value) => {
  const statusMap = {
    'unemployed_looking': '离职-找工作',
    'employed_not_looking': '在职-暂不考虑',
    'employed_looking': '在职-看机会',
    'student_internship': '在校-找实习',
    'fresh_graduate': '应届生'
  }
  return statusMap[value] || '未设置'
}

// 获取薪资标签
const getSalaryLabel = (value) => {
  const option = SALARY_OPTIONS.find(opt => opt.value === value)
  return option ? option.label : '未设置'
}

// 格式化城市
const formatCity = (city) => {
  if (!city) return '未设置'
  return city.split('-').join('、')
}

// 格式化行业
const formatIndustries = (industries) => {
  if (!industries) return '未设置'
  return industries.split(',').join('、')
}
</script>

<style scoped>
/* 移动端适配 */
@media (max-width: 640px) {
  .grid {
    @apply grid-cols-1 gap-3;
  }
  
  .p-4 {
    @apply p-3;
  }
}

/* 悬浮效果 */
.bg-gray-50 {
  transition: all 0.2s ease;
}

/* 图标容器 */
.p-2 {
  transition: all 0.2s ease;
}

.bg-gray-50:hover .p-2 {
  transform: scale(1.1);
}

/* 图标容器悬浮效果 */
.bg-gray-50:hover .p-2 {
  transform: scale(1.1);
  transition: transform 0.2s ease;
}
</style> 