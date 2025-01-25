// 更新画布数据
const updateCanvasData = (canvases) => {
  console.log('更新画布数据，传入的数据:', canvases)
  
  if (!canvases || canvases.length === 0) {
    // 如果没有提供画布数据，创建一个默认画布
    templateData.value = {
      canvases: [{
        id: 0,
        elements: [],
        config: { ...DEFAULT_CANVAS_CONFIG }
      }]
    }
  } else {
    // 确保每个画布都有正确的配置
    const processedCanvases = canvases.map((canvas, index) => ({
      id: index,
      elements: (canvas.elements || []).map(element => ({
        id: element.id || `element-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        type: element.type || 'text',
        x: element.position?.x || element.x || 0,
        y: element.position?.y || element.y || 0,
        width: element.width || 100,
        height: element.height || 100,
        content: element.content || '',
        style: element.style || {},
        props: element.props || {},
        draggable: true,
        resizable: true,
        rotatable: true,
        lockAspectRatio: false,
        selected: false,
        zIndex: element.zIndex || 1,
        transform: element.transform || {
          rotate: 0,
          scaleX: 1,
          scaleY: 1
        }
      })),
      config: {
        width: canvas.config?.width || DEFAULT_CANVAS_CONFIG.width,
        height: canvas.config?.height || DEFAULT_CANVAS_CONFIG.height,
        backgroundColor: canvas.config?.backgroundColor || DEFAULT_CANVAS_CONFIG.backgroundColor,
        showGrid: canvas.config?.showGrid ?? DEFAULT_CANVAS_CONFIG.showGrid,
        showGuideLine: canvas.config?.showGuideLine ?? DEFAULT_CANVAS_CONFIG.showGuideLine,
        gridSize: canvas.config?.gridSize || DEFAULT_CANVAS_CONFIG.gridSize,
        gridColor: canvas.config?.gridColor || DEFAULT_CANVAS_CONFIG.gridColor
      }
    }))

    templateData.value = {
      canvases: processedCanvases
    }
  }
  
  // 重置当前画布ID为0
  currentCanvasId.value = 0
  
  console.log('更新后的画布数据:', templateData.value)
} 