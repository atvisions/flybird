import config from '@/config'

// 获取对象中指定路径的值
const getValueByPath = (obj, path) => {
  if (!obj || !path) {
    console.log('【dataMapping】参数无效:', { obj, path })
    return ''
  }

  // 统一使用 work_experience 作为字段名
  const normalizedPath = path.replace(/^(workExperience|workExperiences)\[/, 'work_experience[')

  // 处理路径为空的情况
  if (normalizedPath === 'basic_info.') {
    return ''
  }

  // 处理数组路径，如 work_experience[0].company
  const arrayMatch = normalizedPath.match(/(.+?)\[(\d+)\]\.(.+)/)
  if (arrayMatch) {
    const [, arrayPath, index, field] = arrayMatch
    console.log('【dataMapping】处理数组路径:', {
      arrayPath,
      index,
      field,
      originalPath: path,
      normalizedPath,
      hasArray: !!obj[arrayPath],
      isArray: Array.isArray(obj[arrayPath]),
      availableKeys: obj ? Object.keys(obj) : []
    })

    // 获取数组
    const array = obj['work_experience']
    if (!array || !Array.isArray(array)) {
      console.log('【dataMapping】数组不存在:', {
        arrayPath,
        availableKeys: obj ? Object.keys(obj) : [],
        value: array
      })
      return ''
    }

    // 获取数组元素
    const item = array[parseInt(index, 10)]
    if (!item) {
      console.log('【dataMapping】数组元素不存在:', {
        index,
        arrayLength: array.length
      })
      return ''
    }

    // 获取字段值
    let value = item[field]
    console.log('【dataMapping】获取字段值:', {
      field,
      value,
      itemKeys: Object.keys(item),
      valueType: typeof value,
      item
    })

    // 特殊处理某些字段
    if (field === 'achievements' || field === 'technologies') {
      if (!value || value === '[]' || (Array.isArray(value) && value.length === 0)) {
        return '未设置'
      }
      try {
        if (typeof value === 'string') {
          if (value === '[]') {
            return '未设置'
          }
          // 如果是普通字符串，直接返回
          if (!value.startsWith('[')) {
            return value
          }
          // 尝试解析 JSON
          const parsed = JSON.parse(value)
          if (Array.isArray(parsed)) {
            return parsed.length > 0 ? parsed.join(field === 'technologies' ? '、' : '\n') : '未设置'
          }
          return String(parsed) || '未设置'
        }
        if (Array.isArray(value)) {
          return value.length > 0 ? value.join(field === 'technologies' ? '、' : '\n') : '未设置'
        }
        return String(value) || '未设置'
      } catch (error) {
        console.warn('【dataMapping】解析数组字段失败:', { field, value, error })
        return typeof value === 'string' ? value : '未设置'
      }
    }
    
    return value === undefined || value === null || value === '' ? '未设置' : value
  }

  const pathParts = normalizedPath.split('.')
  let value = obj

  // 处理 basic_info 字段
  if (pathParts[0] === 'basic_info' && value.basic_info) {
    const field = pathParts[1]

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

  // 检查是否是工作经历字段
  const isWorkExperience = /^work_experience\[/.test(dataPath)
  if (isWorkExperience) {
    console.log('【dataMapping】处理工作经历字段:', { dataPath, value, mappingType })
    const field = dataPath.split('.')[1]
    switch (field) {
      case 'achievements':
        if (!value || value === '[]' || (Array.isArray(value) && value.length === 0)) {
          return '未设置'
        }
        try {
          if (typeof value === 'string' && value !== '[]') {
            return value
          }
          const achievementArray = Array.isArray(value) ? value : [value]
          return achievementArray.length > 0 ? achievementArray.join('\n') : '未设置'
        } catch (error) {
          console.warn('【dataMapping】解析成就数据失败:', { value, error })
          return value || '未设置'
        }
      case 'technologies':
        if (!value || value === '[]' || (Array.isArray(value) && value.length === 0)) {
          return '未设置'
        }
        if (typeof value === 'string' && value !== '[]') {
          return value
        }
        if (Array.isArray(value)) {
          return value.join('、')
        }
        return value || '未设置'
      case 'start_date':
      case 'end_date':
        try {
          if (!value || value === 'Invalid Date') {
            return field === 'end_date' ? '至今' : ''
          }
          const date = new Date(value)
          if (isNaN(date.getTime())) {
            return field === 'end_date' ? '至今' : ''
          }
          const year = date.getFullYear()
          const month = String(date.getMonth() + 1).padStart(2, '0')
          return `${year}.${month}`
        } catch (error) {
          console.warn('【dataMapping】日期格式化失败:', { value, error, field })
          return field === 'end_date' ? '至今' : ''
        }
      case 'company':
      case 'position':
      case 'department':
        return value?.trim() || '未设置'
      case 'description':
        return value?.trim() || '未设置'
      case 'duration':
        return value?.trim() || ''
      default:
        return String(value || '').trim() || '未设置'
    }
  }

  switch (mappingType) {
    case 'avatar':
      if (value.startsWith('http') || value.startsWith('data:image')) {
        return value
      }
      const cleanPath = value.replace(/^\/?(media\/)?/, '')
      return `${config.mediaURL}/${cleanPath}`

    case 'date':
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
          month: 'long'
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
      if (typeof value === 'string' && (value.startsWith('[') || value.startsWith('{'))) {
        try {
          const parsed = JSON.parse(value)
          if (Array.isArray(parsed)) {
            return parsed.length > 0 ? parsed.join('\n') : '未设置'
          }
          return parsed.toString()
        } catch {
          return value || '未设置'
        }
      }
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
      // 检查是否是求职意向字段
      if (dataPath.startsWith('job_intention.')) {
        const field = dataPath.split('.')[1]
        switch (field) {
          case 'job_type':
            const jobTypeMap = {
              'full_time': '全职',
              'part_time': '兼职',
              'internship': '实习',
              'freelance': '自由职业'
            }
            return jobTypeMap[value] || value
          case 'job_status':
            const jobStatusMap = {
              'actively_looking': '积极找工作',
              'open_to_offers': '考虑机会',
              'not_looking': '暂不找工作'
            }
            return jobStatusMap[value] || value
          case 'expected_salary':
            const salaryMap = {
              '0-5': '5K以下',
              '5-10': '5-10K',
              '10-15': '10-15K',
              '15-20': '15-20K',
              '20-30': '20-30K',
              '30-50': '30-50K',
              '50-100': '50-100K',
              '100+': '100K以上'
            }
            return salaryMap[value] || value
          case 'industries':
            if (typeof value === 'string') {
              return value.split(',').join('、')
            }
            return value || ''
          case 'expected_city':
            return value
          default:
            return value
        }
      }
      return String(value)

    default:
      return String(value) || '未设置'
  }
}

// 检查元素是否需要数据映射
export const needsDataMapping = (element) => {
  const needs = element.type === 'resume-field' && (element.dataPath || element.field?.dataPath)
  return needs
}

// 映射用户档案数据到模板元素
export const mapProfileDataToElements = (elements, profileData) => {

  if (!elements || !profileData) {
    return elements
  }

  // 确保使用正确的数据结构
  const data = profileData.data || profileData

  return elements.map(element => {


    // 获取数据路径和映射类型
    const dataPath = element.dataPath || element.field?.dataPath
    const mappingType = element.mappingType || element.field?.type

    // 如果是普通元素或没有数据路径，直接返回
    if (!dataPath) {

      return element
    }

    // 获取映射值
    const value = getValueByPath(data, dataPath)

    
    // 处理值
    const processedValue = processFieldValue(value, mappingType, dataPath)


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