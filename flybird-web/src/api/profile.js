import request from '@/utils/request'

// 定义 profile 对象
const profile = {
  // 基本信息相关
  getBasicInfo: () => {
    return request.get('/api/v1/users/profile/basic/')
  },

  updateBasicInfo: (data) => {
    return request({
      url: '/api/v1/users/profile/basic/',
      method: 'post',
      data
    })
  },

  // 上传头像
  uploadAvatar(formData) {
    return request({
      url: '/api/v1/users/profile/avatar/upload/',
      method: 'post',
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 完整度相关
  getCompleteness: () => {
    return request({
      url: '/api/v1/users/profile/completeness/',
      method: 'get'
    })
  },

  // 工作经历相关
  workExperience: {
    add(data) {
      return request({
        url: '/api/v1/users/profile/work-experiences/',
        method: 'post',
        data
      })
    },

    update(id, data) {
      return request({
        url: `/api/v1/users/profile/work-experiences/${id}/`,
        method: 'put',
        data
      })
    },

    delete(id) {
      return request({
        url: `/api/v1/users/profile/work-experiences/${id}/`,
        method: 'delete'
      })
    },

    get() {
      return request.get('/api/v1/users/profile/work-experiences/')
    }
  },

  // 求职意向相关
  jobIntention: {
    get() {
      return request({
        url: '/api/v1/users/profile/job-intention/',
        method: 'get'
      })
    },

    update(data) {
      return request({
        url: '/api/v1/users/profile/job-intention/',
        method: 'put',
        data
      })
    }
  },

  // 简历优化相关
  optimization: {
    getPreview: () => {
      return request.get('/api/v1/users/profile/content-quality/')
    },

    confirm: (optimizationId) => {
      return request.post('/api/v1/users/profile/content-quality/confirm/', {
        optimization_id: optimizationId
      })
    },

    getCount: () => {
      return request.get('/api/v1/users/profile/content-quality/count/')
    }
  },

  // 布局配置
  layout: {
    update: (data) => {
      return request.put('/api/v1/users/profile/layout/', data)
    }
  }
}

// 导出 profile 对象
export default profile 