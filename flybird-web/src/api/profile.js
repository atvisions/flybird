import request from '@/utils/request'

// 档案数据管理
const profile = {
  // 获取完整档案数据
  getData() {
    return request.get('/api/v1/users/profile/data/')
  },

  // 获取简历完整度
  getCompleteness() {
    return request.get('/api/v1/users/profile/completeness/')
  },

  // 更新模块数据
  updateModule(type, data) {
    // 确保技能模块使用正确的类型名
    const moduleType = type === 'skill' ? 'skills' : type
    const id = data.id
    
    if (id) {
      // 编辑现有数据
      return request({
        url: `/api/v1/users/profile/${moduleType}/${id}/`,
        method: 'put',
        data
      })
    } else {
      // 对于 basic_info，使用不同的处理方式，因为它是一对一关系
      if (moduleType === 'basic_info') {
        return request({
          url: `/api/v1/users/profile/${moduleType}/`,
          method: 'put',
          data
        })
      }
      // 其他模块的新增
      return request({
        url: `/api/v1/users/profile/${moduleType}/`,
        method: 'post',
        data
      })
    }
  },

  // 删除模块项目
  deleteModuleItem(type, id) {
    // 处理特殊的模块类型名称
    const moduleTypeMap = {
      'skill': 'skills',
      'certificate': 'certificates',
      // 添加其他需要映射的类型...
    }
    // 确保技能模块使用正确的类型名
    const moduleType = type === 'skill' ? 'skills' : type
    return request({
      url: `/api/v1/users/profile/${moduleType}/${id}/`,
      method: 'delete'
    })
  },

  // 特殊接口保持不变
  uploadAvatar(formData) {
    return request({
      url: '/api/v1/users/profile/avatar/upload/',
      method: 'post',
      headers: { 'Content-Type': 'multipart/form-data' },
      data: formData
    })
  },

  uploadBackground(formData) {
    return request({
      url: '/api/v1/users/profile/background/upload/',
      method: 'post',
      headers: { 'Content-Type': 'multipart/form-data' },
      data: formData
    })
  },

  // 获取布局配置（保留特殊接口）
  getLayout() {
    return request.get('/api/v1/users/profile/layout/')
  },

  // 更新布局配置（保留特殊接口）
  updateLayout(data) {
    return request({
      url: '/api/v1/users/profile/layout/',
      method: 'put',
      data
    })
  },

}

export default profile 