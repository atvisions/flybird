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
          <button 
            @click.stop="toggleMessageMenu"
            class="hidden md:block p-2 mr-2 text-gray-500 hover:text-indigo-600 relative message-menu"
            :class="{ 'text-indigo-600': isMessageRoute }"
          >
            <BellIcon 
              class="w-5 h-5" 
              :class="{ 'text-indigo-600': isMessageRoute }"
            />
            <!-- 未读消息数量 -->
            <span 
              v-if="unreadMessagesCount > 0"
              class="absolute -top-1 -right-1 min-w-[16px] h-4 bg-red-500 rounded-full text-[10px] font-medium text-white flex items-center justify-center px-1"
            >
              {{ unreadMessagesCount > 99 ? '99+' : unreadMessagesCount }}
            </span>
          </button>

          <!-- 消息下拉菜单 -->
          <div v-if="showMessageMenu" 
            class="fixed lg:absolute top-[72px] bg-white shadow-lg z-[100] w-80 rounded-lg message-menu"
            :style="{
              [isMobile ? '' : 'right']: isMobile ? '' : 'calc((100vw - 1280px) / 2 + 120px)',
            }"
          >
            <!-- 消息菜单头部 -->
            <div class="px-4 py-3 border-b border-gray-100">
              <div class="flex items-center justify-between">
                <h3 class="text-base font-medium text-gray-900">消息通知</h3>
                <button class="text-sm text-gray-500 hover:text-gray-700">全部标记已读</button>
              </div>
            </div>
            
            <!-- 消息列表 -->
            <div class="max-h-[400px] overflow-y-auto">
              <div v-if="messages.length === 0" class="py-8 text-center text-gray-500">
                暂无消息
              </div>
              <div v-else class="divide-y divide-gray-100 py-1">
                <div v-for="message in messages" :key="message.id" 
                  @click.stop="viewMessageDetail(message)"
                  class="px-4 py-3 hover:bg-gray-50 cursor-pointer"
                >
                  <div class="flex items-start space-x-3">
                    <div class="flex-shrink-0">
                      <div class="w-2 h-2 mt-2 rounded-full" 
                        :class="message.isRead ? 'bg-gray-300' : 'bg-blue-500'"
                      ></div>
                    </div>
                    <div class="flex-1 min-w-0">
                      <div class="flex items-center justify-between mb-1">
                        <span 
                          class="text-xs px-1.5 py-0.5 rounded"
                          :class="{
                            'bg-blue-100 text-blue-700': message.type === 'system',
                            'bg-green-100 text-green-700': message.type === 'private'
                          }"
                        >
                          {{ message.type === 'system' ? '系统通知' : '私信' }}
                        </span>
                        <span class="text-xs text-gray-500">{{ message.time }}</span>
                      </div>
                      <p class="text-sm text-gray-900">{{ message.content }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 消息菜单底部 -->
            <div class="px-4 py-3 border-t border-gray-100 text-center">
              <button 
                class="text-sm text-indigo-600 hover:text-indigo-700"
                @click="viewAllMessages"
              >
                查看全部消息
              </button>
            </div>
          </div>

          <div class="relative" ref="dropdownRef">
            <button 
              @click.stop="toggleDropdown"
              class="flex items-center cursor-pointer"
            >
              <img 
                :src="avatarUrl"
                class="h-8 w-8 rounded-full"
                alt="用户头像"
              />
              <span class="hidden lg:inline ml-2">{{ username }}</span>
              <ChevronDownIcon 
                class="h-5 w-5 ml-1"
                :class="{ 'rotate-180': showDropdown }"
              />
            </button>

            <!-- 下拉菜单内容 -->
            <div 
              v-if="showDropdown"
              class="fixed lg:absolute right-0 top-[60px] w-full lg:w-80 bg-white shadow-lg py-1 border-t lg:border lg:border-gray-100 z-50"
              :class="[
                isMobile ? 'inset-x-0' : '',
                isMobile ? 'h-[calc(100vh-60px)]' : '',
                isMobile ? 'overflow-y-auto' : ''
              ]"
              @click.stop
            >
              <!-- 用户信息头部 -->
              <div class="px-4 lg:px-6 py-5 border-b border-gray-100">
                <div class="flex items-center space-x-3">
                  <img 
                    :src="avatarUrl"
                    :key="avatarUrl"
                    class="h-12 lg:h-14 w-12 lg:w-14 rounded-full"
                    alt="用户头像" 
                    @error="handleImageError" 
                  />
                  <div class="flex-1">
                    <div class="flex items-center justify-between">
                      <div>
                        <div class="text-base lg:text-lg font-medium text-gray-900">{{ username }}</div>
                        <div class="text-sm flex flex-col" :class="{
                          'text-[#1A56DB]': isVip
                        }">
                          <span>{{ vipTypeText }}</span>
                          <span v-if="remainingDays" class="mt-0.5 text-xs">{{ remainingDays }}</span>
                        </div>
                      </div>
                      <button
                        @click="handleVipButton"
                        class="px-2.5 lg:px-3 py-1.5 text-xs lg:text-sm bg-gradient-to-r from-[#1A56DB] to-blue-500 text-white rounded-full hover:opacity-90 transition-opacity flex items-center whitespace-nowrap"
                      >
                        <SparklesIcon class="w-3.5 h-3.5 mr-1" />
                        {{ vipButtonText }}
                      </button>
                    </div>
                  </div>
                </div>
                <!-- 积分信息 -->
                <div class="mt-4 flex items-center justify-between px-1">
                  <div class="flex items-center space-x-2">
                    <StarIcon class="w-4 h-4 text-[#1A56DB]" />
                    <span class="text-sm text-gray-600">我的积分</span>
                  </div>
                  <div class="flex items-center space-x-3">
                    <span class="text-lg font-medium text-[#1A56DB]">{{ pointsInfo.balance || 0 }}</span>
                    <button 
                      @click="handlePointsDetail"
                      class="text-xs text-gray-500 hover:text-gray-700 flex items-center"
                    >
                      <span>查看详情</span>
                      <ChevronRightIcon class="w-4 h-4 ml-0.5" />
                    </button>
                  </div>
                </div>
              </div>

              <!-- 菜单项 -->
              <div class="py-2.5">
                <button v-for="item in userMenuItems" :key="item.key"
                  class="block w-full px-4 lg:px-6 py-3 lg:py-3.5 text-sm lg:text-base text-gray-700 hover:bg-blue-50 text-left transition-colors duration-200"
                  @click="item.action">
                  <div class="flex items-center space-x-3">
                    <component 
                      :is="getIcon(item.icon)" 
                      class="flex-shrink-0 h-4 lg:h-5 w-4 lg:w-5 text-[#1A56DB]/60" 
                    />
                    <span>{{ item.label }}</span>
                  </div>
                </button>
              </div>

            </div>
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
      'top-[60px]',
      'bg-white shadow-lg z-[100]',
      'inset-x-0 lg:inset-x-auto',
      'w-full lg:w-80 lg:rounded-lg'
    ]" :style="{
      [isMobile ? '' : 'right']: isMobile ? '' : '0',
    }">
      <!-- 用户信息头部 -->
      <div class="px-6 py-5 border-b border-gray-100">
        <div class="flex items-center space-x-3">
          <img 
            :src="avatarUrl"
            :key="avatarUrl"
            class="h-14 w-14 rounded-full"
            alt="用户头像" 
            @error="handleImageError" 
          />
          <div class="flex-1">
            <div class="flex items-center justify-between">
              <div>
                <div class="text-lg font-medium text-gray-900">{{ username }}</div>
                <div class="text-sm flex flex-col" :class="{
                  'text-[#1A56DB]': isVip
                }">
                  <span>{{ vipTypeText }}</span>
                  <span v-if="remainingDays" class="mt-0.5 text-xs">{{ remainingDays }}</span>
                </div>
              </div>
              <button
                @click="handleVipButton"
                class="px-3 py-1.5 text-sm bg-gradient-to-r from-[#1A56DB] to-blue-500 text-white rounded-full hover:opacity-90 transition-opacity flex items-center whitespace-nowrap"
              >
                <SparklesIcon class="w-3.5 h-3.5 mr-1" />
                {{ vipButtonText }}
              </button>
            </div>
          </div>
        </div>
        <!-- 积分信息 -->
        <div class="mt-4 flex items-center justify-between px-1">
          <div class="flex items-center space-x-2">
            <StarIcon class="w-4 h-4 text-[#1A56DB]" />
            <span class="text-sm text-gray-600">我的积分</span>
          </div>
          <div class="flex items-center space-x-3">
            <span class="text-lg font-medium text-[#1A56DB]">{{ pointsInfo.balance || 0 }}</span>
            <button 
              @click="handlePointsDetail"
              class="text-xs text-gray-500 hover:text-gray-700 flex items-center"
            >
              <span>查看详情</span>
              <ChevronRightIcon class="w-4 h-4 ml-0.5" />
            </button>
          </div>
        </div>
      </div>

      <!-- 菜单项 -->
      <div class="py-2.5">
        <button v-for="item in userMenuItems" :key="item.key"
          class="block w-full px-6 py-3.5 text-base text-gray-700 hover:bg-blue-50 text-left transition-colors duration-200"
          @click="item.action">
          <div class="flex items-center space-x-3">
            <component 
              :is="getIcon(item.icon)" 
              class="flex-shrink-0 h-5 w-5 text-[#1A56DB]/60" 
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
import { useAuthStore } from '@/stores/auth'
import { useAccountStore } from '@/stores/account'
import defaultAvatar from '@/assets/images/default-avatar.png'
import navigation from '@/config/navigation.json'
import { eventBus } from '@/utils/eventBus'
import { showToast } from '@/components/ToastMessage'
import request from '@/utils/request'
import { membership } from '@/api/membership'

