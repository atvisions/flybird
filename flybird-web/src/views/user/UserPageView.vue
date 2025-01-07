<template>
  <div class="user-page">
    <HeadView />
    <div class="pt-4 pb-20 sm:py-8 mt-[60px] md:mt-[72px]">
      <div class="max-w-7xl mx-auto px-2 sm:px-4 lg:px-8 grid grid-cols-1 lg:grid-cols-12 gap-4 lg:gap-8">
        <!-- 左侧个人信息栏 -->
        <div class="lg:col-span-3">
          <!-- 左侧固定区域 -->
          <div class="mb-4 lg:mb-0 lg:sticky lg:top-24">
            <!-- 个人信息卡片 -->
            <div class="bg-white rounded-xl shadow-lg overflow-hidden">
              <!-- 背景封面 -->
              <div class="h-24 sm:h-32 w-full">
                <img 
                  :src="userInfo.background || 'https://picsum.photos/1920/1080?random=1'" 
                  class="w-full h-full object-cover"
                  alt="背景图"
                >
              </div>
              
              <!-- 个人信息卡片 -->
              <div class="p-4 sm:p-6 -mt-12">
                <!-- 头像 -->
                <div class="flex justify-center">
                  <img 
                    :src="userInfo.avatar" 
                    class="w-20 h-20 sm:w-24 sm:h-24 rounded-full border-4 border-white shadow-lg"
                    alt="头像"
                  >
                </div>
                
                <!-- 基本信息 -->
                <div class="text-center mt-4">
                  <h1 class="text-lg sm:text-xl font-bold text-gray-900">{{ userInfo.name }}</h1>
                  <p class="text-sm text-gray-500 mt-1">UID: {{ userInfo.uid }}</p>
                  <p class="text-sm text-gray-500 mt-1">{{ userInfo.location }} · {{ userInfo.age }}岁</p>
                  <p class="text-sm text-gray-500 mt-2">{{ userInfo.bio }}</p>
                </div>
                
                <!-- 操作按钮 -->
                <div class="flex gap-2 mt-4 px-2 sm:px-0">
                  <button 
                    @click="handleFollow"
                    class="flex-1 py-2 bg-blue-600 text-white rounded-full text-sm font-medium hover:bg-blue-700"
                  >
                    {{ isFollowing ? '已关注' : '关注' }}
                  </button>
                  <button 
                    @click="handleMessage"
                    class="flex-1 py-2 bg-gray-100 text-gray-700 rounded-full text-sm font-medium hover:bg-gray-200"
                  >
                    私信
                  </button>
                </div>
                
                <!-- 社交统计 -->
                <div class="grid grid-cols-3 gap-2 sm:gap-4 mt-4 sm:mt-6 pt-4 sm:pt-6 border-t border-gray-100">
                  <button 
                    @click="() => { 
                      showUserList = true; 
                      userListType = 'followers';
                      currentTab = null;
                    }" 
                    class="text-center group"
                  >
                    <div class="text-lg font-bold text-gray-900">{{ stats.followers }}</div>
                    <div class="text-xs text-gray-500 group-hover:text-gray-700">粉丝</div>
                  </button>
                  <button 
                    @click="() => { 
                      showUserList = true; 
                      userListType = 'following';
                      currentTab = null;
                    }" 
                    class="text-center group"
                  >
                    <div class="text-lg font-bold text-gray-900">{{ stats.following }}</div>
                    <div class="text-xs text-gray-500 group-hover:text-gray-700">关注</div>
                  </button>
                  <button 
                    @click="() => { 
                      showUserList = true; 
                      userListType = 'visits';
                      currentTab = null;
                    }" 
                    class="text-center group"
                  >
                    <div class="text-lg font-bold text-gray-900">{{ stats.visits }}</div>
                    <div class="text-xs text-gray-500 group-hover:text-gray-700">访问</div>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 中间内容区 -->
        <div class="lg:col-span-6 space-y-3 sm:space-y-6 lg:pb-8">
          <!-- 作品集展示 -->
          <div class="bg-white rounded-xl shadow-lg overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-200">
              <h2 class="text-lg font-medium text-gray-900">作品集</h2>
            </div>
            <div class="p-4 sm:p-6">
              <PortfolioList :user-id="userInfo.uid" />
            </div>
          </div>

          <!-- 内容标签页 -->
          <div v-if="!showUserList" class="bg-white rounded-xl shadow">
            <!-- 标签页导航 -->
            <div class="border-b border-gray-200 overflow-x-auto">
              <nav class="flex whitespace-nowrap" aria-label="Tabs">
                <button
                  v-for="tab in tabs"
                  :key="tab.key"
                  @click="currentTab = tab.key"
                  class="flex-1 py-3 sm:py-4 px-4 border-b-2 font-medium text-sm text-center"
                  :class="[
                    currentTab === tab.key
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  ]"
                >
                  {{ tab.label }}
                </button>
              </nav>
            </div>

            <!-- 标签页内容 -->
            <div class="p-4 sm:p-6">
              <!-- 文章列表 -->
              <div v-if="currentTab === 'articles'" class="space-y-6">
                <article v-for="article in articles" :key="article.id" class="group">
                  <div class="flex items-center justify-between mb-2">
                    <h3 class="text-lg font-semibold text-gray-900 group-hover:text-blue-600">
                      {{ article.title }}
                    </h3>
                    <div class="hidden sm:flex items-center space-x-4 text-sm text-gray-500">
                      <span class="flex items-center">
                        <EyeIcon class="w-4 h-4 mr-1" />{{ article.views }}
                      </span>
                      <span class="flex items-center">
                        <ChatBubbleLeftIcon class="w-4 h-4 mr-1" />{{ article.comments }}
                      </span>
                      <span class="flex items-center">
                        <HandThumbUpIcon class="w-4 h-4 mr-1" />{{ article.likes }}
                      </span>
                    </div>
                  </div>
                  <!-- 移动端统计信息 -->
                  <div class="flex items-center space-x-4 text-xs text-gray-500 mt-2 sm:hidden">
                    <span class="flex items-center">
                      <EyeIcon class="w-3 h-3 mr-1" />{{ article.views }}
                    </span>
                    <span class="flex items-center">
                      <ChatBubbleLeftIcon class="w-3 h-3 mr-1" />{{ article.comments }}
                    </span>
                    <span class="flex items-center">
                      <HandThumbUpIcon class="w-3 h-3 mr-1" />{{ article.likes }}
                    </span>
                  </div>
                  <p class="text-gray-600 text-sm line-clamp-2">{{ article.description }}</p>
                  <div class="mt-2 flex items-center justify-between">
                    <div class="flex items-center space-x-2 text-sm text-gray-500">
                      <span>{{ article.createTime }}</span>
                      <span>·</span>
                      <span>{{ article.category }}</span>
                    </div>
                  </div>
                </article>
              </div>

              <!-- 粉丝列表 -->
              <div v-if="currentTab === 'followers'" class="space-y-4">
                <div v-for="user in followers" :key="user.id" 
                  class="flex items-center justify-between p-4 hover:bg-gray-50 rounded-lg transition-colors"
                >
                  <div class="flex items-center space-x-3">
                    <img :src="user.avatar" alt="头像" class="w-10 h-10 rounded-full">
                    <div>
                      <h3 class="text-sm font-medium text-gray-900">{{ user.name }}</h3>
                      <p class="text-sm text-gray-500">{{ user.bio || '这个人很懒，什么都没写~' }}</p>
                    </div>
                  </div>
                  <button 
                    class="px-4 py-2 text-sm font-medium text-blue-600 hover:bg-blue-50 rounded-full"
                  >
                    关注
                  </button>
                </div>
              </div>

              <!-- 关注列表 -->
              <div v-if="currentTab === 'following'" class="space-y-4">
                <div v-for="user in followingList" :key="user.id" 
                  class="flex items-center justify-between p-4 hover:bg-gray-50 rounded-lg transition-colors"
                >
                  <div class="flex items-center space-x-3">
                    <img :src="user.avatar" alt="头像" class="w-10 h-10 rounded-full">
                    <div>
                      <h3 class="text-sm font-medium text-gray-900">{{ user.name }}</h3>
                      <p class="text-sm text-gray-500">{{ user.bio || '这个人很懒，什么都没写~' }}</p>
                    </div>
                  </div>
                  <button 
                    class="px-4 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded-full"
                  >
                    已关注
                  </button>
                </div>
              </div>

              <!-- 访问列表 -->
              <div v-if="currentTab === 'visits'" class="space-y-4">
                <div v-for="user in visits" :key="user.id" 
                  class="flex items-center justify-between p-4 hover:bg-gray-50 rounded-lg transition-colors"
                >
                  <div class="flex items-center space-x-3">
                    <img :src="user.avatar" alt="头像" class="w-10 h-10 rounded-full">
                    <div>
                      <h3 class="text-sm font-medium text-gray-900">{{ user.name }}</h3>
                      <p class="text-sm text-gray-500">最近访问：{{ user.visitTime || '刚刚' }}</p>
                    </div>
                  </div>
                  <button 
                    class="px-4 py-2 text-sm font-medium text-blue-600 hover:bg-blue-50 rounded-full"
                  >
                    关注
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- 用户列表（独立板块） -->
          <div v-if="showUserList" class="bg-white rounded-xl shadow">
            <div class="flex items-center justify-between p-4 border-b border-gray-200">
              <h3 class="text-lg font-medium">
                {{ 
                  userListType === 'followers' ? '粉丝列表' : 
                  userListType === 'following' ? '关注列表' : 
                  '访问记录' 
                }}
              </h3>
              <button 
                @click="() => { 
                  showUserList = false; 
                  currentTab = 'articles';
                }" 
                class="text-gray-500 hover:text-gray-700"
              >
                <XMarkIcon class="w-5 h-5" />
              </button>
            </div>
            <div class="p-6">
              <div class="space-y-4">
                <div 
                  v-for="user in userListType === 'followers' ? followers : 
                           userListType === 'following' ? followingList : visits" 
                  :key="user.id" 
                  class="flex items-center justify-between p-4 hover:bg-gray-50 rounded-lg transition-colors"
                >
                  <div class="flex items-center space-x-3">
                    <img :src="user.avatar" alt="头像" class="w-10 h-10 rounded-full">
                    <div>
                      <h3 class="text-sm font-medium text-gray-900">{{ user.name }}</h3>
                      <p class="text-sm text-gray-500">
                        {{ 
                          userListType === 'visits' ? 
                          `最近访问：${user.visitTime || '刚刚'}` : 
                          user.bio || '这个人很懒，什么都没写~' 
                        }}
                      </p>
                    </div>
                  </div>
                  <button 
                    v-if="userListType !== 'following'"
                    class="px-4 py-2 text-sm font-medium text-blue-600 hover:bg-blue-50 rounded-full"
                  >
                    关注
                  </button>
                  <button 
                    v-else
                    class="px-4 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded-full"
                  >
                    已关注
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧广告区 -->
        <div class="lg:col-span-3">
          <!-- 分享版块 -->
          <div class="hidden lg:block bg-white rounded-xl shadow-lg p-6">
            <h3 class="text-sm font-medium text-gray-900 mb-4 flex items-center">
              <ShareIcon class="w-4 h-4 mr-2 text-gray-500" />
              分享主页
            </h3>
            
            <!-- 链接复制区域 -->
            <div class="flex items-center gap-2 mb-4">
              <div class="flex-1 bg-gray-50 px-3 py-2 rounded-lg text-sm text-gray-600 truncate">
                {{ pageUrl }}
              </div>
              <button 
                @click="copyLink"
                class="shrink-0 px-3 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg text-sm font-medium transition-colors flex items-center"
              >
                <DocumentDuplicateIcon class="w-4 h-4 mr-1.5" />
                复制
              </button>
            </div>
            
            <!-- 社交分享 -->
            <div class="flex items-center justify-between">
              <button 
                v-for="platform in sharePlatforms" 
                :key="platform.name"
                @click="shareToPlateform(platform.name)"
                class="flex flex-col items-center gap-1 group"
              >
                <div 
                  class="w-8 h-8 rounded-full flex items-center justify-center transition-colors"
                  :class="platform.bgClass"
                >
                  <component 
                    :is="platform.icon" 
                    class="w-4 h-4"
                    :class="platform.iconClass"
                  />
                </div>
                <span class="text-xs text-gray-500 group-hover:text-gray-700">
                  {{ platform.label }}
                </span>
              </button>
            </div>
          </div>

          <!-- 广告区 -->
          <div class="bg-white rounded-xl shadow-lg p-6 sticky top-24 md:mt-4">
            <h3 class="text-lg font-medium text-gray-900 mb-4">推荐职位</h3>
            <div class="space-y-4">
              <div v-for="job in recommendedJobs" :key="job.id" class="group">
                <div class="flex items-center justify-between">
                  <div>
                    <h4 class="text-sm font-medium text-gray-900 group-hover:text-blue-600">
                      {{ job.title }}
                    </h4>
                    <p class="text-sm text-gray-500">{{ job.company }}</p>
                  </div>
                  <div class="text-sm font-medium text-blue-600">
                    {{ job.salary }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <FootView class="hidden md:block" />

    <!-- 移动端导航抽屉遮罩 -->
    <div 
      v-if="isMobileMenuOpen" 
      class="fixed inset-0 bg-black bg-opacity-25 z-[60] lg:hidden"
      @click="isMobileMenuOpen = false"
    />

    <div 
      :class="[
        'fixed inset-y-0 right-0 w-full max-w-sm bg-white shadow-xl z-[70] transform transition-transform duration-300 ease-in-out lg:hidden',
        isMobileMenuOpen ? 'translate-x-0' : 'translate-x-full'
      ]"
    >
      <div class="h-full flex flex-col">
        <!-- 抽屉头部 -->
        <div class="px-4 py-3 border-b border-gray-200 flex items-center justify-between">
          <h2 class="text-lg font-medium text-gray-900">内容导航</h2>
          <button 
            @click="isMobileMenuOpen = false"
            class="text-gray-500 hover:text-gray-700"
          >
            <XMarkIcon class="w-6 h-6" />
          </button>
        </div>

        <!-- 导航内容 -->
        <div class="flex-1 overflow-y-auto">
          <!-- 主要导航选项 -->
          <div class="px-4 py-2">
            <div class="space-y-1">
              <button
                v-for="tab in tabs"
                :key="tab.key"
                @click="handleMobileTabChange(tab.key)"
                class="w-full flex items-center px-3 py-2 text-sm rounded-lg"
                :class="[
                  currentTab === tab.key
                    ? 'bg-blue-50 text-blue-600'
                    : 'text-gray-700 hover:bg-gray-50'
                ]"
              >
                {{ tab.label }}
              </button>
            </div>
          </div>

          <!-- 用户列表选项 -->
          <div class="px-4 py-2 border-t border-gray-200">
            <h3 class="px-3 text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
              用户列表
            </h3>
            <div class="space-y-1">
              <button
                v-for="option in userListOptions"
                :key="option.key"
                @click="handleMobileUserListChange(option.key)"
                class="w-full flex items-center justify-between px-3 py-2 text-sm rounded-lg"
                :class="[
                  userListType === option.key && showUserList
                    ? 'bg-blue-50 text-blue-600'
                    : 'text-gray-700 hover:bg-gray-50'
                ]"
              >
                <span>{{ option.label }}</span>
                <span class="text-sm font-medium">
                  {{ option.count }}
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 移动端底部工具栏 -->
    <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 lg:hidden safe-area-inset-bottom z-50">
      <div class="grid grid-cols-3 gap-8 px-6 py-3">
        <button 
          @click="handleMessage"
          class="flex flex-col items-center justify-center text-gray-600 active:text-blue-600"
        >
          <EnvelopeIcon class="w-6 h-6" />
          <span class="text-xs mt-1">私信</span>
        </button>
        <button 
          @click="handleFollow"
          class="flex flex-col items-center justify-center text-gray-600 active:text-blue-600"
        >
          <UserPlusIcon class="w-6 h-6" />
          <span class="text-xs mt-1">{{ isFollowing ? '已关注' : '关注' }}</span>
        </button>
        <button 
          @click="showShareMenu = true"
          class="flex flex-col items-center justify-center text-gray-600 active:text-blue-600"
        >
          <ShareIcon class="w-6 h-6" />
          <span class="text-xs mt-1">分享</span>
        </button>
      </div>
    </div>

    <!-- 移动端分享菜单 -->
    <div 
      v-if="showShareMenu"
      class="fixed inset-0 bg-black bg-opacity-50 z-[70] flex items-end lg:hidden"
      @click.self="showShareMenu = false"
    >
      <div class="bg-white w-full rounded-t-xl p-4 space-y-4 animate-slide-up">
        <div class="flex items-center justify-between mb-2">
          <h3 class="text-lg font-medium">分享主页</h3>
          <button @click="showShareMenu = false">
            <XMarkIcon class="w-6 h-6 text-gray-500" />
          </button>
        </div>
        
        <!-- 链接复制区域 -->
        <div class="flex items-center gap-2">
          <div class="flex-1 bg-gray-50 px-3 py-2 rounded-lg text-sm text-gray-600 truncate">
            {{ pageUrl }}
          </div>
          <button 
            @click="copyLink"
            class="shrink-0 px-3 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg text-sm font-medium"
          >
            复制
          </button>
        </div>
        
        <!-- 社交分享按钮 -->
        <div class="grid grid-cols-4 gap-4 py-2">
          <button 
            v-for="platform in sharePlatforms" 
            :key="platform.name"
            @click="shareToPlateform(platform.name)"
            class="flex flex-col items-center gap-2"
          >
            <div 
              class="w-12 h-12 rounded-full flex items-center justify-center"
              :class="platform.bgClass"
            >
              <component 
                :is="platform.icon" 
                class="w-6 h-6"
                :class="platform.iconClass"
              />
            </div>
            <span class="text-xs text-gray-500">
              {{ platform.label }}
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import HeadView from '@/components/HeadView.vue'
import FootView from '@/components/FootView.vue'
import PortfolioList from '@/components/portfolio/PortfolioList.vue'
import {
  CalendarIcon,
  EyeIcon,
  ChatBubbleLeftIcon,
  HandThumbUpIcon,
  UserPlusIcon,
  EnvelopeIcon,
  ShareIcon,
  LinkIcon,
  DocumentDuplicateIcon,
  XMarkIcon,
  Bars3Icon
} from '@heroicons/vue/24/outline'
import WeiboIcon from '@/components/icons/WeiboIcon.vue'
import WechatIcon from '@/components/icons/WechatIcon.vue'
import QQIcon from '@/components/icons/QQIcon.vue'
import TwitterIcon from '@/components/icons/TwitterIcon.vue'
import { showToast } from '@/components/ToastMessage'

