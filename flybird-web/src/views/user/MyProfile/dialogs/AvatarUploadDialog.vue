<template>
  <el-dialog
    v-model="visible"
    title="上传头像"
    width="500px"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
  >
    <div class="avatar-upload-container">
      <!-- 上传按钮 -->
      <div class="upload-btn" v-if="!cropImg">
        <input
          type="file"
          ref="fileInput"
          accept="image/*"
          @change="handleSelectImage"
          style="display: none"
        />
        <el-button type="primary" @click="$refs.fileInput.click()">
          选择图片
        </el-button>
      </div>
      
      <!-- 图片裁剪组件 -->
      <vue-cropper v-if="cropImg"
        ref="cropperRef"
        :img="cropImg"
        :info="true"
        :autoCrop="true"
        :fixedBox="true"
        :centerBox="true"
        :fixed="true"
        :fixedNumber="[1, 1]"
        :canScale="false"
        :full="false"
        :outputType="'png'"
        @realTime="cropImage"
      />
    </div>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleCancel">取消</el-button>
        <el-button v-if="cropImg" @click="handleReselect">重新选择</el-button>
        <el-button type="primary" @click="handleConfirm" :loading="uploading">
          确认上传
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { VueCropper } from 'vue-cropper'
import 'vue-cropper/dist/index.css'
import { useProfileStore } from '@/stores/profile'
import profile from '@/api/profile'
import { showToast } from '@/components/ToastMessage'

const props = defineProps({
  modelValue: Boolean
})

const emit = defineEmits(['update:modelValue', 'success'])

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const profileStore = useProfileStore()
const cropperRef = ref(null)
const cropImg = ref('')
const uploading = ref(false)
const fileInput = ref(null)

// 选择图片
const handleSelectImage = (e) => {
  const file = e.target.files[0]
  if (!file) return
  
  if (!file.type.includes('image/')) {
    showToast('请选择图片文件', 'warning')
    return
  }
  
  const reader = new FileReader()
  reader.onload = (e) => {
    cropImg.value = e.target.result
  }
  reader.readAsDataURL(file)
}

// 裁剪图片
const cropImage = () => {
  // 实时预览
}

// 上传裁剪后的图片
const handleCropUpload = async () => {
  try {
    uploading.value = true
    const blob = await new Promise((resolve) => {
      cropperRef.value.getCropBlob((data) => {
        resolve(data)
      })
    })
    
    const file = new File([blob], 'avatar.png', {
      type: 'image/png'
    })
    
    const formData = new FormData()
    formData.append('avatar', file)
    
    const response = await profileStore.updateAvatar(formData)
    
    if (response?.data?.code === 200) {
      showToast('头像上传成功', 'success')
      emit('success')
      visible.value = false
    }
  } catch (error) {
    console.error('头像上传失败:', error)
    showToast(error.message || '头像上传失败', 'error')
  } finally {
    uploading.value = false
  }
}

// 重新选择图片
const handleReselect = () => {
  cropImg.value = ''
  fileInput.value.value = '' // 清空文件输入
}

// 取消
const handleCancel = () => {
  cropImg.value = ''
  fileInput.value.value = ''
  visible.value = false
}

// 确认上传
const handleConfirm = () => {
  if (!cropImg.value) {
    showToast('请先选择图片', 'warning')
    return
  }
  handleCropUpload()
}
</script>

<style scoped>
.avatar-upload-container {
  width: 100%;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-btn {
  text-align: center;
}

.cropper {
  width: 100%;
  height: 100%;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 20px;
}
</style> 