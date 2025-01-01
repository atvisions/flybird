<template>
  <header class="fixed w-full top-0 z-50 bg-white shadow">
    <!-- 主导航栏 -->
    <nav class="mx-auto flex max-w-7xl items-center justify-between p-4 lg:px-8" aria-label="Global">
      <!-- Logo 区域 -->
      <div class="flex-shrink-0 flex items-center">
        <router-link to="/" class="flex items-center space-x-2">
          <img src="@/assets/images/logo.png" alt="" class="w-8 h-8">
          <span class="text-gray-500 text-xl whitespace-nowrap">飞鸟简历</span>
        </router-link>
      </div>

      <!-- 桌面端导航菜单 -->
      <div class="hidden lg:flex lg:gap-x-12">
        <template v-for="item in navigation.main" :key="item.name">
          <!-- 普通菜单项 -->
          <router-link v-if="!item.children" :to="item.href" :class="[
            'text-base  leading-6',
            isCurrentRoute(item.href)
              ? 'text-indigo-600 font-semibold'
              : 'text-gray-900 hover:text-indigo-600'
          ]">
            {{ item.name }}
          </router-link>

          <!-- 带下拉菜单的项 -->
          <div v-else class="relative resource-menu">
            <button @click.stop="resourceMenuOpen = !resourceMenuOpen"
              class="flex items-center text-base leading-6 text-gray-900 hover:text-indigo-600">
              {{ item.name }}
              <svg class="h-5 w-5 ml-1" :class="{ 'rotate-180': resourceMenuOpen }" viewBox="0 0 20 20"
                fill="currentColor">
                <path fill-rule="evenodd"
                  d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                  clip-rule="evenodd" />
              </svg>
            </button>

            <!-- 下拉菜单内容 -->
            <div v-if="resourceMenuOpen" class="absolute left-1/2  mt-3 w-screen max-w-7xl -translate-x-1/2 z-[100]"
              style="position: fixed; top: 64px; left: 50%;">
              <div class="bg-white shadow-lg ring-1 ring-gray-900/5">
                <div class="grid grid-cols-4 gap-8 p-8">
                  <!-- 遍历主要分类 -->
                  <template v-for="category in getResourceCategories" :key="category.name">
                    <div>
                      <h3 class="text-base font-medium text-gray-900 mb-4">{{ category.name }}</h3>
                      <nav class="space-y-2">
                        <router-link v-for="item in category.children" :key="item.href" :to="item.href"
                          class="flex items-center space-x-3 px-2 py-2 hover:bg-gray-50 group">
                          <component 
                            :is="getIcon(item.key)" 
                            class="flex-shrink-0 h-5 w-5 text-gray-400 group-hover:text-indigo-600" 
                          />
                          <div>
                            <span class="text-sm text-gray-900 group-hover:text-indigo-600">{{ item.name }}</span>
                            <p class="text-xs text-gray-500">{{ item.description }}</p>
                          </div>
                        </router-link>
                      </nav>

                      <!-- 如果有推荐文章，显示在分类下方 -->
                      <div v-if="category.featured" class="mt-4 pt-4 border-t border-gray-100">
                        <h4 class="text-sm font-medium text-gray-900 mb-3">{{ category.featured.title }}</h4>
                        <div class="space-y-3">
                          <router-link v-for="article in category.featured.articles" :key="article.href"
                            :to="article.href" class="group block">
                            <div class="aspect-w-16 aspect-h-9 rounded-lg overflow-hidden mb-2">
                              <img :src="article.image" :alt="article.title"
                                class="object-cover w-full h-full group-hover:opacity-75">
                            </div>
                            <h5 class="text-sm text-gray-900 group-hover:text-indigo-600 line-clamp-2">
                              {{ article.title }}
                            </h5>
                          </router-link>
                        </div>
                      </div>
                    </div>
                  </template>
                </div>

                <!-- 底部链接 -->
                <div class="border-t border-gray-100 p-4">
                  <router-link to="/resources"
                    class="flex items-center justify-between text-sm text-indigo-600 hover:text-indigo-500">
                    <span>查看全部资源</span>
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd"
                        d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" />
                    </svg>
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </template>

        <router-link to="/pro"
          class="text-base leading-6 text-yellow-600 hover:text-yellow-500 flex items-center">
          <svg class="w-5 h-5 mr-1" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M5 16L3 5L8.5 10L12 4L15.5 10L21 5L19 16H5Z" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round" />
          </svg>
          会员
        </router-link>
      </div>

      <!-- 右侧用户区域 -->
      <div class="flex items-center">
        <template v-if="!isAuthenticated">
          <!-- 未登录状态 -->
          <div class="hidden lg:block">
            <router-link to="/login" class="text-base  leading-6 text-gray-900 hover:text-indigo-600">
              登录
            </router-link>
            <router-link to="/register"
              class="ml-4 text-base  leading-6 text-white bg-primary-500 px-3 py-2 rounded-md hover:bg-primary-500">
              注册
            </router-link>
          </div>
        </template>

        <!-- 已登录状态 -->
        <template v-else>
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
                {{ store.state.userInfo?.username || '未设置昵称' }}
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
      [isMobile ? '' : 'right']: isMobile ? '' : 'calc((100% - 1280px) / 2)',
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
            <div class="text-base font-medium text-gray-900">{{ store.state.userInfo?.username || '未设置昵称' }}</div>
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

      <!-- 会员入口 -->
      <div class="py-2 border-t border-gray-100">
        <router-link to="/pro" class="block w-full text-left px-5 py-3 text-base text-yellow-600 hover:bg-gray-50">
          <div class="flex items-center space-x-2">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M5 16L3 5L8.5 10L12 4L15.5 10L21 5L19 16H5Z" stroke-width="2" stroke-linecap="round"
                stroke-linejoin="round" />
            </svg>
            <span>免费升级 ❤️</span>
          </div>
        </router-link>
      </div>

      <!-- 语言选择 -->
      <div class="py-2 border-t border-gray-100">
        <button class="block w-full text-left px-5 py-3 text-base text-gray-700 hover:bg-gray-50">
          <div class="flex items-center justify-between">
            <span>中文（简体）</span>
            <svg class="w-5 h-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd"
                d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                clip-rule="evenodd" />
            </svg>
          </div>
        </button>
      </div>

      <!-- 退出登录 -->
      <div class="py-2 border-t border-gray-100">
        <button @click="handleLogout" class="block w-full text-left px-5 py-3 text-base text-gray-700 hover:bg-gray-50">
          退出登录
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
            <router-link to="/login"
              class="block w-full text-center px-4 py-2 text-[14px] text-gray-900 border border-gray-300 rounded-md hover:bg-gray-50"
              @click="toggleMenu">
              登录
            </router-link>
            <router-link to="/register"
              class="block w-full text-center px-4 py-2 text-[14px] text-white bg-indigo-600 rounded-md hover:bg-indigo-500"
              @click="toggleMenu">
              注册
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>
<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useStore } from 'vuex'
import { showToast } from '@/components/ToastMessage'
import defaultAvatarImage from '@/assets/images/default-avatar.png'
import navigation from '@/config/navigation.json'
import { MEDIA_URL } from '@/config'
import { eventBus } from '@/utils/eventBus'
import { authService } from '@/services/authService'
import { useLogout } from '@/composables/useLogout'

