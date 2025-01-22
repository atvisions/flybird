import request from '@/utils/request'

// 分类相关接口
export const categoryApi = {
  // 获取分类列表
  getList() {
    return request({
      url: '/api/v1/template-editor/categories/',
      method: 'get'
    }).then(response => {
      // 处理分页响应格式
      if (response?.data?.results && Array.isArray(response.data.results)) {
        return response.data.results
      } else if (response?.results && Array.isArray(response.results)) {
        return response.results
      } else if (Array.isArray(response)) {
        return response
      }
      return []
    })
  }
}

// 模板相关接口
export const templateApi = {
  // 获取模板列表
  getList(params) {
    return request({
      url: '/api/v1/template-editor/templates/',
      method: 'get',
      params
    })
  },

  // 创建模板
  create(data) {
    // 确保数据格式正确
    const formData = {
      name: data.name,
      description: data.description || '',
      category: data.category,
      keywords: Array.isArray(data.keywords) ? data.keywords : [],
      is_public: Boolean(data.is_public),
      pages: data.pages.map(page => ({
        page_index: Number(page.page_index),
        page_data: {
          elements: Array.isArray(page.page_data.elements) ? page.page_data.elements : [],
          config: {
            width: Number(page.page_data.config.width) || 794,
            height: Number(page.page_data.config.height) || 1123,
            showGuideLine: Boolean(page.page_data.config.showGuideLine)
          }
        }
      }))
    }

    console.log('发送到服务器的数据:', JSON.stringify(formData, null, 2))

    return request({
      url: '/api/v1/template-editor/templates/',
      method: 'post',
      data: formData,
      headers: {
        'Content-Type': 'application/json'
      }
    }).catch(error => {
      console.error('API 错误详情:', {
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
        message: error.message,
        requestData: formData
      })

      // 尝试解析错误响应
      const errorResponse = error.response?.data
      if (errorResponse) {
        console.log('服务器返回的错误信息:', errorResponse)
        if (typeof errorResponse === 'object') {
          const errorMessage = Object.entries(errorResponse)
            .map(([key, value]) => `${key}: ${value}`)
            .join('\n')
          error.message = errorMessage
        } else if (typeof errorResponse === 'string') {
          error.message = errorResponse
        }
      }
      throw error
    })
  },

  // 更新模板
  update(id, data) {
    return request({
      url: `/api/v1/template-editor/templates/${id}/`,
      method: 'put',
      data
    })
  },

  // 获取模板详情
  getDetail(id) {
    return request({
      url: `/api/v1/template-editor/templates/${id}/`,
      method: 'get'
    })
  },

  // 更新页面数据
  updatePage(id, data) {
    return request({
      url: `/api/v1/template-editor/templates/${id}/pages/`,
      method: 'put',
      data
    })
  },

  // 添加新页面
  addPage(id) {
    return request({
      url: `/api/v1/template-editor/templates/${id}/pages/`,
      method: 'post'
    })
  },

  // 删除页面
  deletePage(id, pageIndex) {
    return request({
      url: `/api/v1/template-editor/templates/${id}/pages/`,
      method: 'delete',
      data: { page_index: pageIndex }
    })
  }
} 