// 导入所需的图标
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
  ChevronDownIcon
} from '@heroicons/vue/24/outline'


// 添加图标映射函数
const getIcon = (menuKey) => {
  const iconMap = {  
    'home': Squares2X2Icon,
    'profile': UserIcon,
    'resumes': DocumentIcon,
    'favorites': HeartIcon,
    'notifications': BellIcon,
    'settings': Cog6ToothIcon,
    'security': ShieldCheckIcon,
    'account': WrenchScrewdriverIcon,
    'logout': ArrowRightOnRectangleIcon,
    'crown': SparklesIcon,
  }
  return iconMap[menuKey] || UserIcon // 默认返回 UserIcon
}

// 状态管理 - 将所有状态管理放在一起
const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const accountStore = useAccountStore()
const mobileMenuOpen = ref(false)
const showDropdown = ref(false)
const showMessageMenu = ref(false)
const resourceMenuOpen = ref(false)
const dropdownRef = ref(null)
const userBasicInfo = ref(null)

// 切换下拉菜单
const toggleDropdown = (e) => {
  e.stopPropagation()
  showDropdown.value = !showDropdown.value
  // 关闭其他菜单
  showMessageMenu.value = false
  resourceMenuOpen.value = false
}

// 处理点击事件
const handleClickOutside = (event) => {
  const target = event.target
  // 如果点击的不是下拉菜单区域，关闭下拉菜单
  if (dropdownRef.value && !dropdownRef.value.contains(target)) {
    showDropdown.value = false
  }
  // 如果点击的不是消息菜单区域，关闭消息菜单
  if (!target.closest('.message-menu')) {
    showMessageMenu.value = false
  }
  // 如果点击的不是资源菜单区域，关闭资源菜单
  if (!target.closest('.resource-menu')) {
    resourceMenuOpen.value = false
  }
}

