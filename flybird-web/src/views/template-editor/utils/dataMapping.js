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
  if (!elements || !profileData) {
    console.warn('映射数据失败: elements 或 profileData 为空', { elements, profileData })
    return elements
  }

  console.log('开始数据映射，用户档案数据:', profileData)

  return elements.map(element => {
    // 获取数据路径和映射类型
    const dataPath = element.props?.dataPath || element.field?.dataPath || element.dataPath
    const mappingType = element.props?.mappingType || element.field?.type || element.mappingType

    console.log('正在处理元素:', {
      elementType: element.type,
      dataPath,
      mappingType,
      elementStructure: element
    })

    // 只处理简历字段类型的元素
    if (element.type === 'resume-field' && dataPath) {
      const value = getValueByPath(profileData, dataPath)
      console.log('字段映射详情:', {
        elementId: element.id,
        dataPath,
        mappingType,
        rawValue: value,
        elementProps: element.props
      })
      
      // 根据字段类型进行特殊处理
      let mappedElement = { ...element }
      let processedValue = value

      switch (mappingType) {
        case 'avatar':
          if (value) {
            processedValue = value.startsWith('http') ? value : `/media/${value.replace(/^\/?(media\/)?/, '')}`
          }
          break
          
        case 'date':
        case 'birth_date':
          if (value) {
            const date = new Date(value)
            processedValue = date.toLocaleDateString('zh-CN', {
              year: 'numeric',
              month: '2-digit',
              day: '2-digit'
            })
          }
          break

        case 'gender':
          processedValue = value === 'male' ? '男' : value === 'female' ? '女' : value || ''
          break
          
        case 'textarea':
          processedValue = value || ''
          mappedElement.props = {
            ...mappedElement.props,
            style: {
              ...mappedElement.props?.style,
              whiteSpace: 'pre-wrap',
              wordBreak: 'break-word'
            }
          }
          break

        case 'job_type':
          const jobTypeMap = {
            'full_time': '全职',
            'part_time': '兼职',
            'internship': '实习',
            'freelance': '自由职业'
          }
          processedValue = jobTypeMap[value] || value || ''
          break

        case 'job_status':
          const jobStatusMap = {
            'looking': '正在找工作',
            'not_looking': '暂不找工作',
            'open': '随时看机会'
          }
          processedValue = jobStatusMap[value] || value || ''
          break

        case 'language_proficiency':
          const proficiencyMap = {
            'beginner': '初级',
            'intermediate': '中级',
            'advanced': '高级',
            'native': '母语'
          }
          processedValue = proficiencyMap[value] || value || ''
          break
          
        default:
          processedValue = value || ''
      }

      // 更新元素的值
      if (mappedElement.props) {
        mappedElement.props.value = processedValue
      } else if (mappedElement.field) {
        mappedElement.field.value = processedValue
      } else {
        mappedElement.value = processedValue
      }

      console.log('映射后的元素:', {
        elementId: mappedElement.id,
        dataPath,
        mappingType,
        mappedValue: processedValue
      })

      return mappedElement
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