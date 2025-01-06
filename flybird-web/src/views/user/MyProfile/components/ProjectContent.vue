<template>
  <div class="relative space-y-0">
    <!-- 时间线 -->
    <div class="absolute left-[0.5625rem] top-3 bottom-3 w-px bg-gray-200"></div>

    <!-- 项目经历列表 -->
    <div 
      v-for="(project, index) in data" 
      :key="index" 
      class="relative pl-12 pb-6"
    >
      <!-- 时间节点 -->
      <div class="absolute left-[0.5625rem] -translate-x-1/2 top-2 w-3 h-3 rounded-full bg-white border-2 border-blue-500"></div>
      
      <!-- 内容卡片 -->
      <div class="bg-gray-50 rounded-lg border border-gray-100 p-4 hover:shadow-sm transition-shadow">
        <!-- 头部信息 -->
        <div class="flex flex-col space-y-2">
          <!-- 项目名称和操作按钮 -->
          <div class="flex items-start justify-between">
            <div class="flex-1 min-w-0">
              <h4 class="text-base font-medium text-gray-900 break-words">{{ project.name }}</h4>
              <div class="text-sm text-gray-500 mt-1">
                {{ formatDate(project.start_date) }} - {{ project.is_current ? '至今' : formatDate(project.end_date) }}
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <button
                @click="$emit('edit', project)"
                class="p-1 hover:bg-white rounded-full transition-colors"
              >
                <PencilSquareIcon class="w-4 h-4 text-gray-400" />
              </button>
              <button
                @click="handleDelete(project.id)"
                class="p-1 hover:bg-white rounded-full transition-colors"
              >
                <TrashIcon class="w-4 h-4 text-gray-400" />
              </button>
            </div>
          </div>

          <!-- 角色 -->
          <div class="text-sm font-medium text-blue-600 break-words">
            {{ project.role }}
          </div>

          <!-- 项目描述 -->
          <div class="mt-3 space-y-2">
            <div class="flex items-center space-x-2">
              <DocumentTextIcon class="w-4 h-4 text-gray-400 flex-shrink-0" />
              <span class="text-sm text-gray-500">项目描述</span>
            </div>
            <div class="text-sm leading-relaxed text-gray-600 pl-6 break-words whitespace-pre-wrap">
              {{ project.description }}
            </div>
          </div>

          <!-- 项目成就 -->
          <div v-if="project.achievement" class="mt-3 space-y-2">
            <div class="flex items-center space-x-2">
              <TrophyIcon class="w-4 h-4 text-yellow-500 flex-shrink-0" />
              <span class="text-sm text-gray-500">项目成就</span>
            </div>
            <div class="text-sm leading-relaxed text-gray-600 pl-6 break-words whitespace-pre-wrap">
              {{ project.achievement }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加按钮 -->
    <div class="relative pl-12">
      <div class="absolute left-[0.5625rem] -translate-x-1/2 top-2 w-3 h-3 rounded-full bg-white border-2 border-gray-300"></div>
      <button
        @click="$emit('add')"
        class="w-full flex items-center justify-center px-4 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-all"
      >
        <PlusIcon class="w-4 h-4 mr-2" />
        添加项目经历
      </button>
    </div>

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
                      确认删除项目经历？
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
  ExclamationTriangleIcon,
  DocumentTextIcon,
  TrophyIcon
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

const props = defineProps({
  data: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['edit', 'delete', 'add'])

// 格式化日期显示
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}`
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