// 模拟消息数据
const messages = ref([
  {
    id: 1,
    content: '您的简历被查看了',
    time: '10分钟前',
    isRead: false,
    type: 'system'
  },
  {
    id: 2,
    content: '有新的职位推荐',
    time: '1小时前',
    isRead: true,
    type: 'system'
  },
  {
    id: 3,
    content: '张三给你发送了一条私信',
    time: '2小时前',
    isRead: false,
    type: 'private'
  }
])

// 切换消息菜单
const toggleMessageMenu = (e) => {
  e.stopPropagation() // 阻止事件冒泡
  showMessageMenu.value = !showMessageMenu.value
  if (showDropdown.value) {
    showDropdown.value = false
  }
}

// 查看全部消息
const viewAllMessages = () => {
  router.push('/messages')
  showMessageMenu.value = false // 关闭消息菜单
}

// 监听 accountStore 中的用户信息变化
watch(
  [() => accountStore.userInfo, () => authStore.isLoggedIn],
  ([newUserInfo, isLoggedIn]) => {
    if (newUserInfo && isLoggedIn) {
      userBasicInfo.value = {
        ...newUserInfo
      }
    } else {
      userBasicInfo.value = null
    }
  },
  { immediate: true, deep: true }
)

// 响应式状态
const windowWidth = ref(window?.innerWidth || 1024)

