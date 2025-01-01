<!-- src/views/user/MyProfile/components/ResumeStatus.vue -->
<template>
    <div class="bg-white rounded-lg shadow">
      <div class="p-4">
        <!-- 标题和总分 -->
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center space-x-4">
            <h3 class="text-base font-medium text-gray-900">简历评分</h3>
            <span class="text-lg font-semibold" :class="progressTextColorClass">
              {{ totalScore }} 分
            </span>
          </div>
          <!-- AI优化按钮 -->
          <button
            @click="showOptimize = true"
            class="flex items-center px-3 py-1.5 text-sm font-medium text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 rounded-md transition-all duration-200 shadow-sm"
          >
            <SparklesIcon class="w-4 h-4 mr-1.5" />
            AI优化
          </button>
        </div>
  
        <!-- 总进度条 -->
        <div class="relative h-2.5 mb-4 bg-gray-200 rounded-full overflow-hidden">
          <div 
            class="h-full flex transition-all duration-500 gap-[2px]"
          >
            <div 
              v-for="n in 20" 
              :key="n"
              class="h-full flex-1"
              :class="[n <= Math.ceil(totalScore / 5) ? progressColorClass : 'bg-gray-200']"
            ></div>
          </div>
        </div>
  
        <!-- 维度得分 -->
        <div class="space-y-3 mb-6">
          <div v-for="(dimension, key) in dimensions" :key="key" class="flex items-center">
            <span class="text-sm text-gray-600 w-24">{{ getDimensionName(key) }}</span>
            <div class="flex-1 mx-2 relative">
              <div class="bg-gray-200 rounded-full h-1.5 overflow-hidden">
                <div 
                  class="h-full flex transition-all duration-500 gap-[2px]"
                >
                  <div 
                    v-for="n in 20" 
                    :key="n"
                    class="h-full flex-1"
                    :class="[n <= Math.ceil(dimension.score / 5) ? 'bg-blue-500' : 'bg-gray-200']"
                  ></div>
                </div>
              </div>
            </div>
            <span class="text-sm text-gray-500">{{ dimension.score }}%</span>
          </div>
        </div>
  
        <!-- 优化建议 -->
        <div v-if="suggestions.length > 0" class="space-y-2">
          <h4 class="text-sm font-medium text-gray-700">优化建议</h4>
          <ul class="space-y-1">
            <li 
              v-for="(suggestion, index) in suggestions" 
              :key="index"
              class="flex items-start space-x-2 text-sm text-gray-600"
            >
              <LightBulbIcon class="w-4 h-4 text-yellow-500 mt-0.5 flex-shrink-0" />
              <span>{{ suggestion }}</span>
            </li>
          </ul>
        </div>
  
        <!-- 其他操作按钮 -->
        <div class="grid grid-cols-2 gap-3 mt-6">
          <button
            @click="$emit('import')"
            class="flex items-center justify-center px-4 py-2 rounded-lg text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 transition-all duration-200"
          >
            <ArrowDownTrayIcon class="w-4 h-4 mr-1.5" />
            导入简历
          </button>
  
          <button
            @click="handlePreview"
            class="flex items-center justify-center px-4 py-2 rounded-lg text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 transition-all duration-200"
          >
            <EyeIcon class="w-4 h-4 mr-1.5" />
            预览简历
          </button>
        </div>
      </div>
    </div>
  
    <!-- 预览对话框 -->
    <TransitionRoot appear :show="!!showPreview" as="template">
      <Dialog as="div" class="relative z-50" @close="showPreview = false">
        <TransitionChild
          as="template"
          :show="true"
          enter="duration-300 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-200 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-black/25" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div class="flex min-h-full items-center justify-center p-4 text-center">
            <TransitionChild
              as="template"
              :show="true"
              enter="duration-300 ease-out"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="duration-200 ease-in"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
            >
              <DialogPanel 
                class="w-full transform overflow-hidden rounded-xl bg-white text-left align-middle shadow-xl transition-all"
                :class="[isMobile ? 'h-full' : 'max-w-4xl']"
              >
                <!-- 头部 -->
                <div class="dialog-header">
                  <div class="flex items-center justify-between">
                    <h3 class="text-lg font-medium text-gray-900">简历预览</h3>
                    <button
                      @click="showPreview = false"
                      class="p-1 rounded-full hover:bg-gray-100 transition-colors duration-200"
                      title="关闭"
                    >
                      <XMarkIcon class="w-6 h-6 text-gray-500" />
                    </button>
                  </div>
                </div>

                <!-- 内容区域 -->
                <div class="dialog-body">
                  <ProfilePreview />
                </div>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  
    <!-- AI优化对话框 -->
    <AIOptimizeDialog
      v-if="showOptimize"
      v-model="showOptimize"
      :profile-data="props.profileData"
      @apply="handleOptimizeApply"
    />
  </template>
  
  <script setup>
  import { ref, computed, watch } from 'vue'
  import { useWindowSize } from '@vueuse/core'
  import { 
    SparklesIcon,
    ArrowDownTrayIcon,
    EyeIcon,
    XMarkIcon,
    LightBulbIcon 
  } from '@heroicons/vue/24/outline'
  import ProfilePreview from './ProfilePreview.vue'
  import AIOptimizeDialog from '../dialogs/AIOptimizeDialog.vue'
  import {
    Dialog,
    DialogPanel,
    DialogTitle,
    TransitionChild,
    TransitionRoot
  } from '@headlessui/vue'

  const props = defineProps({
    completionData: {
      type: Object,
      default: () => ({})
    },
    profileData: {
      type: Object,
      default: () => ({})
    },
    loading: {
      type: Boolean,
      default: false
    }
  })

  defineEmits(['ai-optimize', 'import', 'preview'])

  // 预览对话框控制
  const showPreview = ref(false)

  // 响应式布局
  const { width } = useWindowSize()
  const isMobile = computed(() => width.value < 640)
  const dialogWidth = computed(() => {
    if (isMobile.value) return '100%'
    if (width.value < 1024) return '80%'
    return '800px'  // 预览窗口可以稍微宽一点
  })

  // 总分 - 保留一位小数
  const totalScore = computed(() => {
    const score = props.completionData?.total_score || 0
    return Number(score.toFixed(1))
  })

  // 维度数据 - 保留整数
  const dimensions = computed(() => {
    const dims = props.completionData?.dimensions || {}
    return Object.entries(dims).reduce((acc, [key, value]) => {
      acc[key] = {
        ...value,
        score: Math.round(value.score || 0),
        weighted_score: value.weighted_score || 0
      }
      return acc
    }, {})
  })

  // 建议
  const suggestions = computed(() => {
    const rawSuggestions = props.completionData?.suggestions || []
    // 只返回建议消息
    return rawSuggestions.map(suggestion => suggestion.message)
  })

  // 维度名称映射
  const getDimensionName = (key) => {
    const nameMap = {
      basic_info: '基本信息',
      experience: '工作经历',
      capability: '能力素质',
      achievement: '个人成就'
    }
    return nameMap[key] || key
  }

  // 进度条颜色 - 根据实际分数范围调整
  const progressColorClass = computed(() => {
    const score = totalScore.value
    if (score >= 70) return 'bg-green-500'
    if (score >= 40) return 'bg-yellow-500'
    return 'bg-red-500'
  })

  // 文字颜色 - 与进度条颜色对应
  const progressTextColorClass = computed(() => {
    const score = totalScore.value
    if (score >= 70) return 'text-green-600'
    if (score >= 40) return 'text-yellow-600'
    return 'text-red-600'
  })

  // 处理预览按钮点击
  const handlePreview = () => {
    showPreview.value = true
  }

  // AI优化相关
  const showOptimize = ref(false)

  // 处理优化结果
  const handleOptimizeApply = (optimizedData) => {
    console.log('优化后的数据:', optimizedData)
    // 这里处理优化后的数据，可能需要调用 API 更新档案
  }

  // 监听 profileData 变化，确保数据有效
  watch(
    () => props.profileData,
    (newVal) => {
      if (!newVal || Object.keys(newVal).length === 0) {
        return
      }
      // 处理数据...
    },
    { 
      immediate: true,
      deep: true 
    }
  )
  </script>

