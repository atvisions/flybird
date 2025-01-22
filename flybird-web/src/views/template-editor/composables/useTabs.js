import { ref } from 'vue'

export function useTabs() {
  const tabs = [
    { key: 'templates', label: '模板' },
    { key: 'components', label: '组件' },
    { key: 'icons', label: '图标' },
    { key: 'resume', label: '简历' }
  ]

  const activeTab = ref('templates')

  const switchTab = (key) => {
    activeTab.value = key
  }

  return {
    tabs,
    activeTab,
    switchTab
  }
} 