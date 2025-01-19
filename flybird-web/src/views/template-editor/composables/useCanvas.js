import { ref } from 'vue'

export function useCanvas() {
  const canvasList = ref([
    {
      id: 1,
      name: '画布 1',
      elements: []
    }
  ])
  const currentCanvasId = ref(1)
  const MAX_CANVAS = 5

  // 添加新画布
  const addCanvas = () => {
    if (canvasList.value.length >= MAX_CANVAS) {
      alert('最多只能创建5个画布')
      return
    }
    const newId = canvasList.value[canvasList.value.length - 1].id + 1
    canvasList.value.push({
      id: newId,
      name: `画布 ${newId}`,
      elements: []
    })
    currentCanvasId.value = newId
  }

  // 删除画布
  const removeCanvas = (id) => {
    if (canvasList.value.length <= 1) {
      alert('至少需要保留一个画布')
      return
    }
    const index = canvasList.value.findIndex(canvas => canvas.id === id)
    if (index > -1) {
      canvasList.value.splice(index, 1)
      // 如果删除的是当前画布,切换到第一个画布
      if (currentCanvasId.value === id) {
        currentCanvasId.value = canvasList.value[0].id
      }
    }
  }

  // 切换画布
  const switchCanvas = (id) => {
    currentCanvasId.value = id
  }

  // 重命名画布
  const renameCanvas = (id, newName) => {
    const canvas = canvasList.value.find(c => c.id === id)
    if (canvas) {
      canvas.name = newName
    }
  }

  // 获取当前画布
  const getCurrentCanvas = () => {
    return canvasList.value.find(canvas => canvas.id === currentCanvasId.value)
  }

  // 更新画布元素
  const updateCanvasElements = (elements) => {
    const canvas = getCurrentCanvas()
    if (canvas) {
      canvasList.value = canvasList.value.map(c => {
        if (c.id === currentCanvasId.value) {
          return {
            ...c,
            elements: elements
          }
        }
        return c
      })
    }
  }

  return {
    canvasList,
    currentCanvasId,
    addCanvas,
    removeCanvas,
    switchCanvas,
    renameCanvas,
    getCurrentCanvas,
    updateCanvasElements
  }
} 