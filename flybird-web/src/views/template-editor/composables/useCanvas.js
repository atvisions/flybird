import { ref, computed } from 'vue'
import { useCanvasConfig } from './useCanvasConfig'

// 画布配置
const A4_CONFIG = {
  width: 794, // 210mm = 794px
  height: 1123, // 297mm = 1123px
}

// 使用 useCanvasConfig 中的默认配置
const { canvasConfig: defaultConfig } = useCanvasConfig()

// 默认画布配置
const DEFAULT_CANVAS_CONFIG = {
  ...defaultConfig.value,
  width: A4_CONFIG.width,
  height: A4_CONFIG.height,
}

export function useCanvas() {
  // 初始化模板数据
  const templateData = ref({
    canvases: [{
      id: 0,
      elements: [],
      config: {
        width: 794,
        height: 1123,
        backgroundColor: '#ffffff',
        showGrid: false,
        showGuideLine: true
      }
    }]
  })

  // 当前画布ID
  const currentCanvasId = ref(0)

  // 获取当前画布
  const getCurrentCanvas = () => {
    const canvas = templateData.value.canvases.find(canvas => canvas.id === currentCanvasId.value)
    // 如果找不到当前画布，返回第一个画布
    return canvas || templateData.value.canvases[0]
  }

  // 更新画布元素
  const updateCanvasElements = (elements) => {
    const canvas = getCurrentCanvas()
    if (canvas) {
      canvas.elements = elements
    }
  }

  // 更新画布配置
  const updateCanvasConfig = (config) => {
    const canvas = getCurrentCanvas()
    if (canvas) {
      canvas.config = {
        ...canvas.config,
        ...config
      }
      console.log('Canvas config changed:', canvas.config)
    }
  }

  // 添加新画布
  const addCanvas = () => {
    const newId = templateData.value.canvases.length
    templateData.value.canvases.push({
      id: newId,
      elements: [],
      config: {
        ...DEFAULT_CANVAS_CONFIG
      }
    })
    return newId
  }

  // 删除画布
  const removeCanvas = (id) => {
    const index = templateData.value.canvases.findIndex(canvas => canvas.id === id)
    if (index !== -1 && templateData.value.canvases.length > 1) {
      templateData.value.canvases.splice(index, 1)
      // 如果删除的是当前画布，切换到前一个画布
      if (id === currentCanvasId.value) {
        currentCanvasId.value = templateData.value.canvases[Math.max(0, index - 1)].id
      }
    }
  }

  // 切换画布
  const switchCanvas = (id) => {
    if (templateData.value.canvases.some(canvas => canvas.id === id)) {
      currentCanvasId.value = id
    }
  }

  // 选中的元素
  const selectedElement = ref(null)

  // 选中元素处理
  const handleElementSelect = (element) => {
    selectedElement.value = element
  }

  // 更新元素
  const handleElementUpdate = (element) => {
    const canvas = getCurrentCanvas()
    if (!canvas) return

    const index = canvas.elements.findIndex(el => el.id === element.id)
    if (index !== -1) {
      canvas.elements[index] = element
    }
  }

  // 清空画布
  const handleClear = () => {
    const canvas = getCurrentCanvas()
    if (canvas) {
      canvas.elements = []
    }
  }

  // 更新画布数据
  const updateCanvasData = (canvases) => {
    if (!canvases || canvases.length === 0) {
      // 如果没有提供画布数据，创建一个默认画布
      templateData.value.canvases = [{
        id: 0,
        elements: [],
        config: {
          width: 794,
          height: 1123,
          backgroundColor: '#ffffff',
          showGrid: false,
          showGuideLine: true
        }
      }]
    } else {
      templateData.value.canvases = canvases
    }
    // 重置当前画布ID为0
    currentCanvasId.value = 0
  }

  return {
    templateData,
    currentCanvasId,
    getCurrentCanvas,
    updateCanvasElements,
    updateCanvasConfig,
    addCanvas,
    removeCanvas,
    switchCanvas,
    selectedElement,
    handleElementSelect,
    handleElementUpdate,
    handleClear,
    updateCanvasData,
    A4_CONFIG
  }
} 