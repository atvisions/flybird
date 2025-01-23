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
      console.log('开始创建模板，数据:', data)
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

      console.log('准备发送的表单数据:', {
        name: data.name,
        category: data.category,
        description: data.description,
        is_public: data.is_public,
        keywords: data.keywords,
        status: data.status,
        pages: data.pages
      })

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
      console.log('开始更新模板，ID:', id)
      console.log('接收到的原始数据:', JSON.stringify(data, null, 2))
      
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
      
      console.log('标准化后的数据:', JSON.stringify(normalizedData, null, 2))
      
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
        console.log('添加页面数据:', JSON.stringify(normalizedData.pages, null, 2))
        formData.append('pages', JSON.stringify(normalizedData.pages))
      } else {
        console.warn('页面数据不存在或格式不正确:', normalizedData)
        throw new Error('页面数据不存在或格式不正确')
      }

      // 打印 FormData 内容
      for (let [key, value] of formData.entries()) {
        console.log('FormData 字段:', key, '值类型:', typeof value, '值:', value)
      }

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
      console.error('更新模板失败:', error)
      if (error.response) {
        console.error('错误响应:', error.response.data)
      }
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