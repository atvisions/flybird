import { markRaw } from 'vue'
import {
  Rectangle,
  Round,
  Triangle,
  Minus,
  ArrowRight,
  Star,
  H,
  Text
} from '@icon-park/vue-next'

// 确保所有图标组件都存在
const icons = {
  Rectangle,
  Round,
  Triangle,
  Line: Minus,
  ArrowRight,
  Star,
  H,
  Text
}

// 安全地使用 markRaw
const wrapIcon = (icon) => {
  return icon ? markRaw(icon) : null
}

export const COMPONENT_TYPES = {
  SHAPE: 'shape',
  TEXT: 'text'
}

export const SHAPE_TYPES = {
  RECTANGLE: 'rectangle',
  CIRCLE: 'circle',
  TRIANGLE: 'triangle',
  LINE: 'line',
  ARROW: 'arrow',
  STAR: 'star'
}

export const TEXT_TYPES = {
  HEADING: 'heading',
  PARAGRAPH: 'paragraph'
}

// 组件默认配置
export const DEFAULT_COMPONENT_CONFIG = {
  [COMPONENT_TYPES.SHAPE]: {
    width: 100,
    height: 100,
    backgroundColor: '#ffffff',
    borderColor: '#000000',
    borderWidth: 1,
    borderStyle: 'solid',
    borderRadius: 0,
    opacity: 1,
    rotation: 0,
    zIndex: 1
  },
  [COMPONENT_TYPES.TEXT]: {
    width: 200,
    height: 'auto',
    color: '#000000',
    fontSize: 14,
    fontWeight: 'normal',
    fontFamily: 'Arial',
    textAlign: 'left',
    lineHeight: 1.5,
    opacity: 1,
    rotation: 0,
    zIndex: 1
  }
}

// 组件分组配置
export const COMPONENT_GROUPS = [
  {
    title: '基础图形',
    items: [
      {
        type: 'shape',
        subType: 'circle',
        label: '圆形',
        icon: wrapIcon(icons.Round),
        defaultConfig: {
          width: 100,
          height: 100,
          backgroundColor: '#ffffff',
          borderColor: '#000000',
          borderWidth: 1,
          borderStyle: 'solid',
          rotation: 0
        }
      },
      {
        type: 'shape',
        subType: 'rectangle',
        label: '矩形',
        icon: wrapIcon(icons.Rectangle),
        defaultConfig: {
          width: 120,
          height: 80,
          backgroundColor: '#ffffff',
          borderColor: '#000000',
          borderWidth: 1,
          borderStyle: 'solid',
          rotation: 0
        }
      },
      {
        type: 'shape',
        subType: 'triangle',
        label: '三角形',
        icon: wrapIcon(icons.Triangle),
        defaultConfig: {
          width: 100,
          height: 100,
          backgroundColor: '#000000',
          borderColor: '#000000',
          borderWidth: 0,
          borderStyle: 'none',
          rotation: 0
        }
      },
      {
        type: 'shape',
        subType: 'line',
        label: '线条',
        icon: wrapIcon(icons.Line),
        defaultConfig: {
          width: 100,
          height: 2,
          backgroundColor: '#000000',
          borderColor: '#000000',
          borderWidth: 0,
          borderStyle: 'none',
          rotation: 0
        }
      },
      {
        type: 'shape',
        subType: 'arrow',
        label: '箭头',
        icon: wrapIcon(icons.ArrowRight),
        defaultConfig: {
          width: 120,
          height: 40,
          backgroundColor: '#000000',
          borderColor: '#000000',
          borderWidth: 0,
          borderStyle: 'none',
          rotation: 0
        }
      },
      {
        type: 'shape',
        subType: 'star',
        label: '星形',
        icon: wrapIcon(icons.Star),
        defaultConfig: {
          width: 100,
          height: 100,
          backgroundColor: '#000000',
          borderColor: '#000000',
          borderWidth: 0,
          borderStyle: 'none',
          rotation: 0
        }
      }
    ]
  },
  {
    title: '文本',
    items: [
      {
        type: 'text',
        subType: 'heading',
        label: '标题',
        icon: wrapIcon(icons.H),
        defaultConfig: {
          text: '标题文本',
          fontSize: 24,
          fontWeight: 'bold',
          color: '#000000',
          textAlign: 'left'
        }
      },
      {
        type: 'text',
        subType: 'paragraph',
        label: '段落',
        icon: wrapIcon(icons.Text),
        defaultConfig: {
          text: '这是一段文本',
          fontSize: 14,
          fontWeight: 'normal',
          color: '#000000',
          textAlign: 'left'
        }
      }
    ]
  }
] 