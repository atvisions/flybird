import { ref } from 'vue'

export function useDragDrop() {
  // 当前布局
  const currentLayout = ref(null)

  // 拖拽开始
  const handleDragStart = (event, component) => {
    console.log('开始拖拽:', component)
    event.dataTransfer.effectAllowed = 'move'
    event.dataTransfer.setData('application/json', JSON.stringify(component))
  }

  // 拖拽进入时的处理
  const handleDragEnter = (event) => {
    event.preventDefault()
  }

  // 拖拽离开时的处理
  const handleDragLeave = (event) => {
    event.preventDefault()
  }

  // 拖拽悬停时的处理
  const handleDragOver = (event) => {
    event.preventDefault()
  }

  // 放置处理
  const handleDrop = (event) => {
    event.preventDefault()
    
    const componentData = event.dataTransfer.getData('application/json')
    console.log('放置数据:', componentData)
    
    if (componentData) {
      try {
        const component = JSON.parse(componentData)
        console.log('解析后的组件:', component)
        currentLayout.value = component
      } catch (error) {
        console.error('解析布局数据失败:', error)
      }
    }
  }

  return {
    currentLayout,
    handleDragStart,
    handleDragEnter,
    handleDragLeave,
    handleDragOver,
    handleDrop
  }
} 