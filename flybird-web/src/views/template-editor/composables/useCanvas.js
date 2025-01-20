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
  // 模板数据结构
  const templateData = ref({
    id: null,
    name: '',
    description: '',
    createTime: null,
    updateTime: null,
    canvases: [
      {
        id: 1,
        name: '画布 1',
        elements: [],
        config: { ...DEFAULT_CANVAS_CONFIG },
        order: 1,
        templateId: null,
        createTime: new Date().toISOString(),
        updateTime: new Date().toISOString(),
        metadata: {},
        thumbnail: null,
        version: 1,
        isPublished: false
      }
    ]
  })

  const currentCanvasId = ref(1)
  const selectedElement = ref(null)

  // 获取当前画布
  const getCurrentCanvas = () => {
    return templateData.value.canvases.find(canvas => canvas.id === currentCanvasId.value)
  }

  // 添加新画布
  const addCanvas = () => {
    if (templateData.value.canvases.length >= 5) {
      console.warn('最多只能创建5个画布')
      return
    }

    // 获取当前所有的ID
    const existingIds = templateData.value.canvases.map(canvas => canvas.id)
    
    // 找到1-5之间第一个空缺的ID
    let newId = 1
    while (existingIds.includes(newId) && newId <= 5) {
      newId++
    }

    const newCanvas = {
      id: newId,
      name: `画布 ${newId}`,
      elements: [],
      config: { ...DEFAULT_CANVAS_CONFIG },
      order: newId,
      templateId: templateData.value.id,
      createTime: new Date().toISOString(),
      updateTime: new Date().toISOString(),
      metadata: {},
      thumbnail: null,
      version: 1,
      isPublished: false
    }
    
    // 按id排序插入新画布
    const insertIndex = templateData.value.canvases.findIndex(canvas => canvas.id > newId)
    if (insertIndex === -1) {
      templateData.value.canvases.push(newCanvas)
    } else {
      templateData.value.canvases.splice(insertIndex, 0, newCanvas)
    }
    currentCanvasId.value = newId
  }

  // 删除画布
  const removeCanvas = (id) => {
    if (templateData.value.canvases.length <= 1) {
      console.warn('至少需要保留一个画布')
      return
    }

    const index = templateData.value.canvases.findIndex(canvas => canvas.id === id)
    if (index > -1) {
      templateData.value.canvases.splice(index, 1)
      if (currentCanvasId.value === id) {
        currentCanvasId.value = templateData.value.canvases[Math.max(0, index - 1)]?.id || templateData.value.canvases[0].id
      }
    }
  }

  // 切换画布
  const switchCanvas = (id) => {
    if (templateData.value.canvases.some(canvas => canvas.id === id)) {
      currentCanvasId.value = id
      selectedElement.value = null // 切换画布时清除选中状态
    }
  }

  // 选择元素
  const handleElementSelect = (element) => {
    console.log('handleElementSelect:', { 
      当前选中: selectedElement.value?.id,
      新选中: element?.id 
    })

    // 更新选中状态
    selectedElement.value = element
  }

  // 更新元素
  const handleElementUpdate = (updates) => {
    if (!selectedElement.value) return
    
    // 处理数值类型的属性
    const numericProps = ['x', 'y', 'width', 'height', 'rotate', 'zIndex']
    const processedUpdates = { ...updates }

    // 确保数值类型的属性被正确处理
    Object.keys(updates).forEach(key => {
      if (numericProps.includes(key)) {
        processedUpdates[key] = Math.max(0, parseInt(updates[key]) || 0)
      }
    })
    
    // 更新选中元素
    const updatedElement = { ...selectedElement.value, ...processedUpdates }
    selectedElement.value = updatedElement

    // 更新画布中的元素
    const canvas = getCurrentCanvas()
    if (canvas) {
      const updatedElements = canvas.elements.map(el => 
        el.id === updatedElement.id ? updatedElement : el
      )
      canvas.elements = updatedElements
      canvas.updateTime = new Date().toISOString()
    }
  }

  // 更新画布元素
  const updateCanvasElements = (elements) => {
    const canvas = getCurrentCanvas()
    if (canvas) {
      canvas.elements = [...elements]
      canvas.updateTime = new Date().toISOString()
    }
  }

  // 更新画布配置
  const updateCanvasConfig = (newConfig, applyToAll = false) => {
    console.log('useCanvas updateCanvasConfig:', newConfig, applyToAll)
    const updateTime = new Date().toISOString()
    
    if (applyToAll) {
      // 更新所有画布的配置
      const updatedCanvases = templateData.value.canvases.map(canvas => ({
        ...canvas,
        config: { ...canvas.config, ...newConfig },
        updateTime
      }))
      templateData.value = {
        ...templateData.value,
        canvases: updatedCanvases,
        updateTime
      }
    } else {
      // 只更新当前画布的配置
      const currentCanvas = getCurrentCanvas()
      if (currentCanvas) {
        const updatedCanvas = {
          ...currentCanvas,
          config: { ...currentCanvas.config, ...newConfig },
          updateTime
        }
        const updatedCanvases = templateData.value.canvases.map(canvas =>
          canvas.id === currentCanvas.id ? updatedCanvas : canvas
        )
        templateData.value = {
          ...templateData.value,
          canvases: updatedCanvases,
          updateTime
        }
      }
    }
  }

  // 获取模板数据
  const getTemplateData = () => {
    return { ...templateData.value }
  }

  // 获取单个画布数据
  const getCanvasData = (canvasId) => {
    const canvas = templateData.value.canvases.find(c => c.id === canvasId)
    return canvas ? { ...canvas } : null
  }

  // 加载模板数据
  const loadTemplateData = (data) => {
    if (data && Array.isArray(data.canvases) && data.canvases.length > 0) {
      templateData.value = {
        ...data,
        canvases: data.canvases.map(canvas => ({
          ...canvas,
          config: { ...DEFAULT_CANVAS_CONFIG, ...canvas.config },
          elements: canvas.elements || []
        }))
      }
      currentCanvasId.value = data.canvases[0].id
      selectedElement.value = null // 加载新数据时清除选中状态
    }
  }

  // 清除画布
  const handleClear = () => {
    const canvas = getCurrentCanvas()
    if (canvas) {
      canvas.elements = []
      canvas.updateTime = new Date().toISOString()
      selectedElement.value = null
    }
  }

  // 保存画布
  const handleSave = async () => {
    // TODO: 实现保存功能
    console.log('保存画布:', getTemplateData())
  }

  return {
    templateData,
    currentCanvasId,
    selectedElement,
    getCurrentCanvas,
    addCanvas,
    removeCanvas,
    switchCanvas,
    handleElementSelect,
    handleElementUpdate,
    updateCanvasElements,
    updateCanvasConfig,
    getTemplateData,
    getCanvasData,
    loadTemplateData,
    handleClear,
    handleSave,
    A4_CONFIG,
    DEFAULT_CANVAS_CONFIG
  }
} 