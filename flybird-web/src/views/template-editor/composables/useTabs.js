import { ref } from 'vue'

export function useTabs() {
  // 从localStorage获取上次保存的tab,如果没有则默认为'components'
  const activeTab = ref(localStorage.getItem('editor_active_tab') || 'components')

  const tabs = [
    { key: 'components', label: '组件' },
    { key: 'icons', label: '图标' },
    { key: 'resume', label: '档案' },
    { key: 'templates', label: '模版' }
  ]

  const switchTab = (tab) => {
    activeTab.value = tab
    // 将当前选中的tab保存到localStorage
    localStorage.setItem('editor_active_tab', tab)
  }

  return {
    activeTab,
    tabs,
    switchTab
  }
} 