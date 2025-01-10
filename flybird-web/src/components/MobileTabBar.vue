<template>
  <div class="fixed bottom-0 left-0 right-0 bg-white border-t lg:hidden safe-area-inset-bottom z-50">
    <div class="grid grid-cols-5 gap-1">
      <button
        v-for="action in mobileActions"
        :key="action.key"
        @click="action.handler"
        class="flex flex-col items-center py-2 px-1 relative"
        :class="[
          isActiveAction(action.key)
            ? 'text-blue-600'
            : 'text-gray-500'
        ]"
      >
        <component 
          :is="action.icon" 
          class="w-6 h-6"
          :class="isActiveAction(action.key) ? 'text-blue-600' : 'text-gray-500'"
        />
        <span class="text-xs mt-1 truncate">{{ action.label }}</span>
        <span 
          v-if="action.badge" 
          class="absolute -top-1 right-1/4 bg-red-500 text-white text-xs rounded-full w-4 h-4 flex items-center justify-center"
        >
          {{ action.badge }}
        </span>
      </button>
    </div>
  </div>

  <!-- 移动端更多菜单抽屉的遮罩层 -->
  <div 
    v-if="isMobileMenuOpen" 
    class="fixed inset-0 bg-black bg-opacity-25 z-[60] lg:hidden"
    @click="closeMenu"
  />
  
  <!-- 移动端更多菜单抽屉 -->
  <div 
    :class="[
      'fixed inset-y-0 left-0 w-64 bg-white shadow-xl z-[70] transform transition-transform duration-300 ease-in-out lg:hidden',
      isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'
    ]"
  >
    <div class="h-full flex flex-col">
      <div class="p-4 border-b border-gray-200">
        <div class="flex items-center justify-between">
          <h2 class="text-lg font-medium text-gray-900">更多功能</h2>
          <button 
            @click="closeMenu"
            class="text-gray-500"
          >
            <XMarkIcon class="w-6 h-6" />
          </button>
        </div>
      </div>
      
      <div class="flex-1 overflow-y-auto">
        <div class="px-3 py-4">
          <div v-for="group in currentMenuGroups" :key="group.title" class="mb-6">
            <h3 class="px-3 text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
              {{ group.title }}
            </h3>
            <div class="space-y-1">
              <router-link
                v-for="item in group.items"
                :key="item.path"
                :to="item.path"
                class="group flex items-center w-full px-3 py-2 text-sm font-medium rounded-md"
                :class="[
                  route.path === item.path
                    ? 'bg-blue-50 text-blue-600'
                    : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                ]"
                @click="closeMenu"
              >
                <component
                  :is="item.icon"
                  class="mr-3 h-6 w-6"
                  :class="route.path === item.path ? 'text-blue-600' : 'text-gray-400'"
                />
                {{ item.name }}
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  Bars3Icon,
  XMarkIcon,
  UsersIcon,
  UserCircleIcon,
  PhotoIcon,
  Cog6ToothIcon,
  DocumentTextIcon,
  QuestionMarkCircleIcon,
  ScaleIcon,
  PaintBrushIcon,
  VideoCameraIcon,
  CameraIcon,
  FilmIcon,
  DocumentIcon,
  StarIcon,
  GlobeAltIcon,
  UserIcon,
  HomeIcon,
  EnvelopeIcon,
  ShieldCheckIcon,
  BriefcaseIcon,
  AcademicCapIcon,
  BookOpenIcon,
  LanguageIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  menuGroups: {
    type: Array,
    required: true,
    default: () => []
  },
  unreadMessages: {
    type: Number,
    default: 0
  }
})

const route = useRoute()
const router = useRouter()
const isMobileMenuOpen = ref(false)

// 底部导航按钮
const mobileActions = [
  {
    key: 'more',
    label: '分类',
    icon: Bars3Icon,
    handler: () => { 
      isMobileMenuOpen.value = true 
    }
  },
  {
    key: 'templates',
    label: '模版',
    icon: DocumentTextIcon,
    handler: () => router.push('/templates')
  },
  {
    key: 'community',
    label: '社区',
    icon: UsersIcon,
    handler: () => router.push('/community')
  },
  {
    key: 'portfolio',
    label: '作品集',
    icon: PhotoIcon,
    handler: () => router.push('/portfolio')
  },
  {
    key: 'profile',
    label: '我的',
    icon: UserCircleIcon,
    handler: () => router.push('/user?tab=home')
  }
]

const isActiveAction = (key) => {
  if (key === 'more') return false
  if (key === 'templates') return route.path.startsWith('/templates')
  if (key === 'community') return route.path.startsWith('/community')
  if (key === 'portfolio') return route.path.startsWith('/portfolio')
  if (key === 'profile') {
    return route.path.includes('/user') && 
           !['account', 'privacy'].includes(route.query.tab || '')
  }
  if (key === 'settings') {
    return route.path.includes('/user') && 
           ['account', 'privacy'].includes(route.query.tab || '')
  }
  return false
}

const closeMenu = () => {
  isMobileMenuOpen.value = false
}

// 定义不同场景下的菜单组
const communityMenuGroups = [
  {
    title: '社区功能',
    items: [
      {
        name: '首页',
        path: '/community',
        icon: HomeIcon
      },
      { 
        name: '文章', 
        path: '/community/articles', 
        icon: DocumentTextIcon 
      },
      { 
        name: '问答', 
        path: '/community/questions', 
        icon: QuestionMarkCircleIcon 
      },
      { 
        name: '话题', 
        path: '/community/topics', 
        icon: ScaleIcon 
      }
    ]
  }
]

const portfolioMenuGroups = [
  {
    title: '创作功能',
    items: [
      {
        name: '发现',
        path: '/portfolio',
        icon: HomeIcon
      },
      {
        name: '设计',
        path: '/portfolio/design',
        icon: PaintBrushIcon
      },
      {
        name: '视频',
        path: '/portfolio/video',
        icon: VideoCameraIcon
      },
      {
        name: '摄影',
        path: '/portfolio/photo',
        icon: CameraIcon
      },
      {
        name: '动画',
        path: '/portfolio/animation',
        icon: FilmIcon
      }
    ]
  }
]



// 修改模版菜单组
const templateMenuGroups = [
  {
    title: '简历模板',
    items: [
      { 
        name: '简历', 
        path: '/templates/resume', 
        icon: DocumentIcon 
      },
      { 
        name: '求职信', 
        path: '/templates/cover-letter', 
        icon: AcademicCapIcon 
      }
    ]
  }
]

// 根据当前路由计算要显示的菜单组
const currentMenuGroups = computed(() => {
  if (route.path.startsWith('/templates')) {
    return templateMenuGroups
  }
  if (route.path.startsWith('/community')) {
    return communityMenuGroups
  }
  if (route.path.startsWith('/portfolio')) {
    return portfolioMenuGroups
  }
  if (route.path.includes('/user')) {
    if (route.query.tab === 'account' || 
        route.query.tab === 'privacy') {
      return settingsMenuGroups
    }
    return profileMenuGroups
  }
  return communityMenuGroups
})
</script>

<style scoped>
.safe-area-inset-bottom {
  padding-bottom: env(safe-area-inset-bottom);
}
</style> 