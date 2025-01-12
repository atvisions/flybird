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
            <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-xl bg-white text-left align-middle shadow-xl transition-all">
              <!-- 头部 -->
              <DialogTitle as="div" class="flex items-center justify-between px-6 py-4 border-b border-gray-200">
                <h3 class="text-lg font-medium text-gray-900">更换头像</h3>
                <button
                  @click="handleClose"
                  class="rounded-full p-1 hover:bg-gray-100 transition-colors"
                >
                  <XMarkIcon class="w-5 h-5 text-gray-400" />
                </button>
              </DialogTitle>

              <!-- 提示信息 -->
              <div class="px-6 pt-4">
                <div class="bg-blue-50 rounded-lg p-4 mb-4">
                  <div class="flex">
                    <div class="flex-shrink-0">
                      <InformationCircleIcon class="h-5 w-5 text-blue-400" />
                    </div>
                    <div class="ml-3">
                      <h3 class="text-sm font-medium text-blue-800">上传提示</h3>
                      <div class="mt-2 text-sm text-blue-700">
                        <ul class="list-disc pl-5 space-y-1">
                          <li>请上传真实头像照片</li>
                          <li>图片将被裁剪为正方形</li>
                          <li>支持 JPG、PNG 格式</li>
                          <li>文件大小不超过 2MB</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 裁切区域 -->
              <div class="px-6 py-4">
                <div v-if="!imageUrl" class="border-2 border-dashed border-gray-300 rounded-lg p-8">
                  <div class="text-center">
                    <PhotoIcon class="mx-auto h-12 w-12 text-gray-400" />
                    <div class="mt-4 flex text-sm leading-6 text-gray-600">
                      <label
                        class="relative cursor-pointer rounded-md bg-white font-semibold text-indigo-600 focus-within:outline-none hover:text-indigo-500"
                      >
                        <span>选择图片</span>
                        <input 
                          type="file" 
                          class="sr-only" 
                          accept="image/*"
                          @change="handleFileChange"
                        >
                      </label>
                    </div>
                  </div>
                </div>
                <div v-else class="aspect-square overflow-hidden rounded-lg">
                  <vue-cropper
                    ref="cropper"
                    :img="imageUrl"
                    :auto-crop="true"
                    :fixed-box="true"
                    :center-box="true"
                    :fixed="true"
                    :fixed-number="[1, 1]"
                    :info="true"
                    :full="true"
                    :auto-crop-width="300"
                    :auto-crop-height="300"
                    :output-type="'png'"
                    :output-size="1"
                  />
                </div>
              </div>

              <!-- 底部按钮 -->
              <div class="px-6 py-4 bg-gray-50 border-t border-gray-200">
                <div class="flex justify-end space-x-3">
                  <button
                    type="button"
                    @click="handleClose"
                    class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
                  >
                    取消
                  </button>
                  <button
                    type="button"
                    @click="handleUpload"
                    :disabled="!imageUrl || loading"
                    class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {{ loading ? '上传中...' : '确认' }}
                  </button>
                </div>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { ref } from 'vue'
import 'vue-cropper/dist/index.css'
import { VueCropper } from 'vue-cropper'
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionChild,
  TransitionRoot
} from '@headlessui/vue'
import {
  XMarkIcon,
  PhotoIcon,
  InformationCircleIcon,
  ArrowPathIcon
} from '@heroicons/vue/24/outline'
import { showToast } from '@/components/ToastMessage'

const props = defineProps({
  modelValue: Boolean,
  loading: Boolean
})

const emit = defineEmits(['update:modelValue', 'upload'])

const imageUrl = ref('')
const cropper = ref(null)

const handleClose = () => {
  imageUrl.value = ''
  emit('update:modelValue', false)
}

const handleFileChange = (e) => {
  const file = e.target.files[0]
  if (!file) return

  // 验证文件类型和大小
  if (!file.type.startsWith('image/')) {
    showToast('请选择图片文件', 'error')
    return
  }

  const maxSize = 2 * 1024 * 1024 // 2MB
  if (file.size > maxSize) {
    showToast('图片大小不能超过 2MB', 'error')
    return
  }

  // 读取文件
  const reader = new FileReader()
  reader.onload = (e) => {
    imageUrl.value = e.target.result
  }
  reader.readAsDataURL(file)
}

const rotateLeft = () => {
  cropper.value.rotateLeft()
}

const rotateRight = () => {
  cropper.value.rotateRight()
}

const handleUpload = async () => {
  if (!cropper.value) return
  
  // 获取裁切后的图片 base64 数据
  cropper.value.getCropData((data) => {
    // 将 base64 转换为文件对象
    const arr = data.split(',')
    const mime = arr[0].match(/:(.*?);/)[1]
    const bstr = atob(arr[1])
    let n = bstr.length
    const u8arr = new Uint8Array(n)
    while (n--) {
      u8arr[n] = bstr.charCodeAt(n)
    }
    const file = new File([u8arr], 'avatar.png', { type: mime })
    
    // 触发上传事件
    emit('upload', file)
  })
}

// 组件定义
const components = {
  VueCropper
}
</script>

<style>
.vue-cropper {
  height: 400px !important;
  background-size: contain !important;
}

.cropper-view-box,
.cropper-face {
  border-radius: 0;
}

.cropper-crop-box {
  border: 1px solid rgba(255, 255, 255, 0.8);
}

.cropper-point {
  background-color: #fff;
  width: 8px !important;
  height: 8px !important;
}
</style> 