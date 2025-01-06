<!-- src/views/user/MyProfile/components/BasicInfo.vue -->
<template>
  <div class="bg-white rounded-lg shadow">
    <!-- 背景图部分 -->
    <div class="relative h-48 overflow-hidden rounded-t-lg">
      <img 
        :src="backgroundUrl" 
        class="w-full h-full object-cover"
        @error="handleBackgroundError"
      >
      <div class="absolute top-4 right-4">
        <button
          @click="triggerBackgroundUpload"
          class="flex items-center px-3 py-1.5 text-sm font-medium text-gray-700 bg-white bg-opacity-90 rounded-lg hover:bg-opacity-100 transition-all shadow-sm"
        >
          <svg 
            class="w-4 h-4 mr-1.5 text-gray-600" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              stroke-linecap="round" 
              stroke-linejoin="round" 
              stroke-width="2" 
              d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
            />
          </svg>
          更换背景
        </button>
      </div>
      <input
        ref="backgroundInput"
        type="file"
        accept="image/*"
        class="hidden"
        @change="handleBackgroundChange"
      >
    </div>

    <!-- 个人信息卡片 -->
    <div class="relative px-6 pb-6">
      <!-- 头像部分 - 上移到背景图上 -->
      <div class="absolute -top-16 left-6">
        <div class="relative group">
          <img 
            :src="userAvatar" 
            class="w-32 h-32 rounded-full object-cover border-4 border-white shadow-lg"
            alt="用户头像"
            @error="handleImageError"
          />
          <div 
            @click="triggerUpload"
            class="absolute inset-0 flex items-center justify-center rounded-full bg-black bg-opacity-40 opacity-0 group-hover:opacity-100 cursor-pointer transition-opacity duration-200"
          >
            <CameraIcon class="w-8 h-8 text-white" />
          </div>
          <!-- 性别标识 -->
          <div class="absolute bottom-0 right-0 bg-white rounded-full p-2 shadow">
            <!-- 男性图标 -->
            <svg 
              v-if="currentGender === 'male'" 
              class="w-6 h-6 text-blue-500" 
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
              class="w-6 h-6 text-pink-500" 
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
      </div>

      <!-- 基本信息部分 -->
      <div class="pt-20">
        <!-- 名字和编辑按钮 -->
        <div class="flex items-center justify-between mb-4">
          <h1 class="text-2xl font-bold text-gray-900">{{ formatBasicInfo.name }}</h1>
          <button
            @click="handleEdit"
            class="p-2 rounded-full hover:bg-gray-100 transition-colors"
          >
            <PencilSquareIcon class="w-5 h-5 text-gray-500" />
          </button>
        </div>

        <!-- 个人简介 -->
        <p class="text-gray-600 mb-6">{{ formatBasicInfo.personal_summary || '这个人很懒，还没有填写个人简介' }}</p>

        <!-- 信息网格 -->
        <div class="grid grid-cols-2 gap-6 mb-6">
          <!-- 联系方式 -->
          <div class="space-y-3">
            <h2 class="text-sm font-semibold text-gray-900 mb-2">联系方式</h2>
            <div class="flex items-center space-x-2">
              <PhoneIcon class="w-5 h-5 text-gray-400" />
              <span class="text-gray-600">{{ formatBasicInfo.phone }}</span>
            </div>
            <div class="flex items-center space-x-2">
              <EnvelopeIcon class="w-5 h-5 text-gray-400" />
              <span class="text-gray-600">{{ formatBasicInfo.email }}</span>
            </div>
          </div>

          <!-- 基本资料 -->
          <div class="space-y-3">
            <h2 class="text-sm font-semibold text-gray-900 mb-2">基本资料</h2>
            <div class="flex items-center space-x-2">
              <MapPinIcon class="w-5 h-5 text-gray-400" />
              <span class="text-gray-600">{{ formatBasicInfo.location }}</span>
            </div>
            <div class="flex items-center space-x-2">
              <CakeIcon class="w-5 h-5 text-gray-400" />
              <span class="text-gray-600">{{ formatBasicInfo.age }}</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>

  <!-- 添加头像上传弹窗 -->
  <AvatarUploadDialog
    v-model="showAvatarUpload"
    :loading="loading"
    @upload="handleAvatarUpload"
  />
</template>

<script setup>
import { ref, computed, nextTick, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import defaultAvatarImage from '@/assets/images/default-avatar.png'
import defaultBackground from '@/assets/images/default-background.jpg'
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
import AvatarUploadDialog from '../dialogs/AvatarUploadDialog.vue'

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

onMounted(async () => {
  try {
    await store.dispatch('fetchCompleteness')
  } catch (error) {
    console.error('Failed to fetch completeness:', error)
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
    
    const response = await profile.uploadAvatar(formData)
    if (response.data?.code === 200) {
      showToast('头像上传成功', 'success')
      emit('update')
      const avatarUrl = response.data.data.avatar
      eventBus.emit('avatar-updated', avatarUrl)
      if (props.resumeData) {
        props.resumeData.avatar = avatarUrl
      }
      showAvatarUpload.value = false // 关闭弹窗
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
  showAvatarUpload.value = true
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
  const maxSize = 20 * 1024 * 1024 // 2MB
  if (file.size > maxSize) {
    showToast('图片大小不能超过 2MB', 'error')
    return false
  }

  return true
}

// 背景图相关
const backgroundInput = ref(null)
const backgroundUrl = computed(() => {
  const background = store.state.userInfo?.data?.basic_info?.background
  if (!background) return defaultBackground
  return background.startsWith('http') ? background : `${MEDIA_URL}${background}`
})

const triggerBackgroundUpload = () => {
  backgroundInput.value.click()
}

const handleBackgroundChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  if (!validateFile(file)) {
    return
  }
  
  const formData = new FormData()
  formData.append('background', file)
  
  try {
    loading.value = true
    const response = await profile.uploadBackground(formData)
    if (response.data?.code === 200) {
      showToast('背景图更新成功', 'success')
      emit('update')  // 通知父组件更新
      const backgroundUrl = response.data.data.background
      // 更新本地数据
      if (props.resumeData && props.resumeData.basic_info) {
        props.resumeData.basic_info.background = backgroundUrl
      }
      // 更新 store
      store.commit('UPDATE_BACKGROUND', backgroundUrl)
    }
  } catch (error) {
    console.error('Failed to update background:', error)
    showToast('背景图更新失败', 'error')
  } finally {
    loading.value = false
    event.target.value = ''
  }
}

const handleBackgroundError = (e) => {
  e.target.src = defaultBackground
}

// 添加状态
const showAvatarUpload = ref(false)
</script>