const handleCanvasConfigChange = (config) => {
  canvasConfig.value = {
    ...canvasConfig.value,
    ...config
  }
}

const handleElementSelect = (element) => {
  selectedElement.value = element
}

const handleElementUpdate = (element) => {
  const index = elements.value.findIndex(e => e.id === element.id)
  if (index !== -1) {
    elements.value[index] = element
  }
}

const handleElementDelete = (elementId) => {
  elements.value = elements.value.filter(e => e.id !== elementId)
  selectedElement.value = null
}

const handleElementAdd = (element) => {
  elements.value.push(element)
  selectedElement.value = element
} 