const route = useRoute()
const username = route.params.username

// 控制状态
const showShareMenu = ref(false)
const showFollowers = ref(false)
const showFollowing = ref(false)
const showVisits = ref(false)
const isFollowing = ref(false)
const activeList = ref('followers')

// 用户信息
const userInfo = ref({
  name: username,
  uid: '10086',
  age: 25,
  location: '北京',
  avatar: 'https://picsum.photos/200/200?random=1',
  bio: '前端开发工程师，热爱技术分享',
  joinDate: '2023-12-01',
  background: 'https://picsum.photos/1920/1080?random=1',
  email: 'example@flybird.com'
})

// 统计数据
const stats = ref({
  articles: 12,
  questions: 8,
  topics: 5,
  followers: 128,
  following: 56,
  visits: 1234
})

// 标签页配置
const tabs = [
  { key: 'articles', label: '文章' },
  { key: 'questions', label: '问答' },
  { key: 'topics', label: '话题' }
]

const currentTab = ref('articles')

// 文章列表数据
const articles = ref([
  {
    id: 1,
    title: '2024年前端开发趋势展望',
    description: '探讨新的前端框架、工具和最佳实践，帮助开发者在新的一年保持技术领先。',
    category: '前端开发',
    createTime: '2小时前',
    views: 1234,
    comments: 56,
    likes: 89
  },
  {
    id: 2,
    title: 'Vue3与React的对比分析',
    description: '深入分析Vue3和React在性能、易用性和生态系统方面的优劣。',
    category: '前端开发',
    createTime: '3小时前',
    views: 987,
    comments: 34,
    likes: 76
  },
  {
    id: 3,
    title: 'JavaScript性能优化技巧',
    description: '分享一些实用的JavaScript性能优化技巧，提升前端应用的响应速度。',
    category: 'JavaScript',
    createTime: '5小时前',
    views: 876,
    comments: 45,
    likes: 67
  },
  {
    id: 4,
    title: 'CSS Grid布局指南',
    description: '全面介绍CSS Grid布局的使用方法和最佳实践，帮助开发者构建复杂布局。',
    category: 'CSS',
    createTime: '1天前',
    views: 654,
    comments: 23,
    likes: 54
  },
  {
    id: 5,
    title: '前端工程化的未来',
    description: '探讨前端工程化的发展趋势和未来方向，帮助开发者做好技术储备。',
    category: '前端工程化',
    createTime: '2天前',
    views: 543,
    comments: 12,
    likes: 45
  },
  {
    id: 6,
    title: '使用TypeScript提升代码质量',
    description: '介绍TypeScript的基本用法和优势，帮助开发者编写更健壮的代码。',
    category: 'TypeScript',
    createTime: '3天前',
    views: 432,
    comments: 34,
    likes: 56
  },
  {
    id: 7,
    title: '前端测试框架对比',
    description: '对比Jest、Mocha和Cypress等前端测试框架，帮助开发者选择合适的工具。',
    category: '测试',
    createTime: '4天前',
    views: 321,
    comments: 23,
    likes: 34
  },
  {
    id: 8,
    title: 'Web安全最佳实践',
    description: '分享一些Web安全的最佳实践，帮助开发者保护应用免受攻击。',
    category: '安全',
    createTime: '5天前',
    views: 210,
    comments: 12,
    likes: 23
  },
  {
    id: 9,
    title: '前端性能监控工具推荐',
    description: '推荐一些前端性能监控工具，帮助开发者实时监控应用性能。',
    category: '性能监控',
    createTime: '6天前',
    views: 109,
    comments: 11,
    likes: 12
  },
  {
    id: 10,
    title: '如何优化前端构建速度',
    description: '分享一些优化前端构建速度的方法，提升开发效率。',
    category: '构建工具',
    createTime: '1周前',
    views: 98,
    comments: 10,
    likes: 11
  }
])

