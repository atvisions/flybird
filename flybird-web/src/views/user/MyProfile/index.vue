<!-- src/views/user/MyProfile/index.vue -->
<template>
  <div class="container mx-auto">
    <div class="max-w-4xl mx-auto space-y-4">
      <BasicInfo
        :resumeData="basicInfo"
        :loading="loading"
        :bioExpanded="bioExpanded"
        :showBioExpandButton="showBioExpandButton"
        @edit="handleEdit"
        @toggleBioExpand="toggleBioExpand"
      />

      <ResumeStatus
        :completion-data="completionData"
        :profile-data="profileData"
        :loading="loading"
      />

      <ModuleList
        :active-modules="activeModules"
        :loading="loading"
        @edit="handleEditModule"
        @add="addItem"
        @remove="removeModule"
        @edit-item="editItem"
        @remove-item="removeItem"
      />

      <AddModule
        :inactive-modules="inactiveModules"
        :loading="loading"
        @activate="activateModule"
      />

      <!-- 工作经历编辑弹窗 -->
      <EditWorkExperienceDialog
        v-if="currentModule?.type === 'work_experience'"
        v-model="showEditModal"
        :initial-data="editFormData"
        :loading="loading"
        @submit="handleSubmit"
      />

      <!-- 求职意向编辑弹窗 -->
      <EditJobIntentionDialog
        v-if="currentModule?.type === 'job_intention'"
        v-model="showEditModal"
        :initial-data="editFormData"
        :loading="loading"
        @submit="handleSubmit"
      />

      <!-- 基本信息编辑弹窗 -->
      <EditBasicDialog
        v-if="currentModule?.type === 'basic_info'"
        v-model="showEditModal"
        :initial-data="editFormData"
        :loading="loading"
        @submit="handleSubmit"
      />

      <AIOptimizeDialog
        v-model="showAIOptimizeDialog"
        :profile-data="profileData"
        @apply="handleAIOptimize"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useModules } from './composables/useModules'
import { profile } from '@/api/profile'
import { ElMessage, ElMessageBox } from 'element-plus'

// 组件引入
import BasicInfo from './components/BasicInfo.vue'
import ResumeStatus from './components/ResumeStatus.vue'
import ModuleList from './components/ModuleList.vue'
import AddModule from './components/AddModule.vue'
import EditBasicDialog from './dialogs/EditBasicDialog.vue'
import EditJobIntentionDialog from './dialogs/EditJobIntentionDialog.vue'
import EditWorkExperienceDialog from './dialogs/EditWorkExperienceDialog.vue'
import AIOptimizeDialog from './dialogs/AIOptimizeDialog.vue'

// 状态管理
const { 
  activeModules, 
  currentModule, 
  inactiveModules, 
  addItem, 
  removeModule, 
  activateModule 
} = useModules()

// 基本状态
const showEditModal = ref(false)
const editFormData = ref({})
const loading = ref(false)

// 基本信息控制
const bioExpanded = ref(false)
const showBioExpandButton = ref(false)

// 基本信息数据
const basicInfo = ref({})

// 档案数据
const profileData = ref({
  basic_info: {
    name: '',
    name_en: '',
    personal_summary: '',
    personal_summary_en: '',
    gender: '',
    phone: '',
    email: '',
    location: '',
    birth_date: ''
  },
  job_intention: {
    job_type: '',
    job_status: '',
    expected_salary: '',
    expected_city: '',
    industries: ''
  },
  work_experiences: [],
  educations: [],
  skills: []
})

// 完整度数据
const completionData = ref({
  total_score: 0,
  dimensions: {},
  suggestions: []
})

// 添加缺失的响应式变量
const showAIOptimizeDialog = ref(false)

// 处理 Bio 展开/收起
const toggleBioExpand = () => {
  bioExpanded.value = !bioExpanded.value
}

// 定义组件的 emits
defineEmits([
  'update:modelValue',
  'edit',
  'add',
  'remove',
  'edit-item',
  'remove-item'
])

