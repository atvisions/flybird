<template>
  <el-dialog
    :model-value="visible"
    @update:model-value="$emit('update:visible', $event)"
    :show-close="false"
    width="360px"
    align-center
    class="sign-in-dialog"
  >
    <div class="text-center py-6">
      <!-- 动画效果 -->
      <div class="mb-4 relative">
        <div class="absolute inset-0 bg-primary-100 rounded-full animate-ping opacity-20"></div>
        <div class="w-20 h-20 mx-auto bg-primary-50 rounded-full flex items-center justify-center relative">
          <CheckIcon class="w-10 h-10 text-primary-500 animate-bounce" />
        </div>
      </div>
      
      <!-- 签到成功文字 -->
      <h3 class="text-xl font-bold text-gray-900 mb-2">签到成功</h3>
      <p class="text-gray-600 mb-4">获得 {{ points }} 积分</p>
      
      <!-- 连续签到信息 -->
      <div class="bg-gray-50 rounded-lg p-3 mb-4">
        <p class="text-sm text-gray-600">
          已连续签到 <span class="text-primary-500 font-medium">{{ signInDays }}</span> 天
        </p>
        <template v-if="nextReward">
          <p class="text-sm text-gray-600 mt-1">
            再签到 {{ nextReward.days }} 天可获得 {{ nextReward.points }} 积分奖励
          </p>
        </template>
      </div>
      
      <!-- 确认按钮 -->
      <el-button
        type="primary"
        class="w-full"
        @click="handleClose"
      >
        太棒了
      </el-button>
    </div>
  </el-dialog>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import { CheckIcon } from '@heroicons/vue/24/outline'

defineProps({
  visible: {
    type: Boolean,
    required: true
  },
  points: {
    type: Number,
    required: true
  },
  signInDays: {
    type: Number,
    required: true
  },
  nextReward: {
    type: Object,
    default: null
  }
})

defineEmits(['update:visible'])

const handleClose = () => {
  emit('update:visible', false)
}
</script>

<style scoped>
.sign-in-dialog :deep(.el-dialog) {
  border-radius: 12px;
  overflow: hidden;
}

@keyframes ping {
  75%, 100% {
    transform: scale(2);
    opacity: 0;
  }
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(-5%);
    animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
  }
  50% {
    transform: translateY(0);
    animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
  }
}
</style> 