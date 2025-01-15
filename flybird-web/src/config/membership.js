import {
  DocumentTextIcon,
  SparklesIcon,
  RocketLaunchIcon,
  StarIcon
} from '@heroicons/vue/24/outline'

// 会员权益配置
export const membershipBenefits = [
  {
    name: '会员模板',
    desc: '独享精美模板',
    icon: DocumentTextIcon,
    key: 'premium_templates'
  },
  {
    name: '简历解析',
    desc: '一键导入转换',
    icon: SparklesIcon,
    key: 'resume_parsing'
  },
  {
    name: 'AI优化',
    desc: '智能档案优化', 
    icon: RocketLaunchIcon,
    key: 'ai_optimization'
  },
  {
    name: '无限简历',
    desc: '积分收益翻倍',
    icon: StarIcon,
    key: 'unlimited_resume'
  }
]

// 会员价格配置
export const membershipPricing = {
  daily: 0.25,
  monthly: 7.5,
  yearly: 90
}

// 会员等级配置
export const membershipTiers = {
  free: {
    name: '免费用户',
    level: 0
  },
  pro: {
    name: '专业会员',
    level: 1
  }
} 