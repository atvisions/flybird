<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部背景和用户信息 -->
    <div class="relative">
      <!-- 背景图 -->
      <div class="h-48 bg-gradient-to-r from-gray-900 to-gray-800 relative">
        <div class="absolute inset-0">
          <img
            :src="backgroundUrl"
            class="w-full h-full object-cover opacity-70"
            alt="背景图"
            @error="handleBackgroundError"
          />
          <!-- 调整渐变遮罩 -->
          <div class="absolute inset-0 bg-gradient-to-b from-transparent via-black/10 to-black/30"></div>
        </div>
      </div>

      <!-- 用户信息卡片 -->
      <div class="relative -mt-10 mx-4">
        <div class="bg-white rounded-lg shadow-sm p-4">
          <!-- 头像和用户信息容器 - 改为水平布局 -->
          <div class="flex items-start -mt-20">
            <!-- 头像区域 -->
            <div class="relative flex-shrink-0">
              <img 
                :src="userInfo.avatar_url" 
                class="w-24 h-24 rounded-full border-4 border-white object-cover shadow-sm"
                alt="头像"
                @error="handleImageError"
              />
              <div v-if="isVip" class="absolute -top-1 -right-1 w-6 h-6 bg-[#FFB800] rounded-full flex items-center justify-center border-2 border-white">
                <span class="text-[11px] font-bold text-white">V</span>
              </div>
            </div>

            <!-- 用户信息 - 左对齐 -->
            <div class="ml-4 flex-1 mt-14">
              <div class="flex items-center justify-between">
                <h2 class="text-lg font-bold text-gray-900">{{ userInfo.name }}</h2>
                <button 
                  @click="handleEdit"
                  class="px-3 py-1 text-xs text-gray-600 border border-gray-200 rounded-full hover:bg-gray-50"
                >
                  编辑资料
                </button>
              </div>
              <div class="text-sm text-gray-600 mt-1">
                {{ userInfo.title || userInfo.position || '未设置职位' }}
                <span v-if="userInfo.company" class="ml-1">@ {{ userInfo.company }}</span>
              </div>
              <p class="text-sm text-gray-500 mt-2">
                {{ userInfo.bio || '这个人还没有填写个人简介' }}
              </p>
            </div>
          </div>

          <!-- 统计数据 -->
          <div class="grid grid-cols-4 gap-4 mt-6 pt-4 border-t border-gray-100 w-full">
            <div v-for="stat in statistics" :key="stat.label" class="text-center">
              <div class="text-base font-medium text-gray-900">{{ stat.value }}</div>
              <div class="text-xs text-gray-500">{{ stat.label }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 功能菜单 -->
    <div class="mt-3 bg-white">
      <!-- 我的 -->
      <div class="px-4 py-3 text-sm text-gray-500">我的</div>
      <div class="grid grid-cols-4 px-4 py-4 gap-4">
        <router-link v-for="item in myMenuItems" :key="item.key"
          :to="item.path"
          class="flex flex-col items-center"
        >
          <div :class="['w-12 h-12 rounded-xl flex items-center justify-center mb-1', item.bgColor]">
            <component :is="item.icon" class="w-5 h-5" :class="item.iconColor" />
          </div>
          <span class="text-xs text-gray-600">{{ item.label }}</span>
          <span v-if="item.count" class="text-xs text-blue-600 mt-0.5">{{ item.count }}</span>
        </router-link>
      </div>

      <!-- 设置 -->
      <div class="mt-3">
        <div class="px-4 py-3 text-sm text-gray-500">设置</div>
        <div class="divide-y divide-gray-100">
          <router-link v-for="item in settingItems" :key="item.key"
            :to="item.path"
            class="flex items-center px-4 py-3 hover:bg-gray-50"
          >
            <component :is="item.icon" class="w-5 h-5 text-gray-400" />
            <span class="ml-3 text-sm text-gray-900">{{ item.label }}</span>
            <ChevronRightIcon class="w-5 h-5 text-gray-400 ml-auto" />
          </router-link>
        </div>
      </div>
    </div>

    <!-- 移动端底部导航 -->
    <MobileTabBar
      :current-tab="currentTab"
      :actions="mobileActions"
      @tab-change="handleTabChange"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAccountStore } from '@/stores/account'
import MobileTabBar from '@/components/MobileTabBar.vue'
import {
  BriefcaseIcon,
  UserGroupIcon,
  DocumentTextIcon,
  BuildingOfficeIcon,
  GlobeAltIcon,
  BellIcon,
  Cog6ToothIcon,
  ChevronRightIcon,
  UserIcon,
  Squares2X2Icon,
} from '@heroicons/vue/24/outline'
import profile from '@/api/profile'

