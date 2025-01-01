<!-- src/views/user/MyProfile/components/BasicInfo.vue -->
<template>
    <div class="bg-white rounded-lg shadow">
      <!-- 骨架图加载状态 -->
      <template v-if="loading">
        <div class="p-4">
          <div class="flex items-start space-x-5">
            <!-- 头像骨架 -->
            <div class="relative">
              <div class="w-20 h-20 rounded-full bg-gray-200 animate-pulse"></div>
              <div class="absolute -bottom-1 -right-1 w-6 h-6 rounded-full bg-gray-200 animate-pulse"></div>
            </div>
            
            <!-- 信息骨架 -->
            <div class="flex-1 min-w-0">
              <!-- 名字骨架 -->
              <div class="flex items-center justify-between mb-3">
                <div class="h-6 w-24 bg-gray-200 rounded animate-pulse"></div>
              </div>
              
              <!-- 基本信息骨架 -->
              <div class="grid grid-cols-2 gap-3">
                <div class="flex items-center">
                  <div class="w-4 h-4 bg-gray-200 rounded mr-1.5 animate-pulse"></div>
                  <div class="h-4 w-24 bg-gray-200 rounded animate-pulse"></div>
                </div>
                <div class="flex items-center">
                  <div class="w-4 h-4 bg-gray-200 rounded mr-1.5 animate-pulse"></div>
                  <div class="h-4 w-24 bg-gray-200 rounded animate-pulse"></div>
                </div>
                <div class="flex items-center">
                  <div class="w-4 h-4 bg-gray-200 rounded mr-1.5 animate-pulse"></div>
                  <div class="h-4 w-24 bg-gray-200 rounded animate-pulse"></div>
                </div>
                <div class="flex items-center">
                  <div class="w-4 h-4 bg-gray-200 rounded mr-1.5 animate-pulse"></div>
                  <div class="h-4 w-24 bg-gray-200 rounded animate-pulse"></div>
                </div>
              </div>
              
              <!-- 个人简介骨架 -->
              <div class="mt-3">
                <div class="flex items-center mb-2">
                  <div class="w-4 h-4 bg-gray-200 rounded mr-1.5 animate-pulse"></div>
                  <div class="h-4 w-16 bg-gray-200 rounded animate-pulse"></div>
                </div>
                <div class="bg-gray-50 rounded-md p-4">
                  <div class="space-y-2">
                    <div class="h-4 bg-gray-200 rounded animate-pulse"></div>
                    <div class="h-4 bg-gray-200 rounded animate-pulse"></div>
                    <div class="h-4 w-2/3 bg-gray-200 rounded animate-pulse"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>

      <!-- 实际内容 -->
      <template v-else>
        <div class="p-4">
          <div class="flex items-start space-x-5">
            <!-- 头像部分 -->
            <div class="relative group">
              <img 
                  :src="userAvatar" 
                  class="w-20 h-20 rounded-full object-cover border-2 border-white shadow"
                  alt="用户头像"
                  @error="handleImageError"
                  />
                  <!-- 性别图标 -->
                  <div class="absolute -bottom-1 -right-1 bg-white rounded-full p-1 shadow">
                    <svg v-if="currentGender === 'male'" 
                      class="w-4 h-4 text-blue-500" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 2C9.243 2 7 4.243 7 7v2h10V7c0-2.757-2.243-5-5-5zM9 11H7v9c0 1.654 1.346 3 3 3h4c1.654 0 3-1.346 3-3v-9h-2v9c0 .552-.448 1-1 1h-4c-.552 0-1-.448-1-1v-9z"/>
                    </svg>
                    <svg v-else-if="currentGender === 'female'" 
                      class="w-4 h-4 text-pink-500" viewBox="0 0 24 24" fill="currentColor">
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
                  {{ formatBasicInfo.name }}
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
                  <span class="text-sm truncate">{{ formatBasicInfo.phone }}</span>
                </div>
    
                <!-- 邮箱 -->
                <div class="flex items-center text-gray-600">
                  <EnvelopeIcon class="w-4 h-4 text-gray-400 mr-1.5" />
                  <span class="text-sm truncate">{{ formatBasicInfo.email }}</span>
                </div>
    
                <!-- 所在地 -->
                <div class="flex items-center text-gray-600">
                  <MapPinIcon class="w-4 h-4 text-gray-400 mr-1.5" />
                  <span class="text-sm truncate">{{ formatBasicInfo.location }}</span>
                </div>
    
                <!-- 年龄 -->
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
                    <template v-if="formatBasicInfo.personal_summary !== '未填写'">
                      <p 
                        class="text-sm text-gray-600 leading-relaxed min-h-[4.5em] line-clamp-3"
                        :class="{ 'line-clamp-none': bioExpanded }"
                      >
                        {{ formatBasicInfo.personal_summary }}
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
      </template>
    </div>
  </template>
  
  <script setup>
