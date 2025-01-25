import { request } from '@/utils/request';

export const templateApi = {
  // 获取模板列表
  async getList(params) {
    return request({
      url: '/api/v1/template-editor/templates/',
      method: 'get',
      params
    });
  },

  // 获取模板详情
  async getDetail(id) {
    return request({
      url: `/api/v1/template-editor/templates/${id}/`,
      method: 'get'
    });
  },

  // 创建模板
  async create(data) {
    try {
      const formData = new FormData()
      
      // 添加基本字段
      if (data.name) formData.append('name', data.name)
      if (data.category) formData.append('category', data.category)
      if (data.description) formData.append('description', data.description)
      if (typeof data.is_public === 'boolean') formData.append('is_public', data.is_public)
      if (Array.isArray(data.keywords)) formData.append('keywords', JSON.stringify(data.keywords))
      if (typeof data.status === 'number') formData.append('status', data.status)
      
      // 添加页面数据
      if (data.pages) {
        formData.append('pages', JSON.stringify(data.pages))
      }

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
      throw error
    }
  },

  // 更新模板
  async update(id, data) {
    try {
      // 确保数据是普通对象
      const normalizedData = JSON.parse(JSON.stringify({
        name: data.name,
        category: data.category,
        description: data.description,
        is_public: data.is_public,
        keywords: data.keywords,
        status: data.status,
        pages: data.pages
      }))
      
      const formData = new FormData()
      
      // 添加基本字段
      formData.append('name', normalizedData.name || '')
      formData.append('category', normalizedData.category || '')
      formData.append('description', normalizedData.description || '')
      formData.append('is_public', normalizedData.is_public ?? false)
      formData.append('keywords', JSON.stringify(normalizedData.keywords || []))
      formData.append('status', normalizedData.status ?? 0)
      
      // 添加页面数据
      if (Array.isArray(normalizedData.pages)) {
        formData.append('pages', JSON.stringify(normalizedData.pages))
      } else {
        throw new Error('页面数据不存在或格式不正确')
      }

      const response = await request({
        url: `/api/v1/template-editor/templates/${id}/`,
        method: 'put',
        data: formData,
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return response
    } catch (error) {
      throw error
    }
  },

  // 删除模板
  async delete(id) {
    return request({
      url: `/api/v1/template-editor/templates/${id}/`,
      method: 'delete'
    });
  }
}; 