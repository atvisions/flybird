import config from '@/config'

// 获取对象中指定路径的值
const getValueByPath = (obj, path) => {
  if (!obj || !path) {
    console.log('【dataMapping】参数无效:', { obj, path })
    return ''
  }

  // 处理路径为空的情况
  if (path === 'basic_info.') {
    return ''
  }

  const pathParts = path.split('.')
  let value = obj

  // 处理 basic_info 字段
  if (pathParts[0] === 'basic_info' && value.basic_info) {
    const field = pathParts[1]
    console.log('【dataMapping】处理basic_info字段:', {
      field,
      hasBasicInfo: !!value.basic_info,
      hasField: field in value.basic_info,
      value: value.basic_info[field],
      basicInfoContent: JSON.stringify(value.basic_info)
    })

    // 字段映射
    const fieldMap = {
      'summary': 'personal_summary',
      'description': 'personal_summary',
      'self_evaluation': 'personal_summary'
    }

    // 如果有字段映射，使用映射后的字段名
    const mappedField = fieldMap[field] || field
    const fieldValue = value.basic_info[mappedField]

    if (fieldValue === undefined || fieldValue === null) {
      console.log(`【dataMapping】字段 ${field} 不存在或为空`)
      return ''
    }

    return fieldValue
  }

  // 处理其他字段
  for (const part of pathParts) {
    if (!value || typeof value !== 'object') {
      return ''
    }
    value = value[part]
  }

  return value === undefined || value === null ? '' : value
}

// 处理字段值
const processFieldValue = (value, mappingType, dataPath) => {
  // 如果值为空，根据字段类型返回默认值
  if (!value) {
    return mappingType === 'text' ? '' : '未设置'
  }

  switch (mappingType) {
    case 'avatar':
      if (value.startsWith('http') || value.startsWith('data:image')) {
        return value
      }
      const cleanPath = value.replace(/^\/?(media\/)?/, '')
      return `${config.mediaURL}/${cleanPath}`

    case 'date':
    case 'birth_date':
      try {
        if (value === 'Invalid Date' || !value) {
          return '未设置'
        }
        const date = new Date(value)
        if (isNaN(date.getTime())) {
          return '未设置'
        }
        return date.toLocaleDateString('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit'
        })
      } catch (error) {
        console.error('日期格式化失败:', error)
        return '未设置'
      }

    case 'gender':
      const genderMap = {
        'male': '男',
        'female': '女',
        'other': '其他'
      }
      return genderMap[value] || value

    case 'textarea':
      return value || '未设置'

    case 'text':
      // 对于性别字段，需要进行映射
      if (dataPath === 'basic_info.gender') {
        const genderMap = {
          'male': '男',
          'female': '女',
          'other': '其他'
        }
        return genderMap[value] || value
      }
      // 其他文本字段直接返回值
      return value

    default:
      return value || '未设置'
  }
}

// 检查元素是否需要数据映射
export const needsDataMapping = (element) => {
  const needs = element.type === 'resume-field' && (element.dataPath || element.field?.dataPath)
  console.log('【dataMapping】检查元素是否需要映射:', {
    id: element.id,
    type: element.type,
    hasDataPath: !!element.dataPath,
    hasField: !!element.field,
    hasFieldDataPath: !!element.field?.dataPath,
    needs
  })
  return needs
}

// 映射用户档案数据到模板元素
export const mapProfileDataToElements = (elements, profileData) => {
  console.log('【dataMapping】开始映射数据:', {
    elementsCount: elements?.length,
    profileDataKeys: profileData ? Object.keys(profileData) : [],
    profileDataStructure: profileData ? JSON.stringify(profileData) : null,
    elements: elements
  })

  if (!elements || !profileData) {
    console.log('【dataMapping】无效的参数:', {
      hasElements: !!elements,
      elementsCount: elements?.length,
      hasProfileData: !!profileData,
      profileDataKeys: profileData ? Object.keys(profileData) : []
    })
    return elements
  }

  // 确保使用正确的数据结构
  const data = profileData.data || profileData

  return elements.map(element => {
    // 检查元素是否需要映射
    console.log('【dataMapping】检查元素:', {
      id: element.id,
      type: element.type,
      hasDataPath: !!element.dataPath,
      hasField: !!element.field,
      hasFieldDataPath: !!element.field?.dataPath,
      dataPath: element.dataPath || element.field?.dataPath,
      mappingType: element.mappingType || element.field?.type
    })

    // 获取数据路径和映射类型
    const dataPath = element.dataPath || element.field?.dataPath
    const mappingType = element.mappingType || element.field?.type

    // 如果是普通元素或没有数据路径，直接返回
    if (!dataPath) {
      console.log('【dataMapping】元素无需映射:', {
        id: element.id,
        type: element.type,
        content: element.content
      })
      return element
    }

    // 获取映射值
    const value = getValueByPath(data, dataPath)
    console.log('【dataMapping】获取到的值:', {
      id: element.id,
      dataPath,
      value,
      valueType: typeof value
    })
    
    // 处理值
    const processedValue = processFieldValue(value, mappingType, dataPath)
    console.log('【dataMapping】处理后的值:', {
      id: element.id,
      dataPath,
      originalValue: value,
      processedValue,
      mappingType
    })

    // 返回更新后的元素
    return {
      ...element,
      content: processedValue,
      props: {
        ...element.props,
        value: processedValue
      }
    }
  })
} 