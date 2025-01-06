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
                  {{ initialData?.id ? '编辑语言能力' : '添加语言能力' }}
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
                  <!-- 语言名称 -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      语言名称 <span class="text-red-500">*</span>
                    </label>
                    <input
                      v-model="formData.name"
                      type="text"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                      placeholder="请输入语言名称"
                      required
                    />
                  </div>

                  <!-- 熟练程度 -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      熟练程度 <span class="text-red-500">*</span>
                    </label>
                    <Listbox v-model="formData.proficiency" as="div">
                      <div class="relative">
                        <ListboxButton class="relative w-full cursor-pointer rounded-lg bg-white py-2 pl-3 pr-10 text-left border border-gray-300 hover:border-gray-400 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500">
                          <span class="block truncate">
                            {{ proficiencyMap[formData.proficiency] || '请选择熟练程度' }}
                          </span>
                          <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                            <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                          </span>
                        </ListboxButton>
                        <ListboxOptions class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-lg bg-white py-1 text-sm shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                          <ListboxOption
                            v-for="[value, label] in Object.entries(proficiencyMap)"
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

                  <!-- 语言证书 -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      语言证书
                    </label>
                    <input
                      v-model="formData.certification"
                      type="text"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                      placeholder="请输入语言证书，如：托福、雅思等"
                    />
                  </div>

                  <!-- 证书分数 -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      证书分数
                    </label>
                    <input
                      v-model="formData.score"
                      type="text"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                      placeholder="请输入证书分数"
                    />
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
  TransitionChild
} from '@headlessui/vue'
import { XMarkIcon, ChevronUpDownIcon, CheckIcon } from '@heroicons/vue/24/outline'
import {
  Listbox,
  ListboxButton,
  ListboxOptions,
  ListboxOption
} from '@headlessui/vue'

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
  name: '',          // 语言名称
  proficiency: '',   // 熟练程度
  certification: '', // 语言证书
  score: ''         // 证书分数
})

// 监听初始数据变化
watch(() => props.initialData, (newVal) => {
  if (newVal) {
    formData.value = {
      id: newVal.id || null,
      name: newVal.name || '',
      proficiency: newVal.proficiency || '',
      certification: newVal.certification || '',
      score: newVal.score || ''
    }
  }
}, { immediate: true })

const handleClose = () => {
  emit('update:modelValue', false)
}

const handleSubmit = () => {
  const data = {
    ...formData.value,
    name: formData.value.name.trim(),
    certification: formData.value.certification?.trim() || '',
    score: formData.value.score?.trim() || ''
  }

  // 如果是新建，不传 id
  if (!data.id) {
    delete data.id
  }

  emit('submit', data)
}

// 熟练程度映射
const proficiencyMap = {
  'native': '母语',
  'advanced': '高级',
  'intermediate': '中级',
  'basic': '初级'
}
</script> 