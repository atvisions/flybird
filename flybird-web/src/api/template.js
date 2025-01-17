import request from '@/utils/request'

// 获取模板分类列表
export function getCategories() {
  return request({
    url: '/api/v1/resume/template-categories/',
    method: 'get'
  })
}

// 保存模板
export function saveTemplate(data) {
  const formData = new FormData()
  
  // 添加基本字段
  formData.append('name', data.name)
  formData.append('category', data.category)
  formData.append('description', data.description)
  formData.append('is_vip', data.is_vip)
  
  // 添加缩略图
  if (data.thumbnail) {
    formData.append('thumbnail', data.thumbnail)
  }
  
  // 添加画布内容数据
  if (data.components) {
    formData.append('content', JSON.stringify({
      elements: data.components
    }))
  }

  // 打印请求数据
  console.log('请求数据:', {
    name: data.name,
    category: data.category,
    description: data.description,
    is_vip: data.is_vip,
    thumbnail: data.thumbnail,
    content: JSON.parse(formData.get('content') || '{}')
  })

  return request({
    url: '/api/v1/resume/templates/',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }).catch(error => {
    if (error.response?.data) {
      const errors = error.response.data
      const errorMessages = []
      
      // 处理字段错误
      for (const field in errors) {
        if (Array.isArray(errors[field])) {
          errorMessages.push(`${field}: ${errors[field].join(', ')}`)
        }
      }
      
      console.error('服务器响应错误:', errors)
      throw new Error(errorMessages.join('\n') || '保存失败，请检查表单数据')
    }
    throw error
  })
}

/**
 * 获取模板列表
 * @param {Object} params 查询参数
 * @param {number} params.page 页码
 * @param {number} params.page_size 每页数量
 * @param {string} params.ordering 排序方式
 */
export function getTemplates(params = {}) {
  return request({
    url: '/api/v1/resume/templates/',
    method: 'get',
    params
  })
}

// 获取模板详情
export function getTemplateDetail(id) {
  return request({
    url: `/api/v1/resume/templates/${id}/`,
    method: 'get'
  })
}

// 更新模板
export function updateTemplate(id, data) {
  const formData = new FormData()
  
  // 添加基本字段
  if (data.name) formData.append('name', data.name)
  if (data.category) formData.append('category', data.category)
  if (data.description) formData.append('description', data.description)
  if (typeof data.is_vip === 'boolean') formData.append('is_vip', data.is_vip)
  
  // 添加缩略图
  if (data.thumbnail && data.thumbnail.length > 0) {
    formData.append('thumbnail', data.thumbnail[0])
  }
  
  // 添加布局数据
  if (data.layout) {
    formData.append('layout', JSON.stringify(data.layout))
  }
  
  // 添加组件数据
  if (data.components) {
    formData.append('components', JSON.stringify(data.components))
  }
  
  // 添加主题数据
  if (data.theme) {
    formData.append('theme', JSON.stringify(data.theme))
  }

  return request({
    url: `/api/v1/resume/templates/${id}/`,
    method: 'patch',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 删除模板
export function deleteTemplate(id) {
  return request({
    url: `/api/v1/resume/templates/${id}/`,
    method: 'delete'
  })
}

// 提交模板审核
export function submitForReview(id) {
  return request({
    url: `/api/v1/resume/templates/${id}/submit_for_review/`,
    method: 'post'
  })
} 