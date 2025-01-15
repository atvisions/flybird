//这里是
import request from '@/utils/request'

// 档案数据管理
const profile = {
  // 获取完整档案数据
  getData() {
    console.log('Calling getData...')
    return request.get('/api/v1/users/profile/data/').then(response => {
      console.log('getData raw response:', response)
      return response
    })
  },

  // 获取档案完整度（仅在档案页面使用）
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

  uploadBackground(formData) {
    return request({
      url: '/api/v1/users/profile/background/upload/',
      method: 'post',
      headers: {
        // 让 axios 自动设置 Content-Type 和 boundary
        'Content-Type': undefined
      },
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

  // 上传头像
  uploadAvatar: async (file) => {
    console.log('Profile API - 开始上传职业头像:', {
      fileName: file.name,
      size: file.size,
      type: file.type
    })
    
    // 验证文件类型
    if (!file.type.startsWith('image/')) {
      throw new Error('请上传图片文件')
    }
    
    const formData = new FormData()
    // 添加前缀以区分职业头像
    const fileName = `profile_${file.name}`
    formData.append('avatar', file, fileName)
    
    try {
      const response = await request({
        url: '/api/v1/users/profile/avatar/upload/',
        method: 'post',
        data: formData,
        headers: {
          'Content-Type': undefined
        }
      })
      
      console.log('Profile API - 职业头像上传响应:', response)
      
      return response
    } catch (error) {
      console.error('职业头像上传失败:', error)
      const errorMessage = error.response?.data?.message || error.message
      console.error('错误详情:', {
        message: errorMessage,
        data: error.response?.data
      })
      throw error
    }
  },

  // 解析简历文件
  parseResume(formData, onProgress) {
    return request({
      url: '/api/v1/users/profile/data/import/',
      method: 'post',
      data: formData,
      timeout: 120000, // 设置120秒超时
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress) {
          const progress = Math.min((progressEvent.loaded / progressEvent.total) * 100, 99)
          onProgress(progress)
        }
      }
    })
  },

  // 导入简历数据
  importResumeData(data) {
    return request({
      url: '/api/v1/users/profile/data/import/',
      method: 'put',
      data
    })
  }
}

export default profile 