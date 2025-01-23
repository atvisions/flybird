import request from '@/utils/request'
import html2canvas from 'html2canvas'

// 生成缩略图的辅助函数
async function generateThumbnail(canvasElement) {
  try {
    // A4 纸的宽高比 1:1.414 (794:1123)
    const A4_RATIO = 1.414
    
    // 获取原始画布的尺寸
    const originalWidth = canvasElement.offsetWidth
    const originalHeight = canvasElement.offsetHeight

    // 设置缩略图的宽度
    const THUMB_WIDTH = 300
    // 根据 A4 比例计算高度
    const THUMB_HEIGHT = Math.round(THUMB_WIDTH * A4_RATIO)

    // 计算缩放比例
    const scaleX = THUMB_WIDTH / originalWidth
    const scaleY = THUMB_HEIGHT / originalHeight
    const scale = Math.min(scaleX, scaleY)

    // 配置 html2canvas
    const canvas = await html2canvas(canvasElement, {
      width: originalWidth,
      height: originalHeight,
      backgroundColor: '#ffffff',
      logging: false,
      useCORS: true,
      allowTaint: true,
      scale: 2, // 使用2倍缩放以获得更清晰的图像
      // 确保正确渲染字体
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

    // 创建一个新的 canvas 用于缩放
    const scaledCanvas = document.createElement('canvas')
    scaledCanvas.width = THUMB_WIDTH
    scaledCanvas.height = THUMB_HEIGHT
    const ctx = scaledCanvas.getContext('2d')

    // 设置白色背景
    ctx.fillStyle = '#ffffff'
    ctx.fillRect(0, 0, THUMB_WIDTH, THUMB_HEIGHT)

    // 在中心绘制并缩放原始画布
    const scaledWidth = originalWidth * scale
    const scaledHeight = originalHeight * scale
    const x = (THUMB_WIDTH - scaledWidth) / 2
    const y = (THUMB_HEIGHT - scaledHeight) / 2
    ctx.drawImage(canvas, x, y, scaledWidth, scaledHeight)

    // 将 canvas 转换为 Blob
    return new Promise((resolve) => {
      scaledCanvas.toBlob((blob) => {
        resolve(blob)
      }, 'image/jpeg', 0.9) // 使用 JPEG 格式，90% 质量
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
      console.log('开始请求模板分类')
      const response = await request({
        url: '/api/v1/template-editor/categories/',
        method: 'get'
      })
      console.log('获取模板分类成功:', response)
      return response
    } catch (error) {
      console.error('获取模板分类失败:', error.response || error)
      throw error
    }
  },

  // 获取模板列表
  async getTemplates(params = {}) {
    try {
      console.log('开始请求模板列表，参数:', params)
      const response = await request({
        url: '/api/v1/template-editor/templates/',
        method: 'get',
        params
      })
      console.log('获取模板列表成功:', response)
      return response
    } catch (error) {
      console.error('获取模板列表失败:', error.response || error)
      throw error
    }
  },

  // 获取模板详情
  async getDetail(id) {
    try {
      console.log('开始请求模板详情，ID:', id)
      const response = await request({
        url: `/api/v1/template-editor/templates/${id}/`,
        method: 'get'
      })
      console.log('获取模板详情成功:', response)
      return response
    } catch (error) {
      console.error('获取模板详情失败:', error.response || error)
      throw error
    }
  },

  // 创建模板
  async create(data, canvasElement) {
    try {
      console.log('开始创建模板，数据:', data)
      
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
      console.log('创建模板成功:', response)
      return response
    } catch (error) {
      console.error('创建模板失败:', error.response || error)
      throw error
    }
  },

  // 更新模板
  async update(id, data, canvasElement) {
    try {
      console.log('开始更新模板，ID:', id, '数据:', data)
      
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
      console.log('删除模板成功:', response)
      return response
    } catch (error) {
      console.error('删除模板失败:', error.response || error)
      throw error
    }
  },

  // 点赞/取消点赞模板
  async like(id) {
    try {
      console.log('开始点赞/取消点赞模板，ID:', id)
      const response = await request({
        url: `/api/v1/template-editor/templates/${id}/like/`,
        method: 'post'
      })
      console.log('点赞/取消点赞成功:', response)
      return response
    } catch (error) {
      console.error('点赞/取消点赞失败:', error.response || error)
      throw error
    }
  }
} 