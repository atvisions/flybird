import { ref } from 'vue'

export function useZoom() {
  const MIN_SCALE = 0.1
  const MAX_SCALE = 3
  const SCALE_STEP = 0.1

  const scale = ref(1)

  const handleZoomIn = () => {
    if (scale.value < MAX_SCALE) {
      scale.value = Number((scale.value + SCALE_STEP).toFixed(2))
    }
  }

  const handleZoomOut = () => {
    if (scale.value > MIN_SCALE) {
      scale.value = Number((scale.value - SCALE_STEP).toFixed(2))
    }
  }

  const handleZoomChange = (value) => {
    scale.value = Number(value.toFixed(2))
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