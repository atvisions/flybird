<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    title="AI 优化结果预览"
    :width="900"
    :close-on-click-modal="false"
    class="ai-optimization-result"
  >
    <div v-if="result" class="space-y-6">
      <!-- 主要改进点 -->
      <div class="bg-primary-50 rounded-lg p-4">
        <h4 class="text-sm font-medium text-primary-900 mb-2">主要改进</h4>
        <ul class="space-y-1">
          <li v-for="(improvement, index) in result.summary?.key_improvements || []" 
            :key="index"
            class="text-sm text-primary-700 flex items-start space-x-2"
          >
            <CheckCircleIcon class="w-4 h-4 mt-0.5 flex-shrink-0" />
            <span>{{ improvement }}</span>
          </li>
        </ul>
      </div>

      <!-- 各部分优化内容 -->
      <div class="space-y-4">
        <template v-for="(section, sectionKey) in result.preview || {}" :key="sectionKey">
          <div v-for="(item, itemKey) in section" :key="itemKey">
            <div class="border rounded-lg mb-4">
              <div class="bg-gray-50 px-4 py-2 rounded-t-lg flex items-center justify-between">
                <h4 class="font-medium text-gray-900">{{ getSectionTitle(sectionKey, itemKey) }}</h4>
                <span class="text-xs text-gray-500">{{ getItemTitle(item) }}</span>
              </div>
              <div class="p-4 space-y-4">
                <!-- 前后对比 -->
                <div class="grid grid-cols-2 gap-6">
                  <div class="space-y-2">
                    <div class="flex items-center text-sm text-gray-500">
                      <ClockIcon class="w-4 h-4 mr-1" />
                      <span>当前内容</span>
                    </div>
                    <div class="bg-gray-50 p-3 rounded text-sm text-gray-600">
                      {{ item.before }}
                    </div>
                  </div>
                  <div class="space-y-2">
                    <div class="flex items-center text-sm text-green-600">
                      <SparklesIcon class="w-4 h-4 mr-1" />
                      <span>优化建议</span>
                    </div>
                    <div class="bg-green-50 p-3 rounded text-sm text-gray-800">
                      {{ item.after }}
                    </div>
                  </div>
                </div>
                <!-- 改进说明 -->
                <div class="border-t pt-3">
                  <h5 class="text-sm font-medium text-gray-700 mb-2">优化要点：</h5>
                  <ul class="space-y-1">
                    <li v-for="(change, index) in item.changes || []" 
                      :key="index"
                      class="text-sm text-gray-600 flex items-start space-x-2"
                    >
                      <ArrowTrendingUpIcon class="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                      <span>{{ change }}</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </template>
      </div>

      <!-- 预期效果 -->
      <div class="bg-green-50 rounded-lg p-4">
        <h4 class="text-sm font-medium text-green-900 mb-2">预期效果</h4>
        <ul class="space-y-1">
          <li v-for="(benefit, index) in result.summary?.expected_benefits || []" 
            :key="index"
            class="text-sm text-green-700 flex items-start space-x-2"
          >
            <StarIcon class="w-4 h-4 mt-0.5 flex-shrink-0" />
            <span>{{ benefit }}</span>
          </li>
        </ul>
      </div>

      <!-- 确认按钮 -->
      <div class="flex justify-between items-center pt-4 border-t">
        <div class="text-sm text-gray-500">
          <ExclamationTriangleIcon class="w-4 h-4 inline mr-1 text-yellow-500" />
          确认后将覆盖原有内容
        </div>
        <div class="flex space-x-3">
          <button
            @click="handleCancel"
            class="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 transition-colors"
          >
            放弃优化
          </button>
          <button
            @click="handleConfirm"
            :disabled="loading"
            class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 rounded-md transition-colors disabled:opacity-50"
          >
            <CheckIcon class="w-4 h-4 mr-1.5" />
            {{ loading ? '确认中...' : '确认应用' }}
          </button>
        </div>
      </div>
    </div>
    <div v-else class="py-12 text-center text-gray-500">
      <SparklesIcon class="w-12 h-12 mx-auto mb-4 text-gray-400" />
      <p>正在准备优化结果...</p>
    </div>
  </el-dialog>
</template>

<script setup>
import { 
  SparklesIcon, ClockIcon, CheckCircleIcon, 
  ArrowTrendingUpIcon, StarIcon, CheckIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  modelValue: Boolean,
  result: {
    type: Object,
    required: true
  },
  loading: Boolean
})

const emit = defineEmits(['update:modelValue', 'confirm', 'cancel'])

// 获取章节标题
const getSectionTitle = (section, key) => {
  const titles = {
    basic_info: {
      personal_summary: '个人简介'
    },
    work_experiences: '工作经历',
    educations: '教育背景',
    skills: '专业技能',
    certificates: '证书认证',
    languages: '语言能力',
    portfolios: '项目作品'
  }
  return titles[section]?.[key] || titles[section] || key
}

// 获取项目标题
const getItemTitle = (item) => {
  if (item.name) return item.name
  if (item.title) return item.title
  if (item.company) return `${item.company} - ${item.position}`
  if (item.school) return `${item.school} - ${item.major}`
  return ''
}

// 处理确认
const handleConfirm = () => {
  emit('confirm', props.result.optimization_id)
}

// 处理取消
const handleCancel = () => {
  emit('cancel')
}
</script> 