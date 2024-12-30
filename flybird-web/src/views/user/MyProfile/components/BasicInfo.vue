<!-- src/views/user/MyProfile/components/BasicInfo.vue -->
<template>
    <div class="bg-white rounded-lg shadow">
      <!-- 移除有问题的调试信息 -->
      <!-- <pre class="hidden">{{ JSON.stringify(resumeData, null, 2) }}</pre> -->
      
      <div class="p-4">
        <div class="flex items-start space-x-5">
          <!-- 头像部分 -->
          <div class="relative group">
            <img 
                :src="currentAvatarUrl" 
                class="w-20 h-20 rounded-full object-cover border-2 border-white shadow"
                alt="用户头像"
                @error="handleImageError"
                />
                <!-- 性别图标 -->
                <div class="absolute -bottom-1 -right-1 bg-white rounded-full p-1 shadow">
                  <svg v-if="resumeData.gender === 'male'" class="w-4 h-4 text-blue-500" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2C9.243 2 7 4.243 7 7v2h10V7c0-2.757-2.243-5-5-5zM9 11H7v9c0 1.654 1.346 3 3 3h4c1.654 0 3-1.346 3-3v-9h-2v9c0 .552-.448 1-1 1h-4c-.552 0-1-.448-1-1v-9z"/>
                  </svg>
                  <svg v-else-if="resumeData.gender === 'female'" class="w-4 h-4 text-pink-500" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2C9.243 2 7 4.243 7 7v2h10V7c0-2.757-2.243-5-5-5zM9 11H7v5h10v-5h-2v3H9v-3z"/>
                  </svg>
                </div>
                <div 
                @click="triggerUpload"
                class="absolute inset-0 flex items-center justify-center rounded-full bg-black bg-opacity-40 opacity-0 group-hover:opacity-100 cursor-pointer transition-opacity duration-200"
                >
                  <template v-if="loading">
                    <div class="animate-spin rounded-full h-8 w-8 border-2 border-white border-t-transparent"></div>
                  </template>
                  <template v-else>
                    <CameraIcon class="w-8 h-8 text-white" />
                  </template>
                </div>
                <input
                ref="fileInput"
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleFileChange"
                />
          </div>
  
          <!-- 用户信息 -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between mb-3">
              <h2 class="text-lg font-medium text-gray-900">
                {{ resumeData.name || '未设置姓名' }}
              </h2>
              <div class="flex items-center space-x-2">
                <!-- 使用 heroicons 的编辑图标 -->
                <button
                  @click="handleEdit"
                  class="p-1 rounded-full hover:bg-gray-100 transition-colors duration-200"
                  title="编辑基本信息"
                >
                  <PencilSquareIcon class="w-5 h-5 text-gray-500 hover:text-gray-700" />
                </button>
              </div>
            </div>
  
            <!-- 基本信息列表 -->
            <div class="grid grid-cols-2 gap-3">
              <!-- 手机号 -->
              <div class="flex items-center text-gray-600">
                <PhoneIcon class="w-4 h-4 text-gray-400 mr-1.5" />
                <span class="text-sm truncate">{{ resumeData.phone || '未设置手机号' }}</span>
              </div>
  
              <!-- 邮箱 -->
              <div class="flex items-center text-gray-600">
                <EnvelopeIcon class="w-4 h-4 text-gray-400 mr-1.5" />
                <span class="text-sm truncate">{{ resumeData.email || '未设置邮箱' }}</span>
              </div>
  
              <!-- 所在地 -->
              <div class="flex items-center text-gray-600">
                <MapPinIcon class="w-4 h-4 text-gray-400 mr-1.5" />
                <span class="text-sm truncate">{{ resumeData.location || '未设置所在地' }}</span>
              </div>
  
              <!-- 年龄 (使用图标) -->
              <div class="flex items-center text-gray-600">
                <CakeIcon class="w-4 h-4 text-gray-400 mr-1.5" />
                <span class="text-sm truncate">{{ formatBasicInfo.age }}</span>
              </div>
            </div>
  
            <!-- 个人简介 -->
            <div class="mt-3">
              <div class="flex items-center text-gray-600 mb-2">
                <DocumentTextIcon class="w-4 h-4 text-gray-400 mr-1.5" />
                <span class="text-sm font-medium">个人简介</span>
              </div>
              <div class="bg-gray-50 rounded-md p-4">
                <div class="relative">
                  <template v-if="resumeData.personal_summary">
                    <p 
                      class="text-sm text-gray-600 leading-relaxed min-h-[4.5em] line-clamp-3"
                      :class="{ 'line-clamp-none': bioExpanded }"
                    >
                      {{ resumeData.personal_summary }}
                    </p>
                    <button
                      v-if="showBioExpandButton"
                      @click="toggleBioExpand"
                      class="text-xs text-primary-600 hover:text-primary-700 mt-2 inline-flex items-center"
                    >
                      {{ bioExpanded ? '收起' : '展开全部' }}
                      <ChevronDownIcon 
                        v-if="!bioExpanded" 
                        class="w-4 h-4 ml-0.5" 
                      />
                      <ChevronUpIcon 
                        v-else 
                        class="w-4 h-4 ml-0.5" 
                      />
                    </button>
                  </template>
                  <p 
                    v-else 
                    class="text-sm text-gray-400 text-center min-h-[4.5em] flex items-center justify-center"
                  >
                    你还没有设置个人简介
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
import { ref, computed, nextTick, watch } from 'vue'
import { ElMessage , ElLoading } from 'element-plus'
import request, { API_PATHS } from '@/utils/request'  
import defaultAvatarImage from '@/assets/images/default-avatar.png'
import { useStore } from 'vuex'
import { profile } from '@/api/profile'
import { auth } from '@/api/auth'
import { showToast } from '@/components/ToastMessage'
const store = useStore()
const loading = ref(false)
const loadingInstance = ref(null)
import {
  PencilIcon,
  PhoneIcon,
  EnvelopeIcon,
  MapPinIcon,
  BriefcaseIcon,
  ClockIcon,
  CurrencyYenIcon,
  DocumentTextIcon,
  CameraIcon,
  UserIcon,
  CalendarIcon,
  ChevronDownIcon,
  ChevronUpIcon,
  CakeIcon,
  PencilSquareIcon
} from '@heroicons/vue/24/outline'
// 从 store 获取头像
const avatarUrl = computed(() => store.getters.getUserAvatar)
// 处理图片加载错误
const handleImageError = (e) => {
  e.target.src = defaultAvatarImage
}
const props = defineProps({
  resumeData: {
    type: Object,
    required: true
  },
  loading: Boolean,
  bioExpanded: Boolean,
  showBioExpandButton: Boolean,
  getBioText: String
})

