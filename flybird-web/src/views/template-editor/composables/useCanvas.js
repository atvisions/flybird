import { ref } from 'vue'

// 画布配置
const A4_CONFIG = {
  width: 794, // 210mm = 794px
  height: 1123, // 297mm = 1123px
}

// 默认画布配置
const DEFAULT_CANVAS_CONFIG = {
  backgroundColor: '#ffffff',
  showGrid: false,
  gridSize: 20,
  gridColor: 'rgba(0, 0, 0, 0.1)',
  showRuler: false,
  showGuides: false,
  width: A4_CONFIG.width,
  height: A4_CONFIG.height,
}

export function useCanvas() {
  // 模板数据
  const templateData = ref({
    canvases: [
      {
        id: 1,
        elements: [],
        config: { ...DEFAULT_CANVAS_CONFIG }
      }
    ]
  })

  // 当前画布ID
  const currentCanvasId = ref(1)
  
  // 当前选中的元素
  const selectedElement = ref(null)

  // 获取当前画布
  const getCurrentCanvas = () => {
    return templateData.value.canvases.find(canvas => canvas.id === currentCanvasId.value)
  }

  // 更新画布元素
  const updateCanvasElements = (elements) => {
    const canvas = getCurrentCanvas()
    if (canvas) {
      canvas.elements = elements
    }
  }

  // 更新画布配置
  const updateCanvasConfig = (config, applyToAll = false) => {
    if (applyToAll) {
      // 更新所有画布的配置
      templateData.value.canvases.forEach(canvas => {
        canvas.config = {
          ...canvas.config,
          ...config
        }
      })
    } else {
      // 只更新当前画布的配置
      const canvas = getCurrentCanvas()
      if (canvas) {
        canvas.config = {
          ...canvas.config,
          ...config
        }
      }
    }
  }

  // 添加新画布
  const addCanvas = () => {
    const newId = templateData.value.canvases.length + 1
    templateData.value.canvases.push({
      id: newId,
      elements: [],
      config: { ...DEFAULT_CANVAS_CONFIG }
    })
    currentCanvasId.value = newId
  }

  // 删除画布
  const removeCanvas = (id) => {
    const index = templateData.value.canvases.findIndex(canvas => canvas.id === id)
    if (index !== -1) {
      templateData.value.canvases.splice(index, 1)
      if (currentCanvasId.value === id) {
        currentCanvasId.value = templateData.value.canvases[0]?.id || 1
      }
    }
  }

  // 切换画布
  const switchCanvas = (id) => {
    if (templateData.value.canvases.some(canvas => canvas.id === id)) {
      currentCanvasId.value = id
    }
  }

  // 处理元素选中
  const handleElementSelect = (element) => {
    selectedElement.value = element
  }

  // 处理元素更新
  const handleElementUpdate = (element) => {
    const canvas = getCurrentCanvas()
    if (canvas) {
      canvas.elements = canvas.elements.map(el => 
        el.id === element.id ? element : el
      )
    }
  }

  // 清空画布
  const handleClear = () => {
    const canvas = getCurrentCanvas()
    if (canvas) {
      canvas.elements = []
      selectedElement.value = null
    }
  }

  // 保存模板
  const handleSave = () => {
    console.log('保存模板:', templateData.value)
  }

  return {
    templateData,
    currentCanvasId,
    selectedElement,
    A4_CONFIG,
    getCurrentCanvas,
    updateCanvasElements,
    updateCanvasConfig,
    addCanvas,
    removeCanvas,
    switchCanvas,
    handleElementSelect,
    handleElementUpdate,
    handleClear,
    handleSave
  }
} 