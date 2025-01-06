<template>
  <header class="fixed w-full top-0 z-50 bg-white shadow">
    <!-- 主导航栏 -->
    <nav class="mx-auto flex max-w-7xl items-center p-4 lg:px-8" aria-label="Global">
      <!-- Logo 区域 -->
      <div class="flex-shrink-0 flex items-center mr-8">
        <router-link to="/" class="flex items-center space-x-2">
          <img src="@/assets/images/logo.png" alt="" class="w-8 h-8">
          <span class="text-gray-500 text-xl whitespace-nowrap">飞鸟简历</span>
        </router-link>
      </div>

      <!-- 桌面端导航菜单 -->
      <div class="hidden lg:flex lg:gap-x-8">
        <template v-for="item in navigation.main" :key="item.name">
          <!-- 普通菜单项 -->
          <router-link v-if="!item.children" :to="item.href" :class="[
            'text-base leading-6 py-2 border-b-2',
            isCurrentRoute(item.href)
              ? 'text-gray-900 font-medium border-gray-900'
              : 'text-gray-500 hover:text-gray-900 border-transparent hover:border-gray-300'
          ]">
            {{ item.name }}
          </router-link>       
        </template>

        <router-link to="/pro"
          :class="[
            'text-base leading-6 flex items-center py-2 border-b-2',
            isCurrentRoute('/pro')
              ? 'text-yellow-600 border-yellow-600'
              : 'text-yellow-600 hover:text-yellow-500 border-transparent hover:border-yellow-500'
          ]">
          <svg class="w-5 h-5 mr-1" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M5 16L3 5L8.5 10L12 4L15.5 10L21 5L19 16H5Z" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round" />
          </svg>
          会员
        </router-link>
      </div>

      <!-- 搜索框 -->
      <div class="hidden lg:flex items-center justify-center ml-4">
        <!-- 搜索图标按钮 -->
        <button 
          @click.stop="showSearchModal = true"
          class="p-2 text-gray-500 hover:text-gray-900 rounded-full hover:bg-gray-100"
        >
          <MagnifyingGlassIcon class="w-5 h-5" />
        </button>
      </div>

      <!-- 右侧用户区域 -->
      <div class="flex items-center ml-auto">
        <template v-if="!isAuthenticated">
          <!-- 未登录状态 -->
          <div class="hidden lg:block">
            <router-link 
              :to="`/login?redirect=${encodeURIComponent($route.fullPath)}`" 
              class="text-base leading-6 text-gray-900 hover:text-indigo-600"
            >
              登录
            </router-link>
            <router-link 
              to="/register"
              class="ml-4 text-base leading-6 text-white bg-primary-500 px-3 py-2 rounded-md hover:bg-primary-500"
            >
              注册
            </router-link>
          </div>
        </template>

        <!-- 已登录状态 -->
        <template v-else>
          <!-- 消息图标 -->
          <router-link 
            to="/user?tab=messages"
            class="mr-4 p-1.5 text-gray-500 hover:text-indigo-600 relative inline-flex items-center justify-center"
            :class="{ 'text-indigo-600': isMessageRoute }"
          >
            <BellIcon 
              class="w-6 h-6" 
              :class="{ 'text-indigo-600': isMessageRoute }"
            />
            <!-- 未读消息数量 -->
            <span 
              v-if="unreadMessagesCount > 0"
              class="absolute -top-0.5 -right-0.5 min-w-[16px] h-[16px] bg-red-500 rounded-full text-[10px] font-medium text-white flex items-center justify-center px-1"
            >
              {{ unreadMessagesCount > 99 ? '99+' : unreadMessagesCount }}
            </span>
          </router-link>
          <div class="relative">
            <button @click.stop="userMenuOpen = !userMenuOpen"
              class="flex items-center space-x-1 text-sm font-semibold text-gray-900 hover:text-indigo-600">
              <img 
                :src="avatarUrl"
                @error="handleImageError"
                class="h-8 w-8 rounded-full"
                alt="用户头像"
              />
              <span class="hidden lg:inline">
                {{ username }}
              </span>
              <svg class="h-5 w-5" :class="{ 'rotate-180': userMenuOpen }" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                  clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </template>

        <!-- 移动端菜单按钮 -->
        <button type="button" @click="toggleMenu"
          class="lg:hidden inline-flex items-center justify-center rounded-md ml-2 p-2 text-gray-700">
          <span class="sr-only">打开菜单</span>
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
          </svg>
        </button>
      </div>
    </nav>

    <!-- 用户下拉菜单 -->
    <div v-if="userMenuOpen" :class="[
      'fixed lg:absolute',
      'top-[72px]',
      'bg-white shadow-lg z-[100]',
      'inset-x-0 lg:inset-x-auto',
      'lg:w-64 lg:rounded-lg'
    ]" :style="{
      [isMobile ? '' : 'right']: isMobile ? '' : 'calc((100vw - 1280px) / 2 + 26px)',
    }">
      <!-- 用户信息头部 -->
      <div class="px-5 py-4 border-b border-gray-100">
        <div class="flex items-center space-x-3">
          <img 
            :src="avatarUrl"
            :key="avatarUrl"
            class="h-12 w-12 rounded-full" 
            alt="用户头像" 
            @error="handleImageError" 
          />
          <div>
            <div class="text-base font-medium text-gray-900">{{ username }}</div>
            <div class="text-sm text-gray-500">{{ userType }}</div>
          </div>
        </div>
      </div>

      <!-- 菜单项 -->
      <div class="py-2">
        <button v-for="item in userMenuItems" :key="item.key"
          class="block w-full px-5 py-3 text-base text-gray-700 hover:bg-gray-50 text-left"
          @click="item.action">
          <div class="flex items-center space-x-2">
            <component 
              :is="getIcon(item.icon)" 
              class="flex-shrink-0 h-5 w-5 text-gray-400 group-hover:text-indigo-600" 
            />
            <span>{{ item.label }}</span>
          </div>
        </button>
      </div>

    </div>

    <!-- 移动端菜单抽屉 -->
    <div v-if="mobileMenuOpen" class="fixed inset-0 z-50" @click="toggleMenu">
      <div class="fixed inset-0 bg-black/25"></div>

      <div class="fixed inset-y-0 right-0 z-50 w-full overflow-y-auto bg-white sm:max-w-sm" @click.stop>
        <!-- 移动端菜单头部 -->
        <div class="flex items-center justify-between p-4">
          <router-link to="/" class="flex items-center space-x-2" @click="toggleMenu">
            <img src="@/assets/images/logo.png" alt="" class="w-8 h-8">
            <span class="text-gray-500 text-xl whitespace-nowrap">飞鸟简历</span>
          </router-link>
          <!-- 关闭按钮 -->
          <button type="button" @click="toggleMenu" class="p-2 text-gray-700">
            <span class="sr-only">关闭菜单</span>
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- 移动端菜单内容 -->
        <div class="border-t border-gray-200">
          <!-- 导航菜单 -->
          <div>
            <template v-for="item in navigation.main" :key="item.name">
              <!-- 普通菜单项 -->
              <router-link v-if="!item.children" :to="item.href"
                class="block px-4 py-3 text-base text-gray-900 border-b border-gray-100"
                :class="isCurrentRoute(item.href) ? 'text-indigo-600' : ''" @click="toggleMenu">
                {{ item.name }}
              </router-link>

              <!-- 带子菜单的项 -->
              <div v-else class="border-b border-gray-100">
                <button class="flex items-center justify-between w-full px-4 py-3 text-base text-gray-900"
                  @click="toggleMobileSubmenu(item.name)">
                  <span>{{ item.name }}</span>
                  <svg class="w-5 h-5 transition-transform duration-200"
                    :class="{ 'rotate-180': mobileSubmenuOpen[item.name] }" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd"
                      d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                      clip-rule="evenodd" />
                  </svg>
                </button>

                <div v-show="mobileSubmenuOpen[item.name]" class="bg-gray-50">
                  <template v-for="category in item.children" :key="category.name">
                    <div class="px-4 py-2">
                      <div class="font-medium text-gray-900">{{ category.name }}</div>
                      <div class="mt-1 space-y-1">
                        <router-link v-for="subItem in category.children" :key="subItem.name" :to="subItem.href"
                          class="block py-1 pl-3 text-sm text-gray-600 hover:text-indigo-600" @click="toggleMenu">
                          {{ subItem.name }}
                        </router-link>
                      </div>
                    </div>
                  </template>
                </div>
              </div>
            </template>
          </div>

          <!-- 未登录状态下显示登录注册按钮 -->
          <div v-if="!isAuthenticated" class="p-4 space-y-3">
            <router-link to="/login?redirect=${encodeURIComponent($route.fullPath)}`"
              class="block w-full text-center px-4 py-2 text-[14px] text-gray-900 border border-gray-300 rounded-md hover:bg-gray-50"
              @click="toggleMenu">
              登录
            </router-link>
            <router-link to="/register?redirect=${encodeURIComponent($route.fullPath)}`"
              class="block w-full text-center px-4 py-2 text-[14px] text-white bg-indigo-600 rounded-md hover:bg-indigo-500"
              @click="toggleMenu">
              注册
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- 搜索弹窗 -->
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div v-if="showSearchModal" class="fixed inset-0 z-[100]">
        <!-- 黑色遮罩 -->
        <div 
          class="fixed inset-0 bg-black/50 transition-opacity" 
          @click="showSearchModal = false"
        />
        
        <!-- 关闭按钮 -->
        <button 
          @click="showSearchModal = false"
          class="fixed top-4 right-4 p-2 rounded-full bg-black/20 hover:bg-black/30 transition-colors z-[110]"
        >
          <XMarkIcon class="w-6 h-6 text-white" />
        </button>

        <!-- 搜索框容器 -->
        <div class="relative min-h-screen flex items-start justify-center p-4 sm:p-6" @click.stop>
          <div class="w-full max-w-2xl mt-20">
            <!-- 搜索框 -->
            <div class="bg-white rounded-xl shadow-2xl overflow-hidden">
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <MagnifyingGlassIcon class="h-5 w-5 text-gray-400" />
                </div>
                <input
                  ref="searchInput"
                  type="text"
                  v-model="searchQuery"
                  @keyup.enter="handleSearch"
                  @keyup.esc="showSearchModal = false"
                  placeholder="搜索文章、作品集、用户"
                  class="block w-full pl-12 pr-4 py-4 text-lg bg-transparent border-0 focus:ring-0 placeholder-gray-500"
                  autofocus
                />
              </div>
              
              <!-- 搜索建议 -->
              <div v-if="searchQuery" class="border-t border-gray-100">
                <div class="p-4">
                  <div class="text-xs font-medium text-gray-500 mb-3">搜索建议</div>
                  <div class="space-y-2">
                    <button
                      v-for="(type, index) in searchTypes"
                      :key="index"
                      @click="handleSearchByType(type)"
                      class="w-full text-left px-4 py-3 text-sm text-gray-700 hover:bg-gray-50 rounded-lg flex items-center transition-colors"
                    >
                      <component :is="type.icon" class="w-5 h-5 mr-3 text-gray-400" />
                      在{{ type.label }}中搜索"{{ searchQuery }}"
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </header>
</template>
<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useStore } from 'vuex'
import defaultAvatarImage from '@/assets/images/default-avatar.png'
import navigation from '@/config/navigation.json'
import { eventBus } from '@/utils/eventBus'
import { useLogout } from '@/composables/useLogout'
import { API_URL } from '@/config'
import { showToast } from '@/components/ToastMessage'

