<template>
  <div class="resume-basic-info">
    <ResumeField 
      label="姓名"
      data-path="basic_info.name"
      :width="200"
    />
    <ResumeField 
      label="性别"
      data-path="basic_info.gender"
      :width="150"
    />
    <ResumeField 
      label="年龄"
      data-path="basic_info.age"
      :width="150"
    />
    <ResumeField 
      label="电话"
      data-path="basic_info.phone"
      :width="200"
    />
    <ResumeField 
      label="邮箱"
      data-path="basic_info.email"
      :width="250"
    />
    <ResumeField 
      label="工作年限"
      data-path="basic_info.work_years"
      :width="150"
    />
    <ResumeField 
      label="期望职位"
      data-path="basic_info.expected_position"
      :width="200"
    />
    <ResumeField 
      label="期望城市"
      data-path="basic_info.expected_city"
      :width="200"
    />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useProfileStore } from '@/stores/profile'
import ResumeField from './ResumeField.vue'

const profileStore = useProfileStore()

onMounted(async () => {
  // 确保加载用户档案数据
  if (!profileStore.profileData) {
    await profileStore.loadProfileData()
  }
})
</script>

<style scoped>
.resume-basic-info {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 10px;
  padding: 15px;
  background-color: #fff;
  border-radius: 4px;
}
</style> 