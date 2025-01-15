<template>
  <div class="min-h-screen flex flex-col">
    <HeadView />
    <!-- 主要内容区域 -->
    <main class="flex-1 flex flex-col">
      <div class="flex-1 py-4 lg:py-6 mt-[60px] md:mt-[72px] md:overflow-visible overflow-x-hidden">
        <div class="mx-auto max-w-7xl px-2 sm:px-4 lg:px-8 mt-4 lg:mt-0 relative">
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8">
            <!-- 左侧导航 - 仅桌面端显示 -->
            <div class="hidden lg:block lg:col-span-3">
              <div class="bg-white rounded-lg shadow overflow-hidden sticky top-24">
                <nav class="space-y-1">
                  <button
                      v-for="tab in tabs"
                      :key="tab.key"
                      @click="handleTabChange(tab.key)" 
                      class="w-full flex items-center px-4 py-3 text-sm font-medium group"
                      :class="[
                      currentTab === tab.key
                          ? 'bg-gray-100 text-[#1A56DB]'
                          : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                      ]"
                  >
                  <div class="flex items-center flex-1 min-w-0">
                    <component
                      :is="getTabIcon(tab)"
                      :class="[
                        currentTab === tab.key ? 'text-[#1A56DB]' : 'text-gray-400 group-hover:text-gray-500',
                        'h-5 w-5 flex-shrink-0'
                      ]"
                    />
                    <span class="ml-2 truncate">{{ tab.name }}</span>
                  </div>
                  <span 
                    v-if="getTabMetric(tab.key)"
                    :class="[
                      currentTab === tab.key ? 'bg-blue-100 text-[#1A56DB]' : 'bg-gray-100 text-gray-900',
                      'ml-3 inline-block py-0.5 px-2 text-xs rounded-full'
                    ]"
                  >
                    {{ getTabMetric(tab.key) }}
                  </span>
                </button>
              </nav>
              </div>
            </div>
  
            <!-- 中间内容区 -->
            <div class="lg:col-span-6 pb-20 lg:pb-0 w-full space-y-4">
              <component :is="currentComponent" />
            </div>
  
            <!-- 右侧广告位 - 仅桌面端显示 -->
            <div class="hidden lg:block lg:col-span-3">
              <div class="bg-white rounded-lg shadow p-4 sticky top-24">
                <h3 class="text-lg font-medium text-gray-900 mb-4">推荐职位</h3>
                <div class="space-y-4">
                  <div v-for="job in recommendedJobs" :key="job.id" class="flex space-x-3">
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-medium text-gray-900 truncate">{{ job.title }}</p>
                      <p class="text-sm text-gray-500">{{ job.company }}</p>
                    </div>
                    <div class="flex-shrink-0">
                      <span class="text-sm font-medium text-indigo-600">{{ job.salary }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- 移动端底部导航 -->
        <Transition name="fade">
          <MobileTabBar
            v-if="showMobileTabBar"
            class="md:hidden"
            :current-tab="currentTab"
            :actions="mobileActions"
            :menuGroups="profileMenuGroups"
            @tab-change="handleTabChange"
          />
        </Transition>
      </div>
    </main>

    <!-- 仅在桌面端显示页脚 -->
    <FootView class="hidden lg:block" />
  </div>
</template>
<script setup>
import { ref, computed, watch, onMounted, onUnmounted, defineAsyncComponent, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import profile from '@/api/profile'
import HeadView from '../../components/HeadView.vue'
import FootView from '../../components/FootView.vue'
import {
UserIcon,
DocumentIcon,
Cog6ToothIcon,
Squares2X2Icon,
BellIcon,
Bars3Icon,
SparklesIcon,
} from '@heroicons/vue/24/outline'
import {
UserIcon as UserIconSolid,
DocumentIcon as DocumentIconSolid,
Cog6ToothIcon as Cog6ToothIconSolid,
Squares2X2Icon as Squares2X2IconSolid,
BellIcon as BellIconSolid,
} from '@heroicons/vue/24/solid'
import MobileTabBar from '@/components/MobileTabBar.vue'

// 创建加载组件
const LoadingComponent = {
name: 'LoadingComponent',
template: `
  <div class="p-4 text-center">
    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
    <p class="mt-2 text-gray-600">加载中...</p>
  </div>
`
}

// 异步组件
const MyProfile = defineAsyncComponent({
loader: () => import('@/views/user/MyProfile/index.vue'),
loadingComponent: LoadingComponent,
timeout: 10000,  // 10秒超时
delay: 0,        // 立即显示加载组件
suspensible: false  // 禁用 suspense
})

const MyResumes = defineAsyncComponent({
loader: () => import('@/views/user/MyResumes.vue'),
loadingComponent: LoadingComponent,
timeout: 10000
})


const AccountSettings = defineAsyncComponent({
loader: () => import('@/views/user/AccountSettings.vue'),
loadingComponent: LoadingComponent,
timeout: 10000
})


const UserHome = defineAsyncComponent({
loader: () => import('@/views/user/MyProfile/components/UserHome.vue'),
loadingComponent: LoadingComponent,
timeout: 10000,
delay: 0,
suspensible: false
})

const MyMessages = defineAsyncComponent({
loader: () => import('@/views/user/MyProfile/components/MyMessages.vue'),
loadingComponent: LoadingComponent,
timeout: 10000
})

// 导入会员中心组件
const Membership = defineAsyncComponent({
loader: () => import('@/views/user/Membership/index.vue'),
loadingComponent: LoadingComponent,
timeout: 10000
})

const route = useRoute()
const router = useRouter()

// 统一的 currentTab 声明，使用 URL 参数或 localStorage
const currentTab = ref(route.query.tab || localStorage.getItem('userCenterTab') || 'profile')

// 监听标签变化
watch(currentTab, (newTab) => {
// 更新 localStorage
localStorage.setItem('userCenterTab', newTab)
// 更新 URL 参数
router.replace({
  query: { ...route.query, tab: newTab }
})
})

// 监听 URL 参数变化
watch(
() => route.query.tab,
(newTab) => {
  if (newTab && newTab !== currentTab.value) {
    currentTab.value = newTab
  }
}
)

// 处理标签切换
const handleTabChange = (key) => {
if (showMobileTabBar.value) {
  currentTab.value = key
}
}

// 将原有的tabs拆分为主要和次要标签
const tabs = [
{ 
  key: 'home', 
  name: '用户中心',
  icon: Squares2X2Icon
},
{ 
  key: 'profile', 
  name: '我的档案',
  icon: UserIcon
},
{ 
  key: 'resumes', 
  name: '我的简历',
  icon: DocumentIcon
},
{ 
  key: 'membership', 
  name: '会员中心',
  icon: SparklesIcon
},
{ 
  key: 'messages', 
  name: '系统消息',
  icon: BellIcon
},
{ 
  key: 'account', 
  name: '账户设置',
  icon: Cog6ToothIcon
}
]

// 模拟数据
const portfolioCount = ref(4) // 假设有4个作品
const creationsCount = ref(5) // 假设有5个创作
const favoritesCount = ref(10) // 假设有10个收藏
const unreadMessagesCount = ref(3) // 假设有3条未读消息

const messageBadge = computed(() => unreadMessagesCount.value)

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
  icon: DocumentIcon,
},
{
  key: 'messages',
  label: '消息',
  icon: BellIcon,
  badge: unreadMessagesCount
},
{
  key: 'account',
  label: '设置',
  icon: Cog6ToothIcon,
}
]