// 推荐职位数据
const recommendedJobs = ref([
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
])

// 粉丝列表数据
const followers = ref([
  { id: 1, name: '张三', avatar: 'https://picsum.photos/32/32?random=1' },
  { id: 2, name: '李四', avatar: 'https://picsum.photos/32/32?random=2' },
  { id: 3, name: '王五', avatar: 'https://picsum.photos/32/32?random=3' }
])

// 关注列表数据
const followingList = ref([
  { id: 1, name: '赵六', avatar: 'https://picsum.photos/32/32?random=4' },
  { id: 2, name: '钱七', avatar: 'https://picsum.photos/32/32?random=5' },
  { id: 3, name: '孙八', avatar: 'https://picsum.photos/32/32?random=6' }
])

// 访问列表数据
const visits = ref([
  { id: 1, name: '周九', avatar: 'https://picsum.photos/32/32?random=7' },
  { id: 2, name: '吴十', avatar: 'https://picsum.photos/32/32?random=8' },
  { id: 3, name: '郑十一', avatar: 'https://picsum.photos/32/32?random=9' }
])

// 当前显示的用户列表
const activeUsers = computed(() => {
  switch (activeList.value) {
    case 'followers':
      return followers.value
    case 'following':
      return followingList.value
    case 'visits':
      return visits.value
    default:
      return []
  }
})

