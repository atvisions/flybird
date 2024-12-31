// src/views/user/MyProfile/composables/useModules.js
import { ref, computed } from 'vue'
import { showToast } from '@/components/ToastMessage'
import { user } from '@/api/user'
import { useProfileData } from './useProfileData'
import profile from '@/api/profile'
import { ElMessage } from 'element-plus'

// 所有可用的模块配置
const MODULES_CONFIG = {
  job_intention: { 
    order: 1, 
    visible: true,
    name: '求职意向',
    required: false
  },
  work_experience: { 
    order: 2, 
    visible: true,
    name: '工作经历',
    required: false
  },
  education: { 
    order: 3, 
    visible: false,
    name: '教育经历'
  },
  project: { 
    order: 4, 
    visible: false,
    name: '项目经历'
  },
  skill: { 
    order: 5, 
    visible: false,
    name: '专业技能'
  },
  certificate: { 
    order: 6, 
    visible: false,
    name: '证书奖项'
  },
  language: { 
    order: 7, 
    visible: false,
    name: '语言能力'
  },
  portfolio: { 
    order: 8, 
    visible: false,
    name: '作品展示'
  },
  social_link: { 
    order: 9, 
    visible: false,
    name: '社交主页'
  }
}

export function useModules() {
  const { fetchModuleData } = useProfileData()
  const loading = ref(false)
  const modules = ref(new Map())
  const activeModulesList = ref([])

  // 计算属性保持不变，但从 activeModulesList 读取数据
  const activeModules = computed(() => activeModulesList.value)
  
  // 计算属性：未激活的模块
  const inactiveModules = computed(() => 
    Array.from(modules.value.values())
      .filter(m => !m.visible && !m.required)
      .sort((a, b) => a.order - b.order)
  )

  // 初始化模块状态
  const initModules = () => {
    // 保存当前的模块状态
    const currentModules = modules.value

    const modulesMap = new Map()
    Object.entries(MODULES_CONFIG).forEach(([key, config]) => {
      // 如果已存在该模块，保持其当前状态
      if (currentModules.has(key)) {
        modulesMap.set(key, {
          ...currentModules.get(key),
          name: config.name,  // 更新可能变化的配置
          required: config.required || false
        })
      } else {
        // 新模块使用默认配置
        modulesMap.set(key, {
          type: key,
          name: config.name,
          order: config.order,
          visible: config.visible,
          required: config.required || false,
          data: null
        })
      }
    })
    modules.value = modulesMap
  }

  // 获取模块数据
  const fetchModulesData = async () => {
    try {
      loading.value = true
      
      // 1. 获取布局信息
      const layoutRes = await user.getProfileLayout()
      if (layoutRes.data?.code === 200) {
        const layout = layoutRes.data.data
        // 更新模块的可见性和顺序
        Object.entries(layout).forEach(([key, value]) => {
          if (modules.value.has(key)) {
            const module = modules.value.get(key)
            module.visible = value.visible
            module.order = value.order
          }
        })
      }

      // 2. 获取求职意向数据
      const jobIntentionRes = await profile.jobIntention.get()
      const jobIntentionData = jobIntentionRes?.data?.code === 200 
        ? jobIntentionRes.data.data 
        : {}

      // 3. 获取工作经历数据
      const workExperienceRes = await profile.workExperience.get()
      const workExperienceData = workExperienceRes?.data?.code === 200 
        ? workExperienceRes.data.data 
        : []

      // 4. 更新模块数据
      if (modules.value.has('job_intention')) {
        modules.value.get('job_intention').data = jobIntentionData
      }
      if (modules.value.has('work_experience')) {
        modules.value.get('work_experience').data = workExperienceData
      }

      // 5. 更新激活的模块列表
      activeModulesList.value = Array.from(modules.value.values())
        .filter(module => module.visible)
        .sort((a, b) => a.order - b.order)

    } catch (error) {
      console.error('获取模块数据失败:', error)
      ElMessage.error('获取数据失败，请稍后重试')
    } finally {
      loading.value = false
    }
  }

  // 初始化时调用一次 initModules
  initModules()

  // 移除模块
  const removeModule = async (moduleType) => {
    try {
      const module = modules.value.get(moduleType)
      if (!module || module.required) {
        throw new Error('该模块不能被移除')
      }

      loading.value = true

      // 1. 先更新本地状态
      module.visible = false

      // 2. 构建布局数据
      const layout = {}
      modules.value.forEach((module, key) => {
        layout[key] = {
          order: module.order,
          visible: module.visible
        }
      })

      // 3. 更新服务器布局
      const response = await user.updateProfileLayout({ 
        data: { layout }
      })

      if (response.data?.code === 200) {
        // 4. 重新获取数据以确保同步
        await fetchModulesData()
        ElMessage.success('模块已移除')
      } else {
        // 如果请求失败，回滚本地状态
        module.visible = true
        throw new Error('移除模块失败')
      }
    } catch (error) {
      console.error('移除模块失败:', error)
      ElMessage.error(error.message || '移除模块失败，请重试')
    } finally {
      loading.value = false
    }
  }

  // 添加模块
  const addModule = async (moduleType) => {
    try {
      const module = modules.value.get(moduleType)
      if (!module) {
        throw new Error('模块不存在')
      }

      loading.value = true

      // 1. 先更新本地状态
      module.visible = true
      module.order = activeModulesList.value.length + 1

      // 2. 构建布局数据
      const layout = {}
      modules.value.forEach((module, key) => {
        layout[key] = {
          order: module.order,
          visible: module.visible
        }
      })

      // 3. 更新服务器布局
      const response = await user.updateProfileLayout({ 
        data: { layout }
      })

      if (response.data?.code === 200) {
        // 4. 重新获取数据以确保同步
        await fetchModulesData()
        ElMessage.success('模块已添加')
      } else {
        // 如果请求失败，回滚本地状态
        module.visible = false
        module.order = MODULES_CONFIG[moduleType].order
        throw new Error('添加模块失败')
      }
    } catch (error) {
      console.error('添加模块失败:', error)
      ElMessage.error(error.message || '添加模块失败，请重试')
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
    removeModule
  }
}