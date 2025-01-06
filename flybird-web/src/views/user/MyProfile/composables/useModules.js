// src/views/user/MyProfile/composables/useModules.js
import { ref } from 'vue'
import profile from '@/api/profile'
import { ALL_MODULES } from '@/constants'

export function useModules() {
  const loading = ref(false)
  const activeModules = ref([])
  const inactiveModules = ref([])

  // 获取模块数据
  const fetchModulesData = async () => {
    try {
      loading.value = true
      const response = await profile.getLayout()

      if (response?.data?.code === 200) {
        const layoutData = response.data.data.layout
        
        // 处理激活的模块
        activeModules.value = Object.entries(layoutData)
          .filter(([type, config]) => config.visible)
          .map(([type, config]) => ({
            type,
            name: ALL_MODULES[type].name,
            visible: true,
            order: config.order
          }))
          .sort((a, b) => a.order - b.order)

        // 处理未激活的模块
        inactiveModules.value = Object.entries(layoutData)
          .filter(([type, config]) => {
            if (type === 'basic_info') return false
            return !config.visible
          })
          .map(([type, config]) => ({
            type,
            name: ALL_MODULES[type].name,
            visible: false,
            order: config.order || 999
          }))
      }
    } catch (error) {
      throw new Error('获取模块数据失败')
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    activeModules,
    inactiveModules,
    fetchModulesData
  }
}