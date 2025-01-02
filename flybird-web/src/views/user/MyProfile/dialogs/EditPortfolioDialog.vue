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
                <h3 class="text-lg font-medium text-gray-900">
                  {{ initialData?.id ? '编辑作品展示' : '添加作品展示' }}
                </h3>
                <button
                  @click="handleClose"
                  class="p-1 rounded-full hover:bg-gray-100 transition-colors"
                >
                  <XMarkIcon class="w-5 h-5 text-gray-400" />
                </button>
              </DialogTitle>

              <!-- 表单内容 -->
              <form @submit.prevent="handleSubmit" class="p-6">
                <div class="space-y-4">
                  <!-- 作品名称 -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      作品标题 <span class="text-red-500">*</span>
                    </label>
                    <input
                      v-model="formData.title"
                      type="text"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                      placeholder="请输入作品标题"
                      required
                    />
                  </div>

                  <!-- 作品类型 -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      作品类型 <span class="text-red-500">*</span>
                    </label>
                    <Listbox v-model="formData.type" as="div">
                      <div class="relative">
                        <ListboxButton class="relative w-full cursor-pointer rounded-lg bg-white py-2 pl-3 pr-10 text-left border border-gray-300 hover:border-gray-400 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500">
                          <span class="block truncate">
                            {{ typeMap[formData.type] || '请选择作品类型' }}
                          </span>
                          <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                            <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                          </span>
                        </ListboxButton>
                        <ListboxOptions class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-lg bg-white py-1 text-sm shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                          <ListboxOption
                            v-for="[value, label] in Object.entries(typeMap)"
                            :key="value"
                            :value="value"
                            v-slot="{ active, selected }"
                            as="template"
                          >
                            <li :class="[
                              active ? 'bg-blue-50' : 'text-gray-900',
                              'relative cursor-pointer select-none py-2 pl-3 pr-9'
                            ]">
                              <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">
                                {{ label }}
                              </span>
                              <span v-if="selected" :class="[
                                'text-blue-600',
                                'absolute inset-y-0 right-0 flex items-center pr-4'
                              ]">
                                <CheckIcon class="h-5 w-5" aria-hidden="true" />
                              </span>
                            </li>
                          </ListboxOption>
                        </ListboxOptions>
                      </div>
                    </Listbox>
                  </div>

                  <!-- 作品链接 -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      作品链接 <span class="text-red-500">*</span>
                    </label>
                    <input
                      v-model="formData.url"
                      type="url"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                      placeholder="请输入作品链接"
                      required
                    />
                  </div>

                  <!-- 作品描述 -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      作品描述
                    </label>
                    <textarea
                      v-model="formData.description"
                      rows="4"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                      placeholder="请描述作品的主要内容、特点等"
                    ></textarea>
                  </div>

                  <!-- 项目亮点 -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      项目亮点
                    </label>
                    <textarea
                      v-model="formData.highlights"
                      rows="4"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                      placeholder="请描述项目的亮点和特色"
                    ></textarea>
                  </div>
                </div>

                <!-- 底部按钮 -->
                <div class="mt-6 flex justify-end space-x-3">
                  <button
                    type="button"
                    @click="handleClose"
                    class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
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
import { XMarkIcon, ChevronUpDownIcon, CheckIcon } from '@heroicons/vue/24/outline'
import { ElMessage } from 'element-plus'

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
const formData = ref({
  title: '',         // 作品标题
  url: '',           // 作品链接
  type: '',          // 作品类型
  description: '',   // 作品描述
  highlights: ''     // 项目亮点
})

// 作品类型映射
const typeMap = {
  'project': '项目',
  'website': '网站',
  'app': '应用',
  'article': '文章',
  'design': '设计',
  'video': '视频',
  'other': '其他'
}

// 监听初始数据变化
watch(() => props.initialData, (newVal) => {
  if (newVal) {
    formData.value = {
      id: newVal.id || null,
      title: newVal.title || '',
      url: newVal.url || '',
      type: newVal.type || '',
      description: newVal.description || '',
      highlights: newVal.highlights || ''
    }
  }
}, { immediate: true })

const handleClose = () => {
  emit('update:modelValue', false)
}

const handleSubmit = () => {
  // 验证类型
  if (!formData.value.type || !typeMap[formData.value.type]) {
    ElMessage.error('请选择有效的作品类型')
    return
  }

  const data = {
    ...formData.value,
    title: formData.value.title.trim(),
    url: formData.value.url.trim(),
    description: formData.value.description?.trim() || '',
    highlights: formData.value.highlights?.trim() || ''
  }

  // 如果是新建，不传 id
  if (!data.id) {
    delete data.id
  }

  emit('submit', data)
}
</script> 