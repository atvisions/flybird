<template>
  <div class="resume-avatar" :style="avatarStyle">
    <img
      v-if="value"
      :src="value"
      :alt="label"
      class="avatar-image"
    >
    <el-icon v-else class="avatar-placeholder">
      <UserFilled />
    </el-icon>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { ElIcon } from 'element-plus'
import { UserFilled } from '@element-plus/icons-vue'

const props = defineProps({
  value: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    default: '头像'
  },
  size: {
    type: Number,
    default: 100
  },
  borderRadius: {
    type: String,
    default: '50%'
  }
})

const avatarStyle = computed(() => ({
  width: `${props.size}px`,
  height: `${props.size}px`,
  borderRadius: props.borderRadius
}))
</script>

<style scoped>
.resume-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  border: 1px solid #e4e7ed;
  overflow: hidden;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  font-size: 40px;
  color: #c0c4cc;
}
</style> 