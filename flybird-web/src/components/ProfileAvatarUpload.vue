<template>
  <el-dialog
    v-model="visible"
    title="更新职业头像"
    width="800px"
    :close-on-click-modal="false"
    :before-close="handleClose"
  >
    <div class="flex">
      <!-- 左侧上传区域 -->
      <div class="w-1/2 pr-4 border-r">
        <el-upload
          ref="uploadRef"
          class="avatar-uploader"
          :show-file-list="false"
          :auto-upload="false"
          :on-change="handleChange"
          accept="image/*"
          drag
        >
          <template #trigger>
            <div class="upload-trigger">
              <img v-if="imageUrl" :src="imageUrl" class="avatar-preview" />
              <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
              <div class="upload-text">
                <span>点击或拖拽图片到此处</span>
                <p class="text-gray-400 text-xs mt-2">支持 jpg、png 格式，建议尺寸 300x300px</p>
              </div>
            </div>
          </template>
        </el-upload>

        <!-- 图片调整工具 -->
        <div v-if="imageUrl" class="mt-4 space-y-4">
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-600">缩放</span>
            <el-slider
              v-model="zoom"
              :min="50"
              :max="200"
              :step="1"
              class="w-48"
              @input="handleZoom"
            />
          </div>
          <div class="flex justify-center space-x-4">
            <el-button @click="rotateLeft">
              <template #icon><i class="el-icon-refresh-left" /></template>
              向左旋转
            </el-button>
            <el-button @click="rotateRight">
              <template #icon><i class="el-icon-refresh-right" /></template>
              向右旋转
            </el-button>
          </div>
        </div>
      </div>

      <!-- 右侧预览区域 -->
      <div class="w-1/2 pl-4">
        <h4 class="text-gray-600 mb-4">预览效果</h4>
        <div class="space-y-6">
          <!-- 大尺寸预览 -->
          <div class="preview-container">
            <div class="text-sm text-gray-500 mb-2">大尺寸 (200x200px)</div>
            <div class="preview-box large">
              <img v-if="imageUrl" :src="imageUrl" :style="previewStyle" />
            </div>
          </div>

          <!-- 小尺寸预览 -->
          <div class="flex space-x-8">
            <div class="preview-container">
              <div class="text-sm text-gray-500 mb-2">中尺寸 (100x100px)</div>
              <div class="preview-box medium">
                <img v-if="imageUrl" :src="imageUrl" :style="previewStyle" />
              </div>
            </div>
            <div class="preview-container">
              <div class="text-sm text-gray-500 mb-2">小尺寸 (50x50px)</div>
              <div class="preview-box small">
                <img v-if="imageUrl" :src="imageUrl" :style="previewStyle" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button
          type="primary"
          :loading="uploading"
          :disabled="!imageUrl"
          @click="handleUpload"
        >
          确认上传
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  modelValue: Boolean
})

const emit = defineEmits(['update:modelValue', 'upload'])

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const uploadRef = ref(null)
const imageUrl = ref('')
const uploading = ref(false)
const zoom = ref(100)
const rotation = ref(0)

// 预览样式
const previewStyle = computed(() => ({
  transform: `scale(${zoom.value / 100}) rotate(${rotation.value}deg)`,
  transformOrigin: 'center center'
}))

// 处理文件选择
const handleChange = (file) => {
  if (!file) return

  // 验证文件类型
  if (!file.raw.type.startsWith('image/')) {
    ElMessage.error('请选择图片文件')
    return
  }

  // 验证文件大小 (5MB)
  const maxSize = 5 * 1024 * 1024
  if (file.size > maxSize) {
    ElMessage.error('图片大小不能超过 5MB')
    return
  }

  // 读取文件
  const reader = new FileReader()
  reader.onload = (e) => {
    imageUrl.value = e.target.result
    // 重置缩放和旋转
    zoom.value = 100
    rotation.value = 0
  }
  reader.readAsDataURL(file.raw)
}

// 处理缩放
const handleZoom = (value) => {
  zoom.value = value
}

// 处理旋转
const rotateLeft = () => {
  rotation.value = (rotation.value - 90) % 360
}

const rotateRight = () => {
  rotation.value = (rotation.value + 90) % 360
}

// 处理上传
const handleUpload = async () => {
  if (!imageUrl.value) return

  try {
    uploading.value = true

    // 创建 canvas 以应用变换
    const canvas = document.createElement('canvas')
    const ctx = canvas.getContext('2d')
    const img = new Image()

    await new Promise((resolve, reject) => {
      img.onload = resolve
      img.onerror = reject
      img.src = imageUrl.value
    })

    // 设置画布大小
    canvas.width = 300
    canvas.height = 300

    // 应用变换
    ctx.translate(canvas.width / 2, canvas.height / 2)
    ctx.rotate((rotation.value * Math.PI) / 180)
    ctx.scale(zoom.value / 100, zoom.value / 100)
    ctx.drawImage(
      img,
      -canvas.width / 2,
      -canvas.height / 2,
      canvas.width,
      canvas.height
    )

    // 转换为 Blob
    canvas.toBlob(async (blob) => {
      const file = new File([blob], 'profile_avatar.png', { type: 'image/png' })
      emit('upload', file)
    }, 'image/png')

  } catch (error) {
    console.error('处理图片失败:', error)
    ElMessage.error('处理图片失败，请重试')
  } finally {
    uploading.value = false
  }
}

// 处理关闭
const handleClose = () => {
  visible.value = false
  imageUrl.value = ''
  zoom.value = 100
  rotation.value = 0
  if (uploadRef.value) {
    uploadRef.value.clearFiles()
  }
}
</script>

<style scoped>
.avatar-uploader {
  @apply border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-500 transition-colors;
}

.upload-trigger {
  @apply flex flex-col items-center justify-center p-8 cursor-pointer;
}

.avatar-preview {
  @apply w-48 h-48 object-cover rounded-lg mb-4;
}

.avatar-uploader-icon {
  @apply text-4xl text-gray-400 mb-4;
}

.preview-box {
  @apply border border-gray-200 rounded-lg overflow-hidden bg-gray-50;
}

.preview-box.large {
  @apply w-48 h-48;
}

.preview-box.medium {
  @apply w-24 h-24;
}

.preview-box.small {
  @apply w-12 h-12;
}

.preview-box img {
  @apply w-full h-full object-cover transition-transform duration-200;
}
</style> 