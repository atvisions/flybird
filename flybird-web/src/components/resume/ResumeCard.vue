<template>
  <div class="group relative bg-white rounded-lg overflow-hidden border border-gray-100 hover:border-gray-300 hover:shadow-md transition-all duration-300">
    <!-- 推荐标记 -->
    <div v-if="template.is_recommended" 
      class="absolute -top-0 -right-0 z-10 bg-amber-500 text-white text-xs px-3 py-1.5 rounded-bl font-medium flex items-center">
      <SparklesIcon class="w-3 h-3 mr-1" />
      推荐
    </div>

    <!-- 缩略图 -->
    <div class="relative aspect-[1/0.8] bg-gray-50">
      <img 
        v-if="template.thumbnail" 
        :src="template.thumbnail" 
        :alt="template.name"
        class="w-full h-full object-cover object-top cursor-zoom-in"
        @click="showPreview = true"
      />
      <div v-else class="w-full h-full flex items-center justify-center text-gray-400">
        <DocumentIcon class="w-12 h-12" />
      </div>
    </div>

    <!-- 预览弹窗 -->
    <el-dialog
      v-model="showPreview"
      :title="template.name"
      width="794px"
      class="preview-dialog"
      align-center
      :close-on-click-modal="true"
      :show-close="true"
    >
      <div class="preview-dialog-content">
        <img 
          :src="template.thumbnail" 
          :alt="template.name"
          class="w-[794px] h-[1123px] object-contain bg-white"
        />
      </div>
    </el-dialog>

    <!-- 删除确认弹窗 -->
    <TransitionRoot appear :show="showDeleteConfirm" as="template">
      <Dialog as="div" class="relative z-50" @close="showDeleteConfirm = false">
        <TransitionChild
          as="div"
          :show="true"
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
                <!-- 头部 -->
                <DialogTitle as="div" class="flex items-center justify-between px-6 py-4 border-b border-gray-200">
                  <h3 class="text-lg font-medium text-gray-900">删除确认</h3>
                  <button
                    @click="showDeleteConfirm = false"
                    class="p-1 rounded-full hover:bg-gray-100 transition-colors"
                  >
                    <XMarkIcon class="w-5 h-5 text-gray-400" />
                  </button>
                </DialogTitle>

                <!-- 内容 -->
                <div class="p-6">
                  <p class="text-sm text-gray-600">确定要删除该模板吗？此操作不可恢复。</p>
                  
                  <!-- 底部按钮 -->
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
                      :disabled="deleteLoading"
                      class="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {{ deleteLoading ? '删除中...' : '确认删除' }}
                    </button>
                  </div>
                </div>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>

    <!-- 内容区域 -->
    <div class="p-3">
      <!-- 标题和标签 -->
      <div class="mb-2">
        <h3 class="text-sm font-medium text-gray-900 mb-1 line-clamp-1">{{ template.name }}</h3>
        <div class="flex items-center gap-2">
          <span class="px-2 py-0.5 bg-gray-50 text-gray-600 rounded text-xs">{{ template.category }}</span>
          <span v-if="template.isPro" class="px-2 py-0.5 bg-amber-50 text-amber-600 rounded text-xs">Pro</span>
        </div>
      </div>

      <!-- 简介 -->
      <p v-if="template.description" 
        class="text-sm text-gray-500 mb-3 line-clamp-2 min-h-[2.5rem]">
        {{ template.description }}
      </p>
      <p v-else class="text-sm text-gray-500 mb-3 min-h-[2.5rem]">暂无简介</p>

      <!-- 底部信息 -->
      <div class="flex flex-col gap-3">
        <div class="flex items-center justify-between">
          <!-- 创作者信息 -->
          <div class="flex items-center gap-1.5">
            <div class="relative">
              <a 
                v-if="template.creator"
                :href="`${config.API_URL.split(':')[0]}:${config.API_URL.split(':')[1]}:8080/u/${template.creator}`"
                target="_blank"
                class="block cursor-pointer"
              >
                <img 
                  v-if="template.creator_avatar" 
                  :src="template.creator_avatar" 
                  :alt="template.creator_name"
                  class="w-5 h-5 rounded-full object-cover"
                />
                <div v-else class="w-5 h-5 rounded-full bg-gray-100 flex items-center justify-center">
                  <UserIcon class="w-3 h-3 text-gray-400" />
                </div>
                <!-- VIP 标识 -->
                <div 
                  v-if="template.creator_is_vip" 
                  class="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 bg-gradient-to-r from-amber-500 to-yellow-500 rounded-full flex items-center justify-center"
                >
                  <CrownIcon class="w-1.5 h-1.5 text-white" />
                </div>
              </a>
            </div>
            <span class="text-xs text-gray-500 truncate max-w-[80px]">{{ template.creator_name }}</span>
          </div>

          <!-- 统计信息 -->
          <div class="flex items-center gap-2">
            <button
              @click.stop="$emit('like')"
              class="flex items-center text-gray-400 hover:text-rose-600 text-sm transition-colors"
              :class="{ 
                'text-rose-600': template.isLiked,
                'opacity-60 cursor-not-allowed': likeLoading 
              }"
              :disabled="likeLoading"
            >
              <component 
                :is="template.isLiked ? HeartSolidIcon : HeartOutlineIcon" 
                class="w-4 h-4 mr-1"
              />
              {{ template.likes || 0 }}
            </button>
            <div class="flex items-center text-gray-400 text-xs">
              <EyeIcon class="w-3.5 h-3.5" />
              <span class="ml-0.5">{{ template.viewCount }}</span>
            </div>
          </div>
        </div>

        <!-- 使用按钮 -->
        <button 
          @click="handleUseTemplate(template)"
          class="w-full py-2 bg-blue-500 hover:bg-blue-600 text-white rounded text-sm font-medium transition-colors"
        >
          使用该模版
        </button>
      </div>
    </div>

    <!-- 操作按钮区域 -->
    <div v-if="onlyMine" class="card-actions">
      <button 
        class="action-btn"
        @click="$emit('edit', template)"
      >
        <Edit theme="outline" :size="14" />
        编辑
      </button>
      <button 
        class="action-btn danger"
        @click="handleDelete"
      >
        <Delete theme="outline" :size="14" />
        删除
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { 
  DocumentIcon, 
  UserIcon, 
  EyeIcon, 
  HeartIcon as HeartOutlineIcon,
  PlusIcon,
  CrownIcon,
  SparklesIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'
import { HeartIcon as HeartSolidIcon } from '@heroicons/vue/24/solid'
import { useRouter } from 'vue-router'
import config from '@/config'
import { Edit, Delete, Plus } from '@icon-park/vue-next'
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionRoot,
  TransitionChild
} from '@headlessui/vue'

