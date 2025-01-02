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
                  {{ initialData?.id ? '编辑社交主页' : '添加社交主页' }}
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
                  <!-- 平台选择 -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      平台类型 <span class="text-red-500">*</span>
                    </label>
                    <Listbox v-model="formData.platform" as="div">
                      <div class="relative">
                        <ListboxButton class="relative w-full cursor-pointer rounded-lg bg-white py-2 pl-3 pr-10 text-left border border-gray-300 hover:border-gray-400 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500">
                          <span class="block truncate">
                            {{ platformMap[formData.platform]?.label || '请选择平台' }}
                          </span>
                          <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                            <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                          </span>
                        </ListboxButton>
                        <ListboxOptions class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-lg bg-white py-1 text-sm shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                          <ListboxOption
                            v-for="[value, config] in Object.entries(platformMap)"
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
                                <div class="flex items-center">
                                  <img 
                                    :src="config.icon" 
                                    :alt="config.label"
                                    class="w-4 h-4 mr-2"
                                    v-if="config.icon"
                                    @error="handleIconError"
                                  />
                                  {{ config.label }}
                                </div>
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

                  <!-- 主页链接 -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      主页链接 <span class="text-red-500">*</span>
                    </label>
                    <input
                      v-model="formData.url"
                      type="url"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                      placeholder="请输入主页链接"
                      required
                    />
                  </div>

                  <!-- 补充说明 -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      补充说明
                    </label>
                    <textarea
                      v-model="formData.description"
                      rows="4"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                      placeholder="请输入补充说明"
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
  platform: '',      // 平台类型
  url: '',          // 主页链接
  description: ''   // 补充说明
})

// 平台类型映射
const platformMap = {
  'weibo': {
    label: '新浪微博',
    urlPrefix: 'https://weibo.com/',
    icon: 'https://weibo.com/favicon.ico'
  },
  'zhihu': {
    label: '知乎',
    urlPrefix: 'https://www.zhihu.com/people/',
    icon: 'https://static.zhihu.com/heifetz/favicon.ico'
  },
  'zcool': {
    label: '站酷',
    urlPrefix: 'https://www.zcool.com.cn/u/',
    icon: 'https://static.zcool.cn/git_z/z/site/favicon.ico'
  },
  'douyin': {
    label: '抖音',
    urlPrefix: 'https://www.douyin.com/user/',
    icon: 'https://www.douyin.com/favicon.ico'
  },
  'bilibili': {
    label: 'Bilibili',
    urlPrefix: 'https://space.bilibili.com/',
    icon: 'https://www.bilibili.com/favicon.ico'
  },
  'github': {
    label: 'GitHub',
    urlPrefix: 'https://github.com/',
    icon: 'https://github.com/favicon.ico'
  },
  'twitter': {
    label: 'Twitter',
    urlPrefix: 'https://twitter.com/',
    icon: 'https://twitter.com/favicon.ico'
  },
  'website': {
    label: '个人网站',
    urlPrefix: 'https://',
    icon: null
  },
  'other': {
    label: '其他',
    urlPrefix: '',
    icon: null
  }
}

// 监听初始数据变化
watch(() => props.initialData, (newVal) => {
  if (newVal) {
    formData.value = {
      id: newVal.id || null,
      platform: newVal.platform || '',
      url: newVal.url || '',
      description: newVal.description || ''
    }
    console.log('初始化表单数据:', formData.value)
  }
}, { immediate: true })

// 监听平台类型变化
watch(() => formData.value.platform, (newPlatform) => {
  if (newPlatform && platformMap[newPlatform]) {
    // 如果是新建或者当前 URL 是其他平台的前缀，则更新 URL
    const currentUrl = formData.value.url || ''
    if (!currentUrl) {
      formData.value.url = platformMap[newPlatform].urlPrefix
    }
  }
})

const handleClose = () => {
  emit('update:modelValue', false)
}

const handleSubmit = () => {
  // 验证平台类型
  if (!formData.value.platform || !platformMap[formData.value.platform]) {
    ElMessage.error('请选择有效的平台类型')
    return
  }

  // 验证 URL
  if (!formData.value.url) {
    ElMessage.error('请输入主页链接')
    return
  }

  // 验证 URL 格式
  if (formData.value.platform !== 'other' && formData.value.platform !== 'website') {
    const expectedPrefix = platformMap[formData.value.platform].urlPrefix
    // 如果用户输入的是完整URL，提取用户名部分
    const userMatch = formData.value.url.match(/^https?:\/\/[^/]+\/(.+)/)
    const username = userMatch ? userMatch[1] : formData.value.url
    formData.value.url = expectedPrefix + username.replace(/^\/+|\/+$/g, '')
  }

  const data = {
    ...formData.value,
    platform: formData.value.platform,  // 不需要 trim，保持原始值
    url: formData.value.url.trim(),
    description: formData.value.description?.trim() || ''
  }

  // 如果是新建，不传 id
  if (!data.id) {
    delete data.id
  }

  // 确保数据格式与后端一致
  const submitData = {
    platform: data.platform,
    url: data.url,
    description: data.description
  }

  if (data.id) {
    submitData.id = data.id
  }

  // 确保数据格式正确
  console.log('提交的数据:', submitData)

  emit('submit', submitData)
}

const handleIconError = (event) => {
  event.target.style.display = 'none'
}
</script> 