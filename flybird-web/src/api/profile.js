import request from '@/utils/request'

// 档案数据管理
const profile = {
  // 获取完整档案数据
  getData() {
    console.log('获取完整档案数据')
    return request.get('/api/v1/users/profile/data/')
  },

  // 获取简历完整度
  getCompleteness() {
    console.log('获取简历完整度')
    return request.get('/api/v1/users/profile/completeness/')
  },

  // 更新完整档案数据
  updateData(data) {
    console.log('更新完整档案数据:', data)
    return request({
      url: '/api/v1/users/profile/data/',
      method: 'put',
      data
    })
  },

  // 更新单个模块数据
  updateModule(type, data) {
    console.log('更新模块数据:', { type, data })
    // 如果是基本信息，使用完整档案接口
    if (type === 'basic_info') {
      return request({
        url: '/api/v1/users/profile/basic/',
        method: 'post',
        data: {
          ...data,
          id: data.id
        }
      })
    }
    
    // 其他模块使用独立接口
    const urlMap = {
      work_experience: 'work-experiences',
      education: 'educations',
      project: 'projects',
      skill: 'skills',
      certificate: 'certificates',
      language: 'languages',
      portfolio: 'portfolios',
      social_link: 'social-links',
      job_intention: 'job-intention'
    }
    
    // 需要在 URL 中包含 ID 的模块
    const needIdInUrl = [
      'work_experience', 
      'education', 
      'project', 
      'skill',
      'certificate',
      'language',
      'portfolio'
    ]
    
    // 如果是需要 ID 的模块且有 ID，在 URL 中包含 ID
    if (needIdInUrl.includes(type) && data.id) {
      return request({
        url: `/api/v1/users/profile/${urlMap[type]}/${data.id}/`,
        method: 'put',
        data
      })
    }
    
    return request({
      url: `/api/v1/users/profile/${urlMap[type] || type}/`,
      method: 'put',
      data
    })
  },

  // 添加模块项目
  addModuleItem(type, data) {
    const urlMap = {
      work_experience: 'work-experiences',
      education: 'educations',
      project: 'projects',
      skill: 'skills',
      certificate: 'certificates',
      language: 'languages',
      portfolio: 'portfolios',
      social_link: 'social-links'
    }

    console.log('添加模块项目:', { 
      type, 
      data,
      url: `/api/v1/users/profile/${urlMap[type] || type}/`
    })

    // 根据不同类型处理数据
    let processedData = { ...data }
    if (type === 'skill') {
      // 确保技能数据格式正确，与服务端模型对应
      processedData = {
        name: data.name?.trim() || '',  // 必填，最大长度50
        level: data.level || '初级',    // 使用预定义的选项值
        description: data.description?.trim() || '' // 选填
      }

      // 验证数据
      if (!processedData.name) {
        throw new Error('技能名称不能为空')
      }
      if (processedData.name.length > 50) {
        throw new Error('技能名称不能超过50个字符')
      }
      if (!['初级', '中级', '高级', '专家'].includes(processedData.level)) {
        throw new Error('无效的技能等级')
      }
    }
    
    return request({
      url: `/api/v1/users/profile/${urlMap[type] || type}/`,
      method: 'post',
      data: processedData
    }).catch(error => {
      console.error('添加失败详情:', {
        type,
        data: processedData,
        error: error.response?.data || error
      })
      throw error
    })
  },

  // 删除模块项目
  deleteModuleItem(type, id) {
    console.log('删除模块项目:', { type, id })
    const urlMap = {
      work_experience: 'work-experiences',
      education: 'educations',
      project: 'projects',
      skill: 'skills',
      certificate: 'certificates',
      language: 'languages',
      portfolio: 'portfolios',
      social_link: 'social-links'
    }
    
    const url = `/api/v1/users/profile/${urlMap[type]}/${id}/`
    console.log('Delete request URL:', url)
    
    return request({
      url,
      method: 'delete'
    })
  },

  // 上传头像
  uploadAvatar(formData) {
    console.log('上传头像')
    return request({
      url: '/api/v1/users/profile/avatar/upload/',
      method: 'post',
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      data: formData
    })
  },

  // 获取布局配置
  getLayout() {
    console.log('获取布局配置')
    return request.get('/api/v1/users/profile/layout/')
      .then(response => {
        console.log('布局配置响应:', response.data)
        return response
      })
  },

  // 更新布局配置
  updateLayout(data) {
    console.log('更新布局配置:', data)
    console.log('布局数据结构:', JSON.stringify(data, null, 2))
    return request({
      url: '/api/v1/users/profile/layout/',
      method: 'put',
      data
    })
  }
}

export default profile 