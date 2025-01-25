const initialize = async () => {
  try {
    // 获取用户信息
    const userId = await loadUserInfo()
    console.log('用户信息加载完成:', userId)

    let templateData = null
    let profileData = null
    
    // 获取模板数据
    if (props.templateId) {
      const response = await templateApi.getDetail(props.templateId)
      console.log('获取到模板数据:', response)
      templateData = response.data
      console.log('处理后的模板数据:', templateData)
    }
    
    // 如果是使用模式，获取用户档案数据
    if (props.mode === 'use') {
      console.log('开始获取用户档案数据...')
      const response = await loadProfileData()
      console.log('获取到用户档案数据:', response)
      
      // 确保从 response 中正确提取 profileData
      if (response && response.data) {
        profileData = response.data
        console.log('提取的档案数据:', profileData)
        
        // 存储档案数据用于调试
        localStorage.setItem('debug_profile_data', JSON.stringify(profileData))
        console.log('已存储档案数据到 localStorage')
        
        // 验证档案数据的完整性
        console.log('档案数据完整性检查:', {
          hasBasicInfo: !!profileData.basic_info,
          basicInfoFields: profileData.basic_info ? Object.keys(profileData.basic_info) : [],
          otherFields: Object.keys(profileData)
        })
      } else {
        console.error('档案数据格式不正确:', response)
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
    
    console.log('发出 load-complete 事件，数据:', eventData)
    emit('load-complete', eventData)
    
  } catch (error) {
    console.error('初始化失败:', error)
    emit('load-complete', {
      success: false,
      error: error.message || '加载失败'
    })
  }
}

// 加载用户档案数据
const loadProfileData = async () => {
  loadingText.value = '正在获取用户档案数据...'
  try {
    console.log('开始获取用户档案数据...')
    const response = await profileApi.default.getData()
    console.log('原始响应数据结构:', {
      status: response.status,
      hasData: !!response.data,
      dataKeys: response.data ? Object.keys(response.data) : []
    })
    
    // 检查响应状态和数据结构
    if (!response || response.status !== 200) {
      console.error('档案数据请求失败:', response)
      throw new Error('档案数据请求失败')
    }

    if (!response.data) {
      console.error('响应中缺少 data 字段')
      throw new Error('响应数据格式不正确')
    }
    
    // 提取实际的档案数据
    const rawData = response.data
    console.log('原始档案数据结构:', {
      hasResults: !!rawData.results,
      resultType: rawData.results ? typeof rawData.results : 'undefined',
      firstResult: rawData.results?.[0]
    })

    // 如果数据在 results 数组中，取第一个结果
    const profileData = rawData.results?.[0] || rawData.data || rawData
    console.log('提取的档案数据结构:', {
      hasBasicInfo: !!profileData.basic_info,
      dataKeys: Object.keys(profileData)
    })
    
    // 检查 basic_info 字段
    if (profileData.basic_info) {
      console.log('basic_info 字段结构:', {
        fields: Object.keys(profileData.basic_info),
        hasName: !!profileData.basic_info.name,
        hasGender: !!profileData.basic_info.gender,
        hasBirthDate: !!profileData.basic_info.birth_date,
        hasPhone: !!profileData.basic_info.phone,
        hasEmail: !!profileData.basic_info.email,
        hasLocation: !!profileData.basic_info.location,
        hasPersonalSummary: !!profileData.basic_info.personal_summary,
        hasAvatar: !!profileData.basic_info.avatar
      })
    } else {
      console.warn('档案数据中缺少 basic_info 字段，将创建空对象')
      profileData.basic_info = {}
    }

    // 确保所有必要的字段都存在
    const requiredFields = ['basic_info', 'education', 'work_experience', 'skill']
    for (const field of requiredFields) {
      if (!profileData[field]) {
        console.warn(`档案数据缺少 ${field} 字段，将使用默认值`)
        profileData[field] = field === 'basic_info' ? {} : []
      }
    }

    // 确保 basic_info 中的所有字段都存在
    const basicInfoFields = ['name', 'gender', 'birth_date', 'phone', 'email', 'location', 'personal_summary', 'avatar']
    for (const field of basicInfoFields) {
      if (!profileData.basic_info[field]) {
        console.warn(`basic_info 缺少 ${field} 字段，将使用默认值`)
        profileData.basic_info[field] = ''
      }
    }
    
    console.log('最终处理后的档案数据结构:', {
      hasBasicInfo: !!profileData.basic_info,
      basicInfoFields: Object.keys(profileData.basic_info),
      hasEducation: Array.isArray(profileData.education),
      hasWorkExperience: Array.isArray(profileData.work_experience),
      hasSkill: Array.isArray(profileData.skill)
    })
    
    return {
      data: profileData,
      status: 200
    }
  } catch (error) {
    console.error('加载用户档案数据失败:', error)
    throw new Error('无法获取用户档案数据: ' + error.message)
  }
} 