// 导入所需的图标
import {
  DocumentTextIcon,
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
  XMarkIcon
} from '@heroicons/vue/24/outline'

// 添加图标映射函数
const getIcon = (menuKey) => {
  const iconMap = {  
    // 用户菜单图标
    'profile': UserCircleIcon,
    'resumes': DocumentTextIcon,
    'favorites': HeartIcon,
    'notifications': BellIcon,
    'settings': Cog6ToothIcon,
    'security': ShieldCheckIcon,
    'account': WrenchScrewdriverIcon,
    'logout': ArrowRightOnRectangleIcon,
  }
  return iconMap[menuKey] || UserIcon // 默认返回 UserIcon
}

// 状态管理
const router = useRouter()
const route = useRoute()
const store = useStore()
const mobileMenuOpen = ref(false)
const userMenuOpen = ref(false)
const resourceMenuOpen = ref(false)
const mobileSubmenuOpen = ref({})
const userBasicInfo = ref(null)

// 监听 store 中的用户信息变化，更新用户基本信息
watch(
  () => store.state.userInfo,
  (newUserInfo) => {
    if (newUserInfo?.data?.basic_info) {
      userBasicInfo.value = {
        ...newUserInfo.data.basic_info,
        ...newUserInfo.data.user
      }
    }
  },
  { immediate: true, deep: true }
)

