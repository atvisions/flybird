<template>
  <div class="editor-toolbar">
    <!-- 左侧基础操作按钮 -->
    <div class="toolbar-left">
      <button class="toolbar-btn" @click="$emit('undo')" :disabled="!canUndo">
        <Undo theme="outline" :size="16" />
        <span>撤销</span>
      </button>
      <button class="toolbar-btn" @click="$emit('redo')" :disabled="!canRedo">
        <Redo theme="outline" :size="16" />
        <span>重做</span>
      </button>
      <button class="toolbar-btn" @click="$emit('clear')">
        <Clear theme="outline" :size="16" />
        <span>清空</span>
      </button>
    </div>

    <!-- 右侧操作按钮 -->
    <div class="toolbar-right">
      <!-- 模板编辑模式 -->
      <template v-if="showTemplateButtons">
        <button class="toolbar-btn" @click="handleSaveDraft">
          <Save theme="outline" :size="16" />
          <span>保存草稿</span>
        </button>
        <button class="toolbar-btn primary" @click="handleSubmitReview">
          <Save theme="outline" :size="16" />
          <span>提交审核</span>
        </button>
      </template>

      <!-- 简历创建/编辑模式 -->
      <template v-if="showResumeButtons">
        <button class="toolbar-btn" @click="handleSaveDraft">
          <Save theme="outline" :size="16" />
          <span>保存草稿</span>
        </button>
        <button class="toolbar-btn primary" @click="handleSave('publish')">
          <Save theme="outline" :size="16" />
          <span>{{ $route.name === 'resume-edit' ? '发布简历' : '创建简历' }}</span>
        </button>
      </template>

      <!-- 用户头像和下拉菜单 -->
      <div class="relative" ref="dropdownRef">
        <button 
          @click.stop="toggleDropdown"
          class="ml-4 flex items-center cursor-pointer"
        >
          <div class="relative">
            <img 
              :src="avatarUrl"
              class="h-8 w-8 rounded-full object-cover"
              alt="用户头像"
              @error="handleImageError"
            />
            <!-- VIP 标识 -->
            <div v-if="isVip" 
              class="absolute -top-1 -right-1 w-4 h-4 bg-[#FFB800] rounded-full flex items-center justify-center border border-white shadow-sm"
            >
              <span class="text-[10px] font-bold text-white">V</span>
            </div>
          </div>
          <ChevronDownIcon 
            class="h-5 w-5 ml-1"
            :class="{ 'rotate-180': showDropdown }"
          />
        </button>

        <!-- 下拉菜单 -->
        <div 
          v-if="showDropdown"
          class="absolute right-0 top-[48px] w-48 bg-white shadow-xl rounded-xl overflow-hidden border border-gray-100 z-50"
        >
          <!-- 用户信息头部 -->
          <div class="px-4 py-3 border-b border-gray-100">
            <div class="flex items-center space-x-3">
              <img 
                :src="avatarUrl"
                class="h-10 w-10 rounded-full object-cover"
                alt="用户头像"
              />
              <div>
                <div class="text-sm font-medium text-gray-900">{{ username }}</div>
                <div class="text-xs" :class="{ 'text-[#1A56DB]': isVip }">
                  {{ vipTypeText }}
                </div>
              </div>
            </div>
          </div>

          <!-- 菜单项 -->
          <div class="py-2">
            <router-link 
              to="/user?tab=home"
              class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
              @click="showDropdown = false"
            >
              <UserIcon class="w-5 h-5 mr-3 text-gray-400" />
              个人中心
            </router-link>
            <router-link 
              to="/user?tab=resumes"
              class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
              @click="showDropdown = false"
            >
              <DocumentTextIcon class="w-5 h-5 mr-3 text-gray-400" />
              我的简历
            </router-link>
            <router-link 
              to="/user?tab=account"
              class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
              @click="showDropdown = false"
            >
              <Cog6ToothIcon class="w-5 h-5 mr-3 text-gray-400" />
              账号设置
            </router-link>
          </div>

          <!-- 分割线 -->
          <div class="border-t border-gray-100"></div>

          <!-- 退出登录 -->
          <div class="py-2">
            <button 
              @click="handleLogout"
              class="flex items-center w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50"
            >
              <ArrowRightOnRectangleIcon class="w-5 h-5 mr-3" />
              退出登录
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 添加保存模板弹窗 -->
  <SaveTemplateDialog
    v-model:visible="showSaveDialog"
    :mode="saveMode"
    :type="currentMode.value"
    :template-data="props.currentTemplate"
    @save="handleSaveTemplate"
  />
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useAccountStore } from '@/stores/account'
import defaultAvatar from '@/assets/images/default-avatar.png'
import { Undo, Redo, Clear, Save, Delete, Back, Next, Plus, Minus } from '@icon-park/vue-next'
import { 
  UserIcon, 
  DocumentTextIcon, 
  Cog6ToothIcon, 
  ArrowRightOnRectangleIcon,
  ChevronDownIcon 
} from '@heroicons/vue/24/outline'
import { showToast } from '@/components/ToastMessage'
import config from '@/config'
import SaveTemplateDialog from './SaveTemplateDialog.vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  canUndo: {
    type: Boolean,
    default: false
  },
  canRedo: {
    type: Boolean,
    default: false
  },
  scale: {
    type: Number,
    default: 1
  },
  mode: {
    type: String,
    default: 'create', // 'create' | 'edit' | 'use'
  },
  resumeId: {
    type: [String, Number],
    default: null
  },
  buttonText: {
    type: String,
    default: '保存模板'
  },
  currentTemplate: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['clear', 'save', 'undo', 'redo', 'scale-change', 'create-resume'])
