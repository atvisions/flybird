import * as membership from './membership'
import service from '@/utils/request'

export {
  membership
}

export const templateApi = {
  // 获取模板列表
  getList(params) {
    return service.get('/api/v1/template-editor/templates/', { params })
  },

  // 创建模板
  create(data) {
    return service.post('/api/v1/template-editor/templates/', data)
  },

  // 更新模板
  update(id, data) {
    return service.put(`/api/v1/template-editor/templates/${id}/`, data)
  },

  // 获取模板详情
  getDetail(id) {
    return service.get(`/api/v1/template-editor/templates/${id}/`)
  },

  // 添加画布页面
  addPage(id) {
    return service.post(`/api/v1/template-editor/templates/${id}/pages/`)
  },

  // 更新画布页面
  updatePage(id, data) {
    return service.put(`/api/v1/template-editor/templates/${id}/pages/`, data)
  },

  // 删除画布页面
  deletePage(id, pageIndex) {
    return service.delete(`/api/v1/template-editor/templates/${id}/pages/${pageIndex}/`)
  }
} 