<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    :width="dialogWidth"
    :fullscreen="isMobile"
    :close-on-click-modal="false"
    :show-close="false"
    @close="handleClose"
    class="edit-dialog"
    destroy-on-close
  >
    <div class="dialog-container">
      <!-- Header -->
      <div class="dialog-header">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium text-gray-900">
            {{ initialData.id ? '编辑工作经历' : '添加工作经历' }}
          </h3>
          <!-- 移动端显示关闭按钮 -->
          <button
            v-if="isMobile"
            @click="handleClose"
            class="text-gray-400 hover:text-gray-500"
          >
            <XMarkIcon class="h-6 w-6" />
          </button>
        </div>
      </div>

      <!-- Body -->
      <div class="dialog-body p-4">
        <el-form
          ref="formRef"
          :model="form"
          :disabled="loading"
        >
          <form @submit.prevent="handleSubmit" class="space-y-4 sm:space-y-5">
            <!-- 公司名称 -->
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700">公司名称</label>
              <el-form-item prop="company" class="mb-0">
                <input
                  v-model="form.company"
                  type="text"
                  placeholder="请输入公司名称"
                  class="block w-full rounded-md border-gray-300 bg-gray-50 py-2 px-3 shadow-sm focus:border-gray-900 focus:ring-1 focus:ring-gray-900/10 sm:text-sm"
                />
              </el-form-item>
            </div>

            <!-- 两列布局：所在部门和职位名称 -->
            <div class="grid grid-cols-2 gap-4">
              <!-- 所在部门 -->
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700">所在部门</label>
                <el-form-item prop="department" class="mb-0">
                  <input
                    v-model="form.department"
                    type="text"
                    placeholder="请输入所在部门"
                    class="block w-full rounded-md border-gray-300 bg-gray-50 py-2 px-3 shadow-sm focus:border-gray-900 focus:ring-1 focus:ring-gray-900/10 sm:text-sm"
                  />
                </el-form-item>
              </div>

              <!-- 职位名称 -->
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700">职位名称</label>
                <el-form-item prop="position" class="mb-0">
                  <input
                    v-model="form.position"
                    type="text"
                    placeholder="请输入职位名称"
                    class="block w-full rounded-md border-gray-300 bg-gray-50 py-2 px-3 shadow-sm focus:border-gray-900 focus:ring-1 focus:ring-gray-900/10 sm:text-sm"
                  />
                </el-form-item>
              </div>

              <!-- 在职时间 -->
              <div class="space-y-2 col-span-2">
                <label class="block text-sm font-medium text-gray-700">在职时间</label>
                <div class="flex items-center">
                  <el-form-item prop="start_date" class="mb-0 flex-1">
                    <div class="relative w-full">
                      <input
                        v-model="form.start_date"
                        type="date"
                        class="!w-full block rounded-md border-gray-300 bg-gray-50 py-2 pl-3 pr-10 text-left shadow-sm focus:border-gray-900 focus:outline-none focus:ring-1 focus:ring-gray-900/10 sm:text-sm"
                      />
                      <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                        <CalendarIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                      </span>
                    </div>
                  </el-form-item>
                  
                  <span v-if="!form.is_current" class="text-gray-500 px-1 flex-shrink-0">-</span>
                  
                  <el-form-item v-if="!form.is_current" prop="end_date" class="mb-0 flex-1">
                    <div class="relative w-full">
                      <input
                        v-model="form.end_date"
                        type="date"
                        class="!w-full block rounded-md border-gray-300 bg-gray-50 py-2 pl-3 pr-10 text-left shadow-sm focus:border-gray-900 focus:outline-none focus:ring-1 focus:ring-gray-900/10 sm:text-sm"
                      />
                      <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                        <CalendarIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                      </span>
                    </div>
                  </el-form-item>
                </div>
                
                <div class="mt-2">
                  <label class="inline-flex items-center">
                    <input
                      type="checkbox"
                      v-model="form.is_current"
                      class="rounded border-gray-300 text-gray-900 focus:ring-gray-900/10"
                    />
                    <span class="ml-2 text-sm text-gray-700">至今</span>
                  </label>
                </div>
              </div>
            </div>

            <!-- 工作描述 -->
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700">工作描述</label>
              <el-form-item prop="responsibilities" class="mb-0">
                <textarea
                  v-model="form.responsibilities"
                  rows="4"
                  placeholder="请详细描述您的工作职责和内容（至少50字）"
                  class="block w-full rounded-md border-gray-300 bg-gray-50 py-2 px-3 shadow-sm focus:border-gray-900 focus:ring-1 focus:ring-gray-900/10 sm:text-sm"
                ></textarea>
              </el-form-item>
            </div>

            <!-- 工作成就 -->
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700">工作成就</label>
              <el-form-item prop="achievements" class="mb-0">
                <textarea
                  v-model="form.achievements"
                  rows="3"
                  placeholder="请描述您在这份工作中取得的成就"
                  class="block w-full rounded-md border-gray-300 bg-gray-50 py-2 px-3 shadow-sm focus:border-gray-900 focus:ring-1 focus:ring-gray-900/10 sm:text-sm"
                ></textarea>
              </el-form-item>
            </div>

            <!-- 技术栈 -->
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700">技术栈</label>
              <el-form-item prop="technologies" class="mb-0">
                <textarea
                  v-model="form.technologies"
                  rows="2"
                  placeholder="请列出您使用的主要技术栈"
                  class="block w-full rounded-md border-gray-300 bg-gray-50 py-2 px-3 shadow-sm focus:border-gray-900 focus:ring-1 focus:ring-gray-900/10 sm:text-sm"
                ></textarea>
              </el-form-item>
            </div>
          </form>
        </el-form>
      </div>

      <!-- Footer -->
      <div class="dialog-footer">
        <div class="flex justify-end space-x-3">
          <button
            type="button"
            @click="handleClose"
            class="rounded-md border border-gray-300 bg-white px-3 sm:px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-900/10"
          >
            取消
          </button>
          <button
            type="button"
            @click="handleSubmit"
            :disabled="loading"
            class="rounded-md border border-transparent bg-gray-900 px-3 sm:px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-900/10 disabled:opacity-50"
          >
            {{ loading ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useWindowSize } from '@vueuse/core'
import { XMarkIcon, CalendarIcon } from '@heroicons/vue/24/outline'
import { ElMessage } from 'element-plus'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  initialData: {
    type: Object,
    default: () => ({})
  },
  loading: Boolean
})

