<template>
  <div>
    <template v-if="data">
      <div class="grid grid-cols-2 gap-6">
        <!-- 求职状态 -->
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-lg flex items-center justify-center bg-blue-50">
            <div class="relative">
              <UserCircleIcon class="w-6 h-6 text-blue-500" />
              <div :class="[
                'absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 rounded-full border-2 border-white',
                getStatusColor(data.job_status)
              ]"></div>
            </div>
          </div>
          <div>
            <div class="text-xs text-gray-400">求职状态</div>
            <div class="mt-0.5 text-sm text-gray-700">{{ getJobStatusLabel(data.job_status) }}</div>
          </div>
        </div>

        <!-- 工作类型 -->
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-lg flex items-center justify-center bg-indigo-50">
            <BriefcaseIcon class="w-6 h-6 text-indigo-500" />
          </div>
          <div>
            <div class="text-xs text-gray-400">工作类型</div>
            <div class="mt-0.5 text-sm text-gray-700">{{ getJobTypeLabel(data.job_type) }}</div>
          </div>
        </div>

        <!-- 期望薪资 -->
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-lg flex items-center justify-center bg-emerald-50">
            <CurrencyYenIcon class="w-6 h-6 text-emerald-500" />
          </div>
          <div>
            <div class="text-xs text-gray-400">期望薪资</div>
            <div class="mt-0.5 text-sm text-gray-700">{{ formatSalary(data.expected_salary) }}</div>
          </div>
        </div>

        <!-- 期望城市 -->
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-lg flex items-center justify-center bg-rose-50">
            <MapPinIcon class="w-6 h-6 text-rose-500" />
          </div>
          <div>
            <div class="text-xs text-gray-400">期望城市</div>
            <div class="mt-0.5 text-sm text-gray-700">{{ formatCity(data.expected_city) }}</div>
          </div>
        </div>
      </div>

      <!-- 期望行业 -->
      <div class="mt-6 border-t border-gray-100 pt-4">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-lg flex items-center justify-center bg-purple-50">
            <BuildingOfficeIcon class="w-6 h-6 text-purple-500" />
          </div>
          <div class="flex-1">
            <div class="text-xs text-gray-400">期望行业</div>
            <!-- 已选行业标签 -->
            <div class="mt-2 flex flex-wrap gap-2">
              <div
                v-for="industry in industryList"
                :key="industry"
                class="px-2 py-1 text-xs rounded-full bg-purple-50 text-purple-600"
              >
                {{ industry }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- 空状态 -->
    <div v-else class="flex flex-col items-center justify-center py-12 bg-gray-50 rounded-lg">
      <DocumentPlusIcon class="w-12 h-12 text-gray-300" />
      <p class="mt-2 text-sm text-gray-400">暂无求职意向，点击编辑按钮添加</p>
    </div>
  </div>
</template>

<script setup>
import { 
  BriefcaseIcon,
  UserCircleIcon,
  CurrencyYenIcon,
  MapPinIcon,
  BuildingOfficeIcon,
  DocumentPlusIcon
} from '@heroicons/vue/24/outline'
import { onMounted, watch, computed, ref } from 'vue'

const props = defineProps({
  data: {
    type: Object,
    default: () => ({})
  }
})

// 表单数据
const form = ref({})

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
    'actively_looking': '正在积极找工作',
    'open_to_offers': '对机会持开放态度',
    'not_looking': '暂时不找工作'
  }
  return statusMap[value] || '未设置'
}

// 格式化城市
const formatCity = (city) => {
  if (!city) return '未设置'
  return city.split('-').join('、')
}

// 获取状态对应的颜色
const getStatusColor = (status) => {
  const colorMap = {
    'actively_looking': 'bg-green-500',  // 正在积极找工作 - 绿色
    'open_to_offers': 'bg-blue-500',     // 对机会持开放态度 - 蓝色
    'not_looking': 'bg-gray-400'         // 暂时不找工作 - 灰色
  }
  return colorMap[status] || 'bg-gray-400'
}

// 格式化薪资
const formatSalary = (salary) => {
  if (!salary) return '未设置'
  // 如果已经包含 'K' 或其他单位，直接返回
  if (typeof salary === 'string' && (salary.includes('K') || salary.includes('k'))) {
    return salary
  }
  // 否则添加 'K'
  return `${salary}K`
}

// 计算已选择的行业列表
const industryList = computed(() => {
  if (!props.data?.industries) return ['未设置']
  return props.data.industries.split(',').filter(Boolean)
})

// 调试日志
onMounted(() => {
  if (props.data) {
    form.value = { ...props.data }
  }
})
</script>

<style scoped>
.w-10 {
  transition: transform 0.2s ease;
}

.flex:hover .w-10 {
  transform: scale(1.1);
}

@media (max-width: 640px) {
  .grid-cols-2 {
    @apply grid-cols-1 gap-4;
  }
}
</style>