// 获取档案数据
const fetchProfileData = async () => {
  try {
    loading.value = true
    
    const completenessResponse = await profile.getCompleteness()
    if (completenessResponse.data?.code === 200) {
      const data = completenessResponse.data.data
      completionData.value = {
        total_score: data.total_score || 0,
        dimensions: data.dimensions || {},
        suggestions: data.suggestions || []
      }
    }

    // 获取完整档案数据
    const response = await profile.getComplete()
    if (response.data?.code === 200) {
      const data = response.data.data
      
      // 更新档案数据
      profileData.value = {
        basic_info: data.basic_info || {},
        job_intention: data.job_intention || {},
        work_experiences: data.work_experiences || [],
        educations: data.educations || [],
        skills: data.skills || [],
        certificates: data.certificates || [],
        projects: data.projects || []
      }

      // 更新基本信息
      basicInfo.value = data.basic_info || {}

      // 更新活动模块数据
      const jobIntentionModule = activeModules.value.find(m => m.type === 'job_intention')
      if (jobIntentionModule) {
        jobIntentionModule.data = data.job_intention || {}
      }

      const workExperienceModule = activeModules.value.find(m => m.type === 'work_experience')
      if (workExperienceModule) {
        workExperienceModule.data = data.work_experiences || []
      }
    }
  } catch (error) {
    console.error('获取数据失败:', error)
    ElMessage.error('获取数据失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 监听完整度数据变化
watch(() => completionData.value, (newVal) => {}, { deep: true })

// 处理编辑基本信息
const handleEdit = () => {
  currentModule.value = {
    type: 'basic_info',
    data: basicInfo.value
  }
  editFormData.value = { ...currentModule.value.data }
  showEditModal.value = true
}

// 编辑具体项目（用于工作经历）
const editItem = (moduleId, item) => {
  currentModule.value = activeModules.value.find(m => m.id === moduleId)
  editFormData.value = { ...item }
  showEditModal.value = true
}

// 删除工作经历
const removeItem = async (moduleId, itemId) => {
  try {
    await ElMessageBox.confirm('确定要删除这条记录吗？', '提示', {
      type: 'warning'
    })
    
    if (moduleId === 'work_experience') {
      await profile.deleteWorkExperience(itemId)
      ElMessage.success('删除成功')
      await fetchProfileData()
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 提交表单
const handleSubmit = async (data) => {
  try {
    loading.value = true
    
    if (currentModule.value?.type === 'basic_info') {
      // 基本信息保存
      const response = await profile.updateBasicInfo(data)
      if (response.data?.code === 200) {
        ElMessage.success('保存成功')
        showEditModal.value = false
        await fetchProfileData()
      } else {
        throw new Error(response.data?.message || '保存失败')
      }
    } else if (currentModule.value?.type === 'work_experience') {
      if (data.id) {
        // 更新工作经历
        const response = await profile.workExperience.update(data.id, data)
        if (response.data?.code === 200) {
          ElMessage.success('更新成功')
          showEditModal.value = false
          await fetchProfileData()
        } else {
          throw new Error(response.data?.message || '更新失败')
        }
      } else {
        // 添加工作经历
        const response = await profile.workExperience.add(data)
        if (response.data?.code === 200) {
          ElMessage.success('添加成功')
          showEditModal.value = false
          await fetchProfileData()
        }
      }
    } else if (currentModule.value?.type === 'job_intention') {
      const response = await profile.updateJobIntention(data)
      if (response.data?.code === 200) {
        ElMessage.success('保存成功')
        showEditModal.value = false
        await fetchProfileData()
      }
    }
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error(error.message || '保存失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 处理编辑模块
const handleEditModule = (moduleId) => {
  currentModule.value = activeModules.value.find(m => m.id === moduleId)
  
  if (currentModule.value?.type === 'work_experience') {
    editFormData.value = {}
  } else if (currentModule.value?.type === 'job_intention') {
    editFormData.value = { ...currentModule.value.data }
  }
  
  showEditModal.value = true
}

// 处理 AI 优化结果
const handleAIOptimize = (optimizedData) => {
  Object.entries(optimizedData).forEach(([key, value]) => {
    const [category, field] = key.split('.')
    if (category && field) {
      if (!profileData.value[category]) {
        profileData.value[category] = {}
      }
      profileData.value[category][field] = value
    } else {
      profileData.value[key] = value
    }
  })
}

onMounted(() => {
  fetchProfileData()
})
</script>