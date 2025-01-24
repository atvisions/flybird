import { ref, watch } from 'vue'

export function useTabs() {
  // 定义 tab 顺序
  const tabs = [
    { key: 'components', label: '组件' },
    { key: 'icons', label: '图标' },
    { key: 'resume', label: '档案' },
    { key: 'templates', label: '模版' }
  ]

  // 从 localStorage 获取上次选中的 tab，如果没有则默认为 'components'
  const activeTab = ref(localStorage.getItem('editor_active_tab') || 'components')

  // 监听 activeTab 变化，保存到 localStorage
  watch(activeTab, (newValue) => {
    localStorage.setItem('editor_active_tab', newValue)
  })

  const switchTab = (key) => {
    activeTab.value = key
  }

  return {
    tabs,
    activeTab,
    switchTab
  }
} 