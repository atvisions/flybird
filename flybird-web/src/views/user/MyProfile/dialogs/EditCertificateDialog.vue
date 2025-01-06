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
                  {{ initialData?.id ? '编辑证书奖项' : '添加证书奖项' }}
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
                  <!-- 证书名称 -->
                  <div class="space-y-1">
                    <label class="block text-sm font-medium text-gray-700">
                      证书名称 <span class="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      v-model="form.name"
                      required
                      :class="[
                        'w-full rounded-lg border py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10',
                        errors.name ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
                      ]"
                      placeholder="请输入证书名称"
                    />
                    <p v-if="errors.name" class="text-sm text-red-500 mt-1">{{ errors.name }}</p>
                  </div>

                  <!-- 颁发机构 -->
                  <div class="space-y-1">
                    <label class="block text-sm font-medium text-gray-700">
                      颁发机构 <span class="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      v-model="form.issuing_authority"
                      required
                      :class="[
                        'w-full rounded-lg border py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10',
                        errors.issuing_authority ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
                      ]"
                      placeholder="请输入颁发机构"
                    />
                    <p v-if="errors.issuing_authority" class="text-sm text-red-500 mt-1">{{ errors.issuing_authority }}</p>
                  </div>

                  <!-- 日期选择 -->
                  <div class="grid grid-cols-2 gap-4">
                    <!-- 颁发日期 -->
                    <div class="space-y-1">
                      <label class="block text-sm font-medium text-gray-700">
                        颁发日期 <span class="text-red-500">*</span>
                      </label>
                      <input
                        type="date"
                        v-model="form.issue_date"
                        required
                        :class="[
                          'w-full rounded-lg border py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10',
                          errors.issue_date ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
                        ]"
                      />
                      <p v-if="errors.issue_date" class="text-sm text-red-500 mt-1">{{ errors.issue_date }}</p>
                    </div>

                    <!-- 到期日期 -->
                    <div class="space-y-1">
                      <label class="block text-sm font-medium text-gray-700">
                        到期日期
                      </label>
                      <input
                        type="date"
                        v-model="form.expiry_date"
                        :class="[
                          'w-full rounded-lg border py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10',
                          errors.expiry_date ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
                        ]"
                      />
                      <p v-if="errors.expiry_date" class="text-sm text-red-500 mt-1">{{ errors.expiry_date }}</p>
                    </div>
                  </div>

                  <!-- 证书编号 -->
                  <div class="space-y-1">
                    <label class="block text-sm font-medium text-gray-700">
                      证书编号
                    </label>
                    <input
                      type="text"
                      v-model="form.credential_id"
                      :class="[
                        'w-full rounded-lg border py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10',
                        errors.credential_id ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
                      ]"
                      placeholder="请输入证书编号（选填）"
                    />
                    <p v-if="errors.credential_id" class="text-sm text-red-500 mt-1">{{ errors.credential_id }}</p>
                  </div>

                  <!-- 证书描述 -->
                  <div class="space-y-1">
                    <label class="block text-sm font-medium text-gray-700">
                      证书描述
                    </label>
                    <el-input
                      v-model="form.description"
                      type="textarea"
                      :rows="4"
                      placeholder="请描述证书的相关信息（选填）"
                      :class="[
                        '!w-full',
                        errors.description ? 'is-error' : ''
                      ]"
                    />
                    <p v-if="errors.description" class="text-sm text-red-500 mt-1">{{ errors.description }}</p>
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
import { XMarkIcon } from '@heroicons/vue/24/outline'

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
  id: null,
  name: '',
  issuing_authority: '',
  issue_date: '',
  expiry_date: '',
  credential_id: '',
  description: ''
})

// 错误状态
const errors = ref({
  name: '',
  issuing_authority: '',
  issue_date: '',
  expiry_date: '',
  credential_id: '',
  description: ''
})

// 监听初始数据变化
watch(() => props.initialData, (newVal) => {
  if (newVal) {
    form.value = {
      id: newVal.id || null,
      name: newVal.name || '',
      issuing_authority: newVal.issuing_authority || '',
      issue_date: newVal.issue_date || '',
      expiry_date: newVal.expiry_date || '',
      credential_id: newVal.credential_id || '',
      description: newVal.description || ''
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
    issuing_authority: '',
    issue_date: '',
    expiry_date: '',
    credential_id: '',
    description: ''
  }

  // 必填字段验证
  if (!form.value.name?.trim()) {
    errors.value.name = '请输入证书名称'
    isValid = false
  }

  if (!form.value.issuing_authority?.trim()) {
    errors.value.issuing_authority = '请输入颁发机构'
    isValid = false
  }

  if (!form.value.issue_date) {
    errors.value.issue_date = '请选择颁发日期'
    isValid = false
  }

  // 日期逻辑验证
  if (form.value.issue_date && form.value.expiry_date) {
    const issueDate = new Date(form.value.issue_date)
    const expiryDate = new Date(form.value.expiry_date)
    if (expiryDate < issueDate) {
      errors.value.expiry_date = '到期日期不能早于颁发日期'
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
    name: form.value.name.trim(),
    issuing_authority: form.value.issuing_authority.trim(),
    description: form.value.description?.trim() || ''
  }

  // 如果是新建，不传 id
  if (!formData.id) {
    delete formData.id
  }

  emit('submit', formData)
}
</script> 