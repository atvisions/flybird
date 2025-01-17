<template>
  <div class="basic-info-display">
    <div class="info-header">
      <h2 class="username">{{ data.username }}</h2>
      <div v-if="data.position" class="position">{{ data.position }}</div>
    </div>

    <div class="contact-info">
      <div v-if="data.phone" class="contact-item">
        <v-icon size="16" color="#409eff">mdi-phone</v-icon>
        <span>{{ data.phone }}</span>
      </div>
      <div v-if="data.email" class="contact-item">
        <v-icon size="16" color="#409eff">mdi-email</v-icon>
        <span>{{ data.email }}</span>
      </div>
    </div>

    <div v-if="data.bio" class="bio">
      {{ data.bio }}
    </div>
  </div>
</template>

<script setup>
defineProps({
  data: {
    type: Object,
    default: () => ({
      username: '',
      phone: '',
      email: '',
      position: '',
      bio: ''
    })
  }
})
</script>

<style scoped>
.basic-info-display {
  padding: 24px;
  background: #ffffff;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
}

.info-header {
  margin-bottom: 16px;
}

.username {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px;
}

.position {
  font-size: 16px;
  color: #409eff;
  margin-bottom: 16px;
}

.contact-info {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 16px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #606266;
}

.bio {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
  white-space: pre-wrap;
}
</style> 