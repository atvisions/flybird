// 短信验证码场景
export const SMS_SCENE = {
  LOGIN: 'login',                   // 登录
  REGISTER: 'register',             // 注册
  RESET_PASSWORD: 'reset_password',          // 重置密码
  CHANGE_PHONE: 'change_phone',     // 更换手机号，修改为 change_phone
}

// 所有可用的模块类型
export const ALL_MODULES = {
  basic_info: {
    name: '基本信息',
    showInInactive: false
  },
  job_intention: {
    name: '求职意向',
    showInInactive: true
  },
  work_experience: {
    name: '工作经历',
    showInInactive: true
  },
  education: {
    name: '教育经历',
    showInInactive: true
  },
  project: {
    name: '项目经历',
    showInInactive: true
  },
  skill: {
    name: '专业技能',
    showInInactive: true
  },
  certificate: {
    name: '证书奖项',
    showInInactive: true
  },
  language: {
    name: '语言能力',
    showInInactive: true
  },
  portfolio: {
    name: '作品展示',
    showInInactive: true
  },
  social_link: {
    name: '社交主页',
    showInInactive: true
  }
}

// 核心模块（默认显示）
export const CORE_MODULES = [
  'basic_info',
  'job_intention',
  'work_experience',
  'education'
]

// 可选模块（在"添加更多"中显示）
export const OPTIONAL_MODULES = [
  'project',
  'skill',
  'certificate',
  'language',
  'portfolio',
  'social_link'
]

// 添加限速相关常量
export const RATE_LIMIT = {
  RETRY_AFTER: 'retry-after',  // 响应头中的重试时间字段
  DEFAULT_WAIT: 60,  // 默认等待时间（秒）
  MAX_RETRIES: 3     // 最大重试次数
}

export const STORAGE_KEYS = {
  TOKEN: 'token',
  REFRESH_TOKEN: 'refresh_token',
  REMEMBER_ME: 'remember_me',
  REMEMBERED_PHONE: 'remembered_phone',
  TOKEN_EXPIRES: 'token_expires'
} 