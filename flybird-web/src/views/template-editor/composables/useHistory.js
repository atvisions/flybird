import { ref } from 'vue'

export function useHistory() {
  const history = ref([])
  const currentIndex = ref(-1)

  const canUndo = () => currentIndex.value > 0
  const canRedo = () => currentIndex.value < history.value.length - 1

  const pushState = (state) => {
    // 如果当前不是在最新状态，删除当前位置之后的所有状态
    if (currentIndex.value < history.value.length - 1) {
      history.value.splice(currentIndex.value + 1)
    }
    
    // 深拷贝当前状态
    const newState = state.map(element => ({
      ...element,
      props: element.props ? { ...element.props } : {},
      style: element.style ? { ...element.style } : {}
    }))
    
    // 添加新状态
    history.value.push(newState)
    currentIndex.value++
  }

  const undo = () => {
    if (!canUndo()) return null
    currentIndex.value--
    // 返回深拷贝的状态
    return history.value[currentIndex.value].map(element => ({
      ...element,
      props: element.props ? { ...element.props } : {},
      style: element.style ? { ...element.style } : {}
    }))
  }

  const redo = () => {
    if (!canRedo()) return null
    currentIndex.value++
    // 返回深拷贝的状态
    return history.value[currentIndex.value].map(element => ({
      ...element,
      props: element.props ? { ...element.props } : {},
      style: element.style ? { ...element.style } : {}
    }))
  }

  return {
    pushState,
    undo,
    redo,
    canUndo,
    canRedo
  }
} 