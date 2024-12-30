// src/views/user/MyProfile/composables/useModules.js
import { ref, computed, onMounted } from 'vue'
import { moduleConfig } from '../constants/moduleConfig'
import { BriefcaseIcon } from '@heroicons/vue/24/outline'
import { cityOptions } from '../constants/cityOptions'
import { ElMessage } from 'element-plus'
import { profile, updateLayout } from '@/api/profile'
import request from '@/utils/request'

export function useModules() {
  const activeModules = ref([])
  const currentModule = ref(null)
  const isInitialized = ref(false)

  // 获取布局数据
  const fetchLayout = async () => {
    try {
      const response = await request.get('/api/v1/users/profile/layout/')
      
      if (response.data?.code === 200 && response.data?.data?.layout) {
        const layout = response.data.data.layout
        
        // 初始化模块
        activeModules.value = moduleConfig
          .filter(config => layout[config.id]?.visible)
          .map(config => ({
            ...config,
            order: layout[config.id]?.order || config.order || 0,
            data: config.multiple ? [] : null
          }))
          .sort((a, b) => a.order - b.order)
        
        isInitialized.value = true
      }
    } catch (error) {
      console.error('获取布局失败:', error)
    }
  }

  const getNextOrder = () => {
    return activeModules.value.length + 1
  }

  const inactiveModules = computed(() => {
    const activeIds = activeModules.value.map(m => m.id)
    return moduleConfig.filter(m => !activeIds.includes(m.id))
  })

  const editModule = (moduleId) => {
    const module = activeModules.value.find(m => m.id === moduleId)
    if (module) {
      return {
        ...module,
        data: module.data ? {
          ...module.data,
          description: module.data.description || ''
        } : null
      }
    }
    return null
  }

  const addItem = (moduleId) => {
    const module = activeModules.value.find(m => m.id === moduleId)
    if (module) {
      module.currentItem = null
    }
  }

  const removeModule = async (moduleId) => {
    try {
      console.log('开始移除模块:', moduleId)
      
      // 更新布局，将模块设置为不可见
      const response = await updateLayout({
        [moduleId]: {
          visible: false
        }
      })

      if (response.data?.code === 200) {
        // 从活动模块中移除
        const index = activeModules.value.findIndex(m => m.id === moduleId)
        if (index > -1) {
          activeModules.value.splice(index, 1)
          
          // 重新排序剩余模块
          activeModules.value.forEach((module, idx) => {
            module.order = idx + 1
          })
          
          // 更新所有模块的顺序
          const orderUpdates = activeModules.value.reduce((acc, module) => {
            acc[module.id] = {
              order: module.order,
              visible: true
            }
            return acc
          }, {})
          
          // 发送顺序更新请求
          await updateLayout(orderUpdates)
          
          ElMessage.success('模块移除成功')
        }
      }
    } catch (error) {
      console.error('移除模块失败:', error)
      ElMessage.error('移除失败，请重试')
    }
  }

  // 激活模块
  const activateModule = async (moduleId) => {
    try {
      const module = moduleConfig.find(m => m.id === moduleId)
      if (!module) {
        throw new Error('模块不存在')
      }

      const order = getNextOrder()
      const response = await updateLayout({
        [moduleId]: {
          order,
          visible: true
        }
      })

      if (response.data?.code === 200) {
        const newModule = {
          ...module,
          data: module.multiple ? [] : null,
          order
        }
        activeModules.value.push(newModule)
      }
    } catch (error) {
      console.error('激活模块失败:', error)
    }
  }

  // 在组件挂载时自动获取布局
  onMounted(() => {
    if (!isInitialized.value) {
      fetchLayout()
    }
  })

  return {
    activeModules,
    inactiveModules,
    currentModule,
    editModule,
    addItem,
    removeModule,
    activateModule,
    fetchLayout,
    isInitialized
  }
}