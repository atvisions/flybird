// 基本信息字段配置
export const basicInfoFields = [
  {
    type: 'avatar',
    label: '',
    dataPath: 'basic_info.avatar',
    width: 100,
    height: 100
  },
  {
    type: 'text',
    label: '',
    dataPath: 'basic_info.name',
    width: 200,
    fontSize: 24,
    labelWidth: 0
  },
  {
    type: 'text',
    label: '',
    dataPath: 'basic_info.gender',
    width: 60,
    labelWidth: 0
  },
  {
    type: 'text',
    label: '',
    dataPath: 'basic_info.age',
    width: 60,
    labelWidth: 0,
    suffix: '岁'
  },
  {
    type: 'text',
    label: '电话',
    dataPath: 'basic_info.phone',
    width: 180
  },
  {
    type: 'text',
    label: '邮箱',
    dataPath: 'basic_info.email',
    width: 220
  },
  {
    type: 'text',
    label: '所在地',
    dataPath: 'basic_info.location',
    width: 180
  },
  {
    type: 'text',
    label: '工作年限',
    dataPath: 'basic_info.work_years',
    width: 120,
    suffix: '年'
  },
  {
    type: 'text',
    label: '期望职位',
    dataPath: 'basic_info.expected_position',
    width: 180
  },
  {
    type: 'text',
    label: '期望城市',
    dataPath: 'basic_info.expected_city',
    width: 180
  },
  {
    type: 'text',
    label: '期望薪资',
    dataPath: 'basic_info.expected_salary',
    width: 180
  },
  {
    type: 'text',
    label: '求职状态',
    dataPath: 'basic_info.job_status',
    width: 180
  },
  {
    type: 'textarea',
    label: '个人优势',
    dataPath: 'basic_info.personal_summary',
    width: 600,
    height: 80
  }
] 