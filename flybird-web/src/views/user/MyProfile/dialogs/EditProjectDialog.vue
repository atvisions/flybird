<template>
  <TransitionRoot appear :show="modelValue" as="template">
    <Dialog as="div" class="relative z-50" @close="handleClose">
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
            <DialogPanel class="w-full max-w-2xl transform overflow-hidden rounded-xl bg-white text-left align-middle shadow-xl transition-all">
              <!-- 头部 -->
              <DialogTitle 
                as="div" 
                class="flex items-center justify-between border-b border-gray-200 px-6 py-4"
              >
                <h3 class="text-lg font-medium text-gray-900">
                  {{ initialData?.id ? '编辑项目经历' : '添加项目经历' }}
                </h3>
                <button
                  @click="handleClose"
                  class="rounded-full p-1 hover:bg-gray-100 transition-colors"
                >
                  <XMarkIcon class="w-5 h-5 text-gray-400" />
                </button>
              </DialogTitle>

              <!-- 表单内容 -->
              <form @submit.prevent="handleSubmit" class="p-6">
                <div class="space-y-6">
                  <!-- 项目名称 -->
                  <div class="space-y-1">
                    <label class="block text-sm font-medium text-gray-700">
                      项目名称 <span class="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      v-model="form.name"
                      required
                      :class="[
                        'w-full rounded-lg border py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10',
                        errors.name ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
                      ]"
                      placeholder="请输入项目名称"
                    />
                    <p v-if="errors.name" class="text-sm text-red-500 mt-1">{{ errors.name }}</p>
                  </div>

                  <!-- 项目角色 -->
                  <div class="space-y-1">
                    <label class="block text-sm font-medium text-gray-700">
                      项目角色 <span class="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      v-model="form.role"
                      required
                      :class="[
                        'w-full rounded-lg border py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10',
                        errors.role ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
                      ]"
                      placeholder="请输入你在项目中担任的角色"
                    />
                    <p v-if="errors.role" class="text-sm text-red-500 mt-1">{{ errors.role }}</p>
                  </div>

                  <!-- 起止时间 -->
                  <div class="space-y-2">
                    <label class="block text-sm font-medium text-gray-700">在职时间</label>
                    <div class="flex items-center space-x-4">
                      <div class="relative flex-1">
                        <input
                          v-model="form.start_date"
                          type="date"
                          :class="[
                            'w-full rounded-lg border py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10',
                            errors.start_date ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
                          ]"
                        />
                        <CalendarIcon class="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" />
                      </div>
                      
                      <span v-if="!form.is_current" class="text-gray-500">至</span>
                      
                      <div v-if="!form.is_current" class="relative flex-1">
                        <input
                          v-model="form.end_date"
                          type="date"
                          :class="[
                            'w-full rounded-lg border py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10',
                            errors.end_date ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
                          ]"
                        />
                        <CalendarIcon class="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" />
                      </div>
                    </div>
                    <p v-if="errors.start_date || errors.end_date" class="text-sm text-red-500 mt-1">
                      {{ errors.start_date || errors.end_date }}
                    </p>
                    
                    <label class="inline-flex items-center mt-2">
                      <input
                        type="checkbox"
                        v-model="form.is_current"
                        class="rounded border-gray-300 text-blue-600 focus:ring-blue-500/10"
                      />
                      <span class="ml-2 text-sm text-gray-700">至今</span>
                    </label>
                  </div>

                  <!-- 项目描述 -->
                  <div class="space-y-1">
                    <label class="block text-sm font-medium text-gray-700">
                      项目描述 <span class="text-red-500">*</span>
                    </label>
                    <el-input
                      v-model="form.description"
                      type="textarea"
                      :rows="4"
                      placeholder="请描述项目的主要内容、技术栈和你负责的部分"
                      :class="[
                        '!w-full',
                        errors.description ? 'is-error' : ''
                      ]"
                    />
                    <p v-if="errors.description" class="text-sm text-red-500 mt-1">{{ errors.description }}</p>
                  </div>

                  <!-- 项目成就 -->
                  <div class="space-y-1">
                    <label class="block text-sm font-medium text-gray-700">
                      项目成就
                    </label>
                    <el-input
                      v-model="form.achievement"
                      type="textarea"
                      :rows="3"
                      placeholder="请描述在项目中取得的成就和贡献（选填）"
                      class="!w-full"
                    />
                  </div>

                  <!-- 底部按钮 -->
                  <div class="flex justify-end space-x-3 pt-6">
                    <button
                      type="button"
                      @click="handleClose"
                      class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
                    >
                      取消
                    </button>
                    <button
                      type="submit"
                      :disabled="loading"
                      class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {{ loading ? '保存中...' : '确认' }}
                    </button>
                  </div>
                </div>
              </form>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { ref, watch } from 'vue'
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionRoot,
  TransitionChild
} from '@headlessui/vue'
import { XMarkIcon, CalendarIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  modelValue: Boolean,
  initialData: {
    type: Object,
    default: () => ({})
  },
  loading: Boolean
})

const emit = defineEmits(['update:modelValue', 'submit'])

// 表单数据
const form = ref({
  id: null,          // 添加 id 字段
  name: '',          // 项目名称
  role: '',          // 担任角色
  start_date: '',    // 开始日期
  end_date: '',      // 结束日期
  is_current: false, // 是否进行中
  description: '',   // 项目描述
  achievement: ''    // 项目成就
})

// 添加错误状态
const errors = ref({
  name: '',
  role: '',
  start_date: '',
  end_date: '',
  description: ''
})

// 监听初始数据变化
watch(() => props.initialData, (newVal) => {
  if (newVal) {
    form.value = {
      id: newVal.id || null,
      name: newVal.name || '',
      role: newVal.role || '',
      start_date: newVal.start_date || '',
      end_date: newVal.end_date || '',
      is_current: !!newVal.is_current,
      description: newVal.description || '',
      achievement: newVal.achievement || ''
    }
  }
}, { immediate: true, deep: true })

const handleClose = () => {
  emit('update:modelValue', false)
}

// 验证表单
const validateForm = () => {
  let isValid = true
  errors.value = {
    name: '',
    role: '',
    start_date: '',
    end_date: '',
    description: ''
  }

  // 必填字段验证
  if (!form.value.name?.trim()) {
    errors.value.name = '请输入项目名称'
    isValid = false
  }

  if (!form.value.role?.trim()) {
    errors.value.role = '请输入项目角色'
    isValid = false
  }

  if (!form.value.start_date) {
    errors.value.start_date = '请选择开始时间'
    isValid = false
  }

  if (!form.value.is_current && !form.value.end_date) {
    errors.value.end_date = '请选择结束时间或勾选"至今"'
    isValid = false
  }

  if (!form.value.description?.trim()) {
    errors.value.description = '请输入项目描述'
    isValid = false
  }

  // 日期逻辑验证
  if (form.value.start_date && form.value.end_date && !form.value.is_current) {
    const startDate = new Date(form.value.start_date)
    const endDate = new Date(form.value.end_date)
    if (endDate < startDate) {
      errors.value.end_date = '结束时间不能早于开始时间'
      isValid = false
    }
  }

  return isValid
}

// 提交处理
const handleSubmit = () => {
  if (!validateForm()) {
    return
  }

  const formData = {
    ...form.value,
    // 处理日期和布尔值
    start_date: form.value.start_date,
    end_date: form.value.is_current ? null : form.value.end_date,
    is_current: form.value.is_current,
    // 处理文本字段
    name: form.value.name.trim(),
    role: form.value.role.trim(),
    description: form.value.description.trim(),
    achievement: form.value.achievement?.trim() || ''
  }

  // 如果是新建，不传 id
  if (!formData.id) {
    delete formData.id
  }

  emit('submit', formData)
}
</script>

<style scoped>
/* 添加一些过渡动画 */
.transition-all {
  @apply duration-200;
}

/* 输入框聚焦效果 */
input:focus, select:focus {
  @apply ring-2 ring-blue-500/10 border-blue-500;
}

/* 下拉选项悬停效果 */
.hover\:bg-blue-50:hover {
  @apply bg-blue-50 text-blue-600;
}

/* 移动端适配 */
@media (max-width: 640px) {
  .el-date-picker {
    width: 100% !important;
  }
}
</style> 