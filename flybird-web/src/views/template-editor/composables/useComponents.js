import { ref } from 'vue'
import { COMPONENT_GROUPS } from '../constants/components'

export function useComponents() {
  const componentGroups = ref(COMPONENT_GROUPS)

  const handleDragStart = (event, component) => {
    event.dataTransfer.effectAllowed = 'copy'
    
    const dragData = {
      type: component.type,
      subType: component.subType,
      label: component.label,
      defaultConfig: {
        ...component.defaultConfig,
        width: component.defaultConfig?.width || 100,
        height: component.defaultConfig?.height || 100,
        backgroundColor: component.defaultConfig?.backgroundColor || '#ffffff',
        borderColor: component.defaultConfig?.borderColor || '#000000',
        borderWidth: component.defaultConfig?.borderWidth || 1,
        borderStyle: component.defaultConfig?.borderStyle || 'solid',
        rotation: component.defaultConfig?.rotation || 0
      }
    }
    
    console.log('Drag start data:', dragData)
    
    event.dataTransfer.setData('text/plain', JSON.stringify(dragData))
  }

  return {
    componentGroups,
    handleDragStart
  }
} 