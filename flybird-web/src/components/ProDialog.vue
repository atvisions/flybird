<template>
  <el-dialog
    v-model="dialogVisible"
    :show-close="true"
    width="360px"
    class="pro-dialog"
    @close="handleClose"
  >
    <div class="relative p-6 bg-gradient-to-b from-[#F8F9FF] to-white rounded-xl">
      <!-- 背景装饰 -->
      <div class="absolute inset-0 overflow-hidden rounded-xl">
        <div class="absolute -top-10 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-gradient-radial from-blue-500/10 to-transparent opacity-50"></div>
        <div class="absolute top-0 left-0 w-full h-32 bg-[linear-gradient(40deg,transparent_40%,rgba(255,255,255,0.2)_60%,transparent_70%)] animate-shine"></div>
      </div>

      <div class="relative">
        <!-- 标题 -->
        <div class="text-center mb-6">
          <h3 class="text-lg font-semibold text-gray-900">会员折扣限时领取</h3>
          <div class="text-sm text-gray-500/90 mt-1">
            现在开通 低至
            <span class="text-orange-500 font-medium">{{ dailyPrice }}元/天</span>
          </div>
        </div>

        <!-- 会员权益列表 -->
        <div class="grid grid-cols-3 gap-3 p-4 mb-4 bg-gray-900 rounded-xl">
          <div v-for="(benefit, index) in membershipBenefits.slice(0, 3)" :key="index" 
            class="flex flex-col items-center"
          >
            <div class="w-10 h-10 rounded-lg bg-white/10 flex items-center justify-center mb-2">
              <component :is="benefit.icon" class="w-5 h-5 text-white/90" />
            </div>
            <div class="text-sm text-white/90">{{ benefit.name }}</div>
          </div>
        </div>

        <!-- 按钮 -->
        <button
          class="w-full h-12 relative rounded-full overflow-hidden group"
          @click="handleUpgrade"
        >
          <div class="absolute inset-0 bg-gradient-to-r from-orange-400 to-orange-500"></div>
          <div class="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-gradient-to-r from-orange-500 to-orange-600"></div>
          <span class="relative text-white text-base font-medium">立即开通</span>
        </button>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, defineProps, defineEmits, watch } from 'vue'
import { useRouter } from 'vue-router'
import { CrownIcon } from '@heroicons/vue/24/outline'
import { membershipBenefits, membershipPricing } from '@/config/membership'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])
const router = useRouter()

const dialogVisible = ref(props.modelValue)
const dailyPrice = membershipPricing.daily

// 监听 modelValue 变化
watch(() => props.modelValue, (val) => {
  dialogVisible.value = val
})

// 监听 dialogVisible 变化
watch(() => dialogVisible.value, (val) => {
  emit('update:modelValue', val)
})

const handleClose = () => {
  dialogVisible.value = false
}

const handleUpgrade = () => {
  dialogVisible.value = false
  router.push('/pro')
}
</script>

<style scoped>
.pro-dialog :deep(.el-dialog) {
  border: none;
  border-radius: 20px;
  overflow: hidden;
  background: transparent;
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.2);
}

.pro-dialog :deep(.el-dialog__header) {
  display: none;
}

.pro-dialog :deep(.el-dialog__body) {
  padding: 0;
}

.pro-dialog :deep(.el-dialog__headerbtn) {
  top: -14px;
  right: -14px;
  z-index: 10;
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  width: 32px;
  height: 32px;
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.1),
    0 0 0 4px rgba(255, 255, 255, 0.8);
  transition: all 0.3s;
}

.pro-dialog :deep(.el-dialog__headerbtn:hover) {
  transform: scale(1.1);
  box-shadow: 
    0 6px 16px rgba(0, 0, 0, 0.15),
    0 0 0 6px rgba(255, 255, 255, 0.9);
}

.pro-dialog :deep(.el-dialog__headerbtn .el-dialog__close) {
  color: rgba(0, 0, 0, 0.5);
  font-size: 18px;
  transition: color 0.3s;
}

.pro-dialog :deep(.el-dialog__headerbtn:hover .el-dialog__close) {
  color: rgba(0, 0, 0, 0.7);
}

@keyframes shine {
  from {
    transform: translateX(-100%);
  }
  to {
    transform: translateX(100%);
  }
}

.animate-shine {
  animation: shine 3s infinite;
}

@keyframes floatIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.pro-dialog :deep(.el-dialog) {
  animation: floatIn 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
}
</style> 