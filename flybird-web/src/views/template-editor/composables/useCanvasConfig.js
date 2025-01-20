import { computed } from 'vue'
import { useCanvas } from '../composables/useCanvas'

export function useCanvasConfig() {
  const { getCurrentCanvas, updateCanvasConfig } = useCanvas()

  // 通过计算属性获取当前画布的配置
  const canvasConfig = computed(() => {
    const canvas = getCurrentCanvas()
    return canvas?.config
  })

  // 更新画布配置
  const updateConfig = (config) => {
    updateCanvasConfig(config)
  }

  return {
    canvasConfig,
    updateCanvasConfig: updateConfig
  }
} 