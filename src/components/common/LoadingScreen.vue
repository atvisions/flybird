const initialize = async () => {
  try {
    let templateData = null
    let profileData = null
    
    // 获取模板数据
    if (props.templateId) {
      const response = await templateApi.getDetail(props.templateId)
      templateData = response.data
    }
    
    // 如果是使用模式，获取用户档案数据
    if (props.mode === 'use') {
      const response = await loadProfileData()
      
      // 确保从 response 中正确提取 profileData
      if (response && response.data) {
        profileData = response.data
        
        // 存储档案数据用于调试
        localStorage.setItem('debug_profile_data', JSON.stringify(profileData))
        
        // 验证档案数据的完整性
        const debugData = {
          hasBasicInfo: !!profileData.basic_info,
          basicInfoFields: profileData.basic_info ? Object.keys(profileData.basic_info) : [],
          otherFields: Object.keys(profileData),
          mode: props.mode
        }
        localStorage.setItem('debug_data', JSON.stringify(debugData))
      } else {
        throw new Error('档案数据格式不正确')
      }
    }

    // 发出加载完成事件
    const eventData = {
      success: true,
      templateData,
      profileData,
      mode: props.mode
    }
    
    emit('load-complete', eventData)
    
  } catch (error) {
    emit('load-complete', {
      success: false,
      error: error.message || '加载失败'
    })
  }
}

// 加载用户档案数据
const loadProfileData = async () => {
  try {
    const response = await profileApi.default.getData()
    
    if (!response || response.status !== 200) {
      throw new Error('档案数据请求失败')
    }

    // 提取实际的档案数据
    const rawData = response.data

    // 尝试从不同的数据结构中提取档案数据
    let profileData = null
    if (rawData.results && Array.isArray(rawData.results)) {
      profileData = rawData.results[0]
    } else if (rawData.data) {
      profileData = rawData.data
    } else {
      profileData = rawData
    }
    
    // 检查并确保 basic_info 字段存在
    if (!profileData.basic_info) {
      profileData.basic_info = {}
    }

    // 确保所有必要的字段都存在
    const requiredFields = ['basic_info', 'education', 'work_experience', 'skill']
    for (const field of requiredFields) {
      if (!profileData[field]) {
        profileData[field] = field === 'basic_info' ? {} : []
      }
    }

    // 确保 basic_info 中的所有字段都存在
    const basicInfoFields = ['name', 'gender', 'birth_date', 'phone', 'email', 'location', 'personal_summary', 'avatar']
    for (const field of basicInfoFields) {
      if (!profileData.basic_info[field]) {
        profileData.basic_info[field] = ''
      }
    }
    
    // 存储处理后的数据用于调试
    localStorage.setItem('debug_profile_data', JSON.stringify(profileData))
    
    return {
      data: profileData,
      status: 200
    }
  } catch (error) {
    throw new Error('无法获取用户档案数据: ' + error.message)
  }
} 