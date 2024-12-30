<!-- src/views/user/MyProfile/dialogs/AIDialog.vue -->
<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    title="AI 优化建议"
    :width="900"
    :close-on-click-modal="false"
  >
    <div class="space-y-6">
      <!-- 头部信息：始终显示 -->
      <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
        <div class="flex items-center space-x-6">
          <!-- 评分 -->
          <div>
            <div class="flex items-baseline">
              <span class="text-3xl font-bold" :class="scoreColorClass">{{ totalScore }}</span>
              <span class="ml-1 text-sm text-gray-500">分</span>
            </div>
            <div class="text-xs text-gray-500 mt-1">当前评分</div>
          </div>
          <!-- 剩余次数 -->
          <div>
            <div class="flex items-center space-x-1">
              <SparklesIcon class="w-4 h-4 text-primary-500" />
              <span class="font-medium" :class="{'text-red-600': remainingOptimizations === 0}">
                {{ remainingOptimizations }}/{{ totalOptimizations }}
              </span>
            </div>
            <div class="text-xs text-gray-500 mt-1">剩余优化次数</div>
          </div>
        </div>
        <!-- VIP提示 -->
        <div v-if="!isVip" class="text-xs text-gray-500">
          <router-link to="/vip" class="text-primary-600 hover:text-primary-700">
            升级会员
          </router-link>
          <span class="ml-1">享无限次优化</span>
        </div>
      </div>

      <!-- 主要内容区域：根据状态切换 -->
      <div class="relative min-h-[400px]">
        <!-- 待优化建议列表 -->
        <div v-if="!optimizationResult && !optimizing" class="space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-medium text-gray-900">待改进项</h3>
            <span class="text-sm text-gray-500">按优先级排序</span>
          </div>
          <div class="space-y-3">
            <div 
              v-for="(suggestion, index) in sortedSuggestions" 
              :key="index"
              class="group bg-white rounded-lg p-4 border border-gray-200 hover:border-primary-300 hover:shadow-sm transition-all duration-200"
            >
              <div class="flex items-start space-x-3">
                <div 
                  class="flex-shrink-0 w-2 h-2 mt-2 rounded-full transition-colors"
                  :class="{
                    'bg-red-500 group-hover:animate-pulse': suggestion.importance === 'high',
                    'bg-yellow-500': suggestion.importance === 'medium',
                    'bg-blue-500': suggestion.importance === 'low'
                  }"
                ></div>
                <div class="flex-1">
                  <div class="flex items-center space-x-2">
                    <span class="text-xs font-medium px-2 py-0.5 rounded" 
                      :class="getTypeClass(suggestion.type)">
                      {{ getTypeName(suggestion.type) }}
                    </span>
                    <span class="text-sm text-gray-700">{{ suggestion.message }}</span>
                  </div>
                  <div class="flex items-center mt-2 text-xs text-gray-500">
                    <ChartBarIcon class="w-4 h-4 mr-1" />
                    <span>预计提升：</span>
                    <span class="text-primary-600 font-medium ml-1">+{{ suggestion.score_impact }}分</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 优化中状态 -->
        <div v-else-if="optimizing" class="py-8 text-center">
          <!-- ... 优化中的动画和进度保持不变 ... -->
        </div>

        <!-- 优化结果 -->
        <div v-else class="space-y-6">
          <!-- ... 优化结果的展示保持不变 ... -->
        </div>
      </div>

      <!-- 底部按钮：根据状态显示不同按钮 -->
      <div class="flex justify-between items-center pt-4 border-t">
        <div class="text-sm text-gray-500">
          <template v-if="optimizationResult">
            <ExclamationTriangleIcon class="w-4 h-4 inline mr-1 text-yellow-500" />
            确认后将覆盖原有内容
          </template>
          <template v-else-if="!isVip && remainingOptimizations === 0">
            升级会员享受无限次优化
          </template>
          <template v-else>
            优化后内容可随时修改
          </template>
        </div>

        <div class="flex space-x-3">
          <!-- 开始优化按钮 -->
          <button
            v-if="!optimizationResult && !optimizing"
            @click="startOptimize"
            :disabled="loading || remainingOptimizations === 0"
            class="group relative inline-flex items-center px-8 py-3 text-base font-medium text-white bg-gradient-to-r from-primary-600 to-purple-600 rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed hover:from-primary-700 hover:to-purple-700"
          >
            <SparklesIcon class="w-5 h-5 mr-2 animate-pulse" />
            <span>{{ loading ? '优化中...' : '开始AI优化' }}</span>
          </button>

          <!-- 结果确认按钮 -->
          <template v-if="optimizationResult">
            <button
              @click="handleCancel"
              class="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 transition-colors"
            >
              放弃优化
            </button>
            <button
              @click="handleConfirm"
              :disabled="loading"
              class="inline-flex items-center px-6 py-2 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 rounded-md transition-colors disabled:opacity-50"
            >
              <CheckIcon class="w-4 h-4 mr-1.5" />
              {{ loading ? '确认中...' : '确认应用' }}
            </button>
          </template>
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted, watch } from 'vue'
import { SparklesIcon, InformationCircleIcon, ChartBarIcon, CheckCircleIcon, ClockIcon, ArrowTrendingUpIcon, StarIcon, ExclamationTriangleIcon, CheckIcon, DocumentMagnifyingGlassIcon, PencilSquareIcon, DocumentCheckIcon } from '@heroicons/vue/24/outline'
import { useWindowSize } from '@vueuse/core'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'

