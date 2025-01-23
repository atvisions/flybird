import { ref, computed } from 'vue'
import { useCanvasConfig } from './useCanvasConfig'

export function useCanvas() {
  const { canvasConfig: DEFAULT_CANVAS_CONFIG } = useCanvasConfig()
  
  const templateData = ref({
    canvases: []  // 初始化为空数组
  })

  const currentCanvasId = ref(0)
  const selectedElement = ref(null)
  const selectedElements = ref([])

  const updateCanvasData = (canvases) => {
    console.log('更新画布数据前:', templateData.value)
    // 创建一个新的引用来触发响应式更新
    templateData.value = {
      canvases: JSON.parse(JSON.stringify(canvases))  // 深拷贝确保响应性
    }
    console.log('更新画布数据后:', templateData.value)
  }

  const getCurrentCanvas = computed(() => {
    return templateData.value.canvases[currentCanvasId.value] || null
  })

  const switchCanvas = (id) => {
    currentCanvasId.value = id
    console.log('切换到画布:', id, getCurrentCanvas.value)
  }

  const updateCanvasElements = (elements) => {
    const canvas = getCurrentCanvas.value
    if (!canvas) return

    const canvases = [...templateData.value.canvases]
    canvases[currentCanvasId.value] = {
      ...canvas,
      elements: [...elements]
    }
    
    updateCanvasData(canvases)
  }

  const updateCanvasConfig = (payload) => {
    console.log('更新画布配置:', payload)
    const { canvasId, config } = payload
    
    // 找到要更新的画布
    const canvasIndex = templateData.value.canvases.findIndex(canvas => canvas.id === canvasId)
    if (canvasIndex === -1) {
      console.warn('未找到画布:', canvasId)
      return
    }

    const canvas = templateData.value.canvases[canvasIndex]
    
    // 构造新的配置
    const newConfig = {
      ...DEFAULT_CANVAS_CONFIG,  // 基础默认配置
      ...(canvas.config || {}),  // 当前配置
      ...config  // 新的配置
    }
    
    // 确保布尔值正确设置
    if ('showGrid' in config) {
      newConfig.showGrid = Boolean(config.showGrid)
    }
    if ('showGuideLine' in config) {
      newConfig.showGuideLine = Boolean(config.showGuideLine)
    }
    if ('backgroundColor' in config) {
      newConfig.backgroundColor = config.backgroundColor
    }
    
    console.log('更新后的画布配置:', newConfig)
    
    // 创建新的画布数组并更新配置
    const canvases = templateData.value.canvases.map((c, index) => {
      if (index === canvasIndex) {
        return {
          ...c,
          config: newConfig
        }
      }
      return c
    })
    
    // 更新模板数据
    templateData.value = {
      ...templateData.value,
      canvases
    }
  }

  const handleElementSelect = (element) => {
    selectedElement.value = element
  }

  const handleElementUpdate = (updatedElement) => {
    const canvas = getCurrentCanvas.value
    if (!canvas) return

    const elementIndex = canvas.elements.findIndex(el => el.id === updatedElement.id)
    if (elementIndex === -1) return

    const newElements = [...canvas.elements]
    newElements[elementIndex] = {
      ...canvas.elements[elementIndex],
      ...updatedElement
    }
    
    updateCanvasElements(newElements)
  }

  return {
    templateData,
    currentCanvasId,
    selectedElement,
    selectedElements,
    updateCanvasData,
    getCurrentCanvas,
    switchCanvas,
    updateCanvasElements,
    updateCanvasConfig,
    handleElementSelect,
    handleElementUpdate,
    DEFAULT_CANVAS_CONFIG
  }
} 