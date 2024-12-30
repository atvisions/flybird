<template>
  <div class="bg-white">
    <!-- 头部区域 - 使用渐变背景 -->
    <div class="bg-gradient-to-br from-gray-50 to-gray-100">
      <div class="max-w-4xl mx-auto px-8 py-12">
        <!-- 修改为居中布局 -->
        <div class="flex flex-col items-center text-center">
          <!-- 头像 -->
          <div class="mb-6">
            <div class="relative">
              <img 
                :src="avatarUrl" 
                class="w-32 h-32 rounded-xl object-cover shadow-lg border-4 border-white ring-2 ring-gray-100"
                alt="用户头像"
                @error="handleImageError"
              />
              <div class="absolute inset-0 rounded-xl ring-1 ring-inset ring-black/5"></div>
            </div>
          </div>

          <!-- 基本信息 -->
          <div class="w-full max-w-2xl">
            <!-- 姓名和简介 -->
            <h1 class="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600">
              {{ basicInfo.name || '未设置姓名' }}
            </h1>
            <p class="mt-3 text-gray-500 leading-relaxed max-w-xl mx-auto">
              {{ basicInfo.personal_summary || '未设置个人简介' }}
            </p>

            <!-- 联系信息 -->
            <div class="mt-6 flex justify-center gap-6">
              <div class="flex items-center text-gray-600 hover:text-gray-900 transition-colors">
                <PhoneIcon class="w-4 h-4 mr-2" />
                <span>{{ basicInfo.phone || '未设置手机号' }}</span>
              </div>
              <div class="flex items-center text-gray-600 hover:text-gray-900 transition-colors">
                <EnvelopeIcon class="w-4 h-4 mr-2" />
                <span>{{ basicInfo.email || '未设置邮箱' }}</span>
              </div>
              <div class="flex items-center text-gray-600 hover:text-gray-900 transition-colors">
                <MapPinIcon class="w-4 h-4 mr-2" />
                <span>{{ basicInfo.location || '未设置所在地' }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 内容区域 - 使用卡片式设计 -->
    <div class="max-w-4xl mx-auto px-8 py-12 space-y-12">
      <!-- 求职意向 -->
      <section class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-shadow">
        <h2 class="text-lg font-bold text-gray-900 mb-6 flex items-center">
          <BriefcaseIcon class="w-5 h-5 mr-2 text-gray-400" />
          求职意向
        </h2>
        <div class="grid grid-cols-2 gap-6">
          <div class="space-y-1">
            <span class="text-sm font-medium text-gray-500">工作类型</span>
            <div class="text-gray-900">{{ formatJobIntentionValue('job_type', jobIntention.job_type) }}</div>
          </div>
          <div class="space-y-1">
            <span class="text-sm font-medium text-gray-500">求职状态</span>
            <div class="text-gray-900">{{ formatJobIntentionValue('job_status', jobIntention.job_status) }}</div>
          </div>
          <div class="space-y-1">
            <span class="text-sm font-medium text-gray-500">期望薪资</span>
            <div class="text-gray-900">{{ jobIntention.expected_salary || '未设置' }}</div>
          </div>
          <div class="space-y-1">
            <span class="text-sm font-medium text-gray-500">期望城市</span>
            <div class="text-gray-900">{{ formatCity(jobIntention.expected_city) }}</div>
          </div>
          <div class="col-span-2 space-y-1">
            <span class="text-sm font-medium text-gray-500">期望行业</span>
            <div class="text-gray-900">{{ formatIndustries(jobIntention.industries) }}</div>
          </div>
        </div>
      </section>

      <!-- 工作经历 -->
      <section class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-shadow">
        <h2 class="text-lg font-bold text-gray-900 mb-6 flex items-center">
          <BuildingOfficeIcon class="w-5 h-5 mr-2 text-gray-400" />
          工作经历
        </h2>
        <div class="space-y-8">
          <div v-for="exp in workExperiences" :key="exp.id" 
            class="p-4 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors">
            <div class="flex justify-between items-start">
              <div>
                <h3 class="text-base font-semibold text-gray-900">{{ exp.company }}</h3>
                <p class="mt-1 text-sm text-gray-600">{{ exp.position }}</p>
                <p v-if="exp.department" class="mt-0.5 text-sm text-gray-500">{{ exp.department }}</p>
              </div>
              <div class="text-sm text-gray-500">
                {{ formatDateRange(exp.start_date, exp.end_date, exp.is_current) }}
              </div>
            </div>
            <div class="prose prose-sm max-w-none text-gray-600">
              <div class="mb-3">
                <h4 class="text-sm font-medium text-gray-700 mb-2">工作描述</h4>
                <p>{{ exp.description }}</p>
              </div>
              <div v-if="exp.achievements" class="mb-3">
                <h4 class="text-sm font-medium text-gray-700 mb-2">工作成就</h4>
                <p>{{ exp.achievements }}</p>
              </div>
              <div v-if="exp.technologies">
                <h4 class="text-sm font-medium text-gray-700 mb-2">技术栈</h4>
                <div class="flex flex-wrap gap-2">
                  <span 
                    v-for="tech in exp.technologies.split(',')" 
                    :key="tech"
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
                  >
                    {{ tech }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-if="!workExperiences.length" class="text-sm text-gray-500">暂无工作经历</div>
      </section>

      <!-- 教育经历 -->
      <section class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-shadow">
        <h2 class="text-lg font-bold text-gray-900 mb-6 flex items-center">
          <AcademicCapIcon class="w-5 h-5 mr-2 text-gray-400" />
          教育经历
        </h2>
        <div class="space-y-6">
          <div v-for="edu in educations" :key="edu.id" class="flex justify-between items-start">
            <div>
              <h3 class="text-base font-semibold text-gray-900">{{ edu.school }}</h3>
              <p class="mt-1 text-sm text-gray-600">{{ edu.major }}</p>
              <p class="mt-0.5 text-sm text-gray-500">{{ edu.degree }}</p>
            </div>
            <div class="text-sm text-gray-500">
              {{ formatDateRange(edu.start_date, edu.end_date) }}
            </div>
          </div>
        </div>
        <div v-if="!educations.length" class="text-sm text-gray-500">暂无教育经历</div>
      </section>

      <!-- 技能特长 -->
      <section class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-shadow">
        <h2 class="text-lg font-bold text-gray-900 mb-6 flex items-center">
          <SparklesIcon class="w-5 h-5 mr-2 text-gray-400" />
          技能特长
        </h2>
        <div class="flex flex-wrap gap-2">
          <span 
            v-for="skill in skills" 
            :key="skill"
            class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-50 text-gray-700 hover:bg-gray-100 hover:text-gray-900 transition-colors cursor-default"
          >
            {{ skill }}
          </span>
        </div>
      </section>
    </div>
  </div>
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
import { profile } from '@/api/profile'
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