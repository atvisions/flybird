<template>
  <div class="relative">
    <!-- 时间线 -->
    <div class="absolute left-2 top-4 bottom-4 w-0.5 bg-gray-200"></div>

    <div 
      v-for="item in data" 
      :key="item.id" 
      class="relative pl-10 pb-8 last:pb-0"
    >
      <!-- 时间线圆点 -->
      <div class="absolute left-0 w-4 h-4 bg-white rounded-full border-2 border-blue-500 top-1.5">
        <div class="absolute inset-1 bg-blue-500 rounded-full"></div>
      </div>

      <!-- 标题栏 -->
      <div class="flex items-center justify-between mb-2 bg-white rounded-lg">
        <div class="flex-1 min-w-0">
          <h4 class="text-base font-medium text-gray-900 break-words">
            {{ item.company }}
            <span class="text-sm font-normal text-gray-500 ml-2">{{ item.position }}</span>
          </h4>
        </div>
        <div class="flex items-center space-x-2">
          <!-- 编辑按钮 -->
          <button
            @click="$emit('edit', item)"
            class="p-1 rounded-full hover:bg-gray-100 transition-colors duration-200 group relative"
          >
            <PencilSquareIcon class="w-5 h-5 text-gray-500 hover:text-gray-700" />
            <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 px-2 py-1 text-xs text-white bg-gray-800 rounded opacity-0 group-hover:opacity-100 whitespace-nowrap pointer-events-none transition-opacity duration-150">
              编辑
            </div>
          </button>
          <!-- 删除按钮 -->
          <button
            @click="handleDelete(item.id)"
            class="p-1 rounded-full hover:bg-gray-100 transition-colors duration-200 group relative"
          >
            <TrashIcon class="w-5 h-5 text-gray-500 hover:text-red-600" />
            <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 px-2 py-1 text-xs text-white bg-gray-800 rounded opacity-0 group-hover:opacity-100 whitespace-nowrap pointer-events-none transition-opacity duration-150">
              删除
            </div>
          </button>
        </div>
      </div>

      <!-- 时间信息 -->
      <div class="text-sm text-gray-500 mb-2">
        <span class="text-sm text-gray-500">
          {{ formatDateRange(item.start_date, item.end_date, item.is_current) }}
          <span v-if="item.duration" class="ml-1">({{ item.duration }})</span>
        </span>
      </div>

      <!-- 工作内容 -->
      <div class="space-y-3 text-sm text-gray-600">
        <!-- 工作描述 -->
        <div v-if="item.description" class="bg-gray-50 rounded-lg p-3">
          <div class="flex items-start space-x-2">
            <ClipboardDocumentListIcon class="w-5 h-5 text-blue-500 mt-0.5 flex-shrink-0" />
            <div class="flex-1">
              <div class="font-medium text-gray-700 mb-1.5 flex items-center">
                <span class="text-blue-600">工作内容</span>
                <div class="ml-2 h-4 w-px bg-gray-200"></div>
                <span class="ml-2 text-xs font-normal text-gray-400">{{ item.department || '未设置部门' }}</span>
              </div>
              <div class="whitespace-pre-wrap break-words">{{ item.description }}</div>
            </div>
          </div>
        </div>
        
        <!-- 主要成就 -->
        <div v-if="item.achievements" class="bg-gray-50 rounded-lg p-3">
          <div class="flex items-start space-x-2">
            <TrophyIcon class="w-5 h-5 text-yellow-500 mt-0.5 flex-shrink-0" />
            <div class="flex-1">
              <div class="font-medium text-gray-700 mb-1.5">
                <span class="text-yellow-600">主要成就</span>
              </div>
              <div class="whitespace-pre-wrap break-words">{{ item.achievements }}</div>
            </div>
          </div>
        </div>
        
        <!-- 相关技术 -->
        <div v-if="item.technologies" class="bg-gray-50 rounded-lg p-3">
          <div class="flex items-start space-x-2">
            <CommandLineIcon class="w-5 h-5 text-emerald-500 mt-0.5 flex-shrink-0" />
            <div class="flex-1">
              <div class="font-medium text-gray-700 mb-1.5">
                <span class="text-emerald-600">相关技术</span>
              </div>
              <div class="whitespace-pre-wrap break-words">{{ item.technologies }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div 
      v-if="!data || data.length === 0" 
      class="text-gray-400 text-center py-8 relative z-10 bg-white"
    >
      暂无工作经历，点击上方添加按钮新增
    </div>

    <TransitionRoot :show="showDeleteConfirm" as="template">
      <Dialog as="div" class="relative z-50" @close="showDeleteConfirm = false">
        <!-- 背景遮罩 -->
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

        <!-- 对话框 -->
        <div class="fixed inset-0 overflow-y-auto">
          <div class="flex min-h-full items-center justify-center p-4 text-center">
            <TransitionChild
              as="template"
              enter="duration-300 ease-out"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="duration-200 ease-in"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
            >
              <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-xl bg-white text-left align-middle shadow-xl transition-all">
                <div class="p-6">
                  <div class="flex items-start space-x-3">
                    <div class="p-2 bg-red-50 rounded-full flex-shrink-0">
                      <ExclamationTriangleIcon class="w-6 h-6 text-red-600" />
                    </div>
                    <div class="flex-1">
                      <DialogTitle as="h3" class="text-lg font-medium text-gray-900">
                        确认删除工作经历？
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
                      class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
                    >
                      取消
                    </button>
                    <button
                      type="button"
                      @click="confirmDelete"
                      class="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                    >
                      确认删除
                    </button>
                  </div>
                </div>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>

<script setup>
import { watch, computed, ref } from 'vue'
import { 
  PencilSquareIcon, 
  TrashIcon,
  ClipboardDocumentListIcon,
  TrophyIcon,
  CommandLineIcon
} from '@heroicons/vue/24/outline'
import { ElMessageBox, ElMessage } from 'element-plus'
import { 
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionRoot,
  TransitionChild
} from '@headlessui/vue'
import { ExclamationTriangleIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['edit', 'delete'])

// 格式化日期范围
const formatDateRange = (startDate, endDate, isCurrent) => {
  if (!startDate) return ''
  
  const start = new Date(startDate).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'numeric'
  })
  
  if (isCurrent) {
    return `${start} - 至今`
  }
  
  if (endDate) {
    const end = new Date(endDate).toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'numeric'
    })
    return `${start} - ${end}`
  }
  
  return start
}

