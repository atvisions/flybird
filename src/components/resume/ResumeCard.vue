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
  Dialog as HDialog,
  DialogPanel as HDialogPanel,
  DialogTitle as HDialogTitle,
  TransitionChild,
  TransitionRoot,
} from '@headlessui/vue'
import { ElDialog } from 'element-plus'

const emit = defineEmits(['like', 'edit', 'delete'])

const router = useRouter()
const showPreview = ref(false)
const showDeleteConfirm = ref(false)
const deleteLoading = ref(false)

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
      creator_name: '匿名用户',
      creator_avatar: '',
      creator_is_vip: false,
      creator_position: '',
      useCount: 0,
      viewCount: 0,
      likes: 0,
      isPro: false,
      is_recommended: false,
      isLiked: false,
      is_owner: false
    }),
    validator: (obj) => {
      // 确保必需的属性存在且类型正确
      return typeof obj === 'object' && obj !== null &&
        typeof obj.id !== 'undefined' &&
        typeof obj.name !== 'undefined' &&
        typeof obj.category !== 'undefined'
    }
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

<template>
  <div class="resume-card relative group">
    <!-- 缩略图部分 -->
    <div class="relative overflow-hidden rounded-lg cursor-pointer" @click="showPreview = true">
      <img 
        :src="template.thumbnail" 
        :alt="template.name"
        class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
      />
      
      <!-- 悬浮遮罩 -->
      <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
        <EyeIcon class="w-8 h-8 text-white" />
      </div>
    </div>

    <!-- 模板信息 -->
    <div class="mt-3 space-y-2">
      <div class="flex items-start justify-between">
        <h3 class="text-lg font-medium text-gray-900 truncate flex-1">{{ template.name }}</h3>
        <div class="flex items-center space-x-2">
          <button 
            class="text-gray-400 hover:text-red-500 transition-colors"
            :class="{ 'text-red-500': template.isLiked }"
            @click="$emit('like', template)"
          >
            <component :is="template.isLiked ? HeartSolidIcon : HeartOutlineIcon" class="w-5 h-5" />
          </button>
        </div>
      </div>

      <!-- 创建者信息 -->
      <div class="flex items-center space-x-2 text-sm text-gray-500">
        <img 
          v-if="template.creator_avatar" 
          :src="template.creator_avatar" 
          :alt="template.creator_name"
          class="w-5 h-5 rounded-full"
        />
        <UserIcon v-else class="w-5 h-5" />
        <span>{{ template.creator_name }}</span>
        <CrownIcon v-if="template.creator_is_vip" class="w-5 h-5 text-yellow-500" />
      </div>

      <!-- 统计信息 -->
      <div class="flex items-center space-x-4 text-sm text-gray-500">
        <span class="flex items-center space-x-1">
          <DocumentIcon class="w-4 h-4" />
          <span>{{ template.useCount }}次使用</span>
        </span>
        <span class="flex items-center space-x-1">
          <EyeIcon class="w-4 h-4" />
          <span>{{ template.viewCount }}次浏览</span>
        </span>
      </div>

      <!-- 操作按钮 -->
      <div v-if="template.is_owner" class="flex items-center space-x-2 mt-2">
        <button
          class="flex items-center space-x-1 px-3 py-1 text-sm text-blue-600 hover:bg-blue-50 rounded-md transition-colors"
          @click="$emit('edit', template)"
        >
          <Edit theme="outline" size="16" />
          <span>编辑</span>
        </button>
        <button
          class="flex items-center space-x-1 px-3 py-1 text-sm text-red-600 hover:bg-red-50 rounded-md transition-colors"
          @click="handleDelete"
        >
          <Delete theme="outline" size="16" />
          <span>删除</span>
        </button>
      </div>
    </div>
  </div>

  <!-- 预览弹窗 -->
  <ElDialog
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
  </ElDialog>

  <!-- 删除确认弹窗 -->
  <TransitionRoot appear :show="showDeleteConfirm" as="template">
    <HDialog as="div" class="relative z-50" @close="showDeleteConfirm = false">
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

      <div class="fixed inset-0 overflow-hidden">
        <div class="flex min-h-full items-center justify-center p-4 text-center">
          <TransitionChild
            as="div"
            enter="ease-out duration-300"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="ease-in duration-200"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <HDialogPanel class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
              <HDialogTitle class="text-lg font-medium leading-6 text-gray-900">
                确认删除
              </HDialogTitle>
              <div class="mt-2">
                <p class="text-sm text-gray-500">
                  您确定要删除这个模板吗？
                </p>
              </div>

              <div class="mt-4 flex justify-end space-x-2">
                <button
                  type="button"
                  class="inline-flex justify-center rounded-md border border-transparent bg-red-100 px-4 py-2 text-sm font-medium text-red-900 hover:bg-red-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-red-500 focus-visible:ring-offset-2"
                  @click="confirmDelete"
                >
                  删除
                </button>
                <button
                  type="button"
                  class="inline-flex justify-center rounded-md border border-transparent bg-gray-100 px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-gray-500 focus-visible:ring-offset-2"
                  @click="showDeleteConfirm = false"
                >
                  取消
                </button>
              </div>
            </HDialogPanel>
          </TransitionChild>
        </div>
      </div>
    </HDialog>
  </TransitionRoot>
</template>

<style scoped>
.resume-card {
  @apply bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow duration-300;
}

.preview-dialog :deep(.el-dialog__body) {
  @apply p-0;
}

.preview-dialog-content {
  @apply bg-gray-100 p-4;
}
</style> 