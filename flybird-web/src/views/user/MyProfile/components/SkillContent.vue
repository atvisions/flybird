<template>
  <div class="space-y-4">
    <!-- 技能列表 -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div 
        v-for="(skill, index) in data" 
        :key="index" 
        class="bg-gray-50 rounded-lg border border-gray-100 p-4 hover:shadow-sm transition-all"
      >
        <!-- 技能头部 -->
        <div class="flex items-start justify-between mb-3">
          <div class="flex-1 min-w-0">
            <h4 class="text-base font-medium text-gray-900 break-words">{{ skill.name }}</h4>
          </div>
          <div class="flex items-center space-x-2 ml-4">
            <button
              @click="$emit('edit', skill)"
              class="p-1 hover:bg-white rounded-full transition-colors"
            >
              <PencilSquareIcon class="w-4 h-4 text-gray-400" />
            </button>
            <button
              @click="handleDelete(skill.id)"
              class="p-1 hover:bg-white rounded-full transition-colors"
            >
              <TrashIcon class="w-4 h-4 text-gray-400" />
            </button>
          </div>
        </div>

        <!-- 熟练度进度条 -->
        <div class="mb-3">
          <div class="flex items-center justify-between mb-1">
            <span class="text-sm text-gray-500">熟练度</span>
            <span class="text-sm font-medium" :class="getLevelColor(skill.level).replace('bg-', 'text-')">
              {{ getLevelLabel(skill.level) }}
            </span>
          </div>
          <div class="w-full bg-gray-100 rounded-full h-2">
            <div 
              class="h-2 rounded-full transition-all duration-300"
              :class="getLevelColor(skill.level)"
              :style="{ width: getLevelPercentage(skill.level) }"
            ></div>
          </div>
        </div>

        <!-- 技能描述 -->
        <div class="text-sm text-gray-600 break-words whitespace-pre-wrap">
          {{ skill.description }}
        </div>
      </div>
    </div>

    <!-- 添加按钮 -->
    <button
      @click="$emit('add')"
      class="w-full flex items-center justify-center px-4 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-all"
    >
      <PlusIcon class="w-4 h-4 mr-2" />
      添加专业技能
    </button>

    <!-- 删除确认弹窗 -->
    <TransitionRoot appear :show="showDeleteConfirm" as="template">
      <Dialog as="div" class="relative z-50" @close="showDeleteConfirm = false">
        <TransitionChild
          as="template"
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
            <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-xl bg-white p-6 text-left align-middle shadow-xl transition-all">
              <div>
                <div class="flex items-start space-x-3">
                  <div class="p-2 bg-red-50 rounded-full flex-shrink-0">
                    <ExclamationTriangleIcon class="w-6 h-6 text-red-600" />
                  </div>
                  <div class="flex-1">
                    <DialogTitle as="h3" class="text-lg font-medium text-gray-900">
                      确认删除技能？
                    </DialogTitle>
                    <p class="mt-2 text-sm text-gray-500">
                      删除后将无法恢复，请确认是否继续。
                    </p>
                  </div>
                </div>
                
                <div class="mt-6 flex justify-end space-x-3">
                  <button
                    type="button"
                    @click="showDeleteConfirm = false"
                    class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
                  >
                    取消
                  </button>
                  <button
                    type="button"
                    @click="confirmDelete"
                    class="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-lg hover:bg-red-700"
                  >
                    确定删除
                  </button>
                </div>
              </div>
            </DialogPanel>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>

<script setup>
import { 
  PencilSquareIcon, 
  TrashIcon, 
  PlusIcon,
  ExclamationTriangleIcon 
} from '@heroicons/vue/24/outline'
import { 
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionRoot,
  TransitionChild
} from '@headlessui/vue'
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

defineProps({
  data: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['edit', 'delete', 'add'])

// 修改获取熟练度标签和进度条百分比的方法
const SKILL_LEVELS = {
  '初级': {
    label: '入门',
    percentage: '20%',
    color: 'bg-blue-200'
  },
  '中级': {
    label: '熟练',
    percentage: '50%',
    color: 'bg-blue-400'
  },
  '高级': {
    label: '精通',
    percentage: '80%',
    color: 'bg-blue-500'
  },
  '专家': {
    label: '专家',
    percentage: '100%',
    color: 'bg-blue-600'
  }
}

const getLevelLabel = (level) => {
  return SKILL_LEVELS[level]?.label || level || '未知'
}

const getLevelPercentage = (level) => {
  return SKILL_LEVELS[level]?.percentage || '0%'
}

const getLevelColor = (level) => {
  return SKILL_LEVELS[level]?.color || 'bg-gray-200'
}

// 删除相关
const showDeleteConfirm = ref(false)
const deleteId = ref(null)

const handleDelete = (id) => {
  deleteId.value = id
  showDeleteConfirm.value = true
}

const confirmDelete = async () => {
  try {
    await emit('delete', deleteId.value)
    showDeleteConfirm.value = false
  } catch (error) {
    console.error('删除失败:', error)
    ElMessage.error('删除失败')
  }
}
</script>

<style scoped>
/* 进度条动画 */
.bg-blue-600 {
  transition: width 0.3s ease-in-out;
}

/* 卡片悬停效果 */
.hover\:shadow-sm:hover {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transform: translateY(-1px);
}

/* 响应式布局优化 */
@media (max-width: 640px) {
  .grid-cols-2 {
    grid-template-columns: 1fr;
  }
}

/* 优化进度条动画 */
.h-2 {
  transition: all 0.3s ease-in-out;
}
</style> 