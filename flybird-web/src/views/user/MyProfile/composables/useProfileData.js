import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import profile from '@/api/profile'
import { useProfileStore } from '@/stores/profile'

export function useProfileData() {
  const profileStore = useProfileStore()
  const loading = ref(true)
  const basicInfo = ref({})
  const profileData = ref({})
  const completionData = ref({
    total_score: 0,
    dimensions: {},
    suggestions: []
  })

  // 获取基本信息
  const fetchBasicInfo = async () => {
    try {
      loading.value = true
      const response = await profile.getBasicInfo()
      
      if (response?.data?.code === 200) {
        // 合并 user 和 basic_info 数据
        basicInfo.value = {
          ...response.data.data.user,
          ...response.data.data.basic_info
        }
    
        // 更新 profileData
        profileData.value = { 
          ...profileData.value, 
          basic: basicInfo.value 
        }
        
      } else {
        console.warn('基本信息 API 响应码不是 200:', response?.data?.code)
      }
    } catch (error) {
      console.error('获取基本信息失败:', error)
      console.error('错误详情:', error.response || error)
    } finally {
      loading.value = false
    }
  }

  // 获取完整度数据
  const fetchCompletionData = async () => {
    try {
      loading.value = true
      const response = await profile.getCompleteness()
      if (response?.data?.code === 200) {
        completionData.value = {
          total_score: response.data.data?.total_score || 0,
          dimensions: response.data.data?.dimensions || {},
          suggestions: response.data.data?.suggestions || []
        }
      }
    } catch (error) {
      console.error('获取完整度数据失败:', error)
      ElMessage.error('获取完整度数据失败，请稍后重试')
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
    fetchCompletionData
  }
}