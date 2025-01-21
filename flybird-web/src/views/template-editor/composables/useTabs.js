import { ref } from 'vue'

export const useTabs = () => {
  const activeTab = ref('components')
  
  const tabs = [
    { key: 'components', label: '组件' },
    { key: 'icons', label: '图标' },
    { key: 'resume', label: '档案' },
    { key: 'templates', label: '模版' }
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