const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const accountStore = useAccountStore()
const dropdownRef = ref(null)
const showDropdown = ref(false)

// 用户相关的计算属性
const username = computed(() => accountStore.username || '')
const isVip = computed(() => accountStore.userInfo?.is_vip || false)
const vipTypeText = computed(() => {
  if (!isVip.value) return '普通用户'
  return accountStore.userInfo?.vip_type === 'annual' ? '年度会员' : '月度会员'
})

const avatarUrl = computed(() => {
  const avatar = accountStore.userInfo?.avatar
  if (!avatar) return defaultAvatar
  if (avatar.startsWith('http') || avatar.startsWith('data:image')) {
    return avatar
  }
  const cleanPath = avatar.replace(/^\/?(media\/)?/, '')
  return `${config.mediaURL}/${cleanPath}`
})

// 处理图片加载错误
const handleImageError = (e) => {
  if (e.target) {
    e.target.src = defaultAvatar
  }
}

// 切换下拉菜单
const toggleDropdown = (e) => {
  if (e) {
    e.stopPropagation()
  }
  showDropdown.value = !showDropdown.value
}

// 处理点击外部关闭下拉菜单
const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event?.target)) {
    showDropdown.value = false
  }
}

// 处理退出登录
const handleLogout = async () => {
  try {
    showDropdown.value = false
    await authStore.logout()
    showToast('退出成功', 'success')
    router.push('/login')
  } catch (error) {
    console.error('退出失败:', error)
    showToast('退出失败，请重试', 'error')
  }
}

// 添加保存模板弹窗的显示状态和模式
const showSaveDialog = ref(false)
const saveMode = ref('')

// 根据路由获取当前模式
const currentMode = computed(() => {
  const routeName = route.name
  if (routeName === 'template-edit' || routeName === 'template-create') {
    return 'template'
  } else if (routeName === 'resume-create-from-template' || routeName === 'resume-create' || routeName === 'resume-edit') {
    return 'resume'
  }
  return ''
})

// 是否显示模板相关按钮
const showTemplateButtons = computed(() => currentMode.value === 'template')

// 是否显示简历相关按钮
const showResumeButtons = computed(() => currentMode.value === 'resume')

// 处理保存
const handleSave = (action) => {
  emit('save', { mode: currentMode.value, action })
}

// 处理从模板创建简历
const handleCreateResume = () => {
  const templateId = route.params.id
  router.push({
    name: 'resume-create-from-template',
    params: { templateId }
  })
}

// 处理保存草稿
const handleSaveDraft = () => {
  if (currentMode.value === 'template') {
    // 模板编辑模式：显示保存模板弹窗
    saveMode.value = 'draft'
    showSaveDialog.value = true
  } else {
    // 简历模式：直接触发保存
    handleSave('draft')
  }
}

// 处理提交审核
const handleSubmitReview = () => {
  if (currentMode.value === 'template') {
    // 模板编辑模式：显示保存模板弹窗
    saveMode.value = 'submit'
    showSaveDialog.value = true
  } else {
    // 简历模式：直接触发保存
    handleSave('submit')
  }
}

