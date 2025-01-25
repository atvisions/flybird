// 基本信息字段配置
export const basicInfoFields = [
  {
    type: 'avatar',
    label: '头像',
    key: 'avatar',
    dataPath: 'basic_info.avatar',
    defaultStyle: {
      width: 100,
      height: 100,
      borderRadius: '50%'
    }
  },
  {
    type: 'text',
    label: '姓名',
    key: 'name',
    dataPath: 'basic_info.name',
    defaultStyle: {
      fontSize: 24,
      fontWeight: 'bold'
    }
  },
  {
    type: 'text',
    label: '性别',
    key: 'gender',
    dataPath: 'basic_info.gender',
    defaultStyle: {
      fontSize: 14
    }
  },
  {
    type: 'text',
    label: '出生日期',
    key: 'birth_date',
    dataPath: 'basic_info.birth_date',
    defaultStyle: {
      fontSize: 14
    }
  },
  {
    type: 'text',
    label: '电话',
    key: 'phone',
    dataPath: 'basic_info.phone',
    defaultStyle: {
      fontSize: 14
    }
  },
  {
    type: 'text',
    label: '邮箱',
    key: 'email',
    dataPath: 'basic_info.email',
    defaultStyle: {
      fontSize: 14
    }
  },
  {
    type: 'text',
    label: '所在城市',
    key: 'location',
    dataPath: 'basic_info.location',
    defaultStyle: {
      fontSize: 14
    }
  },
  {
    type: 'textarea',
    label: '个人简介',
    key: 'personal_summary',
    dataPath: 'basic_info.personal_summary',
    defaultStyle: {
      fontSize: 14,
      lineHeight: 1.5
    }
  }
]

// 求职意向字段配置
export const jobIntentionFields = [
  {
    type: 'text',
    label: '工作类型',
    key: 'job_type',
    dataPath: 'job_intention.job_type',
    mappingType: 'job_type',
    mappingOptions: [
      { value: 'full_time', label: '全职' },
      { value: 'part_time', label: '兼职' },
      { value: 'internship', label: '实习' },
      { value: 'freelance', label: '自由职业' }
    ],
    defaultStyle: {
      fontSize: 14
    }
  },
  {
    type: 'text',
    label: '求职状态',
    key: 'job_status',
    dataPath: 'job_intention.job_status',
    mappingType: 'job_status',
    mappingOptions: [
      { value: 'actively_looking', label: '正在积极找工作' },
      { value: 'open_to_offers', label: '对机会持开放态度' },
      { value: 'not_looking', label: '暂时不找工作' }
    ],
    defaultStyle: {
      fontSize: 14
    }
  },
  {
    type: 'text',
    label: '期望薪资',
    key: 'expected_salary',
    dataPath: 'job_intention.expected_salary',
    defaultStyle: {
      fontSize: 14
    }
  },
  {
    type: 'text',
    label: '期望城市',
    key: 'expected_city',
    dataPath: 'job_intention.expected_city',
    defaultStyle: {
      fontSize: 14
    }
  },
  {
    type: 'text',
    label: '期望行业',
    key: 'industries',
    dataPath: 'job_intention.industries',
    defaultStyle: {
      fontSize: 14
    }
  }
]

// 工作经历字段配置
export const workExperienceFields = [
  {
    type: 'text',
    label: '公司名称',
    key: 'company',
    dataPath: 'work_experience[0].company',
    defaultStyle: {
      fontSize: 16,
      fontWeight: 'bold',
      color: '#333333'
    }
  },
  {
    type: 'text',
    label: '职位名称',
    key: 'position',
    dataPath: 'work_experience[0].position',
    defaultStyle: {
      fontSize: 14,
      color: '#666666'
    }
  },
  {
    type: 'text',
    label: '所在部门',
    key: 'department',
    dataPath: 'work_experience[0].department',
    defaultStyle: {
      fontSize: 14,
      color: '#666666'
    }
  },
  {
    type: 'date',
    label: '开始时间',
    key: 'start_date',
    dataPath: 'work_experience[0].start_date',
    defaultStyle: {
      fontSize: 14,
      color: '#666666'
    }
  },
  {
    type: 'date',
    label: '结束时间',
    key: 'end_date',
    dataPath: 'work_experience[0].end_date',
    defaultStyle: {
      fontSize: 14,
      color: '#666666'
    }
  },
  {
    type: 'textarea',
    label: '工作描述',
    key: 'description',
    dataPath: 'work_experience[0].description',
    defaultStyle: {
      fontSize: 14,
      lineHeight: 1.5,
      height: 100,
      color: '#666666'
    }
  },
  {
    type: 'textarea',
    label: '工作成就',
    key: 'achievements',
    dataPath: 'work_experience[0].achievements',
    defaultStyle: {
      fontSize: 14,
      lineHeight: 1.5,
      height: 100,
      color: '#666666'
    }
  },
  {
    type: 'textarea',
    label: '技术栈',
    key: 'technologies',
    dataPath: 'work_experience[0].technologies',
    defaultStyle: {
      fontSize: 14,
      lineHeight: 1.5,
      height: 60,
      color: '#666666'
    }
  }
]

