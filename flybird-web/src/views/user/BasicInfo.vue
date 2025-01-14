<template>
  <div class="basic-info">
    <div class="avatar-wrapper" @click="showAvatarDialog = true">
      <div class="avatar-container">
        <img 
          v-if="profileAvatar" 
          :src="profileAvatar" 
          :key="avatarKey"
          class="avatar" 
          :class="{ 'avatar-loaded': imageLoaded }"
          @load="handleImageLoad"
        />
        <div v-if="!imageLoaded" class="avatar-placeholder">
          <el-icon class="avatar-uploader-icon"><Plus /></el-icon>
        </div>
      </div>
    </div>
    
    <!-- 头像上传对话框 -->
    <avatar-upload-dialog
      v-model="showAvatarDialog"
      :loading="loading"
      @upload="handleAvatarSuccess"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick, onUnmounted } from 'vue'
import { useProfileStore } from '@/stores/profile'
import { eventBus } from '@/utils/eventBus'
import { Plus } from '@element-plus/icons-vue'
import { showToast } from '@/components/ToastMessage'
import AvatarUploadDialog from './MyProfile/dialogs/AvatarUploadDialog.vue'
import profile from '@/api/profile'

const profileStore = useProfileStore()
const showAvatarDialog = ref(false)
const avatarKey = ref(0)
const currentAvatar = ref(null)
const imageLoaded = ref(false)
const loading = ref(false)

const handleImageLoad = () => {
  imageLoaded.value = true
}

const profileAvatar = computed(() => {
  if (!profileStore.basicInfo) return null
  const url = currentAvatar.value || profileStore.basicInfo?.avatar
  if (!url) return null
  return `${import.meta.env.VITE_API_URL}${url}`
})

onMounted(() => {
  profileStore.clearStore()
  
  eventBus.on('avatar-updated', (newAvatar) => {
    imageLoaded.value = false
    currentAvatar.value = newAvatar
    avatarKey.value++
  })

  profileStore.fetchBasicInfo().then(() => {
    currentAvatar.value = profileStore.basicInfo?.avatar
    avatarKey.value++
  })
})

onUnmounted(() => {
  eventBus.off('avatar-updated')
})

const handleAvatarSuccess = async (file) => {
  try {
    loading.value = true
    // 使用 profileStore 的 updateAvatar 方法
    await profileStore.updateAvatar(file)
    // 重新获取基本信息以更新分值
    await profileStore.fetchBasicInfo()
    // 获取最新的完整度数据
    const completenessResponse = await profile.getCompleteness()
    if (completenessResponse?.data?.code === 200) {
      // 触发完整度更新事件
      eventBus.emit('completeness-updated', completenessResponse.data.data)
    }
    // 触发头像更新事件
    eventBus.emit('avatar-updated', profileStore.basicInfo?.avatar)
    showAvatarDialog.value = false
    showToast('头像上传成功', 'success')
  } catch (error) {
    console.error('头像上传失败:', error)
    showToast(error.message || '头像上传失败，请稍后重试', 'error')
  } finally {
    loading.value = false
  }
}

// 添加监听器以确保头像更新后重新获取基本信息
watch(() => profileStore.basicInfo?.avatar, async (newAvatar) => {
  if (newAvatar) {
    // 重新获取基本信息以更新分值
    await profileStore.fetchBasicInfo()
  }
})
</script>

<style scoped>
.avatar-wrapper {
  cursor: pointer;
  position: relative;
  width: 100px;
  height: 100px;
}

.avatar-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.avatar-loaded {
  opacity: 1;
}

.avatar-placeholder {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
  border-radius: 50%;
  border: 1px dashed #d9d9d9;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
}
</style>