// 添加保存模板的处理函数
const handleSaveTemplate = (templateData) => {
  const data = {
    ...templateData,
    status: saveMode.value === 'draft' ? 0 : 2, // 草稿:0, 待审核:2
  }
  
  emit('save', { type: currentMode.value, action: saveMode.value, data })
  showSaveDialog.value = false
  showToast(saveMode.value === 'draft' ? '保存草稿成功' : '提交审核成功', 'success')
}

// 使用 ref 来存储事件监听器，以便在组件卸载时正确移除
const clickOutsideHandler = (event) => {
  handleClickOutside(event)
}

onMounted(() => {
  document.addEventListener('click', clickOutsideHandler)
})

onUnmounted(() => {
  document.removeEventListener('click', clickOutsideHandler)
  // 确保在组件卸载时重置状态
  showDropdown.value = false
})

// 最小和最大缩放比例
const MIN_SCALE = 0.1
const MAX_SCALE = 3

// 处理缩放
const handleZoomIn = () => {
  if (props.scale < MAX_SCALE) {
    emit('scale-change', Math.min(props.scale + 0.1, MAX_SCALE))
  }
}

const handleZoomOut = () => {
  if (props.scale > MIN_SCALE) {
    emit('scale-change', Math.max(props.scale - 0.1, MIN_SCALE))
  }
}

// 导航方法
const goToUserCenter = () => {
  router.push('/user?tab=home')
}

const goToMyResumes = () => {
  router.push('/user?tab=resumes')
}

// 用户头像
const userAvatar = computed(() => accountStore.userInfo?.avatar || '')
</script>

<style scoped>
@import '../styles/editor.css';
@import '../styles/controls.css';

.editor-toolbar {
  height: 48px;
  padding: 0 16px;
  background-color: #fff;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  position: relative;
  z-index: 10;
}

.toolbar-left {
  flex: 1;
}

.toolbar-right {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: flex-end;
}

.toolbar-btn {
  height: 32px;
  padding: 0 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  background: #fff;
  color: #333;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: all 0.3s;
}

.toolbar-btn:hover:not(:disabled) {
  color: #1890ff;
  border-color: #1890ff;
}

.toolbar-btn:disabled {
  cursor: not-allowed;
  color: #d9d9d9;
  background: #f5f5f5;
}

.iconfont {
  font-size: 14px;
}

/* 添加用户头像和下拉菜单样式 */
.rotate-180 {
  transform: rotate(180deg);
  transition: transform 0.2s ease;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  border-radius: 4px;
  transition: all 0.3s;
}

.btn-primary {
  background-color: #1890ff;
  color: white;
}

.btn-primary:hover {
  background-color: #40a9ff;
}

/* 添加头像按钮样式 */
.relative {
  position: relative;
}

button {
  outline: none;
}

button:focus {
  outline: none;
}

.ml-4 {
  margin-left: 1rem;
}

/* 确保下拉菜单在最上层 */
.z-50 {
  z-index: 50;
}

/* 添加过渡动画 */
.transition-transform {
  transition-property: transform;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

/* 工具提示样式 */
.tooltip-container {
  position: relative;
}

.tooltip {
  visibility: hidden;
  position: absolute;
  bottom: -30px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.75);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  white-space: nowrap;
  z-index: 100;
  opacity: 0;
  transition: opacity 0.2s, visibility 0.2s;
}

.tooltip::before {
  content: '';
  position: absolute;
  top: -4px;
  left: 50%;
  transform: translateX(-50%);
  border-width: 0 4px 4px 4px;
  border-style: solid;
  border-color: transparent transparent rgba(0, 0, 0, 0.75) transparent;
}

.tooltip-container:hover .tooltip {
  visibility: visible;
  opacity: 1;
}

/* 禁用状态下不显示工具提示 */
.icon-button:disabled + .tooltip,
.btn:disabled + .tooltip {
  display: none;
}

.btn-text {
  margin-left: 4px;
  font-size: 14px;
}

.toolbar-btn.primary {
  background-color: #1890ff;
  color: white;
  border-color: #1890ff;
}

.toolbar-btn.primary:hover {
  background-color: #40a9ff;
  border-color: #40a9ff;
}

.scale-control {
  margin-left: 16px;
}

.user-menu {
  margin-left: 16px;
}

.user-avatar {
  cursor: pointer;
}
</style> 