// 处理窗口大小变化
const handleResize = () => {
  windowWidth.value = window.innerWidth
}

// 响应式计算
const isMobile = computed(() => {
  return windowWidth.value < 1024
})

// 统一的菜单关闭处理
const closeMenus = (e) => {
  if (!e.target.closest('.resource-menu')) {
    resourceMenuOpen.value = false
  }
  if (!e.target.closest('.message-menu') && !e.target.closest('.message-button')) {
    showMessageMenu.value = false
  }
  if (!e.target.closest('.user-dropdown') && !e.target.closest('.user-button')) {
    showDropdown.value = false
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

// 直接从 store 获取状态
const isAuthenticated = computed(() => {
  // 同时检查登录状态和用户信息
  return authStore.isLoggedIn && accountStore.userInfo !== null
})

const username = computed(() => {
  if (!isAuthenticated.value) return ''
  return accountStore.username
})

const avatarUrl = computed(() => {
  if (!isAuthenticated.value) return defaultAvatar
  const avatar = accountStore.avatar
  if (!avatar || avatar === 'null' || avatar === 'undefined') {
    return defaultAvatar
  }
  // 检查 avatar 是否是完整的 URL 或 base64 数据
  if (avatar.startsWith('http') || avatar.startsWith('data:image')) {
    return avatar
  }
  // 如果是相对路径，则拼接基础 URL
  return avatar.startsWith('/') 
    ? `${process.env.VUE_APP_API_BASE_URL}${avatar}`
    : `${process.env.VUE_APP_API_BASE_URL}/${avatar}`
})

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
watch(() => authStore.isLoggedIn, (newValue) => {
  if (newValue) {
    fetchUnreadMessagesCount()
  } else {
    unreadMessagesCount.value = 0
  }
}, { immediate: true })

// 生命周期钩子
onMounted(async () => {
  document.addEventListener('click', closeMenus)
  window.addEventListener('resize', handleResize)
  
  // 检查登录状态
  const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
  const token = localStorage.getItem('token')
  
  if (isLoggedIn && token) {
    authStore.isLoggedIn = true
    request.defaults.headers.common['Authorization'] = `Bearer ${token}`
  }
  
  if (authStore.isLoggedIn) {
    try {
      await Promise.all([
        accountStore.fetchUserInfo(),
        fetchPointsInfo()
      ])
      console.log('Fetched User Info:', accountStore.userInfo)
    } catch (error) {
      console.error('Failed to fetch user info:', error)
    }
  }
  
  eventBus.on('avatar-updated', handleAvatarUpdate)
  
  // 监听支付成功事件
  window.addEventListener('payment-success', refreshUserInfo)
})

// 保持原有的事件清理
onUnmounted(() => {
  eventBus.off('avatar-updated', handleAvatarUpdate)
  // 移除支付成功事件监听
  window.removeEventListener('payment-success', refreshUserInfo)
})

// 简化头像更新处理方法
const handleAvatarUpdate = (newAvatar) => {
  if (accountStore.userInfo) {
    accountStore.userInfo = {
      ...accountStore.userInfo,
      avatar: newAvatar
    }
  }
}

// 修改会员状态相关的计算属性
const isVip = computed(() => {
  return accountStore.userInfo?.is_vip || false
})

// 会员类型文本
const vipTypeText = computed(() => {
  const userInfo = accountStore.userInfo
  if (!userInfo) return '普通用户'
  return userInfo.vip_status || '普通用户'
})

// 剩余天数文本
const remainingDays = computed(() => {
  const userInfo = accountStore.userInfo
  if (!userInfo?.is_vip || userInfo.vip_type === 'lifetime') return ''
  
  if (userInfo.vip_expire_time) {
    const expireDate = new Date(userInfo.vip_expire_time)
    const now = new Date()
    const diffDays = Math.floor((expireDate - now) / (1000 * 60 * 60 * 24))
    if (diffDays > 0) {
      return `剩余 ${diffDays} 天`
    }
  }
  return ''
})

// 会员按钮文本
const vipButtonText = computed(() => {
  const userInfo = accountStore.userInfo
  if (!userInfo?.is_vip) return '升级会员'
  
  if (userInfo.vip_type === 'lifetime') return '会员中心'
  
  if (userInfo.vip_expire_time) {
    const expireDate = new Date(userInfo.vip_expire_time)
    const now = new Date()
    const diffDays = Math.ceil((expireDate - now) / (1000 * 60 * 60 * 24))
    return diffDays <= 30 ? '续费会员' : '会员中心'
  }
  
  return '会员中心'
})

// 会员状态相关的计算属性
const isExpiringSoon = computed(() => {
  const userInfo = accountStore.userInfo
  if (!userInfo?.is_vip || userInfo.vip_type === 'lifetime') return false
  
  if (userInfo.vip_expire_time) {
    const expireDate = new Date(userInfo.vip_expire_time)
    const now = new Date()
    const diffDays = Math.ceil((expireDate - now) / (1000 * 60 * 60 * 24))
    return diffDays <= 30
  }
  return false
})

// 处理会员按钮点击
const handleVipButton = () => {
  const userInfo = accountStore.userInfo
  if (!userInfo?.is_vip) {
    router.push('/pro')
  } else if (isExpiringSoon.value) {
    router.push('/pro/renew')
  } else {
    router.push('/user?tab=membership')
  }
  showDropdown.value = false
}

// 用户菜单选项
const userMenuItems = computed(() => {
  return [
    {
      key: 'home',
      label: '用户中心',
      icon: 'home',
      action: () => {
        router.push('/user?tab=home')
        showDropdown.value = false
      }
    },
    {
      key: 'profile',
      label: '我的档案',
      icon: 'profile',
      action: () => {
        router.push('/user?tab=profile')
        showDropdown.value = false
      }
    },
    {
      key: 'resumes',
      label: '我的简历',
      icon: 'resumes',
      action: () => {
        router.push('/user?tab=resumes')
        showDropdown.value = false
      }
    },
    {
      key: 'settings',
      label: '账号设置',
      icon: 'settings',
      action: () => {
        router.push('/user?tab=settings')
        showDropdown.value = false
      }
    },
    {
      key: 'membership',
      label: '会员中心',
      icon: 'crown',
      action: () => {
        router.push('/user?tab=membership')
        showDropdown.value = false
      }
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
    showDropdown.value = false
    await authStore.logout()
    // 清除其他状态
    userBasicInfo.value = null
    unreadMessagesCount.value = 0
    messages.value = []
    mobileMenuOpen.value = false
    showMessageMenu.value = false
    resourceMenuOpen.value = false
    
    showToast('退出成功', 'success')
    
    const currentPath = router.currentRoute.value.fullPath
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

const refreshUserInfo = async () => {
  try {
    await accountStore.fetchUserInfo()
    console.log('Refreshed User Info:', accountStore.userInfo)
  } catch (error) {
    console.error('Failed to refresh user info:', error)
  }
}

// 积分信息
const pointsInfo = ref({
  balance: 0,
  level: 1,
  sign_in_days: 0,
  total_earned: 0
})

// 获取积分信息
const fetchPointsInfo = async () => {
  try {
    const response = await membership.getPointsInfo()
    if (response?.data?.code === 200) {
      pointsInfo.value = response.data.data
    }
  } catch (error) {
    console.error('获取积分信息失败:', error)
  }
}

// 合并重复的 onMounted
onMounted(async () => {
  // 添加事件监听
  document.addEventListener('click', handleClickOutside)
  window.addEventListener('resize', handleResize)
  
  try {
    await Promise.all([
      fetchPointsInfo(),
      accountStore.fetchUserInfo()
    ])
  } catch (error) {
    console.error('初始化数据失败:', error)
  }
})

onUnmounted(() => {
  // 移除全局点击事件监听
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('resize', handleResize)
  eventBus.off('avatar-updated', handleAvatarUpdate)
  window.removeEventListener('payment-success', refreshUserInfo)
})

// 处理菜单关闭
const closeDropdown = () => {
  showDropdown.value = false
}

// 处理点击详情按钮
const handleViewDetails = () => {
  router.push('/user?tab=membership')
  showDropdown.value = false
}

// 修改积分详情按钮的点击处理
const handlePointsDetail = () => {
  router.push('/user?tab=membership')
  showDropdown.value = false
}

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

/* 添加积分数字动画 */
@keyframes countUp {
  from {
    transform: translateY(10px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.text-amber-500 {
  animation: countUp 0.3s ease-out;
}
</style>