import { ref } from 'vue'

export function useCanvasConfig() {
  // 画布配置
  const canvasConfig = ref({
    backgroundColor: '#ffffff',
    showGrid: true,
    gridSize: 20,
    gridColor: 'rgba(0, 0, 0, 0.05)',
    showRuler: true,
    showGuides: true
  })

  // 更新画布配置
  const updateCanvasConfig = (config) => {
    canvasConfig.value = {
      ...canvasConfig.value,
      ...config
    }
  }

  return {
    canvasConfig,
    updateCanvasConfig
  }
} 