import { ref, computed, nextTick, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import defaultAvatarImage from '@/assets/images/default-avatar.png'
import { useStore } from 'vuex'
import { MEDIA_URL } from '@/config'
import { showToast } from '@/components/ToastMessage'
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
import profile from '@/api/profile'
import { eventBus } from '@/utils/eventBus'
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionChild,
  TransitionRoot
} from '@headlessui/vue'

// 1. 首先声明 props
const props = defineProps({
  resumeData: {
    type: Object,
    default: () => ({})
  },
  loading: {
    type: Boolean,
    default: false
  },
  bioExpanded: {
    type: Boolean,
    default: false
  },
  showBioExpandButton: {
    type: Boolean,
    default: false
  }
})

// 2. 声明 emits
const emit = defineEmits(['update', 'edit', 'toggleBioExpand'])

// 3. 导入和初始化其他变量
const store = useStore()
const loading = ref(true)
const fileInput = ref(null)
const basicInfo = ref({})

// 4. 计算属性
const formatBasicInfo = computed(() => {
  // 优先使用父组件传入的 resumeData
  const info = props.resumeData || {}
  
  return {
    name: info.name || info.username || '未填写',  // 添加 username 作为备选
    gender: formatGender(info.gender),
    phone: info.phone || '未填写',
    email: info.email || '未填写',
    location: info.location || '未填写',
    age: calculateAge(info.birth_date) || '未填写',
    personal_summary: info.personal_summary || '未填写'
  }
})

const userAvatar = computed(() => {
  const avatar = props.resumeData?.avatar
  if (!avatar) return defaultAvatarImage
  return avatar.startsWith('http') || avatar.startsWith('data:') ? avatar : `${MEDIA_URL}${avatar}`
})

const currentGender = computed(() => {
  return props.resumeData?.gender
})

// 5. 监听器
watch(
  () => props.resumeData,
  (newVal) => {
    if (newVal && Object.keys(newVal).length > 0) {
      loading.value = false
    }
  },
  { immediate: true }
)

// 6. 生命周期钩子
onMounted(async () => {
  try {
    loading.value = true
    // 不需要在这里获取数据，因为父组件会处理
  } catch (error) {
    console.error('初始化失败:', error)
  } finally {
    loading.value = false
  }
})

// 7. 方法定义
const handleFileChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  // 验证文件
  if (!validateFile(file)) {
    return
  }

  await handleAvatarUpload(file)
  
  // 清空文件选择器，以便能够选择同一个文件
  event.target.value = ''
}

const handleEdit = () => {
  console.log('BasicInfo handleEdit - 当前数据:', props.resumeData)
  emit('edit', 'basic_info', props.resumeData)
}

const toggleBioExpand = () => {
  emit('toggleBioExpand')
}

// 8. 工具函数
const calculateAge = (birthDate) => {
  if (!birthDate) return ''
  
  const birth = new Date(birthDate)
  const today = new Date()
  
  let age = today.getFullYear() - birth.getFullYear()
  const monthDiff = today.getMonth() - birth.getMonth()
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    age--
  }
  
  return `${age}岁`
}

const formatGender = (gender) => {
  const genderMap = {
    male: '男',
    female: '女',
    other: '其他'
  }
  return genderMap[gender] || '未填写'
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 调试辅助函数
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

// 添加头像上传处理函数
const handleAvatarUpload = async (file) => {
  try {
    loading.value = true
    const formData = new FormData()
    formData.append('avatar', file)
    
    // 使用 profile API 直接上传
    const response = await profile.uploadAvatar(formData)
    if (response.data?.code === 200) {
      showToast('头像上传成功', 'success')
      // 触发父组件更新
      emit('update')
      // 获取完整的头像URL
      const avatarUrl = response.data.data.avatar
      eventBus.emit('avatar-updated', avatarUrl)
      // 更新本地数据
      if (props.resumeData) {
        props.resumeData.avatar = avatarUrl
      }
    } else {
      throw new Error(response.data?.message || '上传失败')
    }
  } catch (error) {
    console.error('头像上传失败:', error)
    showToast(error.message || '头像上传失败，请稍后重试', 'error')
  } finally {
    loading.value = false
  }
}

// 添加触发文件选择的方法
const triggerUpload = () => {
  fileInput.value.click()
}

// 添加图片加载错误处理
const handleImageError = (e) => {
  e.target.src = defaultAvatarImage
}

// 添加文件验证
const validateFile = (file) => {
  // 验证文件类型
  if (!file.type.startsWith('image/')) {
    showToast('请选择图片文件', 'error')
    return false
  }

  // 验证文件大小（例如限制为 2MB）
  const maxSize = 2 * 1024 * 1024 // 2MB
  if (file.size > maxSize) {
    showToast('图片大小不能超过 2MB', 'error')
    return false
  }

  return true
}
</script>