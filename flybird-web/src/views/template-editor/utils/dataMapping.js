// 数据映射工具函数

/**
 * 根据数据路径获取对象中的值
 * @param {Object} obj - 源数据对象
 * @param {string} path - 数据路径，如 'basic_info.name'
 * @returns {any} 对应路径的值
 */
export const getValueByPath = (obj, path) => {
  if (!obj || !path) return ''
  try {
    return path.split('.').reduce((acc, part) => acc && acc[part], obj)
  } catch (error) {
    console.error(`获取路径 ${path} 的值失败:`, error)
    return ''
  }
}

/**
 * 将用户档案数据映射到模板元素
 * @param {Array} elements - 模板元素数组
 * @param {Object} profileData - 用户档案数据
 * @returns {Array} 映射后的元素数组
 */
export const mapProfileDataToElements = (elements, profileData) => {
  if (!elements || !profileData) return elements

  return elements.map(element => {
    // 获取数据路径和映射类型
    const dataPath = element.dataPath || element.field?.dataPath
    const mappingType = element.mappingType || element.field?.type

    // 只处理简历字段类型的元素
    if (element.type === 'resume-field' && dataPath) {
      const value = getValueByPath(profileData, dataPath)
      console.log('映射数据:', { elementId: element.id, dataPath, value, mappingType })
      
      // 根据字段类型进行特殊处理
      switch (mappingType) {
        case 'avatar':
          // 处理头像URL
          if (value) {
            const avatarUrl = value.startsWith('http') ? value : `/media/${value.replace(/^\/?(media\/)?/, '')}`
            return {
              ...element,
              props: {
                ...element.props,
                value: avatarUrl
              }
            }
          }
          break
          
        case 'date':
        case 'birth_date':
          // 处理日期格式
          if (value) {
            const date = new Date(value)
            return {
              ...element,
              props: {
                ...element.props,
                value: date.toLocaleDateString('zh-CN', {
                  year: 'numeric',
                  month: '2-digit',
                  day: '2-digit'
                })
              }
            }
          }
          break

        case 'gender':
          // 处理性别显示（接口返回的是 male/female）
          return {
            ...element,
            props: {
              ...element.props,
              value: value === 'male' ? '男' : value === 'female' ? '女' : value || ''
            }
          }
          
        case 'textarea':
          // 处理多行文本（如个人总结）
          return {
            ...element,
            props: {
              ...element.props,
              value: value || '',
              style: {
                ...element.props?.style,
                whiteSpace: 'pre-wrap',
                wordBreak: 'break-word'
              }
            }
          }

        case 'job_type':
          // 处理工作类型
          const jobTypeMap = {
            'full_time': '全职',
            'part_time': '兼职',
            'internship': '实习',
            'freelance': '自由职业'
          }
          return {
            ...element,
            props: {
              ...element.props,
              value: jobTypeMap[value] || value || ''
            }
          }

        case 'job_status':
          // 处理求职状态
          const jobStatusMap = {
            'looking': '正在找工作',
            'not_looking': '暂不找工作',
            'open': '随时看机会'
          }
          return {
            ...element,
            props: {
              ...element.props,
              value: jobStatusMap[value] || value || ''
            }
          }

        case 'language_proficiency':
          // 处理语言水平
          const proficiencyMap = {
            'beginner': '初级',
            'intermediate': '中级',
            'advanced': '高级',
            'native': '母语'
          }
          return {
            ...element,
            props: {
              ...element.props,
              value: proficiencyMap[value] || value || ''
            }
          }
          
        default:
          // 处理其他类型字段
          return {
            ...element,
            props: {
              ...element.props,
              value: value || ''
            }
          }
      }
    }
    return element
  })
}

/**
 * 检查元素是否需要数据映射
 * @param {Object} element - 模板元素
 * @returns {boolean} 是否需要数据映射
 */
export const needsDataMapping = (element) => {
  const needs = element.type === 'resume-field' && (element.dataPath || element.field?.dataPath)
  console.log('检查元素是否需要映射:', {
    id: element.id,
    type: element.type,
    hasDataPath: !!element.dataPath,
    hasField: !!element.field,
    hasFieldDataPath: !!element.field?.dataPath,
    needs
  })
  return needs
} 