// 格式化加入日期
const formatJoinDate = (date) => {
  return new Date(date).toLocaleDateString('zh-CN', { year: 'numeric', month: 'long' })
}

// 获取用户数据
const fetchUserData = async () => {
  try {
    // TODO: 调用API获取用户数据
    // const response = await api.getUserProfile(username)
    // userInfo.value = response.data
  } catch (error) {
    console.error('获取用户数据失败:', error)
  }
}

// 处理关注
const handleFollow = () => {
  isFollowing.value = !isFollowing.value
  // TODO: 调用关注/取消关注 API
  showToast(isFollowing.value ? '关注成功' : '已取消关注', 'success')
}

// 处理私信
const handleMessage = () => {
  // TODO: 实现私信功能
  showToast('私信功能开发中...', 'info')
}

// 页面URL
const pageUrl = computed(() => `${window.location.origin}/u/${username}`)

// 分享平台配置
const sharePlatforms = [
  {
    name: 'weixin',
    label: '微信',
    icon: WechatIcon,
    bgClass: 'bg-green-50 group-hover:bg-green-100',
    iconClass: 'text-green-600'
  },
  {
    name: 'weibo',
    label: '微博',
    icon: WeiboIcon,
    bgClass: 'bg-red-50 group-hover:bg-red-100',
    iconClass: 'text-red-600'
  },
  {
    name: 'qq',
    label: 'QQ',
    icon: QQIcon,
    bgClass: 'bg-blue-50 group-hover:bg-blue-100',
    iconClass: 'text-blue-600'
  },
  {
    name: 'twitter',
    label: 'Twitter',
    icon: TwitterIcon,
    bgClass: 'bg-sky-50 group-hover:bg-sky-100',
    iconClass: 'text-sky-600'
  }
]

