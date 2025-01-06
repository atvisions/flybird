import { ref, onMounted } from 'vue'
import profile from '@/api/profile'
import { ElMessage } from 'element-plus'

export function useModules(layoutData) {
  const loading = ref(false)
  const modules = ref([])

  const fetchModulesData = async () => {
    loading.value = true
    try {
      const response = await profile.getData()
      if (response.data?.code === 200) {
        const data = response.data.data
        modules.value = [
          { 
            type: 'basic_info', 
            data: data.basic_info || {},
            name: '基本信息',
            editable: true
          },
          { 
            type: 'job_intention', 
            data: data.job_intention || {},
            name: '求职意向',
            editable: true
          },
          { 
            type: 'work_experience', 
            data: data.work_experience || [],
            name: '工作经历',
            editable: true,
            isArray: true
          },
          { 
            type: 'education', 
            data: data.education || [],
            name: '教育经历',
            editable: true,
            isArray: true
          },
          { 
            type: 'project', 
            data: data.project || [],
            name: '项目经历',
            editable: true,
            isArray: true
          },
          { 
            type: 'skill', 
            data: data.skill || [],
            name: '专业技能',
            editable: true,
            isArray: true
          },
          { 
            type: 'certificate', 
            data: data.certificate || [],
            name: '证书奖项',
            editable: true,
            isArray: true
          },
          { 
            type: 'language', 
            data: data.language || [],
            name: '语言能力',
            editable: true,
            isArray: true
          },
          { 
            type: 'portfolio', 
            data: data.portfolio || [],
            name: '作品展示',
            editable: true,
            isArray: true
          },
          { 
            type: 'social_link', 
            data: data.social_link || [],
            name: '社交主页',
            editable: true,
            isArray: true
          }
        ]
      }
    } catch (error) {
      console.error('获取模块数据失败:', error)
      ElMessage.error('获取模块数据失败')
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    modules,
    fetchModulesData
  }
} 