// 添加计算工作时长的函数
const calculateDuration = (startDate, endDate, isCurrent) => {
  if (!startDate) return ''
  
  const start = new Date(startDate)
  const end = isCurrent ? new Date() : (endDate ? new Date(endDate) : null)
  
  if (!end) return ''
  
  const years = end.getFullYear() - start.getFullYear()
  const months = end.getMonth() - start.getMonth()
  
  let totalMonths = years * 12 + months
  if (end.getDate() < start.getDate()) {
    totalMonths--
  }
  
  const finalYears = Math.floor(totalMonths / 12)
  const finalMonths = totalMonths % 12
  
  let duration = ''
  if (finalYears > 0) {
    duration += `${finalYears}年`
  }
  if (finalMonths > 0) {
    duration += `${finalMonths}个月`
  }
  
  return duration
}

// 添加计算属性处理工作经历数据
const workExperiences = computed(() => {
  return props.data?.map(item => ({
    ...item,
    duration: calculateDuration(item.start_date, item.end_date, item.is_current)
  })) || []
})

// 监听数据变化
watch(() => props.data, (newVal) => {
  // 移除所有 console.log
}, { immediate: true })

const showDeleteConfirm = ref(false)
const deleteId = ref(null)

const handleDelete = (id) => {
  deleteId.value = id
  showDeleteConfirm.value = true
}

const confirmDelete = async () => {
  try {
    console.log('准备删除工作经历:', deleteId.value)
    await emit('delete', deleteId.value)
    showDeleteConfirm.value = false
    ElMessage.success('删除成功')
  } catch (error) {
    console.error('删除失败:', error)
    ElMessage.error('删除失败')
  }
}
</script>

<style scoped>
/* 时间线动画 */
.absolute {
  transition: all 0.3s ease;
}

/* 移动端适配 */
@media (max-width: 640px) {
  .pl-10 {
    @apply pl-8;
  }
  
  .absolute.left-0 {
    @apply -left-0.5;
  }
}

/* 添加内容块的悬浮效果 */
.bg-gray-50 {
  transition: all 0.2s ease;
  @apply shadow-sm;
}

.bg-gray-50:hover {
  @apply bg-gray-50/80 shadow-md;
}

/* 图标样式 */
.w-5 {
  transition: transform 0.2s ease;
}

.bg-gray-50:hover .w-5 {
  transform: scale(1.1);
}

/* 添加以下全局样式 */
:global(.custom-message-box) {
  border-radius: 8px;
}

:global(.custom-confirm-button) {
  background-color: #dc2626 !important;
  border-color: #dc2626 !important;
  color: white !important;
}

:global(.custom-confirm-button:hover) {
  background-color: #b91c1c !important;
  border-color: #b91c1c !important;
}

:global(.custom-cancel-button) {
  border-color: #e5e7eb !important;
  color: #374151 !important;
}

:global(.custom-cancel-button:hover) {
  border-color: #d1d5db !important;
  background-color: #f9fafb !important;
}

/* 添加长文本换行处理 */
.break-words {
  word-wrap: break-word;
  word-break: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
}

/* 优化文本容器样式 */
.whitespace-pre-wrap {
  white-space: pre-wrap;
  max-width: 100%;
}
</style> 