export const vDraggable = {
  mounted(el, binding) {
    const options = binding.value || {}
    let isDragging = false
    let startX = 0
    let startY = 0

    const handleMouseDown = (e) => {
      if (e.button !== 0) return // 只处理左键点击
      
      isDragging = true
      startX = e.clientX
      startY = e.clientY
      
      // 添加全局事件监听
      document.addEventListener('mousemove', handleMouseMove)
      document.addEventListener('mouseup', handleMouseUp)
      
      // 阻止默认行为和冒泡
      e.preventDefault()
      e.stopPropagation()
    }

    const handleMouseMove = (e) => {
      if (!isDragging) return
      
      const deltaX = e.clientX - startX
      const deltaY = e.clientY - startY
      
      // 调用回调函数
      if (options.onDrag) {
        options.onDrag(e, { deltaX, deltaY })
      }
      
      startX = e.clientX
      startY = e.clientY
    }

    const handleMouseUp = (e) => {
      isDragging = false
      
      // 移除全局事件监听
      document.removeEventListener('mousemove', handleMouseMove)
      document.removeEventListener('mouseup', handleMouseUp)
      
      // 调用回调函数
      if (options.onDragEnd) {
        options.onDragEnd(e)
      }
    }

    // 设置样式和事件监听
    el.style.cursor = 'move'
    el.addEventListener('mousedown', handleMouseDown)

    // 保存清理函数
    el._draggableCleanup = () => {
      el.removeEventListener('mousedown', handleMouseDown)
      document.removeEventListener('mousemove', handleMouseMove)
      document.removeEventListener('mouseup', handleMouseUp)
    }
  },

  unmounted(el) {
    // 清理事件监听
    if (el._draggableCleanup) {
      el._draggableCleanup()
      delete el._draggableCleanup
    }
  }
} 