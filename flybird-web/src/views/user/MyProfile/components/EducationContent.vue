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
            {{ item.school }}
            <span class="text-sm font-normal text-gray-500 ml-2">{{ item.major }}</span>
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
        </span>
        <span class="ml-2 px-2 py-0.5 rounded-full text-xs bg-blue-50 text-blue-600">
          {{ getDegreeLabel(item.degree) }}
        </span>
      </div>

      <!-- 教育内容 -->
      <div class="space-y-3 text-sm text-gray-600">
        <!-- 在校经历 -->
        <div v-if="item.description" class="bg-gray-50 rounded-lg p-3">
          <div class="flex items-start space-x-2">
            <AcademicCapIcon class="w-5 h-5 text-blue-500 mt-0.5 flex-shrink-0" />
            <div class="flex-1">
              <div class="font-medium text-gray-700 mb-1.5">
                <span class="text-blue-600">在校经历</span>
              </div>
              <div class="whitespace-pre-wrap break-words">{{ item.description }}</div>
            </div>
          </div>
        </div>
        
        <!-- 在校成就 -->
        <div v-if="item.achievements" class="bg-gray-50 rounded-lg p-3">
          <div class="flex items-start space-x-2">
            <TrophyIcon class="w-5 h-5 text-yellow-500 mt-0.5 flex-shrink-0" />
            <div class="flex-1">
              <div class="font-medium text-gray-700 mb-1.5">
                <span class="text-yellow-600">在校成就</span>
              </div>
              <div class="whitespace-pre-wrap break-words">{{ item.achievements }}</div>
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
      暂无教育经历，点击上方添加按钮新增
    </div>

    <!-- 删除确认弹窗 -->
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
                        确认删除教育经历？
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
import { ref } from 'vue'
import { 
  PencilSquareIcon, 
  TrashIcon,
  AcademicCapIcon,
  TrophyIcon
} from '@heroicons/vue/24/outline'
import { ElMessage } from 'element-plus'
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

// 获取学历显示文本
const getDegreeLabel = (degree) => {
  const degreeMap = {
    'high_school': '高中',
    'junior_college': '大专',
    'bachelor': '本科',
    'master': '硕士',
    'doctor': '博士',
    'other': '其他'
  }
  return degreeMap[degree] || degree
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
    console.log('准备删除教育经历:', deleteId.value)
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
/* 样式与 WorkExperienceContent 相同 */
</style> 