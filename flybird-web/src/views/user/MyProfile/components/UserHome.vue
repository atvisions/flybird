<template>
  <div class="user-home w-full">
    <div v-if="isLoading" class="flex items-center justify-center py-20">
      <div class="text-gray-500">加载中...</div>
    </div>
    <template v-else-if="userInfo">
      <!-- 原有的模板内容 -->
      <div class="relative">
        <!-- 背景图 -->
        <div class="h-48 bg-gradient-to-r from-gray-900 to-gray-800 relative group rounded-t-lg overflow-hidden">
          <div class="absolute inset-0 rounded-t-lg overflow-hidden">
            <img
              :src="backgroundUrl"
              class="w-full h-full object-cover opacity-70"
              alt="背景图"
              @error="handleBackgroundError"
            />
          </div>
          <!-- 背景图上传按钮 -->
          <div 
            class="absolute top-4 right-4 p-2 rounded-full bg-black/30 opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer"
            @click="handleBackgroundUpload"
          >
            <CameraIcon class="w-5 h-5 text-white" />
          </div>
        </div>
        
        <!-- 用户信息卡片 -->
        <div class="-mt-10 relative z-10">
          <!-- 头像和基本身份信息区块 -->
          <div 
            class="relative group w-20 h-20 mx-auto -mb-10 z-20 cursor-pointer"
            @click="openEditModal"
          >
            <img
              :src="userAvatar"
              class="w-20 h-20 rounded-full border-4 border-white object-cover shadow-lg"
              alt="头像"
              @error="handleImageError"
            />
            <!-- 添加悬停效果 -->
            <div class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-30 rounded-full opacity-0 group-hover:opacity-100 transition-opacity">
              <PencilIcon class="w-6 h-6 text-white" />
            </div>
          </div>

          <div class="bg-white rounded-b-lg border border-gray-100 p-4 pb-6 transition-shadow hover:shadow-lg relative">
            <!-- 头像和基本身份信息区块 -->
            <div class="flex flex-col items-center relative z-10">
              <!-- 编辑资料按钮 -->
              <button 
                @click="openEditModal"
                class="absolute right-[-10px] top-[-30px] px-3 py-1 text-xs text-gray-500 hover:text-gray-900 border border-gray-200 rounded-full hover:bg-gray-50 transition-all flex items-center bg-white"
              >
                <PencilIcon class="w-3.5 h-3.5 mr-1" />
                编辑资料
              </button>

              <!-- 用户基本信息 -->
              <div class="flex flex-col items-center min-h-[5rem] pt-8">
                <div class="flex flex-col items-center space-y-3">
                  <!-- 用户名 -->
                  <div class="text-center">
                    <div class="inline-flex items-center group relative">
                      <h2 class="text-xl font-bold text-gray-900">{{ userInfo.username }}</h2>
                    </div>
                  </div>
                  <!-- 当前岗位 -->
                  <div class="mt-1 flex items-center justify-center group">
                    <span v-if="userInfo.position" class="text-sm text-gray-600">{{ userInfo.position }}</span>
                    <span v-else class="text-sm text-gray-400">未设置职位</span>
                  </div>
                  <!-- 个人简介 -->
                  <div class="mt-2 group relative">
                    <div class="relative">
                      <!-- 左引号装饰 -->
                      <span class="absolute -left-4 -top-2 text-gray-300 text-xl font-serif">"</span>
                      <p v-if="userInfo.bio" 
                        class="text-sm text-gray-500 max-w-xl px-6 py-3 bg-gray-50/80 rounded-lg"
                      >
                        {{ userInfo.bio }}
                      </p>
                      <p v-else 
                        class="text-sm text-gray-400 italic px-6 py-3 bg-gray-50/80 rounded-lg"
                      >
                        这个人还没有填写个人简介
                      </p>
                      <!-- 右引号装饰 -->
                      <span class="absolute -right-4 -bottom-2 text-gray-300 text-xl font-serif">"</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="bg-white rounded-b-lg border border-gray-100 p-4 pb-6 transition-shadow hover:shadow-lg relative">
              <!-- 统计数据 -->
              <div class="grid grid-cols-4 gap-4 mt-6 pt-6 border-t border-gray-100 relative z-10">
                <div 
                  v-for="stat in statistics" 
                  :key="stat.label"
                  class="text-center"
                >
                  <div class="text-base font-semibold text-gray-900">{{ stat.value }}</div>
                  <div class="text-xs text-gray-500">{{ stat.label }}</div>
                </div>
                <!-- 个人主页链接 -->
                <div class="col-span-4 flex justify-center mt-4 relative z-10">
                  <a
                    :href="userProfileUrl"
                    target="_blank"
                    class="inline-flex items-center text-xs text-gray-500 hover:text-gray-900 transition-colors group"
                  >
                    <GlobeAltIcon class="w-4 h-4 mr-1.5 text-gray-400 group-hover:text-gray-900" />
                    查看个人主页
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 功能入口区域 -->
      <div class="mt-6 space-y-6 relative z-0">
        <!-- 作品集 -->
        <div class="bg-white rounded-lg border border-gray-100 p-6 transition-shadow hover:shadow-lg">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-base font-medium text-gray-900 flex items-center">
              <PhotoIcon class="w-5 h-5 mr-2 text-gray-900" />
              作品集
            </h3>
            <button
              @click="router.push('/portfolio/create')"
              class="flex items-center text-xs font-medium text-gray-900 hover:text-gray-700 transition-colors"
            >
              <PlusIcon class="w-4 h-4 mr-1" />
              发布
              <ChevronRightIcon class="w-4 h-4 ml-1" />
            </button>
          </div>

          <!-- 存储空间使用情况 -->
          <div class="flex items-center mb-6 px-1">
            <div class="flex items-center justify-between w-full">
              <div class="flex items-center">
                <span class="text-xs text-gray-500">存储空间：</span>
                <span class="text-sm font-medium text-gray-900">{{ formatStorage(storageUsed) }}</span>
                <span class="text-xs text-gray-400 ml-1">/</span>
                <span class="text-xs text-gray-400 ml-1">10GB</span>
              </div>
              <!-- 进度条 -->
              <div class="flex-1 h-1.5 bg-gray-100 rounded-full overflow-hidden mx-6">
                <div 
                  class="h-full rounded-full transition-all duration-300"
                  :class="storageUsedPercent > 80 ? 'bg-red-500' : 'bg-blue-500'"
                  :style="{ width: `${storageUsedPercent}%` }"
                ></div>
              </div>
              <span class="text-xs text-gray-500">{{ storageUsedPercent }}%</span>
            </div>
          </div>

          <!-- 作品卡片网格 -->
          <div v-if="portfolios.length > 0" class="grid grid-cols-2 gap-6">
            <!-- 作品卡片 -->
            <div
              v-for="portfolio in portfolios"
              :key="portfolio.id"
              class="group relative bg-white rounded-xl border border-gray-100 overflow-hidden hover:shadow-lg transition-all duration-300"
            >
              <!-- 操作按钮 -->
              <div class="absolute top-3 right-3 flex items-center space-x-2 z-10">
                <button
                  @click.stop="handleEditPortfolio(portfolio)"
                  class="p-1.5 rounded-full bg-white/90 hover:bg-white shadow-sm transition-colors"
                >
                  <PencilSquareIcon class="w-4 h-4 text-gray-700" />
                </button>
                <button
                  @click.stop="handleDeletePortfolio(portfolio)"
                  class="p-1.5 rounded-full bg-white/90 hover:bg-white shadow-sm transition-colors"
                >
                  <TrashIcon class="w-4 h-4 text-gray-700" />
                </button>
              </div>

              <div class="relative aspect-w-1 aspect-h-1 overflow-hidden">
                <img 
                  :src="portfolio.cover" 
                  class="w-full h-full object-cover transition-transform group-hover:scale-105"
                  @error="handlePortfolioImageError"
                  @click="router.push(`/portfolio/${portfolio.id}`)"
                />
              </div>
              <div class="p-4">
                <h4 class="text-sm font-medium text-gray-900 mb-1">{{ portfolio.title }}</h4>
                <div class="flex items-center justify-between text-xs text-gray-500">
                  <span>{{ portfolio.category }}</span>
                  <div class="flex items-center space-x-2">
                    <EyeIcon class="w-4 h-4" />
                    <span>{{ portfolio.views }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- 空状态展示 -->
          <div 
            v-else 
            class="flex flex-col items-center justify-center py-12 px-4 border border-gray-100 rounded-xl"
          >
            <img 
              src="https://api.iconify.design/solar:gallery-minimalistic-linear.svg" 
              class="w-16 h-16 text-gray-300 mb-4"
            />
            <p class="text-sm text-gray-500 mb-2">还没有作品集展示</p>
            <p class="text-xs text-gray-400">去作品集管理页面创建你的第一个作品集吧</p>
          </div>
        </div>

        <!-- 创作内容模块 -->
        <div 
          ref="creationSection"
          class="bg-white rounded-lg border border-gray-100 p-6 transition-shadow hover:shadow-lg"
        >
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-base font-medium text-gray-900 flex items-center">
              <PencilSquareIcon class="w-5 h-5 mr-2 text-gray-900" />
              我的创作
            </h3>
            <button
              @click="router.push('/article/create')"
              class="flex items-center text-xs font-medium text-gray-900 hover:text-gray-700 transition-colors"
            >
              <PlusIcon class="w-4 h-4 mr-1" />
              发布
              <ChevronRightIcon class="w-4 h-4 ml-1" />
            </button>
          </div>
          
          <!-- 创作类型切换 -->
          <div class="flex items-center space-x-6 mb-6 border-b border-gray-100">
            <button
              v-for="tab in contentTabs"
              :key="tab.key"
              class="pb-3 px-1 text-sm font-medium transition-colors relative"
              :class="currentTab === tab.key ? 'text-gray-900' : 'text-gray-500 hover:text-gray-700'"
              @click="currentTab = tab.key"
            >
              {{ tab.label }}
              <span 
                v-if="tab.count" 
                class="ml-1 text-xs text-gray-400"
              >({{ tab.count }})</span>
              <div 
                v-if="currentTab === tab.key"
                class="absolute bottom-0 left-0 right-0 h-0.5 bg-gray-900"
              ></div>
            </button>
          </div>

          <!-- 文章列表 -->
          <div v-if="currentTab === 'articles'" class="space-y-4">
            <div
              v-for="article in articles"
              :key="article.id"
              class="group flex items-start space-x-4 p-4 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <img
                v-if="article.cover"
                :src="article.cover"
                class="w-24 h-16 object-cover rounded cursor-pointer"
                @error="handleArticleImageError"
                @click="router.push(`/article/${article.id}`)"
              />
              <div class="flex-1 min-w-0 cursor-pointer" @click="router.push(`/article/${article.id}`)">
                <h4 class="text-sm font-medium text-gray-900 mb-1 line-clamp-1 group-hover:text-indigo-600 transition-colors">{{ article.title }}</h4>
                <p class="text-xs text-gray-500 line-clamp-2">{{ article.summary }}</p>
                <div class="flex items-center justify-between mt-2">
                  <div class="flex items-center space-x-4">
                    <span class="text-xs text-gray-400">{{ formatDate(article.created_at) }}</span>
                    <div class="flex items-center space-x-2 text-xs text-gray-400">
                      <EyeIcon class="w-3.5 h-3.5" />
                      <span>{{ article.views }}</span>
                    </div>
                  </div>
                  <!-- 操作按钮 -->
                  <div class="flex items-center space-x-2">
                    <button
                      @click.stop="handleEditArticle(article)"
                      class="p-1.5 rounded-full text-gray-400 hover:text-gray-900 transition-colors"
                    >
                      <PencilSquareIcon class="w-4 h-4" />
                    </button>
                    <button
                      @click.stop="handleDeleteArticle(article)"
                      class="p-1.5 rounded-full text-gray-400 hover:text-red-600 transition-colors"
                    >
                      <TrashIcon class="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 话题列表 -->
          <div v-else-if="currentTab === 'topics'" class="flex flex-col items-center justify-center py-12">
            <div class="w-16 h-16 mb-4 text-gray-200">
              <ChatBubbleLeftRightIcon />
            </div>
            <p class="text-sm text-gray-500 mb-2">还没有发布过话题</p>
            <button
              @click="router.push('/topic/create')"
              class="mt-2 text-xs text-gray-900 hover:text-gray-700 transition-colors flex items-center"
            >
              <PlusIcon class="w-4 h-4 mr-1" />
              发起新话题
            </button>
          </div>
          
          <!-- 问答列表 -->
          <div v-else-if="currentTab === 'qa'" class="flex flex-col items-center justify-center py-12">
            <div class="w-16 h-16 mb-4 text-gray-200">
              <QuestionMarkCircleIcon />
            </div>
            <p class="text-sm text-gray-500 mb-2">还没有参与问答</p>
            <button
              @click="router.push('/qa/ask')"
              class="mt-2 text-xs text-gray-900 hover:text-gray-700 transition-colors flex items-center"
            >
              <PlusIcon class="w-4 h-4 mr-1" />
              提出问题
            </button>
          </div>
          
          <!-- 草稿箱 -->
          <div v-else-if="currentTab === 'drafts'" class="flex flex-col items-center justify-center py-12">
            <div class="w-16 h-16 mb-4 text-gray-200">
              <InboxArrowDownIcon />
            </div>
            <p class="text-sm text-gray-500 mb-2">草稿箱是空的</p>
            <p class="text-xs text-gray-400">未完成的创作会自动保存在这里</p>
          </div>
        </div>

        <!-- 我的收藏模块 -->
        <div class="bg-white rounded-lg border border-gray-100 p-6 transition-shadow hover:shadow-lg">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-base font-medium text-gray-900 flex items-center">
              <BookmarkIcon class="w-5 h-5 mr-2 text-gray-900" />
              我的收藏
            </h3>
          </div>
          
          <!-- 收藏类型切换 -->
          <div class="flex items-center space-x-6 mb-6 border-b border-gray-100">
            <button
              v-for="tab in favoritesTabs"
              :key="tab.key"
              class="pb-3 px-1 text-sm font-medium transition-colors relative"
              :class="currentFavTab === tab.key ? 'text-gray-900' : 'text-gray-500 hover:text-gray-700'"
              @click="currentFavTab = tab.key"
            >
              {{ tab.label }}
              <span 
                v-if="tab.count" 
                class="ml-1 text-xs text-gray-400"
              >({{ tab.count }})</span>
              <div 
                v-if="currentFavTab === tab.key"
                class="absolute bottom-0 left-0 right-0 h-0.5 bg-gray-900"
              ></div>
            </button>
          </div>
          
          <!-- 空状态展示 -->
          <div class="flex flex-col items-center justify-center py-12">
            <div class="w-16 h-16 mb-4 text-gray-200">
              <BookmarkIcon />
            </div>
            <p class="text-sm text-gray-500 mb-2">还没有收藏任何{{ getCurrentFavTabLabel() }}</p>
            <button
              @click="router.push(getFavoritesExploreRoute())"
              class="mt-2 text-xs text-gray-900 hover:text-gray-700 transition-colors flex items-center"
            >
              <ArrowTopRightOnSquareIcon class="w-4 h-4 mr-1" />
              去发现{{ getCurrentFavTabLabel() }}
            </button>
          </div>
        </div>
      </div>

      <!-- 编辑资料弹窗 -->
      <Transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="opacity-0 scale-95"
        enter-to-class="opacity-100 scale-100"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="opacity-100 scale-100"
        leave-to-class="opacity-0 scale-95"
      >
        <div v-if="showEditModal" class="modal-overlay">
          <div class="modal-content">
            <div class="modal-header">
              <h3>编辑个人资料</h3>
              <button class="close-btn" @click="closeEditModal">
                <XMarkIcon class="w-5 h-5" />
              </button>
            </div>
            <div class="modal-body">
              <!-- 头像上传 -->
              <div class="form-group">
                <label class="form-label">头像</label>
                <div class="flex items-center space-x-4">
                  <div class="relative group">
                    <img
                      :src="editAvatarUrl"
                      class="w-20 h-20 rounded-full object-cover border-2 border-gray-200"
                      alt="头像"
                      @error="handleImageError"
                    />
                    <div 
                      @click="handleAvatarSelect"
                      class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-30 rounded-full opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer"
                    >
                      <CameraIcon class="w-6 h-6 text-white" />
                    </div>
                  </div>
                  <input
                    ref="avatarInput"
                    type="file"
                    accept="image/*"
                    class="hidden"
                    @change="handleAvatarChange"
                  />
                  <div class="text-sm text-gray-500">
                    <p>点击头像更换</p>
                    <p class="text-xs mt-1">建议使用正面免冠证件照</p>
                  </div>
                </div>
              </div>
              
              <!-- 用户名 -->
              <div class="form-group">
                <label class="form-label">用户名</label>
                <input 
                  type="text"
                  v-model="editForm.username"
                  placeholder="请输入用户名"
                  :class="{ 'error': usernameError }"
                  :disabled="loading"
                  @input="validateUsername"
                />
                <div v-if="usernameError" class="text-xs text-red-500 mt-1">
                  {{ usernameError }}
                </div>
                <!-- 提示文字 -->
                <div class="text-gray-400 text-xs mt-1">
                  用户名长度4-11个字符，可使用中文、英文字母、数字
                </div>
              </div>
              
              <!-- 职位 -->
              <div class="form-group">
                <label class="form-label">当前职位</label>
                <input 
                  type="text"
                  v-model="editForm.position"
                  placeholder="请输入您的职位"
                  :disabled="loading"
                />
              </div>
              
              <!-- 个人简介 -->
              <div class="form-group">
                <label class="form-label">个人简介</label>
                <textarea
                  v-model="editForm.bio"
                  placeholder="请输入个人简介"
                  :disabled="loading"
                  rows="4"
                  class="form-textarea"
                ></textarea>
              </div>
            </div>
            <div class="modal-footer">
              <button 
                class="btn btn-default" 
                @click="closeEditModal"
                :disabled="loading"
              >
                取消
              </button>
              <button 
                class="btn btn-primary" 
                @click="handleProfileUpdate"
                :disabled="loading"
              >
                {{ loading ? '更新中...' : '确认' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </template>
    <div v-else class="flex items-center justify-center py-20">
      <div class="text-gray-500">暂无数据</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, nextTick, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAccountStore } from '@/stores/account'
import config from '@/config'
import defaultAvatar from '@/assets/images/default-avatar.png'
import defaultBackground from '@/assets/images/default-background.jpg'
import { showToast } from '@/components/ToastMessage'
import {
  CameraIcon,        // 用于头像和背景上传
  PhotoIcon,         // 作品集图标
  PencilSquareIcon,  // 编辑图标
  TrophyIcon,        // 会员图标
  SparklesIcon,      // 升级会员图标
  PencilIcon,        // 编辑昵称图标
  ChevronRightIcon,  // 箭头图标
  PlusIcon,          // 添加图标
  TrashIcon,         // 删除图标
  ChatBubbleLeftRightIcon,  // 话题图标
  QuestionMarkCircleIcon,   // 问答图标
  InboxArrowDownIcon,       // 草稿箱图标
  EyeIcon,                  // 查看图标
  BookmarkIcon,            // 收藏图标
  ArrowTopRightOnSquareIcon, // 外链图标
  GlobeAltIcon,            // 个人主页图标
  XMarkIcon               // 关闭图标
} from '@heroicons/vue/24/outline'
import { user } from '@/api/user'
import { eventBus } from '@/utils/eventBus'

const router = useRouter()
const route = useRoute()
const accountStore = useAccountStore()
const showEditModal = ref(false)
const editForm = ref({
  username: '',
  position: '',
  bio: '',
  avatar: null
})
const avatarInput = ref(null)
const usernameError = ref('')
const creationSection = ref(null)

// 添加加载状态
const isLoading = ref(true)

// 使用 getters 获取用户信息
const userInfo = computed(() => {
  const info = accountStore.userInfo
  if (!info) return null
  return {
    uid: info.uid,
    username: info.username,
    avatar: info.avatar,
    background: info.background_image,
    bio: info.bio || null,
    position: info.position || null
  }
})

// 计算头像 URL
const userAvatar = computed(() => {
  if (!userInfo.value?.avatar) return defaultAvatar
  if (userInfo.value.avatar.startsWith('http') || userInfo.value.avatar.startsWith('data:image')) {
    return userInfo.value.avatar
  }
  return userInfo.value.avatar.startsWith('/media') 
    ? `${config.API_URL}${userInfo.value.avatar}`
    : `${config.API_URL}/media/${userInfo.value.avatar}`
})

// 编辑头像 URL 的计算属性
const editAvatarUrl = computed(() => {
  const avatarUrl = editForm.value.avatar || userInfo.value?.avatar
  if (!avatarUrl) return defaultAvatar
  if (avatarUrl.startsWith('http') || avatarUrl.startsWith('data:image')) {
    return avatarUrl
  }
  return avatarUrl.startsWith('/media') 
    ? `${config.API_URL}${avatarUrl}`
    : `${config.API_URL}/media/${avatarUrl}`
})

// 添加背景图 URL 的计算属性
const backgroundUrl = computed(() => {
  if (!userInfo.value?.background) return defaultBackground
  if (userInfo.value.background.startsWith('http') || userInfo.value.background.startsWith('data:image')) {
    return userInfo.value.background
  }
  return userInfo.value.background.startsWith('/media') 
    ? `${config.API_URL}${userInfo.value.background}`
    : `${config.API_URL}/media/${userInfo.value.background}`
})

// 获取用户信息
const fetchUserInfo = async () => {
  try {
    // 只在 store 中没有数据时获取
    if (!accountStore.userInfo) {
      await accountStore.fetchUserInfo()
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}

// 滚动到创作区域
const scrollToCreation = () => {
  if (creationSection.value) {
    const offset = 100 // 可以根据需要调整这个值
    const elementPosition = creationSection.value.getBoundingClientRect().top
    const offsetPosition = elementPosition + window.pageYOffset - offset
    
    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    })
  }
}

// 监听路由参数变化
watch(
  () => route.query.currentTab,
  (newTab) => {
    if (newTab === 'articles' || newTab === 'drafts') {
      // 等待 DOM 更新后滚动
      nextTick(() => {
        scrollToCreation()
      })
    }
  },
  { immediate: true }
)

// 组件挂载时获取数据
onMounted(async () => {
  try {
    isLoading.value = true
    await accountStore.fetchUserInfo()
    
    // 如果当前是文章或草稿标签，滚动到创作区域
    if (route.query.currentTab === 'articles' || route.query.currentTab === 'drafts') {
      nextTick(() => {
        scrollToCreation()
      })
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
    showToast('获取用户信息失败，请刷新页面重试', 'error')
  } finally {
    isLoading.value = false
  }
})

// 头像上传相关
const showAvatarUpload = ref(false)
const loading = ref(false)

// 处理头像错误
const handleImageError = (e) => {
  e.target.src = defaultAvatar
}

// 处理背景图错误
const handleBackgroundError = (e) => {
  e.target.src = defaultBackground
}

// 处理个人资料更新
const handleProfileUpdate = async () => {
  if (!validateUsername()) return
  
  try {
    loading.value = true
    // 准备更新数据
    const updateData = {
      username: editForm.value.username.trim(),
      position: editForm.value.position?.trim() || '',
      bio: editForm.value.bio?.trim() || '',
      phone: accountStore.phone,
      email: accountStore.email
    }
    
    console.log('Submitting update:', updateData)
      
    const response = await accountStore.updateUserInfo(updateData)
      
    // 使用后端返回的数据更新表单
    if (response?.data?.code === 200) {
      const userData = response.data.data
      editForm.value = {
        username: userData.username,
        position: userData.position || '',
        bio: userData.bio || '',
        avatar: userData.avatar
      }
    }
      
    showToast('更新成功', 'success')
    closeEditModal()
  } catch (error) {
    console.error('更新失败:', error)
    showToast(error.message || '更新失败，请稍后重试', 'error')
  } finally {
    loading.value = false
  }
}

// 实时验证用户名
const validateUsername = () => {
  const value = editForm.value.username
  if (!value) {
    usernameError.value = '用户名不能为空'
  } else if (value.length < 4 || value.length > 11) {
    usernameError.value = '用户名长度必须在4-11个字符之间'
  } else if (!/^[\u4e00-\u9fa5a-zA-Z0-9]+$/.test(value)) {
    usernameError.value = '用户名只能包含中文、英文字母和数字'
  } else {
    usernameError.value = ''
  }
  return !usernameError.value
}

// 打开编辑弹窗时初始化表单数据
const openEditModal = () => {
  editForm.value = {
    username: userInfo.value.username || '',
    position: userInfo.value.position || '',
    bio: userInfo.value.bio || '',
    avatar: userInfo.value.avatar || null
  }
  showEditModal.value = true
}

// 关闭编辑弹窗
const closeEditModal = () => {
  showEditModal.value = false
  editForm.value = {
    username: '',
    position: '',
    bio: '',
    avatar: null
  }
  usernameError.value = ''
}

const handleAvatarChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  // 验证文件
  if (!file.type.startsWith('image/')) {
    showToast('请选择图片文件', 'error')
    return
  }
  
  const maxSize = 2 * 1024 * 1024 // 2MB
  if (file.size > maxSize) {
    showToast('图片大小不能超过2MB', 'error')
    return
  }
  
  try {
    loading.value = true
    
    // 直接使用 user API 上传头像
    const response = await user.updateAvatar(file)
    
    if (response.data.code === 200) {
      const newAvatar = response.data.data.avatar
      // 更新 accountStore 中的头像
      await accountStore.fetchUserInfo()
      // 更新编辑表单中的头像
      editForm.value.avatar = newAvatar
      showToast('头像上传成功', 'success')
      
      // 触发全局事件，通知其他组件（如 HeadView）更新头像
      eventBus.emit('avatar-updated', newAvatar)
    }
  } catch (error) {
    console.error('头像上传失败:', error)
    showToast(error.message || '头像上传失败，请稍后重试', 'error')
  } finally {
    loading.value = false
    // 清空文件选择器
    event.target.value = ''
  }
}

// 格式化存储空间大小
const formatStorage = (bytes) => {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
}

// 存储空间使用数据
const storageUsed = ref(0)  // 字节数
const storageUsedPercent = computed(() => {
  const maxStorage = 10 * 1024 * 1024 * 1024 // 10GB in bytes
  return Math.round((storageUsed.value / maxStorage) * 100)
})

// 统计数据
const statistics = ref([
  { label: '关注', value: '0' },
  { label: '粉丝', value: '0' },
  { label: '点赞', value: '0' },
  { label: '访问', value: '0' }
])

// 内容相关数据
const currentTab = ref(route.query.currentTab || 'articles')
const articles = ref([])
const portfolios = ref([])

// 收藏相关数据
const currentFavTab = ref('portfolios')
const favoritesTabs = [
  { key: 'portfolios', label: '作品集' },
  { key: 'articles', label: '文章' },
  { key: 'topics', label: '话题' }
]

// 内容标签
const contentTabs = [
  { key: 'articles', label: '文章', count: 0 },
  { key: 'topics', label: '话题', count: 0 },
  { key: 'qa', label: '问答', count: 0 },
  { key: 'drafts', label: '草稿箱', count: 0 }
]

// 获取当前收藏标签的标签文本
const getCurrentFavTabLabel = () => {
  const tab = favoritesTabs.find(tab => tab.key === currentFavTab.value)
  return tab ? tab.label : ''
}

// 获取收藏探索路由
const getFavoritesExploreRoute = () => {
  const routes = {
    portfolios: '/explore/portfolios',
    articles: '/explore/articles',
    topics: '/explore/topics'
  }
  return routes[currentFavTab.value] || '/explore'
}

// 处理图片错误
const handlePortfolioImageError = (e) => {
  e.target.src = defaultAvatar
}

const handleArticleImageError = (e) => {
  e.target.src = defaultAvatar
}

// 格式化日期
const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 处理背景图上传
const handleBackgroundUpload = async () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  
  input.onchange = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    
    try {
      loading.value = true
      const formData = new FormData()
      formData.append('background', file)
      
      await accountStore.updateBackground(formData)
      showToast('背景图上传成功', 'success')
    } catch (error) {
      console.error('背景图上传失败:', error)
      showToast(error.message || '背景图上传失败，请稍后重试', 'error')
    } finally {
      loading.value = false
      input.value = ''
    }
  }
  
  input.click()
}

