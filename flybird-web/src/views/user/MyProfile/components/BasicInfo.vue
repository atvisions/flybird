<!-- src/views/user/MyProfile/components/BasicInfo.vue -->
<template>
  <div class="bg-white rounded-lg shadow">
    <!-- 个人信息卡片 -->
    <div class="px-6 py-6">
      <!-- 标题 -->
      <div class="flex items-center mb-6">
        <UserIcon class="w-5 h-5 text-gray-900 mr-2" />
        <h2 class="text-base font-medium text-gray-900">基本信息</h2>
      </div>

      <!-- 头像和基本信息 -->
      <div class="flex items-start space-x-6 mb-8">
        <!-- 头像部分 -->
        <div class="relative group">
          <img 
            :src="userAvatar"
            :key="avatarUpdateTime"
            class="w-24 h-24 rounded-full object-cover border-4 border-white shadow-lg user-avatar"
            alt="用户头像"
            @error="handleImageError"
          />
          <div 
            @click="showAvatarCropper = true"
            class="absolute inset-0 flex items-center justify-center rounded-full bg-black bg-opacity-40 opacity-0 group-hover:opacity-100 cursor-pointer transition-opacity duration-200"
          >
            <CameraIcon class="w-8 h-8 text-white" />
          </div>
          <!-- 性别标识 -->
          <div class="absolute bottom-0 right-0 bg-white rounded-full p-1.5 shadow">
            <!-- 男性图标 -->
            <svg 
              v-if="currentGender === 'male'" 
              class="w-5 h-5 text-blue-500" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor"
            >
              <circle cx="12" cy="12" r="5" stroke-width="2"/>
              <path d="M16 8L21 3" stroke-width="2" stroke-linecap="round"/>
              <path d="M21 3H16M21 3V8" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <!-- 女性图标 -->
            <svg 
              v-else-if="currentGender === 'female'" 
              class="w-5 h-5 text-pink-500" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor"
            >
              <circle cx="12" cy="10" r="5" stroke-width="2"/>
              <path d="M12 15V21" stroke-width="2" stroke-linecap="round"/>
              <path d="M9 18H15" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
        </div>

        <!-- 名字和简介 -->
        <div class="flex-1">
          <div class="flex items-center justify-between">
            <h1 class="text-xl font-bold text-gray-900">{{ formatBasicInfo.name }}</h1>
            <button
              @click="handleEdit"
              class="p-1.5 rounded-full hover:bg-gray-100 transition-colors"
            >
              <PencilSquareIcon class="w-4 h-4 text-gray-500" />
            </button>
          </div>
          <p class="mt-2 text-sm text-gray-600">{{ formatBasicInfo.personal_summary || '这个人很懒，还没有填写个人简介' }}</p>
        </div>
      </div>

      <!-- 基本信息部分 -->
      <div>
        <!-- 信息网格 -->
        <div class="grid grid-cols-2 gap-x-12 gap-y-4 border-t border-gray-100 pt-6">
          <!-- 联系方式 -->
          <div>
            <h2 class="text-xs font-medium text-gray-500 mb-3">联系方式</h2>
            <div class="flex items-center space-x-2">
              <PhoneIcon class="w-4 h-4 text-gray-400" />
              <span class="text-sm text-gray-900">{{ formatBasicInfo.phone }}</span>
            </div>
            <div class="flex items-center space-x-2 mt-2">
              <EnvelopeIcon class="w-4 h-4 text-gray-400" />
              <span class="text-sm text-gray-900">{{ formatBasicInfo.email }}</span>
            </div>
          </div>

          <!-- 基本资料 -->
          <div>
            <h2 class="text-xs font-medium text-gray-500 mb-3">基本资料</h2>
            <div class="flex items-center space-x-2">
              <MapPinIcon class="w-4 h-4 text-gray-400" />
              <span class="text-sm text-gray-900">{{ formatBasicInfo.location }}</span>
            </div>
            <div class="flex items-center space-x-2 mt-2">
              <CakeIcon class="w-4 h-4 text-gray-400" />
              <span class="text-sm text-gray-900">{{ formatBasicInfo.age }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 新的头像裁剪组件 -->
  <ProfileAvatarCropper
    ref="avatarUploadRef"
    v-model="showAvatarCropper"
    @upload="handleAvatarUpload"
  />

  <div v-if="pageLoading" class="loading-state">
    <!-- loading 内容 -->
  </div>
</template>

<script setup>
import { ref, computed, nextTick, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import defaultAvatarImage from '@/assets/images/default-avatar.png'
import { useStore } from 'vuex'
import config from '@/config'
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
import ProfileAvatarCropper from '@/components/ProfileAvatarCropper.vue'
import { useAccountStore } from '@/stores/account'
import { useProfileStore } from '@/stores/profile'
import { user } from '@/api/user'

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

// 3. 声明其他必要的响应式变量
const showAvatarCropper = ref(false)
const avatarUploadRef = ref(null)

// 4. 导入和初始化其他变量
const accountStore = useAccountStore()
const pageLoading = ref(true)
const basicInfo = ref({})
const profileStore = useProfileStore()

// 5. 计算属性
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

// 添加一个 ref 来存储完整的头像 URL
const avatarUrl = ref('')
const avatarUpdateTime = ref(Date.now())

// 修改计算属性
const userAvatar = computed(() => {
  // 只使用 resumeData 中的头像，不使用 store 中的头像
  const avatar = props.resumeData?.avatar
  
  console.log('Computing profile avatar:', {
    propsAvatar: props.resumeData?.avatar,
    finalAvatar: avatar,
    updateTime: avatarUpdateTime.value
  })

  if (!avatar) {
    avatarUrl.value = defaultAvatarImage
    return defaultAvatarImage
  }
  
  // 如果是完整的URL或base64，直接使用
  if (avatar.startsWith('http') || avatar.startsWith('data:image')) {
    avatarUrl.value = avatar
    return avatar
  }
  
  // 处理相对路径
  const cleanPath = avatar.replace(/^\/?(media\/)?/, '')
  const fullUrl = `${config.mediaURL}/${cleanPath}`
  
  // 添加时间戳参数来避免缓存
  avatarUrl.value = `${fullUrl}?t=${avatarUpdateTime.value}`
  return avatarUrl.value
})

const currentGender = computed(() => {
  return props.resumeData?.gender
})

// 6. 监听器
watch(
  () => props.resumeData,
  (newVal) => {
    if (newVal && Object.keys(newVal).length > 0) {
      pageLoading.value = false
    }
  },
  { immediate: true }
)

// 7. 生命周期钩子
onMounted(async () => {
  try {
    pageLoading.value = true
    // 获取完整度数据
    const completenessResponse = await profile.getCompleteness()
    if (completenessResponse.data?.code === 200) {
      eventBus.emit('completeness-updated', completenessResponse.data.data)
    }
  } catch (error) {
    console.error('Failed to fetch completeness:', error)
  } finally {
    pageLoading.value = false
  }
})

// 8. 方法定义
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
  // 确保传递正确的数据结构
  const editData = {
    name: props.resumeData.name,
    gender: props.resumeData.gender,
    birth_date: props.resumeData.birth_date,
    phone: props.resumeData.phone,
    email: props.resumeData.email,
    location: props.resumeData.location,
    personal_summary: props.resumeData.personal_summary
  }
  emit('edit', 'basic_info', editData)
}

const toggleBioExpand = () => {
  emit('toggleBioExpand')
}

// 9. 工具函数
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

// 修改头像上传处理函数
const handleAvatarUpload = async (file) => {
  try {
    loading.value = true
    
    // 使用 profile API 上传证件照
    const response = await profile.uploadAvatar(file)
    
    if (response.data?.code === 200) {
      // 更新时间戳触发头像重新加载
      avatarUpdateTime.value = Date.now()
      
      // 获取最新的完整度数据
      const completenessResponse = await profile.getCompleteness()
      if (completenessResponse.data?.code === 200) {
        eventBus.emit('completeness-updated')
      }
      
      // 触发父组件更新
      emit('update')
      
      showToast('证件照上传成功', 'success')
    } else {
      throw new Error(response.data?.message || '证件照上传失败')
    }
  } catch (error) {
    console.error('证件照上传失败:', error)
    showToast(error.message || '证件照上传失败，请重试', 'error')
  } finally {
    loading.value = false
    showAvatarCropper.value = false
  }
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

// 添加状态
const loading = ref(false)

// 监听 resumeData 变化
watch(
  () => props.resumeData,
  (newVal) => {
    if (newVal) {
      // 强制更新组件
      nextTick(() => {
        if (props.resumeData?.avatar) {
          const img = new Image()
          img.src = userAvatar.value
        }
      })
    }
  },
  { deep: true }
)
</script>