const emit = defineEmits(['update:modelValue', 'submit'])

// 表单引用
const formRef = ref(null)

// 表单数据
const form = ref({
  id: null,
  company: '',
  position: '',
  department: '',
  start_date: null,
  end_date: null,
  is_current: false,
  responsibilities: '',
  achievements: '',
  technologies: ''
})

// 监听初始数据变化
watch(
  () => props.initialData,
  (newVal) => {
    if (newVal) {
      console.log('接收到的初始数据:', newVal)
      form.value = {
        ...newVal,
        responsibilities: newVal.description || '',
      }
      console.log('初始化后的表单数据:', form.value)
    }
  },
  { immediate: true }
)

const { width } = useWindowSize()
const isMobile = computed(() => width.value < 640)

// 根据屏幕宽度设置弹窗宽度
const dialogWidth = computed(() => {
  if (isMobile.value) return '100%'
  if (width.value < 1024) return '80%'
  return '640px'
})

// 处理关闭对话框
const handleClose = () => {
  emit('update:modelValue', false)
}

// 提交表单
const handleSubmit = () => {
  // 打印表单数据，用于调试
  console.log('提交前的表单数据:', form.value)
  
  // 确保数据格式正确，并且字段名匹配
  const formData = {
    ...form.value,
    // 将 responsibilities 映射到 description
    description: form.value.responsibilities || '',
    // 确保日期格式正确
    start_date: form.value.start_date || null,
    end_date: form.value.is_current ? null : form.value.end_date,
    is_current: Boolean(form.value.is_current)
  }

  // 数据验证
  if (!formData.company) {
    ElMessage.error('请输入公司名称')
    return
  }

  if (!formData.description || formData.description.length < 50) {
    ElMessage.error('工作描述至少需要50个字符')
    return
  }

  if (!formData.start_date) {
    ElMessage.error('请选择开始日期')
    return
  }

  if (!formData.is_current && !formData.end_date) {
    ElMessage.error('请选择结束日期或勾选"至今"')
    return
  }

  // 删除多余的字段
  delete formData.responsibilities

  console.log('处理后的提交数据:', formData)
  emit('submit', formData)
}
</script>

<style>
.edit-dialog {
  @apply max-h-screen flex flex-col;
}

.edit-dialog :deep(.el-dialog__body) {
  @apply flex-1 overflow-y-auto;
}

.edit-dialog :deep(.el-dialog__footer) {
  @apply sticky bottom-0 bg-gray-50 z-10;
}

/* 移动端样式 */
@media (max-width: 640px) {
  .edit-dialog {
    margin: 0 !important;
  }

  .edit-dialog :deep(.el-dialog__body) {
    @apply p-0;
    height: calc(100vh - 120px);
    overflow-y: auto;
  }

  /* 调整表单布局 */
  .dialog-body {
    @apply px-4;
  }

  /* 在移动端时所有输入框占满整行 */
  .grid {
    @apply grid-cols-1 gap-3;
  }

  /* 调整输入框在移动端的大小和间距 */
  input, select, textarea {
    @apply text-base py-3;
  }

  /* 调整日期选择器在移动端的显示 */
  input[type="date"] {
    @apply py-2.5;
    min-height: 42px;
  }
}

/* 桌面端样式 */
@media (min-width: 641px) {
  .edit-dialog :deep(.el-dialog__body) {
    @apply p-0;
    max-height: calc(80vh - 120px);
    overflow-y: auto;
  }

  /* 桌面端保持原有的间距 */
  .dialog-body {
    @apply px-6;
  }
}

/* 通用样式 */
.dialog-header {
  @apply px-6 py-4 border-b border-gray-200;
}

.dialog-footer {
  @apply px-6 py-4 bg-gray-50 border-t border-gray-200;
}

/* 输入框聚焦时的样式 */
input:focus, textarea:focus {
  @apply ring-2 ring-gray-900/10 border-gray-900;
}

/* 禁用状态的样式 */
input:disabled, textarea:disabled {
  @apply bg-gray-100 cursor-not-allowed;
}

</style> 