// 教育经历字段配置
export const educationFields = [
  {
    type: 'text',
    label: '学校',
    key: 'school',
    dataPath: 'school',
    defaultStyle: {
      fontSize: 16,
      fontWeight: 'bold'
    }
  },
  {
    type: 'text',
    label: '专业',
    key: 'major',
    dataPath: 'major',
    defaultStyle: {
      fontSize: 14
    }
  },
  {
    type: 'text',
    label: '学历',
    key: 'degree',
    dataPath: 'degree',
    defaultStyle: {
      fontSize: 14
    }
  },
  {
    type: 'dateRange',
    label: '在校时间',
    startKey: 'start_date',
    endKey: 'end_date',
    dataPath: ['start_date', 'end_date'],
    defaultStyle: {
      fontSize: 14
    }
  }
]

// 技能特长字段配置
export const skillFields = [
  {
    type: 'text',
    label: '技能名称',
    key: 'name',
    dataPath: 'name',
    defaultStyle: {
      fontSize: 14,
      fontWeight: 'bold'
    }
  },
  {
    type: 'text',
    label: '掌握程度',
    key: 'level',
    dataPath: 'level',
    defaultStyle: {
      fontSize: 14
    }
  },
  {
    type: 'textarea',
    label: '技能描述',
    key: 'description',
    dataPath: 'description',
    defaultStyle: {
      fontSize: 14
    }
  }
]

// 项目经验字段配置
export const projectFields = [
  {
    type: 'text',
    label: '项目名称',
    key: 'name',
    dataPath: 'name',
    defaultStyle: {
      fontSize: 16,
      fontWeight: 'bold'
    }
  },
  {
    type: 'text',
    label: '担任角色',
    key: 'role',
    dataPath: 'role',
    defaultStyle: {
      fontSize: 14
    }
  },
  {
    type: 'dateRange',
    label: '项目时间',
    startKey: 'start_date',
    endKey: 'end_date',
    dataPath: ['start_date', 'end_date'],
    defaultStyle: {
      fontSize: 14
    }
  },
  {
    type: 'textarea',
    label: '项目描述',
    key: 'description',
    dataPath: 'description',
    defaultStyle: {
      fontSize: 14,
      lineHeight: 1.5
    }
  }
]

// 证书字段配置
export const certificateFields = [
  {
    type: 'text',
    label: '证书名称',
    key: 'name',
    dataPath: 'name',
    defaultStyle: {
      fontSize: 14,
      fontWeight: 'bold'
    }
  },
  {
    type: 'text',
    label: '发证机构',
    key: 'issuing_authority',
    dataPath: 'issuing_authority',
    defaultStyle: {
      fontSize: 14
    }
  },
  {
    type: 'dateRange',
    label: '有效期',
    startKey: 'issue_date',
    endKey: 'expiry_date',
    dataPath: ['issue_date', 'expiry_date'],
    defaultStyle: {
      fontSize: 14
    }
  }
]

// 语言能力字段配置
export const languageFields = [
  {
    type: 'text',
    label: '语言',
    key: 'name',
    dataPath: 'name',
    defaultStyle: {
      fontSize: 14,
      fontWeight: 'bold'
    }
  },
  {
    type: 'text',
    label: '水平',
    key: 'proficiency',
    dataPath: 'proficiency_display',
    defaultStyle: {
      fontSize: 14
    }
  },
  {
    type: 'text',
    label: '证书',
    key: 'certification',
    dataPath: 'certification',
    defaultStyle: {
      fontSize: 14
    }
  },
  {
    type: 'text',
    label: '分数',
    key: 'score',
    dataPath: 'score',
    defaultStyle: {
      fontSize: 14
    }
  }
] 