const emit = defineEmits(['update', 'edit', 'toggleBioExpand'])
const fileInput = ref(null)

// 修改调试日志方式
const logResumeData = () => {
  const plainData = {
    name: props.resumeData.name,
    gender: props.resumeData.gender,
    phone: props.resumeData.phone,
    email: props.resumeData.email,
    location: props.resumeData.location,
    birth_date: props.resumeData.birth_date,
    personal_summary: props.resumeData.personal_summary,
    created_at: props.resumeData.created_at,
    updated_at: props.resumeData.updated_at
  }
  console.log('BasicInfo data:', plainData)
}

// 监听数据变化
watch(() => props.resumeData, (newVal) => {
  // 删除这行
  // console.log('BasicInfo received data:', newVal)
}, { immediate: true })

// 处理文件选择
const handleFileChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  // 验证文件类型
  if (!file.type.startsWith('image/')) {
    showToast('请选择图片文件', 'error')
    return
  }

  // 验证文件大小（例如限制为 2MB）
  const maxSize = 2 * 1024 * 1024 // 2MB
  if (file.size > maxSize) {
    showToast('图片大小不能超过 2MB', 'error')
    return
  }

  await handleAvatarUpload(file)
  
  // 清空文件选择器，以便能够选择同一个文件
  event.target.value = ''
}

// 添加 basicInfo ref
const basicInfo = ref({})

// 修改头像上传处理函数
const handleAvatarUpload = async (file) => {
  try {
    const formData = new FormData()
    formData.append('avatar', file)

    const response = await auth.uploadAvatar(formData)
    
    if (response.data?.code === 200) {
      // 使用 fetchUserInfo action 来更新用户信息
      await store.dispatch('fetchUserInfo')
      showToast('头像上传成功', 'success')
    }
  } catch (error) {
    console.error('头像上传失败:', error)
    showToast(error.message || '头像上传失败，请稍后重试', 'error')
  }
}

// 添加时间戳 ref
const avatarTimestamp = ref(Date.now())

// 计算属性 - 头像 URL
const currentAvatarUrl = computed(() => {
  const baseUrl = store.getters.getUserAvatar
  // 添加时间戳和随机数，确保每次都刷新
  return baseUrl ? `${baseUrl}?t=${avatarTimestamp.value}&r=${Math.random()}` : ''
})

// 触发文件选择
const triggerUpload = () => {
  fileInput.value.click()
}

// 性别显示文本
const genderText = computed(() => {
  const genderMap = {
    male: '男',
    female: '女',
    other: '其他'
  }
  return genderMap[props.resumeData.gender] || '未设置性别'
})

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 处理编辑按钮点击
const handleEdit = () => {
  console.log('点击编辑按钮, 当前数据:', props.resumeData)
  emit('edit')
}

// 处理展开/收起
const toggleBioExpand = () => {
  emit('toggleBioExpand')
}

// 计算年龄的函数
const calculateAge = (birthDate) => {
  if (!birthDate) return ''
  
  const birth = new Date(birthDate)
  const today = new Date()
  
  let age = today.getFullYear() - birth.getFullYear()
  const monthDiff = today.getMonth() - birth.getMonth()
  
  // 如果还没到生日，年龄减1
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    age--
  }
  
  return `${age}岁`
}

// 格式化性别显示
const formatGender = (gender) => {
  const genderMap = {
    male: '男',
    female: '女',
    other: '其他'
  }
  return genderMap[gender] || '未填写'
}

// 格式化基本信息
const formatBasicInfo = computed(() => {
  const info = props.resumeData || {}
  return {
    name: info.name || '未填写',
    gender: formatGender(info.gender),
    phone: info.phone || '未填写',
    email: info.email || '未填写',
    location: info.location || '未填写',
    age: calculateAge(info.birth_date) || '未填写',
    personal_summary: info.personal_summary || '未填写'
  }
})
</script>