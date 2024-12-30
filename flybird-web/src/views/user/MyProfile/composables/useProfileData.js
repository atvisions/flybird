import { ref } from 'vue'
import { profile } from '@/api/profile'

export function useProfileData() {
  const resumeData = ref(null)
  const bioExpanded = ref(false)
  const showBioExpandButton = ref(false)

  const fetchInitialData = async () => {
    try {
      const response = await profile.getBasicInfo()
      if (response.data?.code === 200) {
        resumeData.value = response.data.data
      }
    } catch (error) {
      console.error('获取个人资料失败:', error)
    }
  }

  const updateResumeData = async (data) => {
    try {
      const response = await profile.updateBasicInfo(data)
      if (response.data?.code === 200) {
        resumeData.value = response.data.data
        return true
      }
      return false
    } catch (error) {
      console.error('更新个人资料失败:', error)
      return false
    }
  }

  const getBioText = () => {
    if (!resumeData.value) return ''
    const bio = resumeData.value.personal_summary || ''
    if (!bioExpanded.value && bio.length > 100) {
      showBioExpandButton.value = true
      return bio.slice(0, 100) + '...'
    }
    showBioExpandButton.value = bio.length > 100
    return bio
  }

  const toggleBioExpand = () => {
    bioExpanded.value = !bioExpanded.value
  }

  return {
    resumeData,
    bioExpanded,
    showBioExpandButton,
    fetchInitialData,
    updateResumeData,
    getBioText,
    toggleBioExpand
  }
}