import { ref } from 'vue'

export function useElement(canvasRef) {
  const selectedElement = ref(null)

  const handleElementSelect = (element) => {
    selectedElement.value = element
  }

  const handleElementUpdate = () => {
    if (selectedElement.value) {
      canvasRef.value?.updateElement(selectedElement.value)
    }
  }

  const updateTextAlign = (align) => {
    if (selectedElement.value && selectedElement.value.type === 'text') {
      selectedElement.value.textAlign = align
      handleElementUpdate()
    }
  }

  const handleClear = () => {
    if (confirm('确定要清空画布吗？此操作不可恢复')) {
      canvasRef.value?.clear()
      selectedElement.value = null
    }
  }

  const handleSave = () => {
    // TODO: 实现保存功能
  }

  return {
    selectedElement,
    handleElementSelect,
    handleElementUpdate,
    updateTextAlign,
    handleClear,
    handleSave
  }
} 