// 移动端菜单状态
const isMobileMenuOpen = ref(false)

// 处理移动端标签切换
const handleMobileTabChange = (key) => {
currentTab.value = key
isMobileMenuOpen.value = false
}

// 动态组件
const currentComponent = computed(() => {
switch (currentTab.value) {
  case 'home':
    return UserHome
  case 'membership':
    return Membership
  case 'profile':
    return MyProfile
  case 'resumes':
    return MyResumes
  case 'messages':
    return MyMessages
  case 'account':
    return AccountSettings
  default:
    return UserHome
}
})

// 从 store 或者 API 获取完整度数据
const completionData = ref({
total_score: 0
})

// 获取完整度数据
const fetchCompleteness = async () => {
try {
  const response = await profile.getCompleteness()
  if (response.data?.code === 200 && response.data?.data) {
    completionData.value = response.data.data
  }
} catch (error) {
  console.error('获取简历完整度失败:', error)
}
}

// 获取标签指标
const getTabMetric = (key) => {
switch (key) {
  case 'profile':
    const score = Math.round(completionData.value.total_score || 0)
    return score + '分'
  case 'resumes':
    return '2'
  case 'creations':
    return creationsCount.value
  case 'portfolio':
    return portfolioCount.value
  case 'favorites':
    return favoritesCount.value
  case 'messages':
    return unreadMessagesCount.value || 0
  default:
    return ''
}
}

