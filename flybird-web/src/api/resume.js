import request from '@/utils/request'

const resume = {
  // 获取简历模板列表
  getTemplates() {
    return request.get('/api/v1/resume/templates/')
  },

  // 获取简历模板详情
  getTemplateDetail(id) {
    return request.get(`/api/v1/resume/templates/${id}/`)
  },

  // 获取组件分类列表
  getComponentCategories() {
    return request.get('/api/v1/resume/component-categories/main_categories/')
  },

  // 获取组件列表
  getComponents(categoryId) {
    return request.get(`/api/v1/resume/components/?category=${categoryId}`)
  },

  // 创建简历
  createResume(data) {
    return request({
      url: '/api/v1/resume/resumes/',
      method: 'post',
      data
    })
  },

  // 获取简历详情
  getResumeDetail(id) {
    return request.get(`/api/v1/resume/resumes/${id}/`)
  },

  // 更新简历
  updateResume(id, data) {
    return request({
      url: `/api/v1/resume/resumes/${id}/`,
      method: 'put',
      data
    })
  },

  // 删除简历
  deleteResume(id) {
    return request({
      url: `/api/v1/resume/resumes/${id}/`,
      method: 'delete'
    })
  }
}

export default resume 