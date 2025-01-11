<template>
  <div class="user-home w-full">
    <!-- 顶部背景和用户信息 -->
    <div class="relative">
      <!-- 背景图 - 降低高度并优化渐变 -->
      <div class="h-40 bg-gradient-to-r from-gray-900 to-gray-800 relative group rounded-t-lg overflow-hidden">
        <div class="absolute inset-0 rounded-t-lg overflow-hidden">
          <img
            :src="backgroundUrl"
            class="w-full h-full object-cover opacity-60"
            alt="背景图"
            @error="handleBackgroundError"
          />
          <!-- 添加渐变遮罩 -->
          <div class="absolute inset-0 bg-gradient-to-b from-transparent to-black/30"></div>
        </div>
        <!-- 背景图上传按钮 - 调整位置和样式 -->
        <div 
          class="absolute top-3 right-3 p-1.5 rounded-full bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer hover:bg-black/50"
          @click="handleBackgroundUpload"
        >
          <CameraIcon class="w-4 h-4 text-white" />
        </div>
      </div>
      
      <!-- 用户信息卡片 - 优化布局和间距 -->
      <div class="-mt-8 relative z-10">
        <!-- 头像和基本身份信息区块 -->
        <div 
          class="relative group w-16 h-16 mx-auto -mb-8 z-20 cursor-pointer"
          @click="openEditModal"
        >
          <img
            :src="userAvatar"
            class="w-16 h-16 rounded-full border-4 border-white object-cover shadow-md"
            alt="头像"
            @error="handleImageError"
          />
          <!-- 优化悬停效果 -->
          <div class="absolute inset-0 flex items-center justify-center bg-black/40 rounded-full opacity-0 group-hover:opacity-100 transition-opacity">
            <PencilIcon class="w-5 h-5 text-white" />
          </div>
        </div>

        <div class="bg-white rounded-b-lg border border-gray-100 p-4 transition-shadow hover:shadow-sm">
          <!-- 用户基本信息 - 简化布局 -->
          <div class="flex flex-col items-center pt-6">
            <!-- 编辑资料按钮 - 调整位置和样式 -->
            <div class="absolute right-3 top-3 flex items-center space-x-2">
              <!-- 个人主页链接 - 新位置 -->
              <a
                :href="userProfileUrl"
                target="_blank"
                class="px-2.5 py-1 text-xs text-gray-500 hover:text-gray-700 border border-gray-200 rounded-full hover:bg-gray-50 transition-all flex items-center bg-white/80 backdrop-blur-sm"
              >
                <GlobeAltIcon class="w-3 h-3 mr-1" />
                主页
              </a>
              
              <button 
                @click="openEditModal"
                class="px-2.5 py-1 text-xs text-gray-500 hover:text-gray-700 border border-gray-200 rounded-full hover:bg-gray-50 transition-all flex items-center bg-white/80 backdrop-blur-sm"
              >
                <PencilIcon class="w-3 h-3 mr-1" />
                编辑
              </button>
            </div>

            <!-- 用户基本信息 - 优化间距和排版 -->
            <div class="flex flex-col items-center space-y-2">
              <h2 class="text-lg font-bold text-gray-900">{{ userInfo.username }}</h2>
              <div class="text-sm text-gray-600">{{ userInfo.position || '未设置职位' }}</div>
              <!-- 个人简介 - 优化样式 -->
              <div class="mt-2 max-w-lg text-center">
                <p class="text-sm text-gray-500 leading-relaxed">
                  {{ userInfo.bio || '这个人还没有填写个人简介' }}
                </p>
              </div>
            </div>

            <!-- 统计数据 - 简化显示 -->
            <div class="grid grid-cols-4 gap-4 mt-4 w-full max-w-xl">
              <div 
                v-for="stat in statistics" 
                :key="stat.label"
                class="text-center"
              >
                <div class="text-base font-medium text-gray-900">{{ stat.value }}</div>
                <div class="text-xs text-gray-500">{{ stat.label }}</div>
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
        <div v-if="portfolios?.length > 0" class="grid grid-cols-2 gap-6">
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
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAccountStore } from '@/stores/account'
import config from '@/config'
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

// 使用 getters 获取用户信息
const userInfo = computed(() => ({
  uid: accountStore.uid,
  username: accountStore.username,
  avatar: accountStore.avatar,
  background: accountStore.background,
  bio: accountStore.bio || null,
  position: accountStore.position || null
}))

// 添加背景图 URL 的计算属性
const backgroundUrl = computed(() => {
  const bgImage = userInfo.value?.background
  return bgImage ? formatImageUrl(bgImage) : defaultBackground
})

// 格式化图片 URL
const formatImageUrl = (url) => {
  if (!url || url === 'null') return defaultAvatarImage
  return url.startsWith('http') ? url : `${process.env.VUE_APP_API_BASE_URL}${url}`
}

// 计算头像 URL
const userAvatar = computed(() => {
  return formatImageUrl(userInfo.value?.avatar)
})

// 在编辑弹窗中显示头像
const editAvatarUrl = computed(() => {
  return formatImageUrl(editForm.value.avatar || userInfo.value?.avatar)
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

// 作品集数据初始化为空数组而不是 undefined
const portfolios = ref([])

// 获取作品集数据
const fetchPortfolios = async () => {
  try {
    const response = await portfolio.getUserPortfolios()
    if (response?.data?.code === 200) {
      portfolios.value = response.data.data || []
    }
  } catch (error) {
    console.error('获取作品集失败:', error)
    portfolios.value = []
  }
}

// 在组件挂载时获取数据
onMounted(async () => {
  // ... 其他代码保持不变 ...
  try {
    await Promise.all([
      fetchUserInfo(),
      fetchPortfolios()
    ])
  } catch (error) {
    console.error('初始化数据失败:', error)
  }
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
    const formData = new FormData()
    formData.append('avatar', file)
    
    // 使用 accountStore 更新头像
    await accountStore.updateAvatar(formData)
    editForm.value.avatar = accountStore.avatar
    showToast('头像上传成功', 'success')
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