// 导入所需的图标
import {
  AcademicCapIcon,
  BookOpenIcon,
  BriefcaseIcon,
  ChartBarIcon,
  ComputerDesktopIcon,
  DocumentTextIcon,
  LightBulbIcon,
  PencilIcon,
  UserIcon,
  Cog6ToothIcon,
  ArrowRightOnRectangleIcon,
  HomeIcon,
  DocumentDuplicateIcon,
  StarIcon,
  BellIcon,
  HeartIcon,
  ShieldCheckIcon,
  UserCircleIcon,
  WrenchScrewdriverIcon
} from '@heroicons/vue/24/outline'

// 添加图标映射函数
const getIcon = (menuKey) => {
  const iconMap = {
    // 主导航图标
    'home': HomeIcon,
    'resume': DocumentDuplicateIcon,
    'resources': BookOpenIcon,
    'pro': StarIcon,
    
    // 用户菜单图标
    'profile': UserCircleIcon,
    'resumes': DocumentTextIcon,
    'favorites': HeartIcon,
    'notifications': BellIcon,
    'settings': Cog6ToothIcon,
    'security': ShieldCheckIcon,
    'account': WrenchScrewdriverIcon,
    'logout': ArrowRightOnRectangleIcon,

    // 资源分类图标
    'templates': DocumentDuplicateIcon,
    'guides': LightBulbIcon,
    'tools': ComputerDesktopIcon,
    'career': BriefcaseIcon,
    'education': AcademicCapIcon,
    'statistics': ChartBarIcon,
    'editor': PencilIcon
  }
  return iconMap[menuKey] || UserIcon // 默认返回 UserIcon
}