// 响应式计算
const isMobile = computed(() => {
  return window.innerWidth < 1024
})




// 统一的菜单关闭处理
const closeMenus = (e) => {
  if (!e.target.closest('.resource-menu')) {
    resourceMenuOpen.value = false
  }
  if (!e.target.closest('.user-menu')) {
    userMenuOpen.value = false
  }
}

// 移动端菜单开关
const toggleMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
  if (mobileMenuOpen.value) {
    userMenuOpen.value = false
    resourceMenuOpen.value = false
    mobileSubmenuOpen.value = {}
  }
}




// 判断当前路由是否匹配
const isCurrentRoute = (href) => {
  // 对于模板相关的路由，使用 startsWith 判断
  if (href === '/templates') {
    return route.path.startsWith('/templates')
  }
  // 对于社区相关的路由，使用 startsWith 判断
  if (href === '/community') {
    return route.path.startsWith('/community')
  }
  // 对于作品集相关的路由，使用 startsWith 判断
  if (href === '/portfolio') {
    return route.path.startsWith('/portfolio')
  }
  // 其他路由保持完全匹配
  return route.path === href
}



// 用户昵称计算属性
const username = computed(() => {
  const username = store.state.userInfo?.data?.user?.username
  return username || '未设置昵称'
})

// 头像 URL 计算属性
const avatarUrl = computed(() => {
  const avatar = store.state.userInfo?.data?.basic_info?.avatar
  if (!avatar) return defaultAvatarImage
  
  if (avatar.startsWith('http') || avatar.startsWith('data:')) {
    return avatar
  }
  return `${API_URL}${avatar}`
})