const emit = defineEmits(['like', 'use', 'edit', 'delete'])

const router = useRouter()
const showPreview = ref(false)
const showDeleteConfirm = ref(false)
const deleteLoading = ref(false)

const handleUseTemplate = (template) => {
  router.push(`/editor/resume/new/${template.id}`)
}

const handleDelete = () => {
  showDeleteConfirm.value = true
}

const confirmDelete = async () => {
  deleteLoading.value = true
  try {
    emit('delete', props.template)
    showDeleteConfirm.value = false
  } finally {
    deleteLoading.value = false
  }
}

const props = defineProps({
  template: {
    type: Object,
    required: true,
    default: () => ({
      id: '',
      name: '',
      description: '',
      thumbnail: '',
      category: '',
      creator: '',
      creator_name: '',
      creator_avatar: '',
      creator_is_vip: false,
      creator_position: '',
      useCount: 0,
      viewCount: 0,
      isPro: false,
      is_recommended: false
    })
  },
  likeLoading: {
    type: Boolean,
    default: false
  },
  onlyMine: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.action-btn.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.action-btn:disabled {
  pointer-events: none;
}

.preview-dialog-content {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0;
  background-color: #fff;
}

:deep(.el-dialog) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.el-dialog__body) {
  padding: 0;
  margin: 0;
}

:deep(.el-dialog__header) {
  padding: 16px 20px;
  margin: 0;
  border-bottom: 1px solid #f0f0f0;
}

.card-actions {
  display: flex;
  gap: 8px;
  padding: 12px;
  border-top: 1px solid #f0f0f0;
}

.action-btn {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  height: 32px;
  padding: 0 12px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 14px;
  background: white;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover:not(:disabled) {
  border-color: #d1d5db;
  background: #f9fafb;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-btn.primary {
  color: #1890ff;
  border-color: #1890ff;
}

.action-btn.primary:hover {
  background: #1890ff;
  color: white;
}

.action-btn.danger {
  color: #f43f5e;
  border-color: #f43f5e;
}

.action-btn.danger:hover {
  background: #f43f5e;
  color: white;
}
</style> 