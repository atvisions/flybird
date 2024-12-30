<template>
    <div class="user-center">
      <HeadView />
      <div class="min-h-screen bg-gray-50 pt-20 pb-20 lg:pb-0">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 mt-4 lg:mt-0">
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8">
            <!-- 左侧导航 - 仅桌面端显示 -->
            <div class="hidden lg:block lg:col-span-3">
              <div class="bg-white rounded-lg shadow overflow-hidden sticky top-20">
                <nav class="space-y-1">
                    <button
                        v-for="tab in tabs"
                        :key="tab.key"
                        @click="handleTabChange(tab.key)" 
                        class="w-full flex items-center px-4 py-3 text-sm font-medium group"
                        :class="[
                        currentTab === tab.key
                            ? 'bg-gray-100 text-indigo-600'
                            : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                        ]"
                    >
                    <div class="flex items-center flex-1 min-w-0">
                      <svg
                        :class="[
                          currentTab === tab.key ? 'text-indigo-600' : 'text-gray-400 group-hover:text-gray-500',
                          'h-5 w-5 flex-shrink-0'
                        ]"
                        aria-hidden="true"
                        :viewBox="tab.icon.viewBox"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="1.5"
                      >
                        <path :d="tab.icon.path" />
                      </svg>
                      <span class="ml-2 truncate">{{ tab.name }}</span>
                    </div>
                    <span 
                      v-if="getTabMetric(tab.key)"
                      :class="[
                        currentTab === tab.key ? 'bg-indigo-100 text-indigo-600' : 'bg-gray-100 text-gray-900',
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
            <div class="lg:col-span-6">
              <component :is="currentComponent" />
            </div>
  
            <!-- 右侧广告位 - 仅桌面端显示 -->
            <div class="hidden lg:block lg:col-span-3">
              <div class="bg-white rounded-lg shadow p-4 sticky top-20">
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
  
        <!-- 移动端底部导航栏 -->
        <div class="fixed bottom-0 left-0 right-0 bg-white border-t lg:hidden">
          <nav class="grid grid-cols-4 gap-1">
            <button
              v-for="tab in tabs"
              :key="tab.key"
              @click="currentTab = tab.key"
              class="flex flex-col items-center py-2 px-4"
              :class="currentTab === tab.key ? 'text-indigo-600' : 'text-gray-600'"
            >
              <svg
                class="h-6 w-6 mb-1"
                :class="currentTab === tab.key ? 'text-indigo-600' : 'text-gray-400'"
                aria-hidden="true"
                :viewBox="tab.icon.viewBox"
                fill="none"
                stroke="currentColor"
                stroke-width="1.5"
              >
                <path :d="tab.icon.path" />
              </svg>
              <span class="text-xs truncate max-w-[80px]">{{ tab.name }}</span>
            </button>
          </nav>
        </div>
      </div>
      <FootView />
    </div>
  </template>
<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { profile } from '@/api/profile'
import HeadView from '../../components/HeadView.vue'
import FootView from '../../components/FootView.vue'
import MyProfile from './MyProfile/index.vue'
import MyResumes from './MyResumes.vue'
import MyPortfolio from './MyPortfolio.vue'
import AccountSettings from './AccountSettings.vue'

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
  currentTab.value = key
}
 // 导航标签
 const tabs = [
   { 
     key: 'profile', 
     name: '个人档案',
     icon: {
       viewBox: "0 0 24 24",
       path: "M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"
     }
   },
   { 
     key: 'resumes', 
     name: '我的简历',
     icon: {
       viewBox: "0 0 24 24",
       path: "M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z"
     }
   },
   { 
     key: 'portfolio', 
     name: '作品集',
     icon: {
       viewBox: "0 0 24 24",
       path: "M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"
     }
   },
   { 
     key: 'account', 
     name: '账户设置',
     icon: {
       viewBox: "0 0 24 24",
       path: "M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z"
     }
   }
 ]

 // 动态组件
 const currentComponent = computed(() => {
  switch (currentTab.value) {
    case 'profile':
      return MyProfile
    case 'resumes':
      return MyResumes
    case 'portfolio':
      return MyPortfolio
    case 'account':
      return AccountSettings
    default:
      return MyProfile
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
     case 'portfolio':
       return '3'
     default:
       return ''
   }
 }

 // 在组件挂载时获取数据
 onMounted(async () => {
   await fetchCompleteness()
 })

 // 监听路由变化，在进入个人资料页时刷新数据
 watch(() => route.path, async (newPath) => {
   if (newPath.includes('/user/profile')) {
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
 </script>
 
 <style scoped>
 /* 确保移动端底部导航不会遮挡内容 */
 @media (max-width: 1024px) {
   .user-center {
     padding-bottom: env(safe-area-inset-bottom);
   }
 }
 </style>