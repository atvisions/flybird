<template>
  <Teleport to="body">
    <div v-if="dialogVisible" class="fixed inset-0 z-50 flex items-center justify-center">
      <!-- 遮罩层 -->
      <div class="absolute inset-0 bg-black/60"></div>
      
      <!-- 弹窗内容 -->
      <div class="relative flex flex-col items-center">
        <div class="w-[370px] h-[392px] rounded-2xl overflow-hidden relative">
          <!-- 背景图片 -->
          <div class="absolute inset-0 bg-cover bg-center bg-no-repeat" :style="{ backgroundImage: `url(${vipBg})` }"></div>
          
          <!-- 内容区域 -->
          <div class="relative h-full">
            <!-- 价格信息 -->
            <div class="text-left pl-[30px] pt-[30px]">
              <h2 class="text-3xl font-bold text-yellow-600 mb-1">超值会员尊享价</h2>
              <p class="text-sm text-yellow-600">现在开通低至 0.8 元/天</p>
            </div>

            <!-- 会员权益 -->
            <div class="mt-2 px-8">
              <!-- 上面三个权益 -->
              <div class="flex justify-center space-x-8 mb-4">
                <div class="text-center group cursor-pointer border border-yellow-400/30 rounded-xl px-2 py-1.5 hover:border-yellow-400/60">
                  <div class="w-12 h-12 mx-auto mb-0.5 rounded-lg flex items-center justify-center transition-all duration-300 shadow-lg shadow-yellow-400/20 group-hover:shadow-yellow-400/30">
                    <SquaresPlusIcon class="w-7 h-7 text-yellow-600 transition-all duration-300 group-hover:text-yellow-500" />
                  </div>
                  <span class="text-xs text-yellow-600 transition-colors duration-300 group-hover:text-yellow-500">会员模板</span>
                </div>
                <div class="text-center group cursor-pointer border border-yellow-400/30 rounded-xl px-2 py-1.5 hover:border-yellow-400/60">
                  <div class="w-12 h-12 mx-auto mb-0.5 rounded-lg flex items-center justify-center transition-all duration-300 shadow-lg shadow-yellow-400/20 group-hover:shadow-yellow-400/30">
                    <MagnifyingGlassCircleIcon class="w-7 h-7 text-yellow-600 transition-all duration-300 group-hover:text-yellow-500" />
                  </div>
                  <span class="text-xs text-yellow-600 transition-colors duration-300 group-hover:text-yellow-500">简历解析</span>
                </div>
                <div class="text-center group cursor-pointer border border-yellow-400/30 rounded-xl px-2 py-1.5 hover:border-yellow-400/60">
                  <div class="w-12 h-12 mx-auto mb-0.5 rounded-lg flex items-center justify-center transition-all duration-300 shadow-lg shadow-yellow-400/20 group-hover:shadow-yellow-400/30">
                    <FireIcon class="w-7 h-7 text-yellow-600 transition-all duration-300 group-hover:text-yellow-500" />
                  </div>
                  <span class="text-xs text-yellow-600 transition-colors duration-300 group-hover:text-yellow-500">双倍积分</span>
                </div>
              </div>
              
              <!-- 下面两个权益 -->
              <div class="flex justify-center space-x-16">
                <div class="text-center group cursor-pointer border border-yellow-400/30 rounded-xl px-2 py-1.5 hover:border-yellow-400/60">
                  <div class="w-12 h-12 mx-auto mb-0.5 rounded-lg flex items-center justify-center transition-all duration-300 shadow-lg shadow-yellow-400/20 group-hover:shadow-yellow-400/30">
                    <BoltIcon class="w-7 h-7 text-yellow-600 transition-all duration-300 group-hover:text-yellow-500" />
                  </div>
                  <span class="text-xs text-yellow-600 transition-colors duration-300 group-hover:text-yellow-500">AI档案优化</span>
                </div>
                <div class="text-center group cursor-pointer border border-yellow-400/30 rounded-xl px-2 py-1.5 hover:border-yellow-400/60">
                  <div class="w-12 h-12 mx-auto mb-0.5 rounded-lg flex items-center justify-center transition-all duration-300 shadow-lg shadow-yellow-400/20 group-hover:shadow-yellow-400/30">
                    <ServerIcon class="w-7 h-7 text-yellow-600 transition-all duration-300 group-hover:text-yellow-500" />
                  </div>
                  <span class="text-xs text-yellow-600 transition-colors duration-300 group-hover:text-yellow-500">超大云存储</span>
                </div>
              </div>
            </div>

            <!-- 按钮 -->
            <div class="absolute bottom-6 left-8 right-8">
              <button 
                @click="handleUpgrade"
                class="w-full py-3 bg-gradient-to-b from-[#EEA852] to-[#EC6833] text-[#FFF5C8] font-medium rounded-full hover:opacity-90 transition-all duration-300 transform hover:scale-105"
              >
                立即购买
              </button>
            </div>
          </div>
        </div>

        <!-- 关闭按钮 -->
        <button 
          @click="closeDialog"
          class="mt-8 w-8 h-8 rounded-full border border-[#343A53] flex items-center justify-center hover:bg-white/10 transition-colors"
        >
          <XMarkIcon class="w-5 h-5 text-[#343A53]" />
        </button>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue'
import { XMarkIcon } from '@heroicons/vue/24/outline'
import { 
  SquaresPlusIcon,
  MagnifyingGlassCircleIcon,
  FireIcon,
  BoltIcon,
  ServerIcon
} from '@heroicons/vue/24/solid'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/account'
import vipBg from '@/assets/images/vip.png'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  onImport: {
    type: Function,
    default: null
  }
})

const emit = defineEmits(['update:modelValue'])
const router = useRouter()
const accountStore = useAccountStore()

const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const closeDialog = () => {
  dialogVisible.value = false
}

const handleUpgrade = () => {
  closeDialog()
  router.push('/pro')
}
</script>

<style scoped>
.dialog-enter-active,
.dialog-leave-active {
  transition: opacity 0.3s ease;
}

.dialog-enter-from,
.dialog-leave-to {
  opacity: 0;
}
</style> 