// 将 getIcon 添加到模板中使用
const icons = {
  getIcon
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

// 使用 useLogout composable
const { handleLogout } = useLogout()

// 监听 store 中的用户信息变化
watch(
  () => [store.state.userInfo, store.state.basicInfo],
  ([newUserInfo, newBasicInfo]) => {
    if (newUserInfo || newBasicInfo) {
      userBasicInfo.value = {
        ...newBasicInfo,
        ...newUserInfo
      }
    }
  },
  { immediate: true }
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

// 移动端子菜单开关
const toggleMobileSubmenu = (categoryName) => {
  mobileSubmenuOpen.value[categoryName] = !mobileSubmenuOpen.value[categoryName]
}

// 处理菜单点击
const handleMenuClick = (key) => {
  userMenuOpen.value = false
  router.push({
    path: '/user',
    query: { tab: key }
  })
}

// 判断当前路由是否匹配
const isCurrentRoute = (href) => {
  return route.path === href
}
// 获取资源分类
const getResourceCategories = computed(() => {
  const resourceMenu = navigation.main.find(item => item.name === '职场资源')
  return resourceMenu?.children || []
})


// 从 store 获取用户信息和认证状态
const isAuthenticated = computed(() => store.state.isAuthenticated)

// 用户昵称计算属性
const username = computed(() => {
  return store.state.userInfo?.username || '未设置昵称'
})

// 头像 URL 计算属性
const avatarUrl = computed(() => {
  const avatar = store.state.basicInfo?.avatar
  const baseUrl = process.env.VUE_APP_API_BASE_URL || 'http://192.168.3.16:8000'
  
  // 如果有头像且是相对路径，添加 API 基础路径
  if (avatar && !avatar.startsWith('http')) {
    return `${baseUrl}${avatar}`
  }
  
  return avatar || defaultAvatarImage
})

// 获取用户信息的函数
const fetchUserInfo = async () => {
  if (store.state.isAuthenticated) {
    await store.dispatch('fetchUserInfo')
    

    userBasicInfo.value = {
      ...store.state.basicInfo?.basic_info,
      ...store.state.userInfo?.user
    }
  }
}

// 添加 watch 来监控数据变化
watch(() => store.state.basicInfo, (newVal) => {

}, { deep: true })

watch(() => store.state.userInfo, (newVal) => {
  
}, { deep: true })

// 生命周期钩子
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

// 将 resize 处理函数提取出来
const handleResize = () => {
  if (!isMobile.value) {
    mobileMenuOpen.value = false
  }
}

// 简化头像更新处理方法
const handleAvatarUpdate = (newAvatar) => {
  store.commit('SET_BASIC_INFO', {
    ...store.state.basicInfo,
    avatar: newAvatar
  })
}

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

// 手机号脱敏处理
const maskedPhone = computed(() => '')

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
      key: 'favorites',
      label: '我的收藏',
      icon: 'favorites',
      action: () => router.push('/user/favorites')
    },
    {
      key: 'notifications',
      label: '消息通知',
      icon: 'notifications',
      action: () => router.push('/user/notifications')
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

// 导航菜单
const navItems = computed(() => {
  const items = [
    { label: '首页', path: '/' },
    { label: '关于我们', path: '/about' },
    { label: '联系我们', path: '/contact' }
  ]
  if (store.getters.getUserInfo?.role === 'admin') {
    items.push({ label: '管理后台', path: '/admin' })
  }
  return items
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
</style>