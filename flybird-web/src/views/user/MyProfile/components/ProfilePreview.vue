<template>
  <TransitionRoot appear :show="modelValue" as="div">
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
            as="div"
            :show="true"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <!-- 预览内容保持不变 -->
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { 
  UserIcon,
  BriefcaseIcon,
  BuildingOfficeIcon,
  AcademicCapIcon,
  SparklesIcon,
  PhoneIcon, 
  EnvelopeIcon, 
  MapPinIcon 
} from '@heroicons/vue/24/outline'
import profile from '@/api/profile'
import defaultAvatarImage from '@/assets/images/default-avatar.png'
import { useStore } from 'vuex'

const store = useStore()

const completeness = ref(0)
const basicInfo = ref({})
const jobIntention = ref({})
const workExperiences = ref([])
const educations = ref([])
const skills = ref([])

// 字段标签映射
const fieldLabels = {
  // 基本信息
  name: '姓名',
  gender: '性别',
  birth_date: '出生日期',
  phone: '手机号',
  email: '邮箱',
  location: '所在地',
  
  // 求职意向
  job_type: '工作类型',
  job_status: '求职状态',
  expected_salary: '期望薪资',
  expected_city: '期望城市',
  industries: '期望行业'
}

// 获取字段标签
const getFieldLabel = (key) => {
  return fieldLabels[key] || key
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

// 格式化求职意向的值
const formatJobIntentionValue = (key, value) => {
  if (!value) return '未设置'
  
  switch (key) {
    case 'job_type':
      const jobTypes = {
        'full_time': '全职',
        'part_time': '兼职',
        'internship': '实习',
        'freelance': '自由职业'
      }
      return jobTypes[value] || value
      
    case 'job_status':
      const statusMap = {
        'unemployed_looking': '离职-找工作',
        'employed_not_looking': '在职-暂不考虑',
        'employed_looking': '在职-看机会',
        'student_internship': '在校-找实习',
        'fresh_graduate': '应届生'
      }
      return statusMap[value] || value
      
    case 'expected_city':
      return formatCity(value)
      
    case 'industries':
      return formatIndustries(value)
      
    default:
      return value || '未设置'
  }
}

// 格式化日期范围
const formatDateRange = (startDate, endDate, isCurrent) => {
  if (!startDate) return ''
  
  const start = new Date(startDate).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'numeric'
  })
  
  if (isCurrent) {
    return `${start} - 至今`
  }
  
  if (endDate) {
    const end = new Date(endDate).toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'numeric'
    })
    return `${start} - ${end}`
  }
  
  return start
}

// 获取档案数据
const fetchProfileData = async () => {
  try {
    const response = await profile.getComplete()
    if (response.data?.code === 200) {
      const data = response.data.data
      completeness.value = data.completeness || 0
      basicInfo.value = data.basic_info || {}
      jobIntention.value = data.job_intention || {}
      workExperiences.value = data.work_experiences || []
      educations.value = data.educations || []
      skills.value = data.skills || []
    }
  } catch (error) {
    console.error('获取档案数据失败:', error)
  }
}

// 获取头像
const avatarUrl = computed(() => store.getters.getUserAvatar)

// 处理头像加载错误
const handleImageError = (e) => {
  e.target.src = defaultAvatarImage
}

onMounted(() => {
  fetchProfileData()
})
</script>

<style scoped>
/* 移动端适配 */
@media (max-width: 640px) {
  /* 调整头部区域 */
  .max-w-4xl {
    padding: 0 1rem;
  }

  .px-8 {
    padding-left: 1rem;
    padding-right: 1rem;
  }

  /* 调整联系信息在移动端的布局 */
  .flex.justify-center.gap-6 {
    @apply flex-col gap-3;
  }

  /* 调整头像大小 */
  .w-32.h-32 {
    width: 6rem;
    height: 6rem;
  }

  /* 调整文字大小 */
  .text-2xl {
    font-size: 1.25rem;
  }

  /* 调整简介宽度 */
  .max-w-xl {
    max-width: 100%;
  }

  /* 调整内边距 */
  .py-12 {
    padding-top: 2rem;
    padding-bottom: 2rem;
  }

  .mb-6 {
    margin-bottom: 1rem;
  }

  .mt-6 {
    margin-top: 1rem;
  }
}

/* 打印样式 */
@media print {
  .bg-gray-50 {
    background-color: white !important;
  }
  
  .shadow-md {
    box-shadow: none !important;
  }
  
  .border-b {
    border-color: #e5e7eb !important;
  }
}

/* 添加一些动画效果 */
.rounded-xl {
  transition: all 0.3s ease;
}

.hover\:shadow-md:hover {
  transform: translateY(-1px);
}

/* 技能标签悬浮效果 */
.rounded-full {
  transition: all 0.2s ease;
}

.rounded-full:hover {
  transform: scale(1.05);
}

/* 渐变文字效果 */
.bg-gradient-to-r {
  background-size: 200% auto;
  animation: gradient 8s ease infinite;
}

@keyframes gradient {
  0% { background-position: 0% center; }
  50% { background-position: 100% center; }
  100% { background-position: 0% center; }
}
</style> 