// 用户主页链接
const userProfileUrl = computed(() => {
  return `/u/${userInfo.value.uid}`
})

// 监听路由参数变化，更新当前标签页
watch(
  () => route.query.currentTab,
  (newTab) => {
    if (newTab) {
      currentTab.value = newTab
    }
  }
)

// 处理头像选择
const handleAvatarSelect = () => {
  avatarInput.value?.click()
}

// 监听头像更新事件
onMounted(() => {
  eventBus.on('avatar-updated', async () => {
    await accountStore.fetchUserInfo()
  })
})

onUnmounted(() => {
  eventBus.off('avatar-updated')
})
</script>

<style scoped>
/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
}

.modal-content {
  position: relative;
  width: 91.666667%;
  max-width: 28rem;
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.modal-header {
  padding: 1rem 1.5rem;
  background-color: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
  border-top-left-radius: 0.5rem;
  border-top-right-radius: 0.5rem;
}

.modal-header h3 {
  margin: 0;
  color: #111827;
  font-size: 1.125rem;
  font-weight: 500;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1rem 1.5rem;
  background-color: #f9fafb;
  border-top: 1px solid #e5e7eb;
  border-bottom-left-radius: 0.5rem;
  border-bottom-right-radius: 0.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group input {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  line-height: 1.25rem;
  color: #111827;
  background-color: white;
  transition: border-color 0.15s ease-in-out;
}

.form-group input:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 1px #6366f1;
}

.form-group input:disabled {
  background-color: #f3f4f6;
  cursor: not-allowed;
}

.btn {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  border-radius: 0.375rem;
  transition: all 0.15s ease-in-out;
}

.btn-default {
  color: #374151;
  background-color: white;
  border: 1px solid #d1d5db;
}

.btn-default:not(:disabled):hover {
  background-color: #f9fafb;
}

.btn-primary {
  color: white;
  background-color: #6366f1;
  border: 1px solid transparent;
}

.btn-primary:not(:disabled):hover {
  background-color: #4f46e5;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 关闭按钮样式 */
.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.25rem;
  color: #6b7280;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: color 0.15s ease-in-out;
}

.close-btn:hover {
  color: #374151;
}

.form-group input.error {
  border-color: #ef4444;
}

.form-group input.error:focus {
  border-color: #ef4444;
  box-shadow: 0 0 0 1px #ef4444;
}

/* 添加新的样式 */
.form-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.form-textarea {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  line-height: 1.25rem;
  color: #111827;
  background-color: white;
  transition: border-color 0.15s ease-in-out;
  resize: vertical;
  min-height: 5rem;
}

.form-textarea:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 1px #6366f1;
}

.form-textarea:disabled {
  background-color: #f3f4f6;
  cursor: not-allowed;
}

/* 其他已有的样式保持不变 */
</style> 
