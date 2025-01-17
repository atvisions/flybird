import { ref } from 'vue'
import BasicInfo from '../components/BasicInfo.vue'
import Education from '../components/Education.vue'
import Experience from '../components/Experience.vue'
import Skills from '../components/Skills.vue'
import Projects from '../components/Projects.vue'
import Contact from '../components/Contact.vue'

export function useComponents() {
  // 组件类型映射
  const componentMap = {
    'basic-info': BasicInfo,
    'education': Education,
    'experience': Experience,
    'skills': Skills,
    'projects': Projects,
    'contact': Contact
  }

  // 根据类型获取组件
  const getComponentByType = (type) => {
    return componentMap[type] || null
  }

  // 获取所有可用组件
  const getAvailableComponents = () => {
    return Object.entries(componentMap).map(([type, component]) => ({
      type,
      name: component.name || type,
      component
    }))
  }

  // 验证组件类型是否有效
  const isValidComponentType = (type) => {
    return type in componentMap
  }

  return {
    getComponentByType,
    getAvailableComponents,
    isValidComponentType
  }
}