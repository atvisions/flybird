import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import profile from '@/api/profile'
import { useProfileStore } from '@/stores/profile'

export function useProfileData() {
  const loading = ref(false)
  const basicInfo = ref(null)
  const profileData = ref({})
  const completionData = ref(null)
  const profileStore = useProfileStore()

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
      await profileStore.fetchCompleteness()
      completionData.value = profileStore.completeness
      return completionData.value
    } catch (error) {
      console.error('获取完整度数据失败:', error)
      ElMessage.error('获取完整度数据失败')
    } finally {
      loading.value = false
    }
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