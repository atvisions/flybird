import { ref } from 'vue'

export function useTabs() {
  const activeTab = ref('components')
  
  const tabs = [
    { key: 'components', label: '组件' },
    { key: 'icons', label: '图标' },
    { key: 'templates', label: '模板' }
  ]
  
  const switchTab = (tab) => {
    activeTab.value = tab
  }
  
  return {
    activeTab,
    tabs,
    switchTab
  }
} 