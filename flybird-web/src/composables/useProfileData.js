import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import profile from '@/api/profile'

export function useProfileData() {
  const loading = ref(false)
  const basicInfo = ref(null)
  const profileData = ref({})
  const completionData = ref(null)

  // 获取基本信息
  const fetchBasicInfo = async () => {
    try {
      loading.value = true
      const response = await profile.getData()
      if (response.data?.code === 200) {
        basicInfo.value = response.data.data.basic_info
        profileData.value = response.data.data
        return basicInfo.value
      }
    } catch (error) {
      console.error('获取基本信息失败:', error)
      ElMessage.error('获取基本信息失败')
    } finally {
      loading.value = false
    }
  }

  // 获取模块数据
  const fetchModuleData = async (type) => {
    try {
      loading.value = true
      const response = await profile.getData()
      if (response.data?.code === 200) {
        profileData.value = response.data.data
        return profileData.value[type]
      }
    } catch (error) {
      console.error(`获取${type}数据失败:`, error)
      ElMessage.error(`获取${type}数据失败`)
    } finally {
      loading.value = false
    }
  }

  // 获取完整度数据
  const fetchCompletionData = async () => {
    try {
      loading.value = true
      const response = await profile.getData()
      if (response.data?.code === 200) {
        const data = response.data.data
        
        // 计算完整度
        completionData.value = {
          total: calculateCompleteness(data),
          modules: {
            basic_info: calculateModuleCompleteness(data.basic_info),
            job_intention: calculateModuleCompleteness(data.job_intention),
            work_experience: calculateModuleCompleteness(data.work_experience),
            education: calculateModuleCompleteness(data.education),
            project: calculateModuleCompleteness(data.project),
            skill: calculateModuleCompleteness(data.skill),
            certificate: calculateModuleCompleteness(data.certificate),
            language: calculateModuleCompleteness(data.language),
            portfolio: calculateModuleCompleteness(data.portfolio),
            social_link: calculateModuleCompleteness(data.social_link)
          }
        }
        return completionData.value
      }
    } catch (error) {
      console.error('获取完整度数据失败:', error)
      ElMessage.error('获取完整度数据失败')
    } finally {
      loading.value = false
    }
  }

  // 计算整体完整度
  const calculateCompleteness = (data) => {
    const modules = Object.keys(data)
    const completedModules = modules.filter(module => {
      const moduleData = data[module]
      return moduleData && (
        Array.isArray(moduleData) ? moduleData.length > 0 : Object.keys(moduleData).length > 0
      )
    })
    return Math.round((completedModules.length / modules.length) * 100)
  }

  // 计算单个模块完整度
  const calculateModuleCompleteness = (moduleData) => {
    if (!moduleData) return 0
    if (Array.isArray(moduleData)) {
      return moduleData.length > 0 ? 100 : 0
    }
    const fields = Object.keys(moduleData)
    const completedFields = fields.filter(field => moduleData[field])
    return Math.round((completedFields.length / fields.length) * 100)
  }

  return {
    loading,
    basicInfo,
    profileData,
    completionData,
    fetchBasicInfo,
    fetchModuleData,
    fetchCompletionData
  }
} 