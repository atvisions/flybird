/**
 * 格式化日期
 * @param {Date|string} date - 日期对象或日期字符串
 * @param {string} format - 格式化模式，默认为 'YYYY-MM-DD'
 * @returns {string} 格式化后的日期字符串
 */
export const formatDate = (date, format = 'YYYY-MM-DD') => {
  if (!date) return ''
  
  const d = new Date(date)
  if (isNaN(d.getTime())) return ''

  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hours = String(d.getHours()).padStart(2, '0')
  const minutes = String(d.getMinutes()).padStart(2, '0')
  const seconds = String(d.getSeconds()).padStart(2, '0')

  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds)
}

/**
 * 格式化相对时间
 * @param {Date|string} date - 日期对象或日期字符串
 * @returns {string} 相对时间字符串
 */
export const formatRelativeTime = (date) => {
  if (!date) return ''
  
  const d = new Date(date)
  if (isNaN(d.getTime())) return ''

  const now = new Date()
  const diff = now - d
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)

  if (days > 365) {
    return formatDate(date, 'YYYY-MM-DD')
  } else if (days > 30) {
    return `${Math.floor(days / 30)}个月前`
  } else if (days > 0) {
    return `${days}天前`
  } else if (hours > 0) {
    return `${hours}小时前`
  } else if (minutes > 0) {
    return `${minutes}分钟前`
  } else {
    return '刚刚'
  }
}

/**
 * 格式化日期范围
 * @param {Date|string} startDate - 开始日期
 * @param {Date|string} endDate - 结束日期
 * @returns {string} 格式化后的日期范围字符串
 */
export const formatDateRange = (startDate, endDate) => {
  if (!startDate || !endDate) return ''
  
  const start = formatDate(startDate)
  const end = formatDate(endDate)
  
  return `${start} 至 ${end}`
}

/**
 * 获取日期是星期几
 * @param {Date|string} date - 日期对象或日期字符串
 * @returns {string} 星期几
 */
export const getWeekDay = (date) => {
  if (!date) return ''
  
  const d = new Date(date)
  if (isNaN(d.getTime())) return ''

  const weekDays = ['日', '一', '二', '三', '四', '五', '六']
  return `星期${weekDays[d.getDay()]}`
}

/**
 * 格式化剩余时间
 * @param {Date|string} endDate - 结束日期
 * @returns {string} 剩余时间字符串
 */
export const formatRemainingTime = (endDate) => {
  if (!endDate) return ''
  
  const end = new Date(endDate)
  if (isNaN(end.getTime())) return ''

  const now = new Date()
  const diff = end - now
  
  if (diff <= 0) return '已过期'
  
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
  
  if (days > 0) {
    return `剩余 ${days} 天`
  } else if (hours > 0) {
    return `剩余 ${hours} 小时`
  } else {
    return '即将过期'
  }
} 