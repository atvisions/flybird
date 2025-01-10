<template>
  <div class="basic-info">
    <div class="avatar-wrapper" @click="showAvatarDialog = true">
      <img 
        v-if="profileAvatar" 
        :src="profileAvatar" 
        :key="avatarKey"
        class="avatar" 
      />
      <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
    </div>
    
    <!-- 头像上传对话框 -->
    <avatar-upload-dialog
      v-model="showAvatarDialog"
      @success="handleAvatarSuccess"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick, onUnmounted } from 'vue'
import { useProfileStore } from '@/stores/profile'
import { eventBus } from '@/utils/eventBus'
import { Plus } from '@element-plus/icons-vue'
import AvatarUploadDialog from './dialogs/AvatarUploadDialog.vue'

const profileStore = useProfileStore()
const showAvatarDialog = ref(false)
const avatarKey = ref(0)
const currentAvatar = ref(null)

const profileAvatar = computed(() => {
  console.log('Computing profileAvatar with timestamp:', profileStore.avatarUpdateTime)
  console.log('Current basicInfo:', profileStore.basicInfo)
  if (!profileStore.basicInfo) return null
  const url = currentAvatar.value || profileStore.basicInfo?.avatar
  console.log('Raw avatar URL:', url)
  if (!url) return null
  
  const fullUrl = `${import.meta.env.VITE_API_URL}${url}`
  console.log('Full avatar URL:', fullUrl)
  return fullUrl
})

onMounted(() => {
  // 确保清理旧数据
  profileStore.clearStore()
  
  // 监听头像更新事件
  eventBus.on('avatar-updated', (newAvatar) => {
    console.log('Avatar updated event received:', newAvatar)
    currentAvatar.value = newAvatar
    avatarKey.value++
  })

  // 初始化数据
  profileStore.fetchBasicInfo().then(() => {
    currentAvatar.value = profileStore.basicInfo?.avatar
    avatarKey.value++
  })
})

// 组件卸载时清理
onUnmounted(() => {
  eventBus.off('avatar-updated')
})

const handleAvatarSuccess = async () => {
  showAvatarDialog.value = false
}
</script>

<style scoped>
.avatar-wrapper {
  cursor: pointer;
  position: relative;
  width: 100px;
  height: 100px;
}
.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  text-align: center;
  border: 1px dashed #d9d9d9;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>