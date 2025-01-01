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
      console.log('【ModuleList】开始获取模块数据')
      const response = await profile.layout.update()

      if (response?.data?.code === 200) {
        const layoutData = response.data.data.layout
        console.log('【ModuleList】布局数据:', layoutData)
        const moduleDataPromises = []
        
        // 获取所有可见模块的数据
        for (const [type, config] of Object.entries(layoutData)) {
          if (config.visible) {
            let promise;
            switch (type) {
              case 'education':
                promise = profile.education.get()
                  .then(response => ({
                    type,
                    name: ALL_MODULES[type],
                    data: response.data?.code === 200 ? response.data.data : [],
                    visible: true,
                    order: config.order
                  }))
                  .catch(() => ({
                    type,
                    name: ALL_MODULES[type],
                    data: [],
                    visible: true,
                    order: config.order
                  }));
                break;
                
              case 'job_intention':
                promise = profile.jobIntention.get()
                  .then(response => ({
                    type,
                    name: ALL_MODULES[type],
                    data: response.data?.code === 200 ? response.data.data : null,
                    visible: true,
                    order: config.order
                  }))
                  .catch(() => ({
                    type,
                    name: ALL_MODULES[type],
                    data: null,
                    visible: true,
                    order: config.order
                  }));
                break;
                
              case 'work_experience':
                promise = profile.workExperience.get()
                  .then(response => ({
                    type,
                    name: ALL_MODULES[type],
                    data: response.data?.code === 200 ? response.data.data : [],
                    visible: true,
                    order: config.order
                  }))
                  .catch(() => ({
                    type,
                    name: ALL_MODULES[type],
                    data: [],
                    visible: true,
                    order: config.order
                  }));
                break;

              case 'project':
                promise = profile.project.get()
                  .then(response => {
                    console.log('【ModuleList】获取项目数据响应:', response)
                    return {
                      type,
                      name: ALL_MODULES[type],
                      data: response.data?.data || [],
                      visible: true,
                      order: config.order
                    }
                  })
                  .catch(error => {
                    console.error('【ModuleList】获取项目数据失败:', error)
                    return {
                      type,
                      name: ALL_MODULES[type],
                      data: [],
                      visible: true,
                      order: config.order
                    }
                  });
                break;

              case 'skill':
                promise = profile.skill.get()
                  .then(response => {
                    console.log('【ModuleList】获取专业技能数据:', response)
                    return {
                      type,
                      name: ALL_MODULES[type],
                      data: response.data?.data || [],
                      visible: true,
                      order: config.order
                    }
                  })
                  .catch(error => {
                    console.error('【ModuleList】获取专业技能失败:', error)
                    return {
                      type,
                      name: ALL_MODULES[type],
                      data: [],
                      visible: true,
                      order: config.order
                    }
                  });
                break;

              case 'certificate':
                promise = profile.certificate.get()
                  .then(response => {
                    console.log('【ModuleList】获取证书数据:', response)
                    return {
                      type,
                      name: ALL_MODULES[type],
                      data: response.data?.code === 200 ? response.data.data : [],
                      visible: true,
                      order: config.order
                    }
                  })
                  .catch(error => {
                    console.error('【ModuleList】获取证书数据失败:', error)
                    return {
                      type,
                      name: ALL_MODULES[type],
                      data: [],
                      visible: true,
                      order: config.order
                    }
                  });
                break;

              case 'language':
                promise = profile.language.get()
                  .then(response => {
                    console.log('【ModuleList】获取语言数据:', response)
                    return {
                      type,
                      name: ALL_MODULES[type],
                      data: response.data?.data || [],
                      visible: true,
                      order: config.order
                    }
                  })
                  .catch(error => {
                    console.error('【ModuleList】获取语言数据失败:', error)
                    return {
                      type,
                      name: ALL_MODULES[type],
                      data: [],
                      visible: true,
                      order: config.order
                    }
                  });
                break;

              case 'portfolio':
                promise = Promise.resolve({
                  type,
                  name: ALL_MODULES[type],
                  data: [],
                  visible: true,
                  order: config.order
                });
                break;

              case 'social_link':
                promise = Promise.resolve({
                  type,
                  name: ALL_MODULES[type],
                  data: [],
                  visible: true,
                  order: config.order
                });
                break;

              default:
                // 对于未知类型，返回空数据
                promise = Promise.resolve({
                  type,
                  name: ALL_MODULES[type] || type,
                  data: null,
                  visible: true,
                  order: config.order
                });
                break;
            }
            
            if (promise) {
              moduleDataPromises.push(promise);
            }
          }
        }

        // 等待所有数据获取完成
        const modulesData = await Promise.all(moduleDataPromises)
        console.log('【ModuleList】所有模块数据:', modulesData)

        // 更新模块数据
        activeModules.value = modulesData
          .sort((a, b) => a.order - b.order)
          .map(module => ({
            type: module.type,
            name: module.name,
            data: module.data,
            visible: true,
            order: module.order
          }));

        // 检查项目模块数据
        const projectModule = activeModules.value.find(m => m.type === 'project')
        console.log('【ModuleList】项目模块数据:', projectModule)

        // 更新未激活模块列表
        inactiveModules.value = Object.entries(ALL_MODULES)
          .filter(([type]) => {
            // 过滤掉基本信息和已激活的模块
            return type !== 'basic_info' && !activeModules.value.some(m => m.type === type)
          })
          .map(([type, name]) => ({
            type,
            name,
            visible: false,
            order: 999
          }));

        console.log('【ModuleList】模块数据处理完成:', {
          活动模块: activeModules.value,
          未激活模块: inactiveModules.value
        })
      }
    } catch (error) {
      console.error('【模块数据】获取失败:', error)
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

  return {
    loading,
    activeModules,
    inactiveModules,
    fetchModulesData,
    addModule,     // 确保导出这两个方法
    removeModule
  }
}