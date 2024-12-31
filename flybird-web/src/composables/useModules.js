import { ref, computed } from 'vue'
import { showToast } from '@/components/ToastMessage'
import { user } from '@/api/user'

// 定义默认布局配置
const DEFAULT_LAYOUT = {
  basic_info: { 
    order: 1, 
    visible: true,
    name: '基本信息'
  },
  job_intention: { 
    order: 2, 
    visible: true,
    name: '求职意向'
  },
  work_experience: { 
    order: 3, 
    visible: true,
    name: '工作经历'
  },
  education: { 
    order: 4, 
    visible: false,
    name: '教育经历'
  },
  project: { 
    order: 5, 
    visible: false,
    name: '项目经历'
  },
  skill: { 
    order: 6, 
    visible: false,
    name: '专业技能'
  },
  certificate: { 
    order: 7, 
    visible: false,
    name: '证书奖项'
  },
  language: { 
    order: 8, 
    visible: false,
    name: '语言能力'
  },
  portfolio: { 
    order: 9, 
    visible: false,
    name: '作品展示'
  },
  social_link: { 
    order: 10, 
    visible: false,
    name: '社交主页'
  }
}

export function useModules() {
  const loading = ref(false)
  const activeModules = ref([])
  const inactiveModules = ref([])

  // 获取所有模块
  const allModules = computed(() => [...activeModules.value, ...inactiveModules.value])

  // 获取核心模块
  const coreModules = computed(() => 
    allModules.value.filter(m => ['basic_info', 'job_intention', 'work_experience'].includes(m.type))
  )

  // 获取可选模块
  const optionalModules = computed(() => 
    allModules.value.filter(m => !['basic_info', 'job_intention', 'work_experience'].includes(m.type))
  )

  // 获取布局
  const fetchLayout = async () => {
    try {
      loading.value = true
      console.log('开始获取布局')
      const response = await user.getProfileLayout()
      
      if (response.data?.code === 200) {
        const layout = response.data.data || DEFAULT_LAYOUT
        console.log('获取到的布局数据:', layout)
        
        // 规范化布局数据，确保包含所有默认模块
        const normalizedLayout = Object.entries(DEFAULT_LAYOUT).reduce((acc, [key, defaultConfig]) => {
          const serverConfig = layout[key] || {}
          acc[key] = {
            type: key,
            name: defaultConfig.name,
            order: serverConfig.order || defaultConfig.order,
            visible: serverConfig.visible ?? defaultConfig.visible,
            data: null
          }
          return acc
        }, {})
        console.log('规范化后的布局:', normalizedLayout)
        
        // 转换为数组并排序
        const modules = Object.values(normalizedLayout)
          .filter(m => m.type !== 'basic_info')
          .sort((a, b) => a.order - b.order)
        console.log('转换后的模块列表:', modules)

        // 分离激活和未激活的模块
        activeModules.value = modules.filter(m => m.visible)
        inactiveModules.value = modules.filter(m => !m.visible)
        console.log('激活的模块:', activeModules.value)
        console.log('未激活的模块:', inactiveModules.value)
      }
    } catch (error) {
      console.error('获取布局失败:', error)
      showToast(error.message || '获取布局失败，请重试', 'error')
    } finally {
      loading.value = false
    }
  }

  // 移除模块
  const removeModule = async (moduleType) => {
    try {
      loading.value = true
      
      // 更新本地状态
      const moduleIndex = activeModules.value.findIndex(m => m.type === moduleType)
      if (moduleIndex === -1) return
      
      const module = activeModules.value[moduleIndex]
      module.visible = false
      
      // 准备发送的布局数据
      const normalizedLayout = allModules.value.reduce((acc, m) => {
        acc[m.type] = { order: m.order, visible: m.visible }
        return acc
      }, {})

      console.log('发送的布局数据:', { layout: normalizedLayout })
      
      const response = await user.updateProfileLayout({
        layout: normalizedLayout
      })
      
      if (response.data?.code === 200) {
        // 移动模块到未激活列表
        activeModules.value.splice(moduleIndex, 1)
        inactiveModules.value.push(module)
        showToast('模块已移除', 'success')
      }
    } catch (error) {
      console.error('移除模块失败:', error)
      showToast(error.message || '移除模块失败，请重试', 'error')
    } finally {
      loading.value = false
    }
  }

  // 添加模块
  const addModule = async (moduleType) => {
    try {
      loading.value = true
      console.log('开始添加模块:', moduleType)
      console.log('当前未激活模块:', inactiveModules.value)
      
      // 查找要添加的模块
      const moduleToAdd = inactiveModules.value.find(m => m.type === moduleType)
      console.log('找到要添加的模块:', moduleToAdd)

      let moduleData = moduleToAdd
      if (!moduleToAdd) {
        // 如果在未激活列表中找不到，从默认配置创建
        const defaultConfig = DEFAULT_LAYOUT[moduleType]
        if (!defaultConfig) {
          console.warn('未找到默认配置:', moduleType)
          return
        }
        
        moduleData = {
          type: moduleType,
          name: defaultConfig.name,
          order: activeModules.value.length + 1,
          visible: true,
          data: null
        }
        console.log('从默认配置创建新模块:', moduleData)
      }

      // 设置为可见
      moduleData.visible = true
      
      // 准备发送的布局数据
      const normalizedLayout = [...activeModules.value, moduleData].reduce((acc, m) => {
        acc[m.type] = { 
          order: m.order, 
          visible: m.visible,
          name: m.name
        }
        return acc
      }, {})
      console.log('准备发送的布局数据:', normalizedLayout)
      
      const response = await user.updateProfileLayout({
        layout: normalizedLayout
      })
      console.log('服务器响应:', response.data)
      
      if (response.data?.code === 200) {
        // 从未激活列表中移除
        const moduleIndex = inactiveModules.value.findIndex(m => m.type === moduleType)
        if (moduleIndex > -1) {
          inactiveModules.value.splice(moduleIndex, 1)
        }
        
        // 添加到激活列表
        activeModules.value.push(moduleData)
        console.log('更新后的激活模块列表:', activeModules.value)
        
        // 重新排序
        activeModules.value.sort((a, b) => a.order - b.order)
        
        showToast('模块已添加', 'success')
      }
    } catch (error) {
      console.error('添加模块失败:', error)
      showToast(error.message || '添加模块失败，请重试', 'error')
    } finally {
      loading.value = false
    }
  }

  // 更新模块顺序
  const updateOrder = async (newOrder) => {
    try {
      loading.value = true
      
      // 更新本地状态
      activeModules.value = newOrder.map((type, index) => {
        const module = activeModules.value.find(m => m.type === type)
        return { ...module, order: index + 1 }
      })
      
      // 准备发送的布局数据
      const normalizedLayout = allModules.value.reduce((acc, m) => {
        acc[m.type] = { order: m.order, visible: m.visible }
        return acc
      }, {})
      
      const response = await user.updateProfileLayout({
        layout: normalizedLayout
      })
      
      if (response.data?.code === 200) {
        showToast('布局已更新', 'success')
      }
    } catch (error) {
      console.error('更新顺序失败:', error)
      showToast(error.message || '更新顺序失败，请重试', 'error')
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    activeModules,
    inactiveModules,
    allModules,
    coreModules,
    optionalModules,
    fetchLayout,
    removeModule,
    addModule,
    updateOrder
  }
} 