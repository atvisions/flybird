export const resumeComponents = [
  {
    key: 'basicInfo',
    label: '基本信息',
    type: 'group',
    dataKey: 'basicInfo',
    fields: {
      name: { type: 'text', label: '姓名' },
      avatar: { type: 'image', label: '头像' },
      gender: { type: 'select', label: '性别' },
      birth: { type: 'date', label: '出生日期' },
      phone: { type: 'text', label: '手机号码' },
      email: { type: 'text', label: '电子邮箱' },
      location: { type: 'text', label: '所在地' },
      summary: { type: 'richText', label: '个人简介' }
    },
    props: {
      width: 600,
      height: 280
    }
  },
  {
    key: 'jobIntention',
    label: '求职意向',
    type: 'group',
    dataKey: 'jobIntention',
    fields: {
      jobType: { type: 'select', label: '工作类型' },
      jobStatus: { type: 'select', label: '求职状态' },
      expectedSalary: { type: 'text', label: '期望薪资' },
      expectedCity: { type: 'text', label: '期望城市' },
      industries: { type: 'tags', label: '期望行业' }
    },
    props: {
      width: 600,
      height: 200
    }
  },
  {
    key: 'education',
    label: '教育经历',
    type: 'group',
    dataKey: 'education',
    isArray: true,
    fields: {
      school: { type: 'text', label: '学校名称' },
      major: { type: 'text', label: '专业' },
      degree: { type: 'select', label: '学历' },
      duration: { type: 'dateRange', label: '起止时间' }
    },
    props: {
      width: 600,
      height: 240
    }
  },
  {
    key: 'workExperience',
    label: '工作经历',
    type: 'group',
    dataKey: 'workExperience',
    isArray: true,
    fields: {
      company: { type: 'text', label: '公司名称' },
      position: { type: 'text', label: '职位' },
      duration: { type: 'dateRange', label: '起止时间' },
      description: { type: 'richText', label: '工作内容' }
    },
    props: {
      width: 600,
      height: 320
    }
  },
  {
    key: 'skills',
    label: '专业技能',
    type: 'group',
    dataKey: 'skills',
    isArray: true,
    fields: {
      name: { type: 'text', label: '技能名称' },
      level: { type: 'select', label: '熟练程度' },
      description: { type: 'text', label: '技能描述' }
    },
    props: {
      width: 600,
      height: 200
    }
  },
  {
    key: 'languages',
    label: '语言能力',
    type: 'section',
    dataKey: 'languages',
    isArray: true,
    fields: [
      { key: 'language', label: '语言', type: 'text' },
      { key: 'level', label: '水平', type: 'text' },
      { key: 'certificates', label: '相关证书', type: 'text' }
    ],
    defaultStyle: {
      width: 600,
      padding: 20,
      background: '#fff',
      borderRadius: 8
    }
  },
  {
    key: 'social',
    label: '社交主页',
    type: 'section',
    dataKey: 'social',
    isArray: true,
    fields: [
      { key: 'platform', label: '平台', type: 'text' },
      { key: 'url', label: '链接', type: 'text' },
      { key: 'description', label: '描述', type: 'text' }
    ],
    defaultStyle: {
      width: 600,
      padding: 20,
      background: '#fff',
      borderRadius: 8
    }
  },
  {
    key: 'certificates',
    label: '证书奖项',
    type: 'section',
    dataKey: 'certificates',
    isArray: true,
    fields: [
      { key: 'name', label: '证书名称', type: 'text' },
      { key: 'issuing_authority', label: '发证机构', type: 'text' },
      { key: 'issue_date', label: '获得时间', type: 'text' },
      { key: 'description', label: '描述', type: 'richText' }
    ],
    defaultStyle: {
      width: 600,
      padding: 20,
      background: '#fff',
      borderRadius: 8
    }
  },
  {
    key: 'projects',
    label: '项目经历',
    type: 'section',
    dataKey: 'projects',
    isArray: true,
    fields: [
      { key: 'name', label: '项目名称', type: 'text' },
      { key: 'role', label: '担任角色', type: 'text' },
      { key: 'start_date', label: '开始时间', type: 'text' },
      { key: 'end_date', label: '结束时间', type: 'text' },
      { key: 'description', label: '项目描述', type: 'richText' },
      { key: 'achievements', label: '主要成就', type: 'richText' },
      { key: 'technologies', label: '相关技术', type: 'text' }
    ],
    defaultStyle: {
      width: 600,
      padding: 20,
      background: '#fff',
      borderRadius: 8
    }
  },
  {
    key: 'portfolio',
    label: '作品展示',
    type: 'section',
    dataKey: 'portfolio',
    isArray: true,
    fields: [
      { key: 'title', label: '作品标题', type: 'text' },
      { key: 'cover', label: '封面图片', type: 'image' },
      { key: 'description', label: '作品描述', type: 'richText' },
      { key: 'url', label: '相关链接', type: 'text' }
    ],
    defaultStyle: {
      width: 600,
      padding: 20,
      background: '#fff',
      borderRadius: 8
    }
  }
]

// 字段类型到图标的映射
export const fieldIconMap = {
  text: 'Text',
  richText: 'Editor',
  image: 'Image',
  section: 'Group'
}

// 数据映射配置
export const dataMapping = {
  basicInfo: 'basic_info',
  jobIntention: 'job_intention',
  education: 'education',
  workExperience: 'work_experience',
  skills: 'skills',
  languages: 'languages',
  social: 'social',
  certificates: 'certificates',
  projects: 'projects',
  portfolio: 'portfolio'
} 