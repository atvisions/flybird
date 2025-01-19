import { ref } from 'vue'

export function useZoom() {
  const scale = ref(1)
  const MIN_SCALE = 0.5
  const MAX_SCALE = 2
  const SCALE_STEP = 0.1

  const handleZoomIn = () => {
    if (scale.value < MAX_SCALE) {
      scale.value = Number((scale.value + SCALE_STEP).toFixed(1))
    }
  }

  const handleZoomOut = () => {
    if (scale.value > MIN_SCALE) {
      scale.value = Number((scale.value - SCALE_STEP).toFixed(1))
    }
  }

  const handleZoomChange = (value) => {
    const newScale = typeof value === 'object' ? Number(value.target.value) : Number(value)
    
    scale.value = Math.max(MIN_SCALE, Math.min(MAX_SCALE, newScale))
  }

  return {
    scale,
    MIN_SCALE,
    MAX_SCALE,
    SCALE_STEP,
    handleZoomIn,
    handleZoomOut,
    handleZoomChange
  }
} 