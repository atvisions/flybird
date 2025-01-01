<template>
  <div class="space-y-4">
    <!-- 作品网格 -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div 
        v-for="item in data" 
        :key="item.id" 
        class="bg-white rounded-lg border border-gray-200 hover:shadow-md transition-all duration-200"
      >
        <!-- 作品头部 -->
        <div class="p-4">
          <div class="flex items-start justify-between">
            <div class="flex-1 min-w-0">
              <h4 class="text-base font-medium text-gray-900 break-words">
                {{ item.title }}
                <span class="ml-2 px-2 py-0.5 rounded-full text-xs bg-blue-50 text-blue-600">
                  {{ typeMap[item.type] || item.type }}
                </span>
              </h4>
            </div>
            <div class="flex items-center space-x-2 ml-4">
              <!-- 作品链接 -->
              <a
                v-if="item.url"
                :href="item.url"
                target="_blank"
                class="p-1 rounded-full hover:bg-gray-100 transition-colors duration-200 group relative"
              >
                <LinkIcon class="w-5 h-5 text-gray-500 hover:text-gray-700" />
                <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 px-2 py-1 text-xs text-white bg-gray-800 rounded opacity-0 group-hover:opacity-100 whitespace-nowrap pointer-events-none transition-opacity duration-150">
                  访问作品
                </div>
              </a>
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

          <!-- 作品内容 -->
          <div class="mt-4 space-y-3">
            <!-- 作品描述 -->
            <div v-if="item.description" class="text-sm text-gray-600">
              <div class="font-medium text-gray-700 mb-1">作品描述：</div>
              <div class="whitespace-pre-wrap break-words">{{ item.description }}</div>
            </div>
            
            <!-- 项目亮点 -->
            <div v-if="item.highlights" class="text-sm text-gray-600">
              <div class="font-medium text-gray-700 mb-1">项目亮点：</div>
              <div class="whitespace-pre-wrap break-words">{{ item.highlights }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div 
      v-if="!data || data.length === 0" 
      class="text-gray-400 text-center py-8 bg-gray-50 rounded-lg border border-gray-100"
    >
      暂无作品展示，点击上方添加按钮新增
    </div>

    <!-- 删除确认弹窗 -->
    <TransitionRoot :show="showDeleteConfirm" as="template">
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
                        确认删除作品展示？
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
  DocumentTextIcon,
  SparklesIcon,
  LinkIcon
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

// 作品类型映射
const typeMap = {
  'project': '项目',
  'website': '网站',
  'app': '应用',
  'article': '文章',
  'other': '其他'
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
    ElMessage.success('删除成功')
  } catch (error) {
    console.error('删除失败:', error)
    ElMessage.error('删除失败')
  }
}
</script>

<style scoped>
/* 卡片悬停效果 */
.hover\:shadow-md:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

/* 响应式布局优化 */
@media (max-width: 768px) {
  .md\:grid-cols-2 {
    grid-template-columns: 1fr;
  }
}
</style> 