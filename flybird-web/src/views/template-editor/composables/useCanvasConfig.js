import { ref } from 'vue'

// 默认画布配置
const defaultConfig = {
  backgroundColor: '#ffffff',
  showGrid: true,  // 默认显示网格
  gridSize: 10,    // 默认网格大小改为10px
  gridColor: 'rgba(0, 0, 0, 0.15)',  // 增加网格颜色的透明度
  showGuideLine: true,  // 默认显示辅助线
  width: 794,  // A4 宽度
  height: 1123 // A4 高度
}

export function useCanvasConfig() {
  const canvasConfig = ref({ ...defaultConfig })

  // 更新画布配置
  const updateConfig = (config) => {
    canvasConfig.value = {
      ...canvasConfig.value,
      ...config
    }
  }

  // 重置画布配置
  const resetConfig = () => {
    canvasConfig.value = { ...defaultConfig }
  }

  // 切换网格显示
  const toggleGrid = () => {
    canvasConfig.value.showGrid = !canvasConfig.value.showGrid
  }

  // 更新网格大小
  const updateGridSize = (size) => {
    canvasConfig.value.gridSize = Math.max(5, Math.min(50, size))
  }

  // 更新网格颜色
  const updateGridColor = (color) => {
    canvasConfig.value.gridColor = color
  }

  return {
    canvasConfig,
    updateConfig,
    resetConfig,
    toggleGrid,
    updateGridSize,
    updateGridColor
  }
} 