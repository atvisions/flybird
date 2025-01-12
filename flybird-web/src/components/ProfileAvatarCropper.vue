<template>
  <TransitionRoot appear :show="modelValue" as="template">
    <Dialog as="div" class="relative z-50" @close="closeDialog">
      <TransitionChild as="template" enter="duration-300 ease-out" enter-from="opacity-0" enter-to="opacity-100">
        <div class="fixed inset-0 bg-black/25" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4">
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
          >
            <DialogPanel class="w-full max-w-sm transform overflow-hidden rounded-2xl bg-white shadow-xl transition-all">
              <!-- 头部 -->
              <div class="px-4 py-3 bg-primary-50 border-b border-primary-100">
                <div class="flex items-center justify-between">
                  <h3 class="text-base font-medium text-gray-900">更新头像</h3>
                  <button
                    type="button"
                    class="text-gray-400 hover:text-gray-500"
                    @click="closeDialog"
                  >
                    <XMarkIcon class="h-5 w-5" />
                  </button>
                </div>
              </div>

              <!-- 主要内容区 -->
              <div class="p-4">
                <!-- 裁剪区域 -->
                <div class="relative aspect-square rounded-lg overflow-hidden bg-gray-100 mb-4">
                  <template v-if="imageUrl">
                    <Cropper
                      ref="cropperRef"
                      class="cropper"
                      :src="imageUrl"
                      :stencil-component="CircleStencil"
                      :stencil-props="{
                        aspectRatio: 1,
                        minWidth: '50%',
                        minHeight: '50%'
                      }"
                      :resize-image="{
                        touch: true,
                        wheel: true
                      }"
                      :transitions="true"
                      :canvas="{
                        width: 200,
                        height: 200
                      }"
                      @change="onCrop"
                    />
                  </template>
                  <template v-else>
                    <label class="absolute inset-0 cursor-pointer">
                      <div class="h-full flex flex-col items-center justify-center">
                        <PhotoIcon class="w-12 h-12 text-gray-400" />
                        <p class="mt-2 text-sm font-medium text-gray-900">点击选择照片</p>
                        <p class="mt-1 text-xs text-gray-500">建议使用正面照，保持微笑</p>
                      </div>
                      <input type="file" class="hidden" accept="image/*" @change="handleFileChange">
                    </label>
                  </template>
                </div>

                <!-- 底部操作区 -->
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-4">
                    <div v-if="previewUrl" class="w-12 h-12 rounded-full overflow-hidden border-2 border-gray-200">
                      <img :src="previewUrl" class="w-full h-full object-cover" alt="预览" />
                    </div>
                    <button
                      v-if="imageUrl"
                      type="button"
                      class="text-sm text-gray-600 hover:text-primary-500"
                      @click="resetImage"
                    >
                      重新选择
                    </button>
                  </div>
                  <button
                    v-if="imageUrl"
                    type="button"
                    class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700"
                    :disabled="!hasImage"
                    @click="handleCrop"
                  >
                    确认使用
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
import { ref, watch } from 'vue'
import { Cropper, CircleStencil } from 'vue-advanced-cropper'
import 'vue-advanced-cropper/dist/style.css'
import { Dialog, DialogPanel, TransitionChild, TransitionRoot } from '@headlessui/vue'
import { PhotoIcon, XMarkIcon } from '@heroicons/vue/24/outline'
import { showToast } from '@/components/ToastMessage'

const props = defineProps({
  modelValue: Boolean
})

const emit = defineEmits(['update:modelValue', 'upload'])

const cropperRef = ref(null)
const imageUrl = ref('')
const previewUrl = ref('')
const hasImage = ref(false)

// 处理文件选择
const handleFileChange = (event) => {
  const file = event?.target?.files?.[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    showToast('请选择图片文件', 'error')
    return
  }

  const maxSize = 2 * 1024 * 1024
  if (file.size > maxSize) {
    showToast('图片大小不能超过 2MB', 'error')
    return
  }

  const reader = new FileReader()
  reader.onload = (e) => {
    imageUrl.value = e.target.result
    hasImage.value = true
  }
  reader.readAsDataURL(file)
}

// 监听裁剪变化
const onCrop = ({ coordinates, canvas }) => {
  if (canvas) {
    previewUrl.value = canvas.toDataURL('image/png')
  }
}

// 处理裁剪
const handleCrop = async () => {
  if (!cropperRef.value || !hasImage.value) return
  
  try {
    const { canvas } = cropperRef.value.getResult({
      width: 200,
      height: 200
    })
    
    if (!canvas) {
      throw new Error('裁剪失败')
    }

    canvas.toBlob(async (blob) => {
      if (!blob) {
        throw new Error('图片处理失败')
      }
      const file = new File([blob], 'profile_avatar.png', { type: 'image/png' })
      await emit('upload', file)
      closeDialog()
    }, 'image/png', 0.9)
  } catch (error) {
    console.error('裁剪失败:', error)
    showToast(error.message || '图片处理失败，请重试', 'error')
  }
}

const resetImage = () => {
  clearImage()
  // 触发文件选择
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.onchange = handleFileChange
  input.click()
}

const closeDialog = () => {
  emit('update:modelValue', false)
  clearImage()
}

const clearImage = () => {
  imageUrl.value = ''
  previewUrl.value = ''
  hasImage.value = false
}

watch(() => props.modelValue, (newVal) => {
  if (!newVal) clearImage()
})
</script>

<style>
.cropper {
  height: 100%;
  background: #f3f4f6;
}

.vue-advanced-cropper {
  background: #f3f4f6;
}

.vue-advanced-cropper__foreground {
  background: rgba(0, 0, 0, 0.3);
}

.vue-advanced-cropper__image {
  max-width: none !important;
}

.vue-advanced-cropper__stencil {
  border-radius: 50% !important;
}
</style> 