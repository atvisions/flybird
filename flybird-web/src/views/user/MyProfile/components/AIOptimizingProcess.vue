<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    :show-close="false"
    :close-on-click-modal="false"
    width="560px"
    class="ai-optimizing-process"
  >
    <div class="py-10 px-6">
      <!-- AI 动画区域 -->
      <div class="relative h-48 flex items-center justify-center mb-8">
        <!-- 中心光环 -->
        <div class="absolute w-32 h-32 bg-gradient-to-r from-primary-500 to-purple-500 rounded-full opacity-20 animate-pulse"></div>
        
        <!-- 旋转光环 -->
        <div class="absolute w-40 h-40 border-4 border-primary-500/30 rounded-full animate-spin-slow"></div>
        <div class="absolute w-48 h-48 border-4 border-purple-500/20 rounded-full animate-spin-reverse"></div>
        
        <!-- AI 图标 -->
        <div class="relative z-10">
          <SparklesIcon class="w-16 h-16 text-primary-600 animate-float" />
        </div>

        <!-- 扫描线效果 -->
        <div class="absolute inset-0 overflow-hidden">
          <div class="absolute w-full h-1 bg-gradient-to-r from-transparent via-primary-500 to-transparent top-0 animate-scan"></div>
        </div>
      </div>

      <!-- 优化状态 -->
      <div class="text-center space-y-4 mb-8">
        <h3 class="text-xl font-medium text-gray-900">
          {{ currentPhase.title }}
        </h3>
        <p class="text-sm text-gray-500">{{ currentPhase.description }}</p>
      </div>

      <!-- 进度条 -->
      <div class="space-y-2 mb-6">
        <div class="flex justify-between text-sm">
          <span class="text-gray-500">优化进度</span>
          <span class="text-primary-600 font-medium">{{ progress }}%</span>
        </div>
        <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
          <div 
            class="h-full bg-gradient-to-r from-primary-500 to-purple-500 transition-all duration-500 rounded-full"
            :style="{ width: `${progress}%` }"
          ></div>
        </div>
      </div>

      <!-- 优化阶段指示器 -->
      <div class="flex justify-between">
        <div 
          v-for="(phase, index) in phases" 
          :key="index"
          class="flex flex-col items-center space-y-2"
        >
          <div 
            class="w-8 h-8 rounded-full flex items-center justify-center transition-colors"
            :class="[
              currentPhaseIndex >= index 
                ? 'bg-primary-600 text-white' 
                : 'bg-gray-100 text-gray-400'
            ]"
          >
            <component 
              :is="phase.icon" 
              class="w-4 h-4"
            />
          </div>
          <span 
            class="text-xs"
            :class="[
              currentPhaseIndex >= index 
                ? 'text-primary-600' 
                : 'text-gray-400'
            ]"
          >
            {{ phase.name }}
          </span>
        </div>
      </div>

      <!-- 实时日志 -->
      <div class="mt-6 bg-gray-50 rounded-lg p-4 h-24 overflow-y-auto">
        <div 
          v-for="(log, index) in optimizationLogs" 
          :key="index"
          class="text-sm"
          :class="{
            'text-gray-500': index !== optimizationLogs.length - 1,
            'text-primary-600': index === optimizationLogs.length - 1
          }"
        >
          {{ log }}
        </div>
      </div>

      <!-- 添加提示文字 -->
      <div class="text-center text-sm text-gray-500 mt-4">
        <p>AI 优化需要 1-2 分钟，请耐心等待</p>
        <p class="mt-1">优化期间请勿关闭页面</p>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { 
  SparklesIcon,
  DocumentMagnifyingGlassIcon,
  DocumentCheckIcon,
  PencilSquareIcon,
  CheckCircleIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  modelValue: Boolean,
  loading: Boolean
})

const emit = defineEmits(['update:modelValue'])

// 优化阶段定义
const phases = [
  {
    name: '分析',
    icon: DocumentMagnifyingGlassIcon,
    title: '正在分析简历内容',
    description: 'AI 正在深度分析您的简历内容和结构'
  },
  {
    name: '优化',
    icon: PencilSquareIcon,
    title: '正在优化内容',
    description: 'AI 正在根据行业标准优化简历表达'
  },
  {
    name: '校对',
    icon: DocumentCheckIcon,
    title: '正在校对完善',
    description: 'AI 正在校对并完善细节'
  },
  {
    name: '完成',
    icon: CheckCircleIcon,
    title: '优化完成',
    description: '您的简历已经焕然一新'
  }
]

const currentPhaseIndex = ref(0)
const progress = ref(0)
const optimizationLogs = ref([
  '开始简历优化...',
  '正在加载 AI 模型...'
])

// 当前阶段信息
const currentPhase = computed(() => phases[currentPhaseIndex.value])

// 模拟优化过程
let progressInterval
let phaseInterval

const startOptimization = () => {
  // 进度更新 - 调整速度更慢一些
  progressInterval = setInterval(() => {
    if (progress.value < 95) {  // 最多到95%，等待实际完成
      progress.value += 1
    } else {
      clearInterval(progressInterval)
    }
  }, 1200)  // 每1.2秒增加1%

  // 阶段更新
  phaseInterval = setInterval(() => {
    if (currentPhaseIndex.value < phases.length - 1) {
      currentPhaseIndex.value += 1
      optimizationLogs.value.push(phases[currentPhaseIndex.value].description)
    } else {
      clearInterval(phaseInterval)
    }
  }, 20000) // 每20秒切换一个阶段
}

onMounted(() => {
  startOptimization()
})

onUnmounted(() => {
  clearInterval(progressInterval)
  clearInterval(phaseInterval)
})
</script> 