const props = defineProps({
  modelValue: Boolean,
  suggestions: Array,
  totalScore: Number,
  remainingOptimizations: Number,
  totalOptimizations: Number,
  loading: Boolean,
  optimizationResult: Object
})

const emit = defineEmits(['update:modelValue', 'start-optimize', 'confirm', 'cancel'])

const store = useStore()
const { width } = useWindowSize()

// 弹窗宽度
const dialogWidth = computed(() => {
  if (width.value < 640) return '94%'
  if (width.value < 1024) return '80%'
  return '640px'
})

// 总分颜色
const scoreColorClass = computed(() => {
  if (props.totalScore >= 80) return 'text-green-600'
  if (props.totalScore >= 60) return 'text-yellow-600'
  return 'text-red-600'
})

// 建议类型样式
const getTypeClass = (type) => {
  const classMap = {
    basic_info: 'bg-blue-50 text-blue-700',
    work_experience: 'bg-purple-50 text-purple-700',
    skill: 'bg-green-50 text-green-700',
    education: 'bg-yellow-50 text-yellow-700',
    project: 'bg-indigo-50 text-indigo-700',
    achievement: 'bg-pink-50 text-pink-700'
  }
  return classMap[type] || 'bg-gray-50 text-gray-700'
}

// 建议类型名称
const getTypeName = (type) => {
  const typeMap = {
    basic_info: '基本信息',
    work_experience: '工作经历',
    skill: '技能特长',
    education: '教育背景',
    project: '项目经验',
    achievement: '个人成就'
  }
  return typeMap[type] || type
}

// 按重要性和提升分数排序的建议
const sortedSuggestions = computed(() => {
  const importanceOrder = { high: 3, medium: 2, low: 1 }
  return [...props.suggestions].sort((a, b) => {
    const importanceDiff = importanceOrder[b.importance] - importanceOrder[a.importance]
    if (importanceDiff !== 0) return importanceDiff
    return b.score_impact - a.score_impact
  })
})

// 是否是VIP会员
const isVip = computed(() => store.getters.isVip)

// 优化中状态
const optimizing = ref(false)

// 开始优化
const startOptimize = () => {
  optimizing.value = true
  emit('start-optimize')
}

// 处理确认
const handleConfirm = () => {
  emit('confirm', props.optimizationResult.optimization_id)
}

// 处理取消
const handleCancel = () => {
  optimizing.value = false
  emit('cancel')
}

// 监听优化结果
watch(() => props.optimizationResult, (newVal) => {
  if (newVal) {
    optimizing.value = false
  }
})

// 监听对话框关闭
watch(() => props.modelValue, (newVal) => {
  if (!newVal) {
    // 重置状态
    optimizing.value = false
  }
})
</script>

<style scoped>
.animate-spin-slow {
  animation: spin 8s linear infinite;
}

.animate-float {
  animation: float 3s ease-in-out infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}
</style>