import request from '@/utils/request'
import html2canvas from 'html2canvas'

// 生成缩略图的辅助函数
async function generateThumbnail(canvasElement) {
  try {
    // A4 纸的标准尺寸 (794:1123)
    const A4_WIDTH = 794
    const A4_HEIGHT = 1123
    
    // 获取原始画布的尺寸（这里的尺寸应该已经是 A4 比例）
    const originalWidth = canvasElement.offsetWidth
    const originalHeight = canvasElement.offsetHeight

    // 配置 html2canvas，使用 1 倍缩放以保持原始清晰度
    const canvas = await html2canvas(canvasElement, {
      width: originalWidth,
      height: originalHeight,
      backgroundColor: '#ffffff',
      logging: false,
      useCORS: true,
      allowTaint: true,
      scale: 1, // 使用1倍缩放，保持原始清晰度
      onclone: (clonedDoc) => {
        // 等待字体加载完成
        const promises = [];
        clonedDoc.fonts.forEach((font) => {
          if (!font.loaded) {
            promises.push(font.load());
          }
        });

        // 在克隆的文档中找到目标元素
        const clonedElement = clonedDoc.querySelector('.canvas-wrapper');
        if (clonedElement) {
          // 确保只显示画布内容
          clonedElement.style.overflow = 'hidden';
          clonedElement.style.backgroundColor = '#ffffff';
          // 移除所有工具栏和辅助元素
          const toolbars = clonedElement.querySelectorAll('.toolbar, .ruler, .guide-line');
          toolbars.forEach(toolbar => toolbar.remove());
        }

        return Promise.all(promises);
      }
    })

    // 创建一个新的 canvas，使用 A4 标准尺寸
    const scaledCanvas = document.createElement('canvas')
    scaledCanvas.width = A4_WIDTH
    scaledCanvas.height = A4_HEIGHT
    const ctx = scaledCanvas.getContext('2d')

    // 设置白色背景
    ctx.fillStyle = '#ffffff'
    ctx.fillRect(0, 0, A4_WIDTH, A4_HEIGHT)

    // 直接将原始画布缩放到 A4 尺寸
    ctx.drawImage(canvas, 0, 0, A4_WIDTH, A4_HEIGHT)

    // 将 canvas 转换为 Blob，使用较低的压缩质量来控制文件大小
    return new Promise((resolve) => {
      scaledCanvas.toBlob((blob) => {
        resolve(blob)
      }, 'image/jpeg', 0.6) // 使用 JPEG 格式，60% 质量
    })
  } catch (error) {
    console.error('生成缩略图失败:', error)
    throw error
  }
}

// 导出统一的API对象
export const templateApi = {
  // 获取模板分类
  async getCategories() {
    try {
      const response = await request({
        url: '/api/v1/template-editor/categories/',
        method: 'get'
      })
      return response
    } catch (error) {
      console.error('获取模板分类失败:', error.response || error)
      throw error
    }
  },

  // 获取模板列表
  async getTemplates(params = {}) {
    try {
      const response = await request({
        url: '/api/v1/template-editor/templates/',
        method: 'get',
        params
      })
      return response
    } catch (error) {
      console.error('获取模板列表失败:', error.response || error)
      throw error
    }
  },

  // 获取模板详情
  async getDetail(id) {
    try {
      const response = await request({
        url: `/api/v1/template-editor/templates/${id}/`,
        method: 'get'
      })
      return response
    } catch (error) {
      console.error('获取模板详情失败:', error.response || error)
      throw error
    }
  },

  // 创建模板
  async create(data, canvasElement) {
    try {
      // 生成缩略图
      const thumbnail = await generateThumbnail(canvasElement)
      
      // 构造API期望的数据结构
      const apiData = {
        name: data.name,
        category: data.category,
        description: data.description || '',
        is_public: data.is_public || false,
        is_pro: data.is_pro || false,
        status: data.status,
        keywords: data.keywords,
        pages: data.pages
      }

      const formData = new FormData()
      
      // 添加基本字段
      formData.append('name', apiData.name)
      formData.append('category', apiData.category)
      formData.append('description', apiData.description)
      formData.append('is_public', apiData.is_public)
      formData.append('is_pro', apiData.is_pro)
      if (typeof apiData.status === 'number') {
        formData.append('status', apiData.status)
      }
      
      // 添加关键词
      if (Array.isArray(apiData.keywords)) {
        formData.append('keywords', JSON.stringify(apiData.keywords))
      }
      
      // 添加缩略图
      formData.append('thumbnail', thumbnail, 'thumbnail.jpg')
      
      // 添加页面数据
      formData.append('pages', JSON.stringify(apiData.pages))

      const response = await request({
        url: '/api/v1/template-editor/templates/',
        method: 'post',
        data: formData,
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return response
    } catch (error) {
      console.error('创建模板失败:', error.response || error)
      throw error
    }
  },

  // 更新模板
  async update(id, data, canvasElement) {
    try {     
      // 生成缩略图
      const thumbnail = await generateThumbnail(canvasElement)
      
      // 构造API期望的数据结构
      const apiData = {
        name: data.name,
        category: data.category,
        description: data.description || '',
        is_public: data.is_public,
        is_pro: data.is_pro,
        status: data.status,
        keywords: data.keywords,
        pages: data.pages
      }

      const formData = new FormData()
      
      // 添加基本字段
      if (apiData.name) formData.append('name', apiData.name)
      if (apiData.category) formData.append('category', apiData.category)
      if (apiData.description) formData.append('description', apiData.description)
      if (typeof apiData.is_public === 'boolean') formData.append('is_public', apiData.is_public)
      if (typeof apiData.is_pro === 'boolean') formData.append('is_pro', apiData.is_pro)
      if (typeof apiData.status === 'number') formData.append('status', apiData.status)
      
      // 添加关键词
      if (Array.isArray(apiData.keywords)) {
        formData.append('keywords', JSON.stringify(apiData.keywords))
      }
      
      // 添加缩略图
      formData.append('thumbnail', thumbnail, 'thumbnail.jpg')
      
      // 添加页面数据
      formData.append('pages', JSON.stringify(apiData.pages))

      const response = await request({
        url: `/api/v1/template-editor/templates/${id}/`,
        method: 'put',
        data: formData,
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      console.log('更新模板成功:', response)
      return response
    } catch (error) {
      console.error('更新模板失败:', error.response || error)
      throw error
    }
  },

  // 删除模板
  async delete(id) {
    try {
      console.log('开始删除模板，ID:', id)
      const response = await request({
        url: `/api/v1/template-editor/templates/${id}/`,
        method: 'delete'
      })
      return response
    } catch (error) {
      console.error('删除模板失败:', error.response || error)
      throw error
    }
  },

  // 点赞/取消点赞模板
  async like(id) {
    try {
      const response = await request({
        url: `/api/v1/template-editor/templates/${id}/like/`,
        method: 'post'
      })
      return response
    } catch (error) {
      console.error('点赞/取消点赞失败:', error.response || error)
      throw error
    }
  }
} 