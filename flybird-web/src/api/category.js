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