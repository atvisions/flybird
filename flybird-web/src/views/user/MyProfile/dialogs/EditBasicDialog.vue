<!-- src/views/user/MyProfile/dialogs/EditBasicDialog.vue -->
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
          <h3 class="text-lg font-medium text-gray-900">编辑基本信息</h3>
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
      <div class="dialog-body  pt-4 pb-6">
        <el-form
          ref="formRef"
          :model="form"
          :disabled="loading"
        >
          <form @submit.prevent="handleSubmit" class="space-y-4 sm:space-y-5">
            <!-- 两列布局 -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-5">
              <!-- 姓名 -->
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700">姓名</label>
                <el-form-item prop="name" class="mb-0">
                  <input
                    v-model="form.name"
                    type="text"
                    placeholder="请输入姓名"
                    class="block w-full rounded-md border-gray-300 bg-gray-50 py-2 px-3 shadow-sm focus:border-gray-900 focus:ring-1 focus:ring-gray-900/10 sm:text-sm"
                  />
                </el-form-item>
              </div>

              <!-- 性别 -->
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700">性别</label>
                <el-form-item prop="gender" class="mb-0">
                  <Listbox v-model="form.gender">
                    <div class="relative w-full">
                      <ListboxButton class="relative w-full cursor-default rounded-md border border-gray-300 bg-gray-50 py-2 pl-3 pr-10 text-left shadow-sm focus:border-gray-900 focus:outline-none focus:ring-1 focus:ring-gray-900/10 sm:text-sm">
                        <span class="block truncate">{{ getGenderLabel(form.gender) }}</span>
                        <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                          <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                        </span>
                      </ListboxButton>

                      <transition
                        leave-active-class="transition ease-in duration-100"
                        leave-from-class="opacity-100"
                        leave-to-class="opacity-0"
                      >
                        <ListboxOptions class="absolute z-10 mt-1 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                          <ListboxOption
                            v-for="option in GENDER_OPTIONS"
                            :key="option.value"
                            :value="option.value"
                            v-slot="{ active, selected }"
                          >
                            <div :class="[
                              active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                              'relative cursor-default select-none py-2 pl-3 pr-9'
                            ]">
                              <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">
                                {{ option.label }}
                              </span>
                              <span v-if="selected" :class="[active ? 'text-gray-900' : 'text-gray-600', 'absolute inset-y-0 right-0 flex items-center pr-4']">
                                <CheckIcon class="h-5 w-5" aria-hidden="true" />
                              </span>
                            </div>
                          </ListboxOption>
                        </ListboxOptions>
                      </transition>
                    </div>
                  </Listbox>
                </el-form-item>
              </div>

              <!-- 手机号 -->
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700">手机号</label>
                <el-form-item prop="phone" class="mb-0">
                  <input
                    v-model="form.phone"
                    type="tel"
                    placeholder="请输入手机号"
                    class="block w-full rounded-md border-gray-300 bg-gray-50 py-2 px-3 shadow-sm focus:border-gray-900 focus:ring-1 focus:ring-gray-900/10 sm:text-sm"
                  />
                </el-form-item>
              </div>

              <!-- 邮箱 -->
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700">邮箱</label>
                <el-form-item prop="email" class="mb-0">
                  <input
                    v-model="form.email"
                    type="email"
                    placeholder="请输入邮箱"
                    class="block w-full rounded-md border-gray-300 bg-gray-50 py-2 px-3 shadow-sm focus:border-gray-900 focus:ring-1 focus:ring-gray-900/10 sm:text-sm"
                  />
                </el-form-item>
              </div>

              <!-- 所在地 -->
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700">所在地</label>
                <el-form-item prop="location" class="mb-0">
                  <input
                    v-model="form.location"
                    type="text"
                    placeholder="请输入所在地"
                    class="block w-full rounded-md border-gray-300 bg-gray-50 py-2 px-3 shadow-sm focus:border-gray-900 focus:ring-1 focus:ring-gray-900/10 sm:text-sm"
                  />
                </el-form-item>
              </div>

              <!-- 出生日期 -->
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700">出生日期</label>
                <el-form-item prop="birth_date" class="mb-0">
                  <div class="relative w-full">
                    <input
                      v-model="form.birth_date"
                      type="date"
                      class="!w-full block rounded-md border-gray-300 bg-gray-50 py-2 pl-3 pr-10 text-left shadow-sm focus:border-gray-900 focus:outline-none focus:ring-1 focus:ring-gray-900/10 sm:text-sm"
                    />
                    <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                      <CalendarIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                    </span>
                  </div>
                </el-form-item>
              </div>
            </div>

            <!-- 个人简介 -->
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700">个人简介</label>
              <el-form-item prop="personal_summary" class="mb-0">
                <textarea
                  v-model="form.personal_summary"
                  rows="4"
                  placeholder="请输入个人简介"
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
import { XMarkIcon, ChevronUpDownIcon, CheckIcon, CalendarIcon } from '@heroicons/vue/24/outline'
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from '@headlessui/vue'

const props = defineProps({
  modelValue: Boolean,
  initialData: {
    type: Object,
    default: () => ({})
  },
  loading: Boolean
})

const emit = defineEmits(['update:modelValue', 'submit'])

const form = ref({
  name: '',
  gender: '',
  phone: '',
  email: '',
  location: '',
  birth_date: '',
  personal_summary: ''
})

// 监听初始数据变化
watch(
  () => props.initialData,
  (newVal) => {
    if (newVal) {
      form.value = { ...newVal }
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
  // 直接提交表单数据，不需要额外包装
  emit('submit', form.value)
}

const GENDER_OPTIONS = [
  { value: 'male', label: '男' },
  { value: 'female', label: '女' }
]

const getGenderLabel = (value) => {
  const option = GENDER_OPTIONS.find(option => option.value === value)
  return option ? option.label : ''
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

  .dialog-body {
    @apply px-4;  /* 减小内边距 */
  }

  /* 在移动端时所有输入框占满整行 */
  .grid {
    @apply grid-cols-1 gap-3;
  }

  /* 调整输入框在移动端的大小和间距 */
  input, select, textarea {
    @apply text-base py-3;  /* 增加高度使触摸更容易 */
  }

  /* 调整标签和输入框的间距 */
  .space-y-2 {
    @apply space-y-1.5;
  }

  /* 调整表单项之间的间距 */
  .space-y-4 {
    @apply space-y-3;
  }

  /* 确保底部按钮有足够的大小和间距 */
  .dialog-footer button {
    @apply py-2.5 px-4 text-base;
  }
}

/* 桌面端样式 */
@media (min-width: 641px) {
  .edit-dialog :deep(.el-dialog__body) {
    @apply p-0;
    max-height: calc(80vh - 120px);
    overflow-y: auto;
  }
}

/* 通用样式 */
.dialog-header {
  @apply px-6 pt-4 pb-0 border-b border-gray-200;
}
</style>