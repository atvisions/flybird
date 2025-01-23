import request from '@/utils/request'

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
  async create(data) {
    try {
      console.log('开始创建模板，数据:', data)
      // 构造API期望的数据结构
      const apiData = {
        name: data.name,
        category: data.category,
        description: data.description || '',
        is_public: data.is_public || false,
        is_pro: data.is_pro || false,
        content: {
          pages: data.content.pages.map(page => ({
            page_data: {
              elements: page.page_data.elements.map(element => ({
                type: element.type || 'text',
                position: element.position || { x: 0, y: 0 },
                style: element.style || {},
                content: element.content || '',
                props: element.props || {}
              })),
              config: {
                width: page.page_data.config?.width || 794,
                height: page.page_data.config?.height || 1123,
                backgroundColor: page.page_data.config?.backgroundColor || '#ffffff',
                showGrid: page.page_data.config?.showGrid || false,
                showGuideLine: page.page_data.config?.showGuideLine || true,
                scale: page.page_data.config?.scale || 1
              }
            }
          }))
        }
      }

      const formData = new FormData()
      
      // 添加基本字段
      formData.append('name', apiData.name)
      formData.append('category', apiData.category)
      formData.append('description', apiData.description)
      formData.append('is_public', apiData.is_public)
      formData.append('is_pro', apiData.is_pro)
      
      // 添加缩略图
      if (data.thumbnail) {
        formData.append('thumbnail', data.thumbnail)
      }
      
      // 添加内容数据
      formData.append('content', JSON.stringify(apiData.content))

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
  async update(id, data) {
    try {
      console.log('开始更新模板，ID:', id, '数据:', data)
      // 构造API期望的数据结构
      const apiData = {
        name: data.name,
        category: data.category,
        description: data.description || '',
        is_public: data.is_public,
        is_pro: data.is_pro,
        content: {
          pages: data.content.pages.map(page => ({
            page_data: {
              elements: page.page_data.elements.map(element => ({
                type: element.type || 'text',
                position: element.position || { x: 0, y: 0 },
                style: element.style || {},
                content: element.content || '',
                props: element.props || {}
              })),
              config: {
                width: page.page_data.config?.width || 794,
                height: page.page_data.config?.height || 1123,
                backgroundColor: page.page_data.config?.backgroundColor || '#ffffff',
                showGrid: page.page_data.config?.showGrid || false,
                showGuideLine: page.page_data.config?.showGuideLine || true,
                scale: page.page_data.config?.scale || 1
              }
            }
          }))
        }
      }

      const formData = new FormData()
      
      // 添加基本字段
      if (apiData.name) formData.append('name', apiData.name)
      if (apiData.category) formData.append('category', apiData.category)
      if (apiData.description) formData.append('description', apiData.description)
      if (typeof apiData.is_public === 'boolean') formData.append('is_public', apiData.is_public)
      if (typeof apiData.is_pro === 'boolean') formData.append('is_pro', apiData.is_pro)
      
      // 添加缩略图
      if (data.thumbnail) {
        formData.append('thumbnail', data.thumbnail)
      }
      
      // 添加内容数据
      formData.append('content', JSON.stringify(apiData.content))

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