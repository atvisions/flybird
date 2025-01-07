<template>
  <div class="user-home w-full">
    <!-- 顶部背景和用户信息 -->
    <div class="relative">
      <!-- 背景图 -->
      <div class="h-48 bg-gradient-to-r from-gray-900 to-gray-800 relative group rounded-t-lg overflow-hidden">
        <div class="absolute inset-0 rounded-t-lg overflow-hidden">
          <img
            :src="userInfo.coverImage ? formatImageUrl(userInfo.coverImage) : defaultBackground"
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
        <!-- 头像上传区域 -->
        <div class="relative group w-20 h-20 mx-auto -mb-10 z-20">
          <img
            :src="userAvatar"
            class="w-20 h-20 rounded-full border-4 border-white object-cover"
            alt="头像"
            @error="handleImageError"
          />
          <div 
            @click="showAvatarUpload = true"
            class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-30 rounded-full opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer"
          >
            <CameraIcon class="w-6 h-6 text-white" />
          </div>
          <span 
            v-if="userInfo.gender" 
            class="absolute bottom-0 right-0 w-6 h-6 bg-white rounded-full flex items-center justify-center"
          >
            <!-- 性别图标 -->
          </span>
        </div>

        <div class="bg-white rounded-b-lg border border-gray-100 p-4 pb-6 transition-shadow hover:shadow-lg relative">
          <!-- 头像和基本身份信息区块 -->
          <div class="flex flex-col items-center relative z-10">
            <!-- 编辑资料按钮 -->
            <button 
              @click="openNicknameModal"
              class="absolute right-[-10px] top-[-30px] px-3 py-1 text-xs text-gray-500 hover:text-gray-900 border border-gray-200 rounded-full hover:bg-gray-50 transition-all flex items-center bg-white"
            >
              <PencilIcon class="w-3.5 h-3.5 mr-1" />
              编辑资料
            </button>

            <!-- 用户基本信息 -->
            <div class="flex flex-col items-center min-h-[5rem] pt-8">
              <div class="flex flex-col items-center space-y-3">
                <!-- 昵称 -->
                <div class="text-center">
                  <div class="inline-flex items-center group relative">
                    <h2 class="text-xl font-bold text-gray-900">{{ userInfo.nickname }}</h2>
                  </div>
                </div>
                <!-- 当前岗位 -->
                <div class="mt-1 flex items-center justify-center group">
                  <span v-if="userInfo.jobTitle" class="text-sm text-gray-600">{{ userInfo.jobTitle }}</span>
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
                  <button 
                    @click="router.push('/user?tab=profile')"
                    class="absolute -right-10 top-1/2 -translate-y-1/2 p-1 opacity-0 group-hover:opacity-50 transition-opacity rounded-full text-gray-400 hover:text-gray-900 hover:bg-gray-100"
                  >
                    <PencilIcon class="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            </div>
          </div>

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
      <div class="bg-white rounded-lg border border-gray-100 p-6 transition-shadow hover:shadow-lg">
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

    <!-- 昵称设置弹窗 -->
    <div v-if="showNicknameModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h3>修改昵称</h3>
          <button class="close-btn" @click="closeNicknameModal">
            <XMarkIcon class="w-5 h-5" />
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <input 
              type="text"
              v-model="nickname.state.value"
              placeholder="请输入新昵称"
              :disabled="nickname.state.loading"
              @input="validateNickname"
              :class="{ 'error': nickname.state.error }"
            />
            <!-- 错误提示 -->
            <div v-if="nickname.state.error" class="text-red-500 text-sm mt-1">
              {{ nickname.state.error }}
            </div>
            <!-- 简单的提示文字 -->
            <div class="text-gray-400 text-xs mt-1">
              昵称长度4-8个字符，可使用中文、英文字母、数字
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button 
            class="btn btn-default" 
            @click="closeNicknameModal"
            :disabled="nickname.state.loading"
          >
            取消
          </button>
          <button 
            class="btn btn-primary" 
            @click="handleNicknameUpdate"
            :disabled="nickname.state.loading"
          >
            {{ nickname.state.loading ? '更新中...' : '确认' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 添加头像上传弹窗 -->
    <AvatarUploadDialog
      v-model="showAvatarUpload"
      :loading="loading"
      @upload="handleAvatarUpload"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useStore } from 'vuex'
import { useNickname } from '@/composables/useNickname'
import { MEDIA_URL } from '@/config'
import defaultAvatarImage from '@/assets/images/default-avatar.png'
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
import profile from '@/api/profile'
import { eventBus } from '@/utils/eventBus'
import AvatarUploadDialog from '../dialogs/AvatarUploadDialog.vue'

const router = useRouter()
const store = useStore()
const nickname = useNickname()
const showNicknameModal = ref(false)

// 用户信息的计算属性
const userInfo = computed(() => {
  return {
    uid: store.state.userInfo?.data?.user?.uid,
    nickname: store.state.userInfo?.data?.user?.username,
    avatar: store.state.userInfo?.data?.basic_info?.avatar,
    isVip: store.state.userInfo?.data?.user?.is_vip,
    coverImage: store.state.userInfo?.data?.basic_info?.background,
    bio: store.state.userInfo?.data?.basic_info?.personal_summary,
    jobTitle: store.state.userInfo?.data?.job_intention?.job_title || null,
  }
})

// 格式化头像 URL
const formatImageUrl = (url) => {
  if (!url) return defaultAvatarImage
  return url.startsWith('http') ? url : `${MEDIA_URL}${url}`
}

// 计算头像 URL
const userAvatar = computed(() => {
  return formatImageUrl(userInfo.value?.avatar)
})

// 获取用户信息
const fetchUserInfo = async () => {
  try {
    // 从 store 中获取用户信息
    const userInfo = store.state.userInfo
    if (!userInfo) {
      await store.dispatch('getProfile')
    }
    // 从 store 中获取统计数据
    const stats = store.state.userInfo?.data?.stats || {}
    statistics.value = [
      { label: '关注', value: stats.following_count || '0' },
      { label: '粉丝', value: stats.followers_count || '0' },
      { label: '点赞', value: stats.likes_count || '0' },
      { label: '访问', value: stats.views_count || '0' }
    ]
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}

// 组件挂载时获取数据
onMounted(async () => {
  await fetchUserInfo()
})

// 头像上传相关
const showAvatarUpload = ref(false)
const loading = ref(false)

// 处理头像错误
const handleImageError = (e) => {
  e.target.src = defaultAvatarImage
}

// 处理背景图错误
const handleBackgroundError = (e) => {
  e.target.src = defaultBackground
}

const handleNicknameUpdate = async () => {
  const success = await nickname.handleUpdate()
  if (success) {
    closeNicknameModal()
    // 重新获取用户信息
    await store.dispatch('getProfile')
    eventBus.emit('user-info-updated')
  }
}

// 昵称修改相关方法
const openNicknameModal = () => {
  nickname.state.value = store.state.userInfo?.data?.user?.username || ''
  showNicknameModal.value = true
}

const closeNicknameModal = () => {
  showNicknameModal.value = false
  nickname.state.value = ''
}

// 实时验证昵称
const validateNickname = () => {
  nickname.state.error = nickname.validateNickname(nickname.state.value)
}

const handleAvatarUpload = async (file) => {
  try {
    loading.value = true
    const formData = new FormData()
    formData.append('avatar', file)
    
    const response = await profile.uploadAvatar(formData)
    if (response.data?.code === 200) {
      showToast('头像上传成功', 'success')
      const avatarUrl = response.data.data.avatar
      // 更新 store 中的用户信息
      store.commit('SET_USER_INFO', {
        ...store.state.userInfo,
        data: {
          ...store.state.userInfo.data,
          basic_info: {
            ...store.state.userInfo.data.basic_info,
            avatar: avatarUrl
          }
        }
      })
      // 触发全局事件
      eventBus.emit('avatar-updated', avatarUrl)
      showAvatarUpload.value = false
    } else {
      throw new Error(response.data?.message || '上传失败')
    }
  } catch (error) {
    console.error('头像上传失败:', error)
    showToast(error.message || '头像上传失败，请稍后重试', 'error')
  } finally {
    loading.value = false
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
const currentTab = ref('articles')
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
  e.target.src = defaultAvatarImage
}

const handleArticleImageError = (e) => {
  e.target.src = defaultAvatarImage
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
  // 创建文件输入框
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  
  // 监听文件选择
  input.onchange = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    
    try {
      loading.value = true
      const formData = new FormData()
      formData.append('background', file)
      
      const response = await profile.uploadBackground(formData)
      if (response.data?.code === 200) {
        showToast('背景图上传成功', 'success')
        const backgroundUrl = response.data.data.background
        // 更新 store 中的用户信息
        store.commit('SET_USER_INFO', {
          ...store.state.userInfo,
          data: {
            ...store.state.userInfo.data,
            basic_info: {
              ...store.state.userInfo.data.basic_info,
              background: backgroundUrl
            }
          }
        })
        // 触发全局事件
        eventBus.emit('background-updated', backgroundUrl)
      } else {
        throw new Error(response.data?.message || '上传失败')
      }
    } catch (error) {
      console.error('背景图上传失败:', error)
      showToast(error.message || '背景图上传失败，请稍后重试', 'error')
    } finally {
      loading.value = false
    }
  }
  
  // 触发文件选择
  input.click()
}

// 用户主页链接
const userProfileUrl = computed(() => {
  return `/u/${userInfo.value.uid}`
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

/* 其他已有的样式保持不变 */
</style> 