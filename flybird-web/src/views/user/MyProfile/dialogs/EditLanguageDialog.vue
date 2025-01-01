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
                  {{ initialData?.id ? '编辑语言能力' : '添加语言能力' }}
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
                  <!-- 语言名称 -->
                  <div class="space-y-1">
                    <label class="block text-sm font-medium text-gray-700">
                      语言名称 <span class="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      v-model="form.name"
                      required
                      :class="[
                        'w-full rounded-lg border py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10',
                        errors.name ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
                      ]"
                      placeholder="请输入语言名称，如：英语、日语等"
                    />
                    <p v-if="errors.name" class="text-sm text-red-500 mt-1">{{ errors.name }}</p>
                  </div>

                  <!-- 掌握程度 -->
                  <div class="space-y-1">
                    <label class="block text-sm font-medium text-gray-700">
                      掌握程度 <span class="text-red-500">*</span>
                    </label>
                    <select
                      v-model="form.proficiency"
                      required
                      :class="[
                        'w-full rounded-lg border py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10',
                        errors.proficiency ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
                      ]"
                    >
                      <option value="">请选择掌握程度</option>
                      <option v-for="option in PROFICIENCY_OPTIONS" 
                        :key="option.value" 
                        :value="option.value"
                      >
                        {{ option.label }}
                      </option>
                    </select>
                    <p v-if="errors.proficiency" class="text-sm text-red-500 mt-1">{{ errors.proficiency }}</p>
                  </div>

                  <!-- 语言描述 -->
                  <div class="space-y-1">
                    <label class="block text-sm font-medium text-gray-700">
                      补充说明
                    </label>
                    <el-input
                      v-model="form.description"
                      type="textarea"
                      :rows="4"
                      placeholder="请描述语言能力的具体情况，如：通过了某项语言考试等（选填）"
                      :class="[
                        '!w-full',
                        errors.description ? 'is-error' : ''
                      ]"
                    />
                    <p v-if="errors.description" class="text-sm text-red-500 mt-1">{{ errors.description }}</p>
                  </div>

                  <!-- 语言证书 -->
                  <div class="space-y-1">
                    <label class="block text-sm font-medium text-gray-700">
                      语言证书
                    </label>
                    <input
                      type="text"
                      v-model="form.certification"
                      :class="[
                        'w-full rounded-lg border py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10',
                        errors.certification ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
                      ]"
                      placeholder="如：托福、雅思等（选填）"
                    />
                  </div>

                  <!-- 考试分数 -->
                  <div class="space-y-1">
                    <label class="block text-sm font-medium text-gray-700">
                      考试分数
                    </label>
                    <input
                      type="text"
                      v-model="form.score"
                      :class="[
                        'w-full rounded-lg border py-2.5 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10',
                        errors.score ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
                      ]"
                      placeholder="如：100分、7.0分等（选填）"
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
  proficiency: '',
  certification: '',
  score: ''
})

// 错误状态
const errors = ref({
  name: '',
  proficiency: '',
  certification: '',
  score: ''
})

// 监听初始数据变化
watch(() => props.initialData, (newVal) => {
  if (newVal) {
    form.value = {
      id: newVal.id || null,
      name: newVal.name || '',
      proficiency: newVal.proficiency || '',
      certification: newVal.certification || '',
      score: newVal.score || ''
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
    proficiency: ''
  }

  if (!form.value.name?.trim()) {
    errors.value.name = '请输入语言名称'
    isValid = false
  }

  if (!form.value.proficiency) {
    errors.value.proficiency = '请选择掌握程度'
    isValid = false
  }

  return isValid
}

// 提交处理
const handleSubmit = () => {
  if (!validateForm()) {
    return
  }

  console.log('【EditLanguageDialog】准备提交数据:', form.value)

  const formData = {
    ...form.value,
    name: form.value.name.trim(),
    proficiency: form.value.proficiency
  }

  // 如果是新建，不传 id
  if (!formData.id) {
    delete formData.id
  }

  console.log('【EditLanguageDialog】处理后的提交数据:', formData)

  emit('submit', formData)
}

// 添加 level 选项的映射
const PROFICIENCY_OPTIONS = [
  { value: 'elementary', label: '入门' },
  { value: 'intermediate', label: '中级' },
  { value: 'advanced', label: '高级' },
  { value: 'native', label: '母语' }
]
</script> 