// 修改状态管理
const showMobileTabBar = ref(false)

// 修改生命周期钩子
onMounted(() => {
// 延迟显示 MobileTabBar，确保 DOM 完全加载
nextTick(() => {
  showMobileTabBar.value = true
})
window.addEventListener('resize', handleResize)
fetchCompleteness()
})

onUnmounted(() => {
showMobileTabBar.value = false
window.removeEventListener('resize', handleResize)
})

// 修改 handleResize
const handleResize = () => {
if (showMobileTabBar.value) {
  window.dispatchEvent(new Event('resize'))
}
}

// 监听路由变化，在进入个人资料页时刷新数据
watch(() => route.path, async (newPath) => {
if (showMobileTabBar.value && newPath.includes('/user/profile')) {
  await fetchCompleteness()
}
})

// 推荐职位数据
const recommendedJobs = [
{
  id: 1,
  title: '高级前端工程师',
  company: '字节跳动',
  salary: '25-35K'
},
{
  id: 2,
  title: '资深产品经理',
  company: '腾讯',
  salary: '30-45K'
},
{
  id: 3,
  title: 'UI设计师',
  company: '阿里巴巴',
  salary: '20-30K'
}
]

// 判断标签是否激活
const isActiveTab = (key) => {
if (key === 'more') {
  return false // "更多"按钮永远不会处于激活状态
}
return currentTab.value === key
}

// 定义菜单组
const menuGroups = ref([
{
  title: '内容管理',
  items: [
    {
      label: '作品集',
      icon: 'portfolio',
      route: '/user/center?tab=portfolio'
    },
    {
      label: '文章',
      icon: 'article',
      route: '/user/center?tab=articles'
    },
    {
      label: '话题',
      icon: 'topic',
      route: '/user/center?tab=topics'
    },
    {
      label: '问答',
      icon: 'qa',
      route: '/user/center?tab=qa'
    }
  ]
},
{
  title: '互动管理',
  items: [
    {
      label: '评论',
      icon: 'comment',
      route: '/user/center?tab=comments'
    },
    {
      label: '收藏',
      icon: 'favorite',
      route: '/user/center?tab=favorites'
    },
    {
      label: '关注',
      icon: 'follow',
      route: '/user/center?tab=following'
    }
  ]
}
])

// 获取当前标签对应的图标
const getTabIcon = (tab) => {
if (currentTab.value === tab.key) {
  // 选中状态使用实心图标
  switch (tab.key) {
    case 'home':
      return Squares2X2IconSolid
    case 'profile':
      return UserIconSolid
    case 'resumes':
      return DocumentIconSolid
    case 'messages':
      return BellIconSolid
    case 'account':
      return Cog6ToothIconSolid
    default:
      return tab.icon
  }
}
// 未选中状态使用描边图标
return tab.icon
}

// 添加移动端视图判断
const isMobileView = computed(() => {
return window.innerWidth < 768
})

// 添加 profileMenuGroups 数据
const profileMenuGroups = [
{
  title: '内容管理',
  items: [
    { key: 'home', label: '用户中心', icon: Squares2X2Icon },
    { key: 'profile', label: '我的档案', icon: UserIcon },
    { key: 'resumes', label: '我的简历', icon: DocumentIcon }
  ]
},
{
  title: '账号管理',
  items: [
    { key: 'messages', label: '消息', icon: BellIcon },
    { key: 'account', label: '设置', icon: Cog6ToothIcon }
  ]
}
]
</script>

<style scoped>
/* 确保内容区域占满剩余空间 */
main {
 min-height: calc(100vh - 60px);
}

.footer-container {
 margin-top: auto;
}

/* 添加过渡动画样式 */
.fade-enter-active,
.fade-leave-active {
 transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
 opacity: 0;
}
</style>