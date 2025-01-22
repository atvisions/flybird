<template>
  <div class="resume-basic-info">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <el-skeleton animated :rows="6" />
    </div>
    
    <!-- 错误状态 -->
    <div v-else-if="error" class="error-state">
      <el-alert
        title="加载用户档案失败"
        type="error"
        :description="error"
        show-icon
      />
    </div>

    <!-- 正常显示内容 -->
    <template v-else>
      <!-- 头像和姓名部分 -->
      <div class="header-section">
        <div class="avatar-wrapper">
          <ResumeField 
            label=""
            data-path="basic_info.avatar"
            :width="100"
            :height="100"
            type="avatar"
          />
        </div>
        <div class="name-section">
          <ResumeField 
            label=""
            data-path="basic_info.name"
            :width="200"
            :fontSize="24"
            :labelWidth="0"
          />
          <div class="basic-row">
            <ResumeField 
              label=""
              data-path="basic_info.gender"
              :width="60"
              :labelWidth="0"
            />
            <ResumeField 
              label=""
              data-path="basic_info.age"
              :width="60"
              :labelWidth="0"
              suffix="岁"
            />
          </div>
        </div>
      </div>

      <!-- 联系信息部分 -->
      <div class="contact-section">
        <div class="info-row">
          <ResumeField 
            label="电话"
            data-path="basic_info.phone"
            :width="180"
          />
          <ResumeField 
            label="邮箱"
            data-path="basic_info.email"
            :width="220"
          />
        </div>
        <div class="info-row">
          <ResumeField 
            label="所在地"
            data-path="basic_info.location"
            :width="180"
          />
          <ResumeField 
            label="工作年限"
            data-path="basic_info.work_years"
            :width="120"
            suffix="年"
          />
        </div>
      </div>

      <!-- 求职意向部分 -->
      <div class="intention-section">
        <div class="info-row">
          <ResumeField 
            label="期望职位"
            data-path="basic_info.expected_position"
            :width="180"
          />
          <ResumeField 
            label="期望城市"
            data-path="basic_info.expected_city"
            :width="180"
          />
        </div>
        <div class="info-row">
          <ResumeField 
            label="期望薪资"
            data-path="basic_info.expected_salary"
            :width="180"
          />
          <ResumeField 
            label="求职状态"
            data-path="basic_info.job_status"
            :width="180"
          />
        </div>
      </div>

      <!-- 个人优势/自我评价 -->
      <div class="summary-section">
        <ResumeField 
          label="个人优势"
          data-path="basic_info.personal_summary"
          :width="600"
          :height="80"
          type="textarea"
        />
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useProfileStore } from '@/stores/profile'
import ResumeField from './ResumeField.vue'
import { ElSkeleton, ElAlert } from 'element-plus'

const profileStore = useProfileStore()
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  if (!profileStore.profileData) {
    loading.value = true
    error.value = ''
    
    try {
      await profileStore.loadProfileData()
    } catch (err) {
      error.value = err.message || '加载失败,请重试'
    } finally {
      loading.value = false
    }
  }
})
</script>

<style scoped>
.resume-basic-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  width: 100%;
}

.header-section {
  display: flex;
  gap: 20px;
  align-items: center;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.avatar-wrapper {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
}

.name-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.basic-row {
  display: flex;
  gap: 10px;
  align-items: center;
}

.contact-section,
.intention-section {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.info-row {
  display: flex;
  gap: 20px;
  align-items: center;
}

.summary-section {
  padding-top: 10px;
}

.loading-state,
.error-state {
  padding: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.error-state {
  width: 100%;
}
</style> 