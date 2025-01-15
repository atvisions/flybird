import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useAccountStore } from '@/stores/account'
import { getPointsInfo, getSignInStatus } from '@/api/membership'
import {
  DocumentTextIcon,
  DocumentIcon,
  UserIcon,
  Cog6ToothIcon,
  ArrowRightOnRectangleIcon,
  BellIcon,
  HeartIcon,
  ShieldCheckIcon,
  UserCircleIcon,
  WrenchScrewdriverIcon,
  MagnifyingGlassIcon,
  PhotoIcon,
  UserGroupIcon,
  XMarkIcon,
  Squares2X2Icon,
  SparklesIcon,
  StarIcon,
  ChevronRightIcon,
  ChevronDownIcon,
  IdentificationIcon
} from '@heroicons/vue/24/outline'

// 初始化 store
const authStore = useAuthStore()
const accountStore = useAccountStore()

// 声明所有响应式变量
const pointsInfo = ref({
  balance: 0,
  level: 1,
  sign_in_days: 0,
  total_earned: 0,
  signed_today: false
})

const signInInfo = ref({
  can_sign_in: false,
  sign_in_days: 0,
  next_reward: null
})

// 获取积分信息的方法
const fetchPointsInfo = async () => {
  if (!authStore.isAuthenticated) return
  
  try {
    const response = await getPointsInfo()
    if (response?.data?.code === 200) {
      pointsInfo.value = response.data.data
      // 更新签到状态
      await fetchSignInStatus()
    }
  } catch (error) {
    console.error('获取积分信息失败:', error)
  }
}

// 获取签到状态的方法
const fetchSignInStatus = async () => {
  if (!authStore.isAuthenticated) return
  
  try {
    const response = await getSignInStatus()
    if (response?.data?.code === 200) {
      signInInfo.value = response.data.data
    }
  } catch (error) {
    console.error('获取签到状态失败:', error)
  }
}

// 监听登录状态
watch(() => authStore.isAuthenticated, async (newValue) => {
  if (newValue) {
    // 用户已登录，获取积分信息
    await fetchPointsInfo()
  } else {
    // 用户未登录，重置积分信息
    pointsInfo.value = {
      balance: 0,
      level: 1,
      sign_in_days: 0,
      total_earned: 0,
      signed_today: false
    }
    signInInfo.value = {
      can_sign_in: false,
      sign_in_days: 0,
      next_reward: null
    }
  }
}, { immediate: true })

// 添加图标映射函数
const getIcon = (menuKey) => {
  const iconMap = {  
    'home': Squares2X2Icon,
    'profile': UserIcon,
    'resumes': DocumentIcon,
    'document': DocumentTextIcon,
    'users': UserGroupIcon,
    'photo': PhotoIcon,
    'favorites': HeartIcon,
    'notifications': BellIcon,
    'settings': Cog6ToothIcon,
    'security': ShieldCheckIcon,
    'account': WrenchScrewdriverIcon,
    'logout': ArrowRightOnRectangleIcon,
    'crown': SparklesIcon,
    'identification': IdentificationIcon
  }
  return iconMap[menuKey] || UserIcon // 默认返回 UserIcon
}

// 搜索类型配置
const searchTypes = [
  {
    key: 'articles',
    label: '文章',
    path: '/search/articles',
    icon: DocumentTextIcon
  },
  {
    key: 'portfolios',
    label: '作品集',
    path: '/search/portfolios',
    icon: PhotoIcon
  },
  {
    key: 'users',
    label: '用户',
    path: '/search/users',
    icon: UserIcon
  }
]

// ... 其他代码 ... 