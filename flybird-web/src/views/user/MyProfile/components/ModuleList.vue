<!-- src/views/user/MyProfile/components/ModuleList.vue -->
<template>
  <div class="space-y-4">
    <div v-for="module in activeModules" :key="module.id" class="bg-white rounded-lg shadow">
      <!-- 模块头部 -->
      <div class="flex items-center justify-between px-4 py-3 border-b">
        <div class="flex items-center space-x-2">
          <component :is="module.icon" class="w-5 h-5 text-gray-500" />
          <h3 class="text-base font-medium">{{ module.name }}</h3>
        </div>
        <div class="flex items-center space-x-2">
          <!-- 编辑/添加按钮 -->
          <button
            v-if="module.type === 'work_experience'"
            @click="$emit('edit', module.id)"
            class="p-1 rounded-full hover:bg-gray-100 transition-colors duration-200"
            title="添加工作经历"
          >
            <PlusIcon class="w-5 h-5 text-gray-900 hover:text-gray-700" />
          </button>
          <!-- 其他模块保持编辑按钮 -->
          <button
            v-else
            @click="$emit('edit', module.id)"
            class="p-1 rounded-full hover:bg-gray-100 transition-colors duration-200"
            title="编辑"
          >
            <PencilSquareIcon class="w-5 h-5 text-gray-900 hover:text-gray-700" />
          </button>
          <!-- 移除按钮 -->
          <button
            @click="handleRemove(module.id)"
            class="p-1 rounded-full hover:bg-gray-100 transition-colors duration-200"
            title="移除"
          >
            <TrashIcon class="w-5 h-5 text-gray-900 hover:text-red-600" />
          </button>
        </div>
      </div>

      <!-- 模块内容 -->
      <div class="p-4">
        <!-- 求职意向内容 -->
        <JobIntentionContent
          v-if="module.type === 'job_intention'"
          :data="module.data"
        />
        <!-- 工作经历内容 -->
        <WorkExperienceContent 
          v-else-if="module.type === 'work_experience'"
          :data="module.data"
          @edit="item => $emit('edit-item', module.id, item)"
          @remove="id => $emit('remove-item', module.id, id)"
        />
        <!-- 其他模块的默认内容 -->
        <slot v-else :name="module.id" :data="module.data">
          <div v-if="module.data" class="text-gray-600">
            {{ JSON.stringify(module.data) }}
          </div>
          <div v-else class="text-gray-400 text-center py-4">
            暂无内容，点击编辑添加
          </div>
        </slot>
      </div>
    </div>
  </div>

  <!-- 删除确认弹窗 -->
  <el-dialog
    v-model="showDeleteConfirm"
    width="400px"
    :show-close="false"
    class="delete-confirm-dialog"
    destroy-on-close
  >
    <div class="p-6">
      <div class="flex items-start space-x-3">
        <div class="p-2 bg-red-50 rounded-full">
          <ExclamationTriangleIcon class="w-6 h-6 text-red-600" />
        </div>
        <div class="flex-1">
          <h3 class="text-lg font-medium text-gray-900">确认移除板块？</h3>
          <p class="mt-2 text-sm text-gray-500">
            移除板块后，该板块下的所有数据将被删除且无法恢复，请谨慎操作。
          </p>
        </div>
      </div>
      
      <div class="mt-6 flex justify-end space-x-3">
        <button
          @click="showDeleteConfirm = false"
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
        >
          取消
        </button>
        <button
          @click="confirmRemove"
          class="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
        >
          确认移除
        </button>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref } from 'vue'
import { 
  PencilSquareIcon, 
  TrashIcon,
  PlusIcon,
  ExclamationTriangleIcon 
} from '@heroicons/vue/24/outline'
import JobIntentionContent from './JobIntentionContent.vue'
import WorkExperienceContent from './WorkExperienceContent.vue'

defineProps({
  activeModules: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

defineEmits(['edit', 'add', 'remove', 'edit-item', 'remove-item'])

// 添加错误处理
const handleError = (error) => {
  console.error('WorkExperienceContent error:', error)
}

// 删除确认相关
const showDeleteConfirm = ref(false)
const moduleToDelete = ref(null)

// 处理移除按钮点击
const handleRemove = (moduleId) => {
  moduleToDelete.value = moduleId
  showDeleteConfirm.value = true
}

// 确认移除
const confirmRemove = () => {
  emit('remove', moduleToDelete.value)
  showDeleteConfirm.value = false
  moduleToDelete.value = null
}
</script>

<style scoped>
.module-header {
  @apply flex items-center justify-between px-4 py-3 border-b;
}

.module-title {
  @apply flex items-center space-x-2;
}

.module-actions {
  @apply flex items-center space-x-2;
}

.module-content {
  @apply p-4;
}

.empty-content {
  @apply text-gray-400 text-center py-4;
}

.delete-confirm-dialog :deep(.el-dialog__body) {
  @apply p-0;
}

/* 移动端适配 */
@media (max-width: 640px) {
  .delete-confirm-dialog {
    margin: 0 !important;
  }
  
  .p-6 {
    @apply p-4;
  }
}
</style>