// src/views/user/MyProfile/constants/moduleConfig.js
import { 
  AcademicCapIcon,
  BriefcaseIcon,
  SparklesIcon,
  LanguageIcon,
  DocumentTextIcon,
  UserGroupIcon
} from '@heroicons/vue/24/outline'
import { cityOptions } from './cityOptions'

export const moduleConfig = [
  {
    id: 'job_intention',
    type: 'job_intention',
    name: '求职意向',
    icon: BriefcaseIcon,
    required: false,
    multiple: false,
    formConfig: {
      fields: [
        {
          name: 'job_type',
          label: '工作类型',
          type: 'select',
          required: false,
          options: [
            { label: '全职', value: 'full_time' },
            { label: '兼职', value: 'part_time' },
            { label: '实习', value: 'internship' },
            { label: '自由职业', value: 'freelance' }
          ]
        },
        {
          name: 'job_status',
          label: '求职状态',
          type: 'select',
          required: false,
          options: [
            { label: '在找工作', value: 'open' },
            { label: '暂不找工作', value: 'closed' }
          ]
        },
        {
          name: 'expected_salary',
          label: '期望薪资',
          type: 'input',
          required: false,
          placeholder: '例如：15K-20K、20K以上'
        },
        {
          name: 'expected_city',
          label: '期望城市',
          type: 'input',
          required: false,
          placeholder: '例如：北京、上海-浦东'
        },
        {
          name: 'industries',
          label: '期望行业',
          type: 'input',
          required: false,
          placeholder: '例如：互联网、人工智能'
        }
      ]
    }
  },
  {
    id: 'education',
    type: 'education',
    name: '教育经历',
    icon: AcademicCapIcon,
    required: false,
    multiple: true
  },
  {
    id: 'work_experience',
    type: 'work_experience',
    name: '工作经历',
    icon: BriefcaseIcon,
    required: false,
    multiple: true,
    order: 2
  },
  {
    id: 'skills',
    type: 'skills',
    name: '技能特长',
    icon: SparklesIcon,
    required: false,
    multiple: true
  },
  {
    id: 'languages',
    type: 'languages',
    name: '语言能力',
    icon: LanguageIcon,
    required: false,
    multiple: true
  },
  {
    id: 'certificates',
    type: 'certificates',
    name: '证书奖项',
    icon: DocumentTextIcon,
    required: false,
    multiple: true
  },
  {
    id: 'social',
    type: 'social',
    name: '社交主页',
    icon: UserGroupIcon,
    required: false,
    multiple: true
  }
]