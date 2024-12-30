import request from '@/utils/request'

// 辅助函数：格式化薪资
const formatSalary = (min, max) => {
  if (!min && !max) return ''
  if (!max) return `${min}K以上`
  if (!min) return `${max}K以下`
  return `${min}K-${max}K`
}

// 辅助函数：格式化城市
const formatCity = (city) => {
  if (!city || !city.length) return ''
  return city.map(c => c.label || c).join('-')
}

export const profile = {
  // 获取基本信息
  getBasicInfo: () => {
    return request({
      url: '/api/v1/users/profile/basic/',
      method: 'get'
    })
  },

  // 获取完整度评分
  getCompleteness: () => {
    return request({
      url: '/api/v1/users/profile/completeness/',
      method: 'get'
    })
  },

  // 更新基本信息
  updateBasicInfo: (data) => {
    // 确保数据格式正确
    const cleanData = {
      name: data.name?.trim(),
      gender: data.gender,
      birth_date: data.birth_date,
      phone: data.phone?.trim(),
      email: data.email?.trim(),
      location: data.location?.trim(),
      personal_summary: data.personal_summary?.trim()
    }

    return request({
      url: '/api/v1/users/profile/basic/',
      method: 'post',  // 确保使用 POST 方法
      data: cleanData
    })
  },

  // 获取详细资料
  getProfile: () => {
    return request({
      url: '/api/v1/users/profile/basic/',
      method: 'get'
    })
  },

  // 更新详细资料
  updateProfile: (data) => {
    return request({
      url: '/api/v1/users/profile/basic/',
      method: 'post',
      data
    })
  },

  // 上传头像
  uploadAvatar: (file) => {
    return new Promise((resolve, reject) => {
      const formData = new FormData()
      formData.append('avatar', file)
      
      const xhr = new XMLHttpRequest()
      xhr.open('POST', `${process.env.VUE_APP_API_URL}/api/v1/users/profile/avatar/upload/`)
      
      const token = localStorage.getItem('access_token')
      if (token) {
        xhr.setRequestHeader('Authorization', `Bearer ${token}`)
      }
      
      xhr.onload = () => {
        if (xhr.status === 200) {
          try {
            const response = JSON.parse(xhr.responseText)
            resolve({ data: response })
          } catch (error) {
            reject(new Error('解析响应失败'))
          }
        } else {
          reject({
            response: {
              data: JSON.parse(xhr.responseText)
            }
          })
        }
      }
      
      xhr.onerror = () => {
        reject(new Error('网络错误'))
      }
      
      xhr.upload.onprogress = (event) => {
        // 移除进度日志
      }
      
      xhr.send(formData)
    })
  },

  // 获取优化预览
  getOptimizationPreview: () => {
    return request({
      url: '/api/v1/users/profile/content-quality/',
      method: 'get',
      timeout: 120000  // 设置2分钟超时
    })
  },

  // 确认优化
  confirmOptimization: (optimizationId) => {
    return request({
      url: '/api/v1/users/profile/content-quality/confirm/',
      method: 'post',
      data: {
        optimization_id: optimizationId
      }
    })
  },

  // 获取优化次数
  getOptimizationCount: () => {
    return request({
      url: '/api/v1/users/profile/content-quality/count/',
      method: 'get'
    })
  },

  // 获取求职意向
  getJobIntention: () => {
    return request({
      url: '/api/v1/users/profile/job-intention/',
      method: 'get'
    }).catch(error => {
      // 如果是因为用户没有求职意向记录，返回空数据
      if (error.response?.status === 500 && 
          error.response?.data?.message === 'User has no job_intention.') {
        return {
          data: {
            code: 200,
            data: null
          }
        }
      }
      throw error
    })
  },

  // 更新求职意向
  updateJobIntention: (data) => {
    const statusMap = {
      'open': 'unemployed_looking',
      'closed': 'employed_not_looking'
    }
    
    const cleanData = {
      job_type: data.job_type || '',
      expected_salary: data.expected_salary || '',
      expected_city: data.expected_city || '',
      job_status: statusMap[data.job_status] || data.job_status || 'employed_not_looking',
      industries: data.industries || ''
    }

    return request({
      url: '/api/v1/users/profile/job-intention/',
      method: 'put',
      data: cleanData
    })
  },

  // 工作经历相关接口
  workExperience: {
    // 添加工作经历
    add(data) {
      const cleanData = {
        company: data.company?.trim() || '',
        position: data.position?.trim() || '',
        department: data.department?.trim() || '',
        start_date: data.start_date || '',
        end_date: data.is_current ? null : (data.end_date || ''),
        is_current: Boolean(data.is_current),
        description: data.description?.trim() || '',
        achievements: data.achievements?.trim() || '',
        technologies: data.technologies?.trim() || ''
      }

      return request({
        url: '/api/v1/users/profile/work-experiences/',
        method: 'post',
        data: cleanData
      })
    },

    // 更新工作经历
    update(id, data) {
      const cleanData = {
        company: data.company?.trim() || '',
        position: data.position?.trim() || '',
        department: data.department?.trim() || '',
        start_date: data.start_date || null,
        end_date: data.is_current ? null : data.end_date,
        is_current: Boolean(data.is_current),
        description: data.description?.trim() || '',
        achievements: data.achievements?.trim() || '',
        technologies: data.technologies?.trim() || ''
      }

      // 验证必填字段
      if (!cleanData.company) {
        return Promise.reject(new Error('请输入公司名称'))
      }

      if (!cleanData.description || cleanData.description.length < 50) {
        return Promise.reject(new Error('工作描述至少需要50个字符'))
      }

      if (!cleanData.start_date) {
        return Promise.reject(new Error('请选择开始日期'))
      }

      if (!cleanData.is_current && !cleanData.end_date) {
        return Promise.reject(new Error('请选择结束日期或勾选"至今"'))
      }

      return request({
        url: `/api/v1/users/profile/work-experiences/${id}/`,
        method: 'put',
        data: cleanData
      }).catch(error => {
        if (error.response?.data?.errors) {
          const errors = error.response.data.errors
          const firstError = Object.values(errors)[0]
          throw new Error(Array.isArray(firstError) ? firstError[0] : firstError)
        }
        throw error
      })
    },

    // 删除工作经历
    delete(id) {
      return request({
        url: `/api/v1/users/profile/work-experiences/${id}/`,
        method: 'delete'
      })
    },

    // 获取工作经历列表
    list() {
      return request({
        url: '/api/v1/users/profile/work-experiences/',
        method: 'get'
      })
    }
  },

  // 获取完整档案
  getComplete: () => {
    return request({
      url: '/api/v1/users/profile/complete/',
      method: 'get'
    })
  }
}

// 更新布局配置
export function updateLayout(data) {
  return request({
    url: '/api/v1/users/profile/layout/',
    method: 'put',
    data
  })
} 