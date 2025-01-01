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
  },

  // 教育经历相关
  education: {
    get() {
      return request.get('/api/v1/users/profile/educations/')
    },

    add(data) {
      return request({
        url: '/api/v1/users/profile/educations/',
        method: 'post',
        data
      })
    },

    update(id, data) {
      return request({
        url: `/api/v1/users/profile/educations/${id}/`,
        method: 'put',
        data
      })
    },

    delete(id) {
      return request({
        url: `/api/v1/users/profile/educations/${id}/`,
        method: 'delete'
      })
    }
  },

  // 项目经历
  project: {
    get() {
      return request({
        url: '/api/v1/users/profile/projects/',
        method: 'get'
      })
    },
    add(data) {
      return request({
        url: '/api/v1/users/profile/projects/',
        method: 'post',
        data
      })
    },
    update(id, data) {
      return request({
        url: `/api/v1/users/profile/projects/${id}/`,
        method: 'put',
        data
      })
    },
    delete(id) {
      return request({
        url: `/api/v1/users/profile/projects/${id}/`,
        method: 'delete'
      })
    }
  },

  // 专业技能
  skill: {
    get: () => request({
      url: '/api/v1/users/profile/skills/',
      method: 'get'
    }),
    add: (data) => request({
      url: '/api/v1/users/profile/skills/',
      method: 'post',
      data
    }),
    update: (id, data) => request({
      url: `/api/v1/users/profile/skills/${id}/`,
      method: 'put',
      data
    }),
    delete: (id) => request({
      url: `/api/v1/users/profile/skills/${id}/`,
      method: 'delete'
    })
  },

  // 证书奖项
  certificate: {
    get() {
      return request({
        url: '/api/v1/users/profile/certificates/',
        method: 'get'
      })
    },
    add(data) {
      return request({
        url: '/api/v1/users/profile/certificates/',
        method: 'post',
        data
      })
    },
    update(id, data) {
      return request({
        url: `/api/v1/users/profile/certificates/${id}/`,
        method: 'put',
        data
      })
    },
    delete(id) {
      return request({
        url: `/api/v1/users/profile/certificates/${id}/`,
        method: 'delete'
      })
    }
  },

  // 语言能力
  language: {
    get() {
      return request.get('/api/v1/users/profile/languages/')
    },
    add(data) {
      console.log('【Language API】准备提交数据:', data)
      return request.post('/api/v1/users/profile/languages/', {
        name: data.name,
        proficiency: data.proficiency,
        certification: data.certification || '',
        score: data.score || ''
      })
    },
    update(id, data) {
      return request.put(`/api/v1/users/profile/languages/${id}/`, {
        name: data.name,
        proficiency: data.proficiency,
        certification: data.certification || '',
        score: data.score || ''
      })
    },
    delete(id) {
      return request.delete(`/api/v1/users/profile/languages/${id}/`)
    }
  },

  // 作品展示
  portfolio: {
    get() {
      return request.get('/api/v1/users/profile/portfolios/')
    },
    add(data) {
      return request.post('/api/v1/users/profile/portfolios/', data)
    },
    update(id, data) {
      return request.put(`/api/v1/users/profile/portfolios/${id}/`, data)
    },
    delete(id) {
      return request.delete(`/api/v1/users/profile/portfolios/${id}/`)
    }
  },

  // 社交主页
  social_link: {
    get() {
      return request.get('/api/v1/users/profile/social-links/')
    },
    add(data) {
      return request.post('/api/v1/users/profile/social-links/', data)
    },
    update(id, data) {
      return request.put(`/api/v1/users/profile/social-links/${id}/`, data)
    },
    delete(id) {
      return request.delete(`/api/v1/users/profile/social-links/${id}/`)
    }
  },

  // 求职意向相关方法
  jobIntention: {
    // 更新求职意向
    update: (data) => {
      return request({
        url: '/api/v1/users/profile/job-intention/',
        method: 'put',
        data
      })
    },

    get() {
      return request({
        url: '/api/v1/users/profile/job-intention/',
        method: 'get'
      })
    }
  },
}

// 导出 profile 对象
export default profile 