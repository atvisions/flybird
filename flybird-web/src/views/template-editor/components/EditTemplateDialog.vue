<template>
  <TransitionRoot appear :show="modelValue" as="template">
    <Dialog as="div" class="relative z-50" @close="handleClose">
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
            <DialogPanel class="w-full max-w-2xl transform overflow-hidden rounded-xl bg-white text-left align-middle shadow-xl transition-all">
              <!-- 头部 -->
              <DialogTitle as="div" class="flex items-center justify-between px-6 py-4 border-b border-gray-200">
                <h3 class="text-lg font-medium text-gray-900">保存模板</h3>
                <button
                  @click="handleClose"
                  class="p-1 rounded-full hover:bg-gray-100 transition-colors"
                >
                  <XMarkIcon class="w-5 h-5 text-gray-400" />
                </button>
              </DialogTitle>

              <!-- 表单内容 -->
              <form @submit.prevent="handleConfirm" class="p-6">
                <div class="space-y-4">
                  <!-- 保存方式选择 -->
                  <div class="flex flex-col gap-3 p-4 bg-gray-50 rounded-lg">
                    <div class="text-sm font-medium text-gray-700">选择保存方式</div>
                    <div class="flex gap-4">
                      <label class="flex items-center gap-2 cursor-pointer">
                        <input
                          v-model="saveMode"
                          type="radio"
                          value="draft"
                          class="w-4 h-4 text-blue-500 focus:ring-blue-500"
                        />
                        <span class="text-sm text-gray-900">保存草稿</span>
                      </label>
                      <label class="flex items-center gap-2 cursor-pointer">
                        <input
                          v-model="saveMode"
                          type="radio"
                          value="publish"
                          class="w-4 h-4 text-blue-500 focus:ring-blue-500"
                        />
                        <span class="text-sm text-gray-900">正式发布</span>
                      </label>
                    </div>
                    <div class="text-xs text-gray-500">
                      {{ saveMode === 'draft' ? '草稿不会展示在作品集中，可随时继续编辑' : '发布后将展示在作品集中，可选择是否公开' }}
                    </div>
                  </div>

                  <!-- 审核提示 - 仅发布时显示 -->
                  <div v-if="saveMode === 'publish'" class="flex items-start p-3 bg-blue-50 rounded-lg">
                    <div class="flex-shrink-0">
                      <svg class="h-5 w-5 text-blue-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a.75.75 0 000 1.5h.253a.25.25 0 01.244.304l-.459 2.066A1.75 1.75 0 0010.747 15H11a.75.75 0 000-1.5h-.253a.25.25 0 01-.244-.304l.459-2.066A1.75 1.75 0 009.253 9H9z" clip-rule="evenodd" />
                      </svg>
                    </div>
                    <div class="ml-3">
                      <p class="text-sm text-blue-700">
                        为确保模板质量，发布的模板需要经过系统审核。审核通过后，模板将在市场中展示。
                      </p>
                    </div>
                  </div>

                  <!-- 模板名称 -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      模板名称
                      <span class="text-red-500">*</span>
                    </label>
                    <input
                      v-model="formData.name"
                      type="text"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                      placeholder="请输入模板名称"
                      required
                      maxlength="50"
                    />
                  </div>

                  <!-- 分类 -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      分类
                      <span class="text-red-500">*</span>
                    </label>
                    <Listbox v-model="formData.category">
                      <div class="relative">
                        <ListboxButton class="relative w-full cursor-pointer rounded-lg border border-gray-300 bg-white py-2 pl-3 pr-10 text-left focus:outline-none focus:ring-1 focus:ring-blue-500 sm:text-sm">
                          <span class="block truncate">{{ getCategoryLabel(formData.category) || '请选择分类' }}</span>
                          <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                            <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                          </span>
                        </ListboxButton>
                        <ListboxOptions class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                          <ListboxOption
                            v-for="category in categories"
                            :key="category.id"
                            :value="category.id"
                            v-slot="{ active, selected }"
                          >
                            <li :class="[
                              active ? 'bg-blue-500 text-white' : 'text-gray-900',
                              'relative cursor-pointer select-none py-2 pl-10 pr-4'
                            ]">
                              <span :class="[selected ? 'font-medium' : 'font-normal', 'block truncate']">
                                {{ category.name }}
                              </span>
                              <span v-if="selected" :class="[
                                active ? 'text-white' : 'text-blue-500',
                                'absolute inset-y-0 left-0 flex items-center pl-3'
                              ]">
                                <CheckIcon class="h-5 w-5" aria-hidden="true" />
                              </span>
                            </li>
                          </ListboxOption>
                        </ListboxOptions>
                      </div>
                    </Listbox>
                  </div>

                  <!-- 描述 -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      描述
                      <span class="text-red-500">*</span>
                    </label>
                    <textarea
                      v-model="formData.description"
                      rows="3"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                      placeholder="请输入模板描述（至少10个字符）"
                      required
                      maxlength="200"
                    ></textarea>
                  </div>

                  <!-- 以下字段仅在发布时显示 -->
                  <template v-if="saveMode === 'publish'">
                    <!-- 关键词 -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        关键词
                      </label>
                      <input
                        v-model="formData.keywords"
                        type="text"
                        class="w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                        placeholder="请输入关键词，多个关键词用逗号分隔"
                      />
                    </div>

                    <!-- 是否公开 -->
                    <div class="flex flex-col gap-1">
                      <div class="flex items-center">
                        <input
                          v-model="formData.is_public"
                          type="checkbox"
                          class="h-4 w-4 rounded border-gray-300 text-blue-500 focus:ring-blue-500 ring-1 ring-gray-400"
                        />
                        <label class="ml-2 text-sm text-gray-700">设为公开模板</label>
                      </div>
                      <div class="ml-6 space-y-1">
                        <p class="text-xs text-gray-500">若不设置为公开模板，发布后仅自己可见，但会在您的作品集中展示</p>
                        <p class="text-xs text-blue-500">设为公开模板后，当其他用户使用您的模板时，您将获得积分奖励</p>
                      </div>
                    </div>
                  </template>
                </div>

                <!-- 按钮组 -->
                <div class="mt-6 flex justify-end gap-3">
                  <button
                    type="button"
                    @click="handleClose"
                    class="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                  >
                    取消
                  </button>
                  <button
                    type="submit"
                    :disabled="loading"
                    class="rounded-lg bg-blue-500 px-4 py-2 text-sm font-medium text-white hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
                  >
                    {{ loading ? '保存中...' : (saveMode === 'draft' ? '保存草稿' : '发布模板') }}
                  </button>
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
  TransitionChild,
  Listbox,
  ListboxButton,
  ListboxOptions,
  ListboxOption
} from '@headlessui/vue'
import { 
  XMarkIcon,
  ChevronUpDownIcon,
  CheckIcon 
} from '@heroicons/vue/24/outline'
import { categoryApi } from '@/api/category'
import { ElMessage } from 'element-plus'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  mode: {
    type: String,
    default: 'draft'
  },
  template: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'confirm'])

