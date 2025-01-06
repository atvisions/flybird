// 行业选项
export const industryOptions = [
  { value: 'internet', label: '互联网/IT/通信' },
  { value: 'finance', label: '金融/投资/银行' },
  { value: 'real_estate', label: '房地产/建筑' },
  { value: 'consumer', label: '消费品/零售/贸易' },
  { value: 'manufacturing', label: '制造业' },
  { value: 'medical', label: '医疗/健康/制药' },
  { value: 'education', label: '教育/培训' },
  { value: 'service', label: '专业服务/咨询' },
  { value: 'media', label: '传媒/广告/文化' },
  { value: 'entertainment', label: '娱乐/休闲/体育' },
  { value: 'energy', label: '能源/环保' },
  { value: 'logistics', label: '物流/运输' },
  { value: 'agriculture', label: '农业/畜牧' },
  { value: 'government', label: '政府/非营利组织' },
  { value: 'others', label: '其他行业' }
]

// 行业分类
export const INDUSTRY_CATEGORIES = {
  TECH: {
    label: '科技/互联网',
    industries: ['互联网', '人工智能', '大数据', '云计算', '物联网', '区块链']
  },
  FINANCE: {
    label: '金融/投资',
    industries: ['银行', '证券', '保险', '投资', '基金', '信托']
  },
  ENTERPRISE: {
    label: '企业服务',
    industries: ['咨询', '法律', '人力资源', '财务', '市场营销', '广告']
  },
  CONSUMER: {
    label: '消费/零售',
    industries: ['电商', '零售', '快消品', '奢侈品', '餐饮', '旅游']
  },
  EDUCATION: {
    label: '教育/培训',
    industries: ['K12', '高等教育', '职业培训', '语言培训', '在线教育']
  },
  MEDICAL: {
    label: '医疗/健康',
    industries: ['医疗器械', '生物医药', '健康管理', '医疗服务', '养老服务']
  }
}

// 获取所有行业列表
export const getAllIndustries = () => {
  return Object.values(INDUSTRY_CATEGORIES).reduce((acc, category) => {
    return [...acc, ...category.industries]
  }, [])
}

// 根据分类获取行业
export const getIndustriesByCategory = (category) => {
  return INDUSTRY_CATEGORIES[category]?.industries || []
} 