<style scoped>
/* 添加按钮悬停效果 */
button {
  position: relative;
  overflow: hidden;
}

button::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.1);
  transform: translate(-50%, -50%) scale(0);
  border-radius: inherit;
  transition: transform 0.3s ease;
}

button:hover::after {
  transform: translate(-50%, -50%) scale(1.5);
}

/* 渐变进度条效果 */
.bg-green-500 {
  background: linear-gradient(90deg, #10B981 0%, #34D399 100%);
}

.bg-yellow-500 {
  background: linear-gradient(90deg, #F59E0B 0%, #FBBF24 100%);
}

.bg-red-500 {
  background: linear-gradient(90deg, #EF4444 0%, #F87171 100%);
}

/* 预览对话框样式 */
.preview-dialog {
  @apply max-h-screen flex flex-col;
}

.preview-dialog :deep(.el-dialog__body) {
  @apply flex-1 overflow-y-auto p-0;
}

.dialog-header {
  @apply px-6 py-4 border-b border-gray-200;
}

.dialog-body {
  @apply p-0;
  height: calc(100vh - 120px);
  overflow-y: auto;
}

/* 移动端适配 */
@media (max-width: 640px) {
  .preview-dialog {
    margin: 0 !important;
  }

  .dialog-header {
    @apply px-4;
  }
}
</style>