const loading = ref(false)
const categories = ref([])
const saveMode = ref('draft')

// 表单数据
const formData = ref({
  name: '',
  category: '',
  description: '',
  is_public: false,
  keywords: ''
})

// 初始化表单数据
const initFormData = () => {
  console.log('初始化表单数据，模板数据:', props.template)
  const template = props.template || {}
  formData.value = {
    name: template.name || '',
    category: template.category || '',
    description: template.description || '',
    is_public: template.is_public ?? false,
    keywords: Array.isArray(template.keywords) ? template.keywords.join(',') : '',
    status: template.status || 0
  }
  // 确保每次初始化时都设置为draft
  saveMode.value = 'draft'
}

// 监听对话框显示状态
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    // 当对话框打开时，重新初始化表单数据
    initFormData()
  }
}, { immediate: true })

// 加载分类数据
const loadCategories = async () => {
  try {
    const res = await categoryApi.getList()
    categories.value = Array.isArray(res) ? res : []
  } catch (error) {
    ElMessage.error('获取分类列表失败')
  }
}

// 获取分类显示文本
const getCategoryLabel = (value) => {
  const category = categories.value.find(cat => cat.id === value)
  const label = category ? category.name : ''
  return label
}

// 处理关闭
const handleClose = () => {
  emit('update:modelValue', false)
}

// 处理确认
const handleConfirm = async () => {
  // 表单验证
  if (!formData.value.name?.trim()) {
    ElMessage.warning('请输入模板名称')
    return
  }
  if (!formData.value.category) {
    ElMessage.warning('请选择分类')
    return
  }
  if (!formData.value.description?.trim()) {
    ElMessage.warning('请输入模板描述')
    return
  }
  if (formData.value.description.length < 10) {
    ElMessage.warning('描述至少需要10个字符')
    return
  }

  try {
    loading.value = true
    console.log('提交的保存模式:', saveMode.value)
    console.log('提交的表单数据:', formData.value)
    const submitData = {
      ...formData.value,
      status: saveMode.value === 'draft' ? 0 : 2,
      keywords: formData.value.keywords ? formData.value.keywords.split(',').filter(Boolean) : []
    }
    console.log('最终提交的数据:', submitData)
    await emit('confirm', submitData)
    handleClose()
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败，请重试')
  } finally {
    loading.value = false
  }
}

// 组件挂载时加载分类
loadCategories()
</script>

<style scoped>
/* 移动端适配 */
@media (max-width: 640px) {
  .p-6 {
    @apply p-4;
  }
}

/* 禁用状态样式 */
.disabled\\:opacity-50:disabled {
  opacity: 0.5;
}

.disabled\\:cursor-not-allowed:disabled {
  cursor: not-allowed;
}
</style> 