// 分享到社交平台
const shareToPlateform = (platform) => {
  const shareText = `${userInfo.value.name}的个人主页`
  const url = encodeURIComponent(pageUrl.value)
  
  switch (platform) {
    case 'weibo':
      window.open(`http://service.weibo.com/share/share.php?url=${url}&title=${shareText}`)
      break
    case 'twitter':
      window.open(`https://twitter.com/intent/tweet?text=${shareText}&url=${url}`)
      break
    case 'qq':
      window.open(`http://connect.qq.com/widget/shareqq/index.html?url=${url}&title=${shareText}`)
      break
    case 'weixin':
      showToast('请使用微信扫描二维码分享', 'info')
      break
  }
}

// 复制链接
const copyLink = async () => {
  try {
    await navigator.clipboard.writeText(pageUrl.value)
    showToast('链接已复制到剪贴板', 'success')
  } catch (error) {
    showToast('复制失败，请手动复制', 'error')
  }
}

// 用户列表显示状态
const showUserList = ref(false)
const userListType = ref('')  // 'followers' | 'following' | 'visits'

// 移动端菜单状态
const isMobileMenuOpen = ref(false)

// 用户列表选项配置
const userListOptions = computed(() => [
  { 
    key: 'followers', 
    label: '粉丝列表',
    count: stats.value.followers 
  },
  { 
    key: 'following', 
    label: '关注列表',
    count: stats.value.following 
  },
  { 
    key: 'visits', 
    label: '访问记录',
    count: stats.value.visits 
  }
])

// 处理移动端标签切换
const handleMobileTabChange = (key) => {
  currentTab = key
  showUserList = false
  isMobileMenuOpen = false
}

// 处理移动端用户列表切换
const handleMobileUserListChange = (key) => {
  userListType = key
  showUserList = true
  currentTab = null
  isMobileMenuOpen = false
}

onMounted(() => {
  fetchUserData()
})
</script>

<style scoped>
.user-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 确保移动端底部导航不会遮挡内容 */
@media (max-width: 1024px) {
  .user-page {
    padding-bottom: calc(env(safe-area-inset-bottom) + 64px);
  }
  
  .safe-area-inset-bottom {
    padding-bottom: env(safe-area-inset-bottom);
  }
}

/* 处理标签页滚动条 */
.overflow-x-auto {
  scrollbar-width: none;  /* Firefox */
  -ms-overflow-style: none;  /* IE and Edge */
}

.overflow-x-auto::-webkit-scrollbar {
  display: none;  /* Chrome, Safari and Opera */
}

.user-page > div:nth-child(2) {
  flex: 1;
}

.animate-slide-up {
  animation: slide-up 0.3s ease-out;
}

@keyframes slide-up {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}
</style> 