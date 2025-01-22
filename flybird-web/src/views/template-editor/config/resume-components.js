export const resumeComponents = [
  {
    key: 'basicInfo',
    label: '基本信息',
    fields: [
      { label: '姓名', dataPath: 'basic_info.name', width: 200 },
      { label: '性别', dataPath: 'basic_info.gender', width: 100 },
      { label: '出生日期', dataPath: 'basic_info.birth_date', width: 200 },
      { label: '电话', dataPath: 'basic_info.phone', width: 200 },
      { label: '邮箱', dataPath: 'basic_info.email', width: 200 },
      { label: '所在城市', dataPath: 'basic_info.location', width: 200 },
      { label: '个人简介', dataPath: 'basic_info.personal_summary', width: 400, type: 'textarea', height: 100 }
    ]
  },
  {
    key: 'jobIntention',
    label: '求职意向',
    fields: [
      { label: '工作类型', dataPath: 'job_intention.job_type', width: 200 },
      { label: '求职状态', dataPath: 'job_intention.job_status', width: 200 },
      { label: '期望薪资', dataPath: 'job_intention.expected_salary', width: 200 },
      { label: '期望城市', dataPath: 'job_intention.expected_city', width: 200 },
      { label: '期望行业', dataPath: 'job_intention.industries', width: 400 }
    ]
  },
  {
    key: 'workExperience',
    label: '工作经历',
    fields: [
      { label: '公司名称', dataPath: 'work_experience.company', width: 300 },
      { label: '职位名称', dataPath: 'work_experience.position', width: 200 },
      { label: '所在部门', dataPath: 'work_experience.department', width: 200 },
      { label: '开始时间', dataPath: 'work_experience.start_date', width: 200 },
      { label: '结束时间', dataPath: 'work_experience.end_date', width: 200 },
      { label: '工作描述', dataPath: 'work_experience.description', width: 400, type: 'textarea', height: 100 },
      { label: '工作成就', dataPath: 'work_experience.achievements', width: 400, type: 'textarea', height: 100 }
    ]
  },
  {
    key: 'education',
    label: '教育经历',
    fields: [
      { label: '学校名称', dataPath: 'education.school', width: 300 },
      { label: '专业', dataPath: 'education.major', width: 200 },
      { label: '学历', dataPath: 'education.degree', width: 200 },
      { label: '入学时间', dataPath: 'education.start_date', width: 200 },
      { label: '毕业时间', dataPath: 'education.end_date', width: 200 },
      { label: '在校经历', dataPath: 'education.description', width: 400, type: 'textarea', height: 100 }
    ]
  },
  {
    key: 'project',
    label: '项目经历',
    fields: [
      { label: '项目名称', dataPath: 'project.name', width: 300 },
      { label: '担任角色', dataPath: 'project.role', width: 200 },
      { label: '开始时间', dataPath: 'project.start_date', width: 200 },
      { label: '结束时间', dataPath: 'project.end_date', width: 200 },
      { label: '项目描述', dataPath: 'project.description', width: 400, type: 'textarea', height: 100 },
      { label: '项目成就', dataPath: 'project.achievement', width: 400, type: 'textarea', height: 100 }
    ]
  },
  {
    key: 'skills',
    label: '技能特长',
    fields: [
      { label: '技能名称', dataPath: 'skill.name', width: 200 },
      { label: '掌握程度', dataPath: 'skill.level', width: 200 },
      { label: '技能描述', dataPath: 'skill.description', width: 400, type: 'textarea', height: 100 }
    ]
  },
  {
    key: 'languages',
    label: '语言能力',
    fields: [
      { label: '语言名称', dataPath: 'language.name', width: 200 },
      { label: '掌握程度', dataPath: 'language.proficiency', width: 200 },
      { label: '语言证书', dataPath: 'language.certification', width: 200 },
      { label: '证书分数', dataPath: 'language.score', width: 200 }
    ]
  },
  {
    key: 'certificates',
    label: '证书',
    fields: [
      { label: '证书名称', dataPath: 'certificate.name', width: 300 },
      { label: '发证机构', dataPath: 'certificate.issuing_authority', width: 200 },
      { label: '发证日期', dataPath: 'certificate.issue_date', width: 200 },
      { label: '证书编号', dataPath: 'certificate.credential_id', width: 200 },
      { label: '证书描述', dataPath: 'certificate.description', width: 400, type: 'textarea', height: 100 }
    ]
  },
  {
    key: 'social',
    label: '社交账号',
    fields: [
      { label: '平台名称', dataPath: 'social_link.platform', width: 200 },
      { label: '主页链接', dataPath: 'social_link.url', width: 300 },
      { label: '账号描述', dataPath: 'social_link.description', width: 400 }
    ]
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