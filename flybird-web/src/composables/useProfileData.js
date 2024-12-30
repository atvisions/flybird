import { ref, onMounted } from 'vue'
import { profile } from '@/api/profile'
import { showToast } from '@/components/ToastMessage'

export function useProfileData() {
  const profileData = ref({})
  const loading = ref(false)

  const fetchProfileData = async () => {
    loading.value = true
    try {
      const response = await profile.getProfile()
      if (response.data.code === 200) {
        profileData.value = response.data.data
      } else {
        throw new Error(response.data.message || '获取资料失败')
      }
    } catch (error) {
      console.error('获取用户资料失败:', error)
      showToast(error.message || '获取用户资料失败', 'error')
    } finally {
      loading.value = false
    }
  }

  const updateProfileData = async (data) => {
    loading.value = true
    try {
      const response = await profile.updateProfile(data)
      if (response.data.code === 200) {
        showToast('资料更新成功', 'success')
        await fetchProfileData()  // 重新获取最新数据
        return true
      } else {
        throw new Error(response.data.message || '更新资料失败')
      }
    } catch (error) {
      console.error('更新用户资料失败:', error)
      showToast(error.message || '更新用户资料失败', 'error')
      return false
    } finally {
      loading.value = false
    }
  }

  onMounted(() => {
    fetchProfileData()
  })

  return {
    profileData,
    loading,
    fetchProfileData,
    updateProfileData
  }
} 