// 移除本地图片导入
// 使用在线默认图片
const DEFAULT_BG_IMAGE = 'https://images.unsplash.com/photo-1557683316-973673baf926?w=1600&h=400&fit=crop'
const DEFAULT_AVATAR_IMAGE = 'https://api.dicebear.com/7.x/avataaars/svg'

const router = useRouter()
const route = useRoute()
const accountStore = useAccountStore()

const userInfo = computed(() => accountStore.userInfo || {})

const isVip = computed(() => userInfo.value?.is_vip)

// 当前选中的标签
const currentTab = ref(route.query.tab || 'home')

// 处理标签切换
const handleTabChange = (key) => {
  currentTab.value = key
  router.push({ query: { ...route.query, tab: key }})
}

// 移动端底部导航按钮
const mobileActions = [
  {
    key: 'home',
    label: '用户中心',
    icon: Squares2X2Icon,
  },
  {
    key: 'profile',
    label: '档案',
    icon: UserIcon,
  },
  {
    key: 'resumes',
    label: '简历',
    icon: DocumentTextIcon,
  },
  {
    key: 'messages',
    label: '消息',
    icon: BellIcon,
    badge: 3 // 未读消息数
  },
  {
    key: 'account',
    label: '设置',
    icon: Cog6ToothIcon,
  }
]

// 我的菜单项
const myMenuItems = [
  {
    key: 'work',
    label: '工作',
    path: '/user/work',
    icon: BriefcaseIcon,
    bgColor: 'bg-blue-50',
    iconColor: 'text-blue-600'
  },
  {
    key: 'contacts',
    label: '联络人',
    path: '/user/contacts',
    icon: UserGroupIcon,
    bgColor: 'bg-purple-50',
    iconColor: 'text-purple-600'
  },
  {
    key: 'resume',
    label: '简历',
    path: '/user/resumes',
    icon: DocumentTextIcon,
    bgColor: 'bg-green-50',
    iconColor: 'text-green-600',
    count: '1'
  },
  {
    key: 'companies',
    label: '追踪的公司',
    path: '/user/companies',
    icon: BuildingOfficeIcon,
    bgColor: 'bg-orange-50',
    iconColor: 'text-orange-600',
    count: '0'
  }
]

// 设置菜单项
const settingItems = [
  {
    key: 'language',
    label: '语言',
    path: '/user/language',
    icon: GlobeAltIcon
  },
  {
    key: 'notification',
    label: '通知设定',
    path: '/user/notifications',
    icon: BellIcon
  },
  {
    key: 'account',
    label: '账号设定',
    path: '/user/settings',
    icon: Cog6ToothIcon
  }
]

// 用户统计数据
const statistics = ref([
  { label: '作品', value: '0' },
  { label: '文章', value: '0' },
  { label: '收藏', value: '0' },
  { label: '关注', value: '0' }
])

// 获取用户统计数据
const fetchUserStatistics = async () => {
  try {
    const { data } = await profile.getStatistics()
    if (data) {
      statistics.value = [
        { label: '作品', value: data.portfolios_count || '0' },
        { label: '文章', value: data.articles_count || '0' },
        { label: '收藏', value: data.favorites_count || '0' },
        { label: '关注', value: data.followings_count || '0' }
      ]
    }
  } catch (error) {
    console.error('Failed to fetch user statistics:', error)
  }
}

// 在组件挂载时获取数据
onMounted(async () => {
  await fetchUserStatistics()
})

// 监听用户信息变化，重新获取统计数据
watch(() => userInfo.value?.id, async (newVal) => {
  if (newVal) {
    await fetchUserStatistics()
  }
})

// 处理图片加载错误
const handleBackgroundError = (e) => {
  e.target.src = DEFAULT_BG_IMAGE
}

const handleImageError = (e) => {
  e.target.src = DEFAULT_AVATAR_IMAGE
}

// 处理编辑按钮点击
const handleEdit = () => {
  router.push('/user/profile')
}
</script>

<style scoped>
.min-h-screen {
  padding-bottom: 60px;
}

/* 添加图片加载过渡效果 */
img {
  transition: opacity 0.3s ease;
}

img[src=""] {
  opacity: 0;
}

/* 确保内容不会被顶部背景遮挡 */
.relative {
  z-index: 1;
}
</style> 