<template>
  <div class="editor-toolbar">
    <!-- 左侧返回和标题 -->
    <div class="toolbar-left">
      <button class="toolbar-btn back-btn" @click="handleBack">
        <Back theme="outline" :size="16" />
        <span>返回</span>
      </button>
      <div class="template-title">
        {{ currentTemplate?.name || '未命名模板' }}
      </div>
    </div>

    <!-- 中间撤销重做按钮 -->
    <div class="toolbar-center">
      <div class="undo-redo-group">
        <button class="toolbar-btn" @click="$emit('undo')" :disabled="!canUndo">
          <Undo theme="outline" :size="16" />
          <span>撤销</span>
        </button>
        <button class="toolbar-btn" @click="$emit('redo')" :disabled="!canRedo">
          <Redo theme="outline" :size="16" />
          <span>重做</span>
        </button>
      </div>
    </div>

    <!-- 右侧操作按钮 -->
    <div class="toolbar-right">
      <!-- 模板编辑模式 -->
      <template v-if="showTemplateButtons">
        <button class="toolbar-btn" @click="handlePrintPreview">
          <Printer theme="outline" :size="16" />
          <span>打印预览</span>
        </button>
        <button class="toolbar-btn primary" @click="handleSubmitReview">
          <Save theme="outline" :size="16" />
          <span>保存模板</span>
        </button>
      </template>

      <!-- 简历创建/编辑模式 -->
      <template v-if="showResumeButtons">
        <button class="toolbar-btn" @click="handlePrintPreview">
          <Printer theme="outline" :size="16" />
          <span>打印预览</span>
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
  <EditTemplateDialog
    v-model="showSaveDialog"
    :mode="saveMode"
    :template="currentTemplate"
    @confirm="handleSaveTemplate"
  />
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useAccountStore } from '@/stores/account'
import defaultAvatar from '@/assets/images/default-avatar.png'
import { Undo, Redo, Clear, Save, Delete, Back, Next, Plus, Minus, Printer } from '@icon-park/vue-next'
import { 
  UserIcon, 
  DocumentTextIcon, 
  Cog6ToothIcon, 
  ArrowRightOnRectangleIcon,
  ChevronDownIcon 
} from '@heroicons/vue/24/outline'
import { showToast } from '@/components/ToastMessage'
import config from '@/config'
import EditTemplateDialog from './EditTemplateDialog.vue'
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
    default: 'create' // 'create' | 'edit' | 'use'
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
    required: true
  }
})

const emit = defineEmits([
  'clear', 
  'save', 
  'undo', 
  'redo', 
  'scale-change', 
  'create-resume', 
  'update:template',
  'print-preview'  // 添加打印预览事件
])
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

// 判断当前模式
const editorMode = computed(() => {
  if (route.name === 'template-create') return 'create'
  if (route.name === 'template-edit') return 'edit'
  if (route.name === 'template-use') return 'use'
  return ''
})

// 显示模板按钮
const showTemplateButtons = computed(() => {
  return ['create', 'edit'].includes(editorMode.value)
})

// 显示简历按钮
const showResumeButtons = computed(() => {
  return editorMode.value === 'use'
})

// 保存按钮文本
const saveButtonText = computed(() => {
  switch (editorMode.value) {
    case 'create':
      return '创建模板'
    case 'edit':
      return '保存修改'
    case 'use':
      return '保存简历'
    default:
      return '保存'
  }
})

// 处理保存
const handleSave = async () => {
  try {
    if (props.mode === 'draft') {
      await emit('save', 'draft')
      ElMessage.success('草稿保存成功')
    } else {
      await emit('save', 'publish')
      ElMessage.success('提交审核成功')
    }
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败，请重试')
  }
}

// 处理从模板创建简历
const handleCreateResume = () => {
  const templateId = route.params.id
  router.push({
    name: 'resume-create-from-template',
    params: { templateId }
  })
}

// 处理提交审核
const handleSubmitReview = () => {
  saveMode.value = 'review'
  showSaveDialog.value = true
}

// 计算当前模板数据
const currentTemplate = computed(() => {
  console.log('计算当前模板数据，props:', props.currentTemplate)
  if (!props.currentTemplate) return null
  
  // 确保返回一个新的对象，避免直接修改 props
  const template = {
    id: props.currentTemplate.id,
    name: props.currentTemplate.name || '',
    category: props.currentTemplate.category || '',
    description: props.currentTemplate.description || '',
    is_public: props.currentTemplate.is_public ?? false,
    keywords: Array.isArray(props.currentTemplate.keywords) ? props.currentTemplate.keywords : [],
    status: props.currentTemplate.status || 0,
    pages: props.currentTemplate.pages || []
  }
  console.log('处理后的模板数据:', template)
  return template
})

// 处理保存模板
const handleSaveTemplate = (templateData) => {
  console.log('EditorToolbar - 保存模板，接收到的数据:', templateData)
  const data = {
    ...templateData,
    status: templateData.status // 使用传入的数据中的status
  }
  console.log('EditorToolbar - 最终发送的数据:', data)
  
  emit('save', { 
    mode: editorMode.value, 
    action: templateData.status === 0 ? 'draft' : 'review', // 根据status判断action
    data,
    callback: (success) => {
      if (success) {
        showSaveDialog.value = false
        ElMessage.success(data.status === 0 ? '草稿保存成功' : '提交审核成功')
        
        // 通知父组件更新模板数据
        emit('update:template', {
          ...props.currentTemplate,
          ...data
        })
      }
    }
  })
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

// 处理返回
const handleBack = () => {
  router.push('/templates/resume')
}

// 处理打印预览
const handlePrintPreview = () => {
  // 触发打印预览事件
  emit('print-preview')
}
</script>

<style scoped>
@import '../styles/editor.css';
@import '../styles/controls.css';

.editor-toolbar {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  padding: 0 16px;
  height: 56px;
  background: #fff;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.toolbar-center {
  display: flex;
  justify-content: center;
  align-items: center;
}

.undo-redo-group {
  display: flex;
  gap: 8px;
  padding: 0 16px;
  border-left: 1px solid rgba(0, 0, 0, 0.06);
  border-right: 1px solid rgba(0, 0, 0, 0.06);
}

.toolbar-right {
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: flex-end;
}

.back-btn {
  color: #666;
}

.back-btn:hover {
  color: #1890ff;
  background: rgba(24, 144, 255, 0.1);
}

.template-title {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin: 0 16px;
}

.divider {
  width: 1px;
  height: 24px;
  background: rgba(0, 0, 0, 0.06);
  margin: 0 8px;
}

.toolbar-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: 1px solid transparent;
  border-radius: 6px;
  background: transparent;
  color: #666;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  height: 36px;
}

.toolbar-btn:hover:not(:disabled) {
  color: #1890ff;
  background: rgba(24, 144, 255, 0.04);
}

.toolbar-btn:active:not(:disabled) {
  background: rgba(24, 144, 255, 0.08);
}

.toolbar-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.toolbar-btn.primary {
  background: rgba(24, 144, 255, 0.08);
  color: #1890ff;
  border: 1px solid rgba(24, 144, 255, 0.2);
}

.toolbar-btn.primary:hover:not(:disabled) {
  background: rgba(24, 144, 255, 0.12);
  border-color: #1890ff;
}

.toolbar-btn.primary:active:not(:disabled) {
  background: rgba(24, 144, 255, 0.16);
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
  background-color: transparent;
  color: #1890ff;
  border-color: currentColor;
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