import { ref } from 'vue'

export function useTabs() {
  const tabs = [
    { key: 'templates', label: '模板' },
    { key: 'components', label: '组件' },
    { key: 'icons', label: '图标' }
  ]
  
  const activeTab = ref('components')

  return {
    tabs,
    activeTab
  }
} 