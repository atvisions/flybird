import { ref } from 'vue'

export function useComponents() {
  const components = ref([
    {
      type: 'basic',
      title: '基础图形',
      items: [
        { 
          type: 'rectangle', 
          name: '矩形', 
          icon: 'rectangle-one',
          defaultProps: {
            width: 100,
            height: 100,
            fill: '#1890ff',
            stroke: '#1890ff',
            strokeWidth: 0,
            opacity: 1
          }
        },
        { 
          type: 'circle', 
          name: '圆形', 
          icon: 'round',
          defaultProps: {
            width: 100,
            height: 100,
            fill: '#1890ff',
            stroke: '#1890ff',
            strokeWidth: 0,
            opacity: 1
          }
        },
        { 
          type: 'triangle', 
          name: '三角形', 
          icon: 'triangle',
          defaultProps: {
            width: 200,
            height: 200,
            fill: '#1890ff',
            stroke: '#1890ff',
            strokeWidth: 0,
            opacity: 1
          }
        },
        { 
          type: 'line', 
          name: '线条', 
          icon: 'minus',
          defaultProps: {
            width: 100,
            height: 2,
            stroke: '#1890ff',
            strokeWidth: 2,
            opacity: 1
          }
        },
        { 
          type: 'arrow', 
          name: '箭头', 
          icon: 'arrow-right',
          defaultProps: {
            width: 100,
            height: 2,
            stroke: '#1890ff',
            strokeWidth: 2,
            opacity: 1
          }
        },
        { 
          type: 'star', 
          name: '星形', 
          icon: 'star',
          defaultProps: {
            width: 100,
            height: 100,
            fill: '#1890ff',
            stroke: '#1890ff',
            strokeWidth: 0,
            opacity: 1,
            points: 5
          }
        }
      ]
    },
    {
      type: 'text',
      title: '文本',
      items: [
        { 
          type: 'title', 
          name: '标题', 
          icon: 'title-level',
          defaultProps: {
            width: 200,
            height: 40,
            content: '标题',
            color: '#1890ff',
            fontSize: 24,
            fontFamily: 'Arial',
            fontWeight: 'bold',
            textAlign: 'center',
            italic: false,
            underline: false,
            lineHeight: 1.2,
            opacity: 1,
            editable: true
          }
        },
        { 
          type: 'text', 
          name: '文本', 
          icon: 'text',
          defaultProps: {
            width: 100,
            height: 30,
            content: '请输入文本',
            color: '#000000',
            fontSize: 14,
            fontFamily: 'Arial',
            fontWeight: 'normal',
            textAlign: 'left',
            italic: false,
            underline: false,
            lineHeight: 1.5,
            opacity: 1,
            editable: true
          }
        }
      ]
    }
  ])

  const handleDragStart = (e, component) => {
    e.dataTransfer.setData('component', JSON.stringify(component))
    
    // 设置拖拽时的视觉效果
    if (e.dataTransfer.setDragImage) {
      const dragImage = document.createElement('div')
      dragImage.className = 'drag-image'
      dragImage.textContent = component.name
      document.body.appendChild(dragImage)
      e.dataTransfer.setDragImage(dragImage, 0, 0)
      setTimeout(() => document.body.removeChild(dragImage), 0)
    }
  }

  return {
    components,
    handleDragStart
  }
} 