// 获取用户信息的函数
const fetchUserInfo = async () => {
  if (store.state.isAuthenticated) {
    try {
      await store.dispatch('fetchUserInfo')
      userBasicInfo.value = {
        ...store.state.userInfo?.data?.basic_info,
        ...store.state.userInfo?.data?.user
      }
    } catch (error) {
      console.error('Failed to fetch user info:', error)
    }
  }
}

// 判断是否在消息页面
const isMessageRoute = computed(() => {
  return route.path.includes('/user') && route.query.tab === 'messages'
})

// 测试用：模拟未读消息数量
const unreadMessagesCount = ref(5)

// 获取未读消息数量
const fetchUnreadMessagesCount = async () => {
  try {
    // TODO: 调用 API 获取未读消息数量
    // const response = await api.getUnreadMessagesCount()
    // unreadMessagesCount.value = response.data.count
    unreadMessagesCount.value = 5 // 临时测试数据
  } catch (error) {
    console.error('获取未读消息数量失败:', error)
  }
}

// 在用户登录状态变化时获取未读消息数量
watch(() => store.state.isAuthenticated, (newValue) => {
  if (newValue) {
    fetchUnreadMessagesCount()
  } else {
    unreadMessagesCount.value = 0
  }
}, { immediate: true })

// 生命周期钩子，监听事件，监听登录状态
onMounted(async () => {
  document.addEventListener('click', closeMenus)
  window.addEventListener('resize', () => {
    if (!isMobile.value) {
      mobileMenuOpen.value = false
    }
  })
  
  if (store.state.isAuthenticated) {
    try {
      await fetchUserInfo()
    } catch (error) {
      console.error('Failed to fetch user info:', error)
      if (error.response?.status === 401) {
        store.commit('SET_LOGGED_IN', false)
      }
    }
  }
  
  eventBus.on('avatar-updated', handleAvatarUpdate)
})

// 保持原有的事件清理
onUnmounted(() => {
  eventBus.off('avatar-updated', handleAvatarUpdate)
})

// 简化头像更新处理方法
const handleAvatarUpdate = (newAvatar) => {
  store.commit('SET_USER_INFO', {
    ...store.state.userInfo,
    data: {
      ...store.state.userInfo?.data,
      basic_info: {
        ...store.state.userInfo?.data?.basic_info,
        avatar: newAvatar
      }
    }
  })
}
// 从 store 获取用户信息和认证状态，并计算是否已登录
const isAuthenticated = computed(() => store.state.isAuthenticated)
// 监听登录状态变化
watch(() => store.state.isAuthenticated, (newValue) => {
  if (newValue) {
    fetchUserInfo()
  } else {
    userBasicInfo.value = null
  }
}, { immediate: true })

// 监听头像更新
watch(() => store.state.avatarUpdateTime, () => {
  if (store.state.isAuthenticated) {
    fetchUserInfo()
  }
})

// 处理图片加载错误
const handleImageError = (e) => {
  e.target.src = defaultAvatarImage
}

// 用户类型
const userType = computed(() => '普通用户')

// 用户菜单选项
const userMenuItems = computed(() => {
  return [
    {
      key: 'profile',
      label: '我的档案',
      icon: 'profile',
      action: () => router.push('/user?tab=profile')
    },
    {
      key: 'resumes',
      label: '我的简历',
      icon: 'resumes',
      action: () => router.push('/user?tab=resumes')
    },
    {
      key:'creations',
      label:'我的创作',
      icon:'creations',
      action: () => router.push('/user?tab=creations')
    },
    {
      key: 'portfolio',
      label: '我的作品集',
      icon: 'portfolio',
      action: () => router.push('/user?tab=portfolio')
    },
    {
      key: 'favorites',
      label: '我的收藏',
      icon: 'favorites',
      action: () => router.push('/user?tab=favorites')
    },
    {
      key: 'notifications',
      label: '消息通知',
      icon: 'notifications',
      action: () => router.push('/user?tab=messages')
    },
    {
      key: 'homepage',
      label: '我的主页',
      icon: 'homepage',
      action: () => router.push('/u/10001')
    },
    {
      key: 'settings',
      label: '账号设置',
      icon: 'settings',
      action: () => router.push('/user?tab=account')
    },
    {
      key: 'logout',
      label: '退出登录',
      icon: 'logout',
      action: handleLogout
    }
  ]
})

// 处理退出登录
const handleLogout = async () => {
  try {
    // 关闭用户菜单
    userMenuOpen.value = false
    
    await store.dispatch('logout')
    showToast('退出成功', 'success')
    
    // 获取当前路径作为重定向地址
    const currentPath = router.currentRoute.value.fullPath
    // 跳转到登录页面，并带上当前路径作为 redirect 参数
    router.push(`/login?redirect=${encodeURIComponent(currentPath)}`)
    
  } catch (error) {
    console.error('退出失败:', error)
    showToast('退出失败，请重试', 'error')
  }
}

// 搜索相关状态
const searchQuery = ref('')
const showSearchModal = ref(false)
const searchInput = ref(null)

// 监听 ESC 键关闭搜索弹窗
onMounted(() => {
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      showSearchModal.value = false
    }
  })
})

// 修改搜索处理函数
const handleSearch = () => {
  if (!searchQuery.value.trim()) return
  router.push({
    path: '/search',
    query: { q: searchQuery.value }
  })
  showSearchModal.value = false
}

const handleSearchByType = (type) => {
  if (!searchQuery.value.trim()) return
  router.push({
    path: type.path,
    query: { q: searchQuery.value }
  })
  showSearchModal.value = false
}

// 搜索类型配置
const searchTypes = [
  { 
    label: '文章', 
    type: 'articles',
    icon: DocumentTextIcon,
    path: '/search/articles'
  },
  { 
    label: '作品集', 
    type: 'portfolio',
    icon: PhotoIcon,
    path: '/search/portfolio'
  },
  { 
    label: '用户', 
    type: 'users',
    icon: UserGroupIcon,
    path: '/search/users'
  }
]

// 监听点击事件，关闭搜索建议
onMounted(() => {
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.search-container')) {
      showSearchModal.value = false
    }
  })
})

</script>
<style scoped>
/* 添加过渡动画 */
.aspect-h-9 {
  position: relative;
  padding-bottom: 56.25%;
}

.aspect-h-9 img {
  position: absolute;
  height: 100%;
  width: 100%;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  transition: opacity 0.3s ease;
}

/* 添加菜单hover效果 */
.hover\:bg-gray-100:hover {
  background-color: rgba(243, 244, 246, 1);
}

/* 确保下拉菜单定位正确 */
.resource-menu {
  position: static;
}

@media (min-width: 1024px) {
  .resource-menu {
    position: relative;
  }
}

/* 添加过渡动画 */
.transition-transform {
  transition-property: transform;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}

/* 移动端菜单动画 */
.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition: transform 0.3s ease-in-out;
}

.mobile-menu-enter-from,
.mobile-menu-leave-to {
  transform: translateX(100%);
}

/* 下拉菜单动画 */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
/* 确保下拉菜单始终最上层 */
:deep(.el-dropdown-menu) {
  z-index: 3000 !important;
}

/* 调整资源菜单定位 */
.resource-menu {
  position: static;
}

@media (min-width: 1024px) {
  .resource-menu {
    position: relative;
  }
}

/* 消息图标动画 */
@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.animate-pulse {
  animation: pulse 2s infinite;
}

/* 消息数量的动画效果 */
@keyframes scaleIn {
  from {
    transform: scale(0);
  }
  to {
    transform: scale(1);
  }
}

.absolute {
  animation: scaleIn 0.2s ease-out;
}
</style>