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
                  {{ initialData?.id ? '编辑专业技能' : '添加专业技能' }}
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
                  <!-- 技能名称 -->
                  <div class="space-y-1">
                    <label class="block text-sm font-medium text-gray-700">
                      技能名称 <span class="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      v-model="form.name"
                      required
                      :class="[
                        'w-full rounded-lg border py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10',
                        errors.name ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
                      ]"
                      placeholder="请输入技能名称"
                    />
                    <p v-if="errors.name" class="text-sm text-red-500 mt-1">{{ errors.name }}</p>
                  </div>

                  <!-- 熟练度 -->
                  <div class="space-y-1">
                    <label class="block text-sm font-medium text-gray-700">
                      熟练度 <span class="text-red-500">*</span>
                    </label>
                    <select
                      v-model="form.level"
                      required
                      :class="[
                        'w-full rounded-lg border py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10',
                        errors.level ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
                      ]"
                    >
                      <option value="">请选择熟练度</option>
                      <option value="beginner">入门</option>
                      <option value="intermediate">熟练</option>
                      <option value="advanced">精通</option>
                      <option value="expert">专家</option>
                    </select>
                    <p v-if="errors.level" class="text-sm text-red-500 mt-1">{{ errors.level }}</p>
                  </div>

                  <!-- 技能描述 -->
                  <div class="space-y-1">
                    <label class="block text-sm font-medium text-gray-700">
                      技能描述 <span class="text-red-500">*</span>
                    </label>
                    <el-input
                      v-model="form.description"
                      type="textarea"
                      :rows="4"
                      placeholder="请描述你的技能水平、应用场景和相关经验"
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
  id: null,          // ID
  name: '',          // 技能名称
  level: '',         // 熟练度
  description: ''    // 技能描述
})

// 错误状态
const errors = ref({
  name: '',
  level: '',
  description: ''
})

// 监听初始数据变化
watch(() => props.initialData, (newVal) => {
  if (newVal) {
    form.value = {
      id: newVal.id || null,
      name: newVal.name || '',
      level: newVal.level || '',
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
    level: '',
    description: ''
  }

  if (!form.value.name?.trim()) {
    errors.value.name = '请输入技能名称'
    isValid = false
  }

  if (!form.value.level) {
    errors.value.level = '请选择熟练度'
    isValid = false
  }

  if (!form.value.description?.trim()) {
    errors.value.description = '请输入技能描述'
    isValid = false
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
    description: form.value.description.trim()
  }

  // 如果是新建，不传 id
  if (!formData.id) {
    delete formData.id
  }

  emit('submit', formData)
}
</script> 