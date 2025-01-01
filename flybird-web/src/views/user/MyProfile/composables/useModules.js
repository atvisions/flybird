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
      const response = await profile.layout.update()
      console.log('【模块数据】服务器返回的布局数据:', response.data)

      if (response?.data?.code === 200) {
        const layoutData = response.data.data.layout
        
        // 处理活动和非活动模块
        const active = []
        const inactive = []
        
        // 过滤掉特殊字段
        const moduleEntries = Object.entries(layoutData).filter(([key]) => 
          !['layout', 'modules', 'timestamp'].includes(key)
        )
        
        // 获取各模块数据
        const moduleDataPromises = []
        
        // 如果求职意向模块可见，获取数据
        if (layoutData.job_intention?.visible) {
          moduleDataPromises.push(
            profile.jobIntention.get()
              .then(response => ({
                type: 'job_intention',
                data: response.data?.code === 200 ? response.data.data : null
              }))
              .catch(error => {
                console.error('获取求职意向数据失败:', error)
                return { type: 'job_intention', data: null }
              })
          )
        }
        
        // 如果工作经历模块可见，获取数据
        if (layoutData.work_experience?.visible) {
          moduleDataPromises.push(
            profile.workExperience.get()
              .then(response => ({
                type: 'work_experience',
                data: response.data?.code === 200 ? response.data.data : null
              }))
              .catch(error => {
                console.error('获取工作经历数据失败:', error)
                return { type: 'work_experience', data: null }
              })
          )
        }
        
        // 等待所有数据获取完成
        const modulesData = await Promise.all(moduleDataPromises)
        const moduleDataMap = modulesData.reduce((acc, { type, data }) => {
          acc[type] = data
          return acc
        }, {})
        
        // 处理模块数据
        moduleEntries.forEach(([type, config]) => {
          const moduleData = {
            type,
            name: ALL_MODULES[type] || type,
            order: config.order,
            timestamp: layoutData.timestamp,
            data: moduleDataMap[type] || null
          }
          
          if (config.visible) {
            active.push(moduleData)
          } else {
            inactive.push(moduleData)
          }
        })
        
        // 根据 order 排序活动模块
        activeModules.value = active.sort((a, b) => a.order - b.order)
        inactiveModules.value = inactive

        console.log('【模块数据】处理后的活动模块:', activeModules.value)
        console.log('【模块数据】处理后的未激活模块:', inactiveModules.value)
      }
    } catch (error) {
      console.error('获取模块数据失败:', error)
      activeModules.value = []
      inactiveModules.value = []
    } finally {
      loading.value = false
    }
  }

  // 添加模块（激活模块）
  const addModule = async (moduleType) => {
    try {
      loading.value = true
      console.log('【模块数据】准备激活模块:', moduleType)
      
      // 获取当前所有可见模块的配置
      const visibleModules = {}
      activeModules.value.forEach((module, index) => {
        visibleModules[module.type] = {
          visible: true,
          order: index + 1  // 保持现有模块的顺序
        }
      })
      
      // 添加新模块到最后
      const layoutUpdate = {
        ...visibleModules,  // 保持现有模块的配置
        [moduleType]: {
          visible: true,
          order: activeModules.value.length + 1  // 新模块放在最后
        }
      }
      
      console.log('【模块数据】更新布局:', layoutUpdate)
      const response = await profile.layout.update(layoutUpdate)
      console.log('【模块数据】服务器返回的更新结果:', response.data)

      if (response?.data?.code === 200) {
        await fetchModulesData()
      }
    } catch (error) {
      console.error('激活模块失败:', error)
    } finally {
      loading.value = false
    }
  }

  // 移除模块（取消激活）
  const removeModule = async (moduleType) => {
    try {
      loading.value = true
      console.log('【模块数据】准备取消激活模块:', moduleType)
      
      // 获取当前所有模块的配置（除了要移除的）
      const updatedModules = {}
      activeModules.value
        .filter(module => module.type !== moduleType)
        .forEach((module, index) => {
          updatedModules[module.type] = {
            visible: true,
            order: index + 1  // 重新排序剩余模块
          }
        })
      
      // 添加要移除的模块配置
      const layoutUpdate = {
        ...updatedModules,
        [moduleType]: {
          visible: false,
          order: 999  // 移到未激活模块区域
        }
      }
      
      console.log('【模块数据】更新布局:', layoutUpdate)
      const response = await profile.layout.update(layoutUpdate)
      console.log('【模块数据】服务器返回的更新结果:', response.data)

      if (response?.data?.code === 200) {
        await fetchModulesData()
      }
    } catch (error) {
      console.error('取消激活模块失败:', error)
    } finally {
      loading.value = false
    }
  }

  // 更新模块顺序
  const updateModuleOrder = async (modules) => {
    try {
      loading.value = true
      const layoutUpdate = modules.reduce((acc, module, index) => {
        acc[module.type] = {
          visible: true,
          order: index + 1
        }
        return acc
      }, {})
      
      const response = await profile.layout.update(layoutUpdate)
      if (response?.data?.code === 200) {
        await fetchModulesData()
      }
    } catch (error) {
      console.error('更新模块顺序失败:', error)
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    activeModules,
    inactiveModules,
    fetchModulesData,
    addModule,
    removeModule,
    updateModuleOrder
  }
}