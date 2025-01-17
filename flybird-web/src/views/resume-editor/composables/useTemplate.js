import { ref } from 'vue'
import templateApi from '@/api/template'

export function useTemplate() {
  const defaultTheme = {
    colors: {
      primary: '#1867C0',
      secondary: '#5CBBF6',
      accent: '#4CAF50',
      background: '#FFFFFF',
      text: '#2C3E50',
      border: '#E0E0E0'
    },
    typography: {
      body: {
        font: 'Arial',
        size: '14px',
        weight: 'normal'
      },
      heading: {
        font: 'Arial',
        size: '16px',
        weight: 'bold'
      }
    },
    spacing: {
      padding: '16px',
      margin: '16px',
      gap: '16px'
    }
  }

  // 准备模板数据
  const prepareTemplateData = (layoutData, currentTemplate, formData) => {
    const layout = layoutData[0]
    
    return {
      name: formData.name,
      description: formData.description,
      // 布局配置
      layout: {
        type: layout.config.type || 'grid',
        areas: layout.config.areas || [],
        columns: layout.config.columns || 12,
        gap: layout.config.gap || '20px'
      },
      // 组件配置
      components: layout.config.components.map(comp => ({
        id: comp.id,
        type: comp.type,
        name: comp.name,
        area: comp.area || 'main',
        config: {
          fields: {}, // 清空字段数据，只保留配置
          styles: comp.config.styles || {},
          layout: comp.config.layout || {}
        }
      })),
      // 主题配置
      theme: currentTemplate?.theme || defaultTheme,
      // TODO: 生成预览图
      thumbnail: ''
    }
  }

  // 保存模板
  const saveTemplate = async (layoutData, currentTemplate, formData) => {
    const templateData = prepareTemplateData(layoutData, currentTemplate, formData)
    console.log('保存的模板数据:', templateData)
    return await templateApi.createTemplate(templateData)
  }

  // 获取模板列表
  const getTemplates = async () => {
    return await templateApi.getTemplates()
  }

  // 获取模板详情
  const getTemplateDetail = async (id) => {
    return await templateApi.getTemplateDetail(id)
  }

  return {
    saveTemplate,
    getTemplates,
    getTemplateDetail,
    prepareTemplateData
  }
} 