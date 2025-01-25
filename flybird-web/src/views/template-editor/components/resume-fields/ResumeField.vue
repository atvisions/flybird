<template>
  <div class="resume-field" :style="containerStyle">
    <!-- 头像类型 -->
    <template v-if="type === 'avatar'">
      <div class="avatar-field" :style="{ width: `${props.width}px`, height: `${props.height}px` }">
        <template v-if="previewValue">
          <img :src="previewValue" :alt="getPlaceholder" class="avatar-image" @error="handleImageError" />
        </template>
        <div v-else class="avatar-placeholder">
          <UserOutlined />
          <div class="avatar-text">头像</div>
        </div>
      </div>
    </template>

    <!-- 文本区域类型 -->
    <template v-else-if="type === 'textarea'">
      <div v-if="props.label" class="field-label" :style="labelStyle">{{ props.label }}</div>
      <div class="field-value textarea" :style="valueStyle">
        <div :class="{ 'placeholder-text': !isPreview }">{{ displayContent }}</div>
      </div>
    </template>

    <!-- 默认文本类型 -->
    <template v-else>
      <div v-if="props.label" class="field-label" :style="labelStyle">{{ props.label }}</div>
      <div class="field-value" :style="valueStyle">
        <div :class="{ 'placeholder-text': !isPreview }">{{ displayContent }}</div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { UserOutlined } from '@ant-design/icons-vue'
import { useProfileStore } from '@/stores/profile'
import config from '@/config'
import defaultAvatar from '@/assets/images/default-avatar.png'

// 添加日期格式化函数
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  try {
    const date = new Date(dateStr)
    if (isNaN(date.getTime())) return ''
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  } catch (error) {
    console.error('日期格式化错误:', error)
    return ''
  }
}

const props = defineProps({
  label: {
    type: String,
    default: ''
  },
  dataPath: {
    type: String,
    required: true
  },
  type: {
    type: String,
    default: 'text'
  },
  mappingType: {
    type: String,
    default: ''
  },
  isPreview: {
    type: Boolean,
    default: false
  },
  fontSize: {
    type: Number,
    default: 14
  },
  color: {
    type: String,
    default: '#333333'
  },
  labelWidth: {
    type: Number,
    default: 70
  },
  labelColor: {
    type: String,
    default: '#666666'
  },
  width: {
    type: Number,
    default: 200
  },
  height: {
    type: Number,
    default: 30
  },
  suffix: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:value'])

const profileStore = useProfileStore()

// 处理不同类型的值
const processValue = (value) => {
  if (value === undefined || value === null) {
    return ''
  }

  switch (props.mappingType) {
    case 'avatar':
      // 处理头像URL
      if (!value) return defaultAvatar
      // 如果已经是完整URL或者是Data URL，直接返回
      if (value.startsWith('http') || value.startsWith('data:image')) {
        return value
      }
      // 清理路径并使用环境变量中的API URL
      const cleanPath = value.replace(/^\/?(media\/)?/, '')
      return `${config.mediaURL}/${cleanPath}`
      
    case 'date':
    case 'birth_date':
      return formatDate(value)
      
    case 'gender':
      // 处理性别显示
      return value === 'male' ? '男' : value === 'female' ? '女' : value
      
    case 'location':
      // 处理所在地显示
      return value || props.label
      
    case 'personal_summary':
      // 处理个人简介显示
      return value || props.label
      
    case 'job_type':
      // 处理工作类型
      const jobTypeMap = {
        'full_time': '全职',
        'part_time': '兼职',
        'internship': '实习',
        'freelance': '自由职业'
      }
      return jobTypeMap[value] || value
      
    case 'job_status':
      // 处理求职状态
      const jobStatusMap = {
        'looking': '正在找工作',
        'not_looking': '暂不找工作',
        'open': '随时看机会'
      }
      return jobStatusMap[value] || value
      
    case 'language_proficiency':
      // 处理语言水平
      const proficiencyMap = {
        'beginner': '初级',
        'intermediate': '中级',
        'advanced': '高级',
        'native': '母语'
      }
      return proficiencyMap[value] || value
      
    default:
      return value
  }
}

// 获取用户档案数据
const previewValue = computed(() => {
  // 预览模式下获取实际数据
  if (!profileStore.profileData) {
    return ''
  }
  
  const pathParts = props.dataPath.split('.')
  let value = profileStore.profileData
  
  for (const part of pathParts) {
    if (!value || !(part in value)) {
      return ''
    }
    value = value[part]
  }
  
  // 处理值
  const processedValue = processValue(value)
  const finalValue = `${processedValue}${props.suffix}`
  
  console.log('字段值映射:', {
    id: props.id,
    dataPath: props.dataPath,
    mappingType: props.mappingType,
    rawValue: value,
    processedValue,
    finalValue
  })
  
  emit('update:value', finalValue)
  return finalValue
})

// 根据数据路径获取占位符文本
const getPlaceholder = computed(() => {
  const pathMap = {
    // 基本信息
    'basic_info.name': '姓名',
    'basic_info.gender': '性别',
    'basic_info.birth_date': '出生日期',
    'basic_info.phone': '手机号码',
    'basic_info.email': '电子邮箱',
    'basic_info.location': '所在城市',
    'basic_info.personal_summary': '个人简介',
    'basic_info.avatar': '头像',
    
    // 求职意向
    'job_intention.job_type': '工作类型',
    'job_intention.job_status': '求职状态',
    'job_intention.expected_salary': '期望薪资',
    'job_intention.expected_city': '期望城市',
    'job_intention.industries': '期望行业',
    
    // 工作经验
    'work_experience.company': '公司名称',
    'work_experience.position': '职位名称',
    'work_experience.department': '所在部门',
    'work_experience.start_date': '开始时间',
    'work_experience.end_date': '结束时间',
    'work_experience.description': '工作描述',
    'work_experience.achievements': '工作成就',
    
    // 教育经历
    'education.school': '学校名称',
    'education.major': '专业',
    'education.degree': '学历',
    'education.start_date': '入学时间',
    'education.end_date': '毕业时间',
    'education.description': '在校经历',
    
    // 项目经历
    'project.name': '项目名称',
    'project.role': '担任角色',
    'project.start_date': '开始时间',
    'project.end_date': '结束时间',
    'project.description': '项目描述',
    'project.achievement': '项目成就',
    
    // 技能特长
    'skill.name': '技能名称',
    'skill.level': '掌握程度',
    'skill.description': '技能描述',
    
    // 语言能力
    'language.name': '语言名称',
    'language.proficiency': '掌握程度',
    'language.certification': '语言证书',
    'language.score': '证书分数',
    
    // 证书
    'certificate.name': '证书名称',
    'certificate.issuing_authority': '发证机构',
    'certificate.issue_date': '发证日期',
    'certificate.credential_id': '证书编号',
    'certificate.description': '证书描述',
    
    // 社交账号
    'social_link.platform': '平台名称',
    'social_link.url': '主页链接',
    'social_link.description': '账号描述'
  }
  
  return pathMap[props.dataPath] || props.label || '请输入'
})

// 显示内容
const displayContent = computed(() => {
  if (!props.isPreview) {
    return `{{ ${props.label} }}`
  }
  return previewValue.value
})

// 样式计算
const containerStyle = computed(() => ({
  width: `${props.width}px`,
  height: props.type === 'textarea' ? `${props.height}px` : 'auto',
  minHeight: props.type === 'textarea' ? `${props.height}px` : `${props.height}px`,
  fontSize: `${props.fontSize}px`,
  color: props.color
}))

const labelStyle = computed(() => ({
  width: `${props.labelWidth}px`,
  color: props.labelColor
}))

const valueStyle = computed(() => ({
  width: props.label ? `calc(100% - ${props.labelWidth}px)` : '100%',
  height: props.type === 'textarea' ? `calc(100% - 22px)` : 'auto',
  minHeight: props.type === 'textarea' ? `calc(100% - 22px)` : 'auto'
}))

// 添加图片错误处理
const handleImageError = (e) => {
  if (e.target) {
    e.target.src = defaultAvatar
  }
}
</script>

<style scoped>
.resume-field {
  display: flex;
  align-items: flex-start;
  padding: 0 10px;
  box-sizing: border-box;
  min-height: 30px;
  height: auto;
}

.field-label {
  flex-shrink: 0;
  font-weight: 500;
  padding-top: 2px;
}

.field-value {
  flex: 1;
  overflow: visible;
  white-space: pre-wrap;
  word-break: break-word;
  height: auto;
}

.field-value.textarea {
  white-space: pre-wrap;
  line-height: 1.5;
  padding: 8px;
  background: #fafafa;
  border-radius: 4px;
}

.placeholder-text {
  color: #999;
  font-style: italic;
}

.avatar-field {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  overflow: hidden;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #999;
}

.avatar-text {
  font-size: 12px;
  margin-top: 4px;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}
</style> 