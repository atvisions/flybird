import request from '@/utils/request'

// 更新基本信息
export const updateBasicInfo = (data) => {
  // 过滤掉空值，但保留合法的空字符串和false值
  const formatData = Object.entries(data).reduce((acc, [key, value]) => {
    // 对日期字段特殊处理
    if (key === 'birth_date') {
      // 如果日期为空，显式设置为null
      acc[key] = value ? new Date(value).toISOString().split('T')[0] : null
      console.log(`格式化日期: ${value} -> ${acc[key]}`)
    } else if (value !== undefined) {
      acc[key] = value
    }
    return acc
  }, {})

  console.log('发送到后端的数据:', formatData)

  return request({
    url: '/api/v1/users/profile/basic/',
    method: 'post',
    data: formatData
  })
} 