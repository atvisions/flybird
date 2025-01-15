<template>
  <div class="resume-import">
    <!-- 导入对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="导入简历"
      width="550px"
      :close-on-click-modal="false"
      class="resume-import-dialog"
    >
      <div class="p-6">
        <!-- 上传区域 -->
        <div
          class="border-2 border-dashed border-gray-200 hover:border-blue-400 rounded-2xl p-8 text-center transition-all duration-300 bg-gray-50/50 hover:bg-blue-50/50 group cursor-pointer"
          @drop.prevent="handleDrop"
          @dragover.prevent
          @click="triggerFileInput"
        >
          <input
            ref="fileInput"
            type="file"
            class="hidden"
            @change="handleFileChange"
            accept=".doc,.docx,.pdf,.jpg,.jpeg,.png"
          />
          <div class="space-y-4">
            <DocumentArrowUpIcon class="w-16 h-16 mx-auto text-gray-300 group-hover:text-blue-400 transition-colors duration-300" />
            <div class="text-sm text-gray-600">
              <span class="font-medium text-blue-500 hover:text-blue-600 transition-colors">
                点击上传
              </span>
              或将文件拖拽到这里
            </div>
            <p class="text-xs text-gray-500">
              支持 Word、PDF、JPG 格式文件
            </p>
          </div>
        </div>

        <!-- 文件信息 -->
        <div v-if="selectedFile" class="mt-6">
          <div class="flex items-center justify-between p-4 bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-blue-50 rounded-lg flex items-center justify-center">
                <DocumentIcon class="w-6 h-6 text-blue-500" />
              </div>
              <div class="flex flex-col">
                <span class="text-sm font-medium text-gray-900">{{ selectedFile.name }}</span>
                <span class="text-xs text-gray-500">{{ formatFileSize(selectedFile.size) }}</span>
              </div>
            </div>
            <button
              @click="clearFile"
              class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 text-gray-400 hover:text-gray-600 transition-colors"
            >
              <XMarkIcon class="w-5 h-5" />
            </button>
          </div>
        </div>

        <!-- 导入进度 -->
        <div v-if="importing" class="mt-6">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-medium text-gray-700">正在解析文件...</span>
            <span class="text-sm font-medium text-blue-500">{{ importProgress }}%</span>
          </div>
          <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
            <div
              class="h-full bg-gradient-to-r from-blue-400 to-blue-500 rounded-full transition-all duration-300 ease-out"
              :style="{ width: importProgress + '%' }"
            ></div>
          </div>
        </div>
      </div>

      <!-- 对话框底部按钮 -->
      <template #footer>
        <div class="flex justify-end space-x-3 px-6 pb-6">
          <el-button 
            @click="closeDialog"
            class="!px-6 !h-10 !rounded-lg border !border-gray-200 !text-gray-700 hover:!bg-gray-50"
          >
            取消
          </el-button>
          <el-button
            type="primary"
            @click="handleImport(selectedFile)"
            :loading="importing"
            :disabled="!selectedFile"
            class="!px-6 !h-10 !rounded-lg !bg-blue-500 hover:!bg-blue-600 !border-none"
          >
            {{ importing ? '导入中...' : '开始导入' }}
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 预览对话框 -->
    <el-dialog
      v-model="showPreviewDialog"
      title="导入预览"
      width="800px"
      :close-on-click-modal="false"
      class="resume-preview-dialog"
    >
      <div class="p-6">
        <div class="space-y-8">
          <!-- 基本信息 -->
          <div v-if="previewData?.basic_info" class="preview-section">
            <div class="flex items-center space-x-2 mb-4">
              <UserIcon class="w-5 h-5 text-blue-500" />
              <h3 class="text-lg font-medium text-gray-900">基本信息</h3>
            </div>
            <div class="grid grid-cols-2 gap-6">
              <!-- 头像显示 -->
              <div v-if="previewData.basic_info.avatar" class="col-span-2 mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-2">头像</label>
                <div class="relative group">
                  <img 
                    :src="previewData.basic_info.avatar" 
                    class="w-32 h-32 object-cover rounded-xl shadow-sm group-hover:shadow-md transition-shadow"
                    alt="用户头像"
                  />
                </div>
              </div>
              <!-- 个人简介 -->
              <div v-if="previewData.basic_info.personal_summary" class="col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-2">个人简介</label>
                <textarea
                  v-model="previewData.basic_info.personal_summary"
                  rows="3"
                  class="block w-full rounded-lg border-gray-200 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm"
                ></textarea>
              </div>
              <!-- 其他基本信息 -->
              <div v-for="(value, key) in previewData.basic_info" :key="key" class="space-y-1">
                <template v-if="!['avatar', 'personal_summary'].includes(key)">
                  <label class="block text-sm font-medium text-gray-700">{{ getFieldLabel('basic_info', key) }}</label>
                  <input
                    type="text"
                    v-model="previewData.basic_info[key]"
                    class="block w-full rounded-lg border-gray-200 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm"
                  />
                </template>
              </div>
            </div>
          </div>

          <!-- 工作经历 -->
          <div v-if="previewData?.work_experiences?.length" class="preview-section">
            <div class="flex items-center space-x-2 mb-4">
              <BriefcaseIcon class="w-5 h-5 text-blue-500" />
              <h3 class="text-lg font-medium text-gray-900">工作经历</h3>
            </div>
            <div v-for="(exp, index) in previewData.work_experiences" :key="index" class="mb-6 p-6 bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
              <div class="grid grid-cols-2 gap-6">
                <div v-for="(value, key) in exp" :key="key" class="space-y-1">
                  <label class="block text-sm font-medium text-gray-700">{{ getFieldLabel('work_experience', key) }}</label>
                  <div class="mt-1">
                    <input
                      v-if="!['description', 'achievements', 'technologies'].includes(key)"
                      type="text"
                      v-model="previewData.work_experiences[index][key]"
                      class="block w-full rounded-lg border-gray-200 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm"
                    />
                    <textarea
                      v-else
                      v-model="previewData.work_experiences[index][key]"
                      rows="3"
                      class="block w-full rounded-lg border-gray-200 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm"
                    ></textarea>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 教育经历 -->
          <div v-if="previewData?.educations?.length" class="preview-section">
            <div class="flex items-center space-x-2 mb-4">
              <AcademicCapIcon class="w-5 h-5 text-blue-500" />
              <h3 class="text-lg font-medium text-gray-900">教育经历</h3>
            </div>
            <div v-for="(edu, index) in previewData.educations" :key="index" class="mb-6 p-6 bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
              <div class="grid grid-cols-2 gap-6">
                <div v-for="(value, key) in edu" :key="key" class="space-y-1">
                  <label class="block text-sm font-medium text-gray-700">{{ getFieldLabel('education', key) }}</label>
                  <div class="mt-1">
                    <input
                      v-if="!['description', 'achievements'].includes(key)"
                      type="text"
                      v-model="previewData.educations[index][key]"
                      class="block w-full rounded-lg border-gray-200 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm"
                    />
                    <textarea
                      v-else
                      v-model="previewData.educations[index][key]"
                      rows="3"
                      class="block w-full rounded-lg border-gray-200 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm"
                    ></textarea>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 项目经历 -->
          <div v-if="previewData?.projects?.length" class="preview-section">
            <div class="flex items-center space-x-2 mb-4">
              <RocketLaunchIcon class="w-5 h-5 text-blue-500" />
              <h3 class="text-lg font-medium text-gray-900">项目经历</h3>
            </div>
            <div v-for="(proj, index) in previewData.projects" :key="index" class="mb-6 p-6 bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
              <div class="grid grid-cols-2 gap-6">
                <div v-for="(value, key) in proj" :key="key" class="space-y-1">
                  <label class="block text-sm font-medium text-gray-700">{{ getFieldLabel('project', key) }}</label>
                  <div class="mt-1">
                    <input
                      v-if="!['description', 'achievement'].includes(key)"
                      type="text"
                      v-model="previewData.projects[index][key]"
                      class="block w-full rounded-lg border-gray-200 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm"
                    />
                    <textarea
                      v-else
                      v-model="previewData.projects[index][key]"
                      rows="3"
                      class="block w-full rounded-lg border-gray-200 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm"
                    ></textarea>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 技能特长 -->
          <div v-if="previewData?.skills?.length" class="preview-section">
            <div class="flex items-center space-x-2 mb-4">
              <LightBulbIcon class="w-5 h-5 text-blue-500" />
              <h3 class="text-lg font-medium text-gray-900">技能特长</h3>
            </div>
            <div class="p-6 bg-white rounded-xl border border-gray-100 shadow-sm">
              <div class="flex flex-wrap gap-2">
                <div v-for="(skill, index) in previewData.skills" :key="index" 
                  class="inline-flex items-center px-4 py-2 rounded-lg text-sm bg-blue-50 text-blue-700 hover:bg-blue-100 transition-colors">
                  {{ skill.name }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 预览对话框底部按钮 -->
      <template #footer>
        <div class="flex justify-end space-x-3 px-6 pb-6">
          <el-button 
            @click="showPreviewDialog = false"
            class="!px-6 !h-10 !rounded-lg border !border-gray-200 !text-gray-700 hover:!bg-gray-50"
          >
            取消
          </el-button>
          <el-button
            type="primary"
            @click="confirmImport"
            :loading="importing"
            class="!px-6 !h-10 !rounded-lg !bg-blue-500 hover:!bg-blue-600 !border-none"
          >
            确认导入
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, watch, onUnmounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import {
  DocumentArrowUpIcon,
  DocumentIcon,
  XMarkIcon,
  UserIcon,
  BriefcaseIcon,
  AcademicCapIcon,
  RocketLaunchIcon,
  LightBulbIcon
} from '@heroicons/vue/24/outline'
import profile from '@/api/profile'
import { eventBus } from '@/utils/eventBus'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'success'])

// 对话框显示状态
const dialogVisible = ref(false)

// 监听 modelValue 变化
watch(() => props.modelValue, (val) => {
  dialogVisible.value = val
})

// 监听对话框状态变化
watch(() => dialogVisible.value, (val) => {
  emit('update:modelValue', val)
})

// 关闭对话框
const closeDialog = () => {
  dialogVisible.value = false
  // 清除已选文件
  clearFile()
}

// 组件状态
const showImportDialog = ref(false)
const showPreviewDialog = ref(false)
const fileInput = ref(null)
const selectedFile = ref(null)
const importing = ref(false)
const importProgress = ref(0)
const previewData = ref(null)

// 添加模拟进度的定时器
const progressTimer = ref(null)

// 开始模拟进度
const startProgressSimulation = () => {
  importProgress.value = 0
  progressTimer.value = setInterval(() => {
    if (importProgress.value < 90) {
      // 前30%快速增加
      if (importProgress.value < 30) {
        importProgress.value += 5
      } 
      // 30-60%中速增加
      else if (importProgress.value < 60) {
        importProgress.value += 2
      }
      // 60-90%慢速增加
      else {
        importProgress.value += 0.5
      }
    }
  }, 1000)
}

// 停止模拟进度
const stopProgressSimulation = () => {
  if (progressTimer.value) {
    clearInterval(progressTimer.value)
    progressTimer.value = null
  }
}

// 字段标签映射
const fieldLabels = {
  basic_info: {
    name: '姓名',
    gender: '性别',
    birth_date: '出生日期',
    phone: '手机号',
    email: '邮箱',
    location: '所在地',
    personal_summary: '个人简介',
    avatar: '头像'
  },
  work_experience: {
    company: '公司名称',
    position: '职位',
    department: '部门',
    start_date: '入职时间',
    end_date: '离职时间',
    is_current: '是否在职',
    description: '工作描述',
    achievements: '工作成就',
    technologies: '技术栈'
  },
  education: {
    school: '学校名称',
    major: '专业',
    degree: '学历',
    start_date: '入学时间',
    end_date: '毕业时间',
    is_current: '是否在读',
    description: '在校经历',
    achievements: '在校成就'
  },
  project: {
    name: '项目名称',
    role: '担任角色',
    start_date: '开始日期',
    end_date: '结束日期',
    is_current: '是否进行中',
    description: '项目描述',
    achievement: '项目成果'
  },
  skill: {
    name: '技能名称',
    level: '熟练程度',
    description: '技能描述',
    projects: '相关项目'
  },
  language: {
    name: '语言名称',
    proficiency: '熟练程度',
    certification: '语言证书',
    score: '考试分数'
  },
  social_link: {
    platform: '平台名称',
    url: '链接地址',
    description: '链接描述'
  }
}

// 获取字段标签
const getFieldLabel = (module, key) => {
  return fieldLabels[module]?.[key] || key
}

// 触发文件选择
const triggerFileInput = () => {
  fileInput.value.click()
}

// 处理文件拖放
const handleDrop = (event) => {
  const file = event.dataTransfer.files[0]
  if (validateFile(file)) {
    selectedFile.value = file
  }
}

// 处理文件选择
const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (validateFile(file)) {
    selectedFile.value = file
  }
}

// 格式化文件大小
const formatFileSize = (bytes) => {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
}

// 验证文件
const validateFile = (file) => {
  const allowedTypes = [
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/pdf',
    'image/jpeg',
    'image/png'
  ]
  
  if (!allowedTypes.includes(file.type)) {
    ElMessage.error('请上传 Word、PDF 或图片格式的文件')
    return false
  }
  
  const maxSize = 10 * 1024 * 1024 // 10MB
  if (file.size > maxSize) {
    ElMessage.error('文件大小不能超过 10MB')
    return false
  }
  
  return true
}

// 清除已选文件
const clearFile = () => {
  selectedFile.value = null
  fileInput.value.value = ''
}

// 处理导入
const handleImport = async (file) => {
  try {
    importing.value = true
    importProgress.value = 10
    
    const formData = new FormData()
    formData.append('file', file)
    // 添加 need_avatar 参数，启用头像解析
    formData.append('need_avatar', '1')
    
    const response = await profile.parseResume(formData)
    console.log('原始响应:', response)
    console.log('响应数据:', response.data)
    
    if (response.data) {
      const data = response.data.data || response.data
      console.log('处理前的数据:', JSON.stringify(data, null, 2))
      
      // 处理基本信息
      if (!data.basic_info) {
        data.basic_info = {}
      }
      
      // 处理头像数据 - 从 result 字段获取
      let avatarData = null;
      if (data.result) {
        avatarData = data.result.avatar_data || data.result.avatar_url;
      }
      
      console.log('找到的头像数据:', avatarData);
      
      // 设置头像数据
      if (avatarData) {
        // 如果是 base64 格式的图片数据，直接使用
        if (typeof avatarData === 'string') {
          if (avatarData.startsWith('data:image')) {
            data.basic_info.avatar = avatarData;
          } else if (avatarData.startsWith('http')) {
            // 如果是 URL，直接使用
            data.basic_info.avatar = avatarData;
          } else {
            // 如果是纯 base64 数据，添加前缀
            data.basic_info.avatar = `data:image/jpeg;base64,${avatarData}`;
          }
        }
      }
      
      console.log('头像数据处理结果:', data.basic_info.avatar);
      
      // 确保所有必要的字段都存在，并使用正确的字段名
      data.basic_info = {
        ...data.basic_info,
        name: data.basic_info.name || '',
        gender: data.basic_info.gender || '',
        birth_date: data.basic_info.birth_date || '',
        phone: data.basic_info.phone || '',
        email: data.basic_info.email || '',
        location: data.basic_info.location || '',
        personal_summary: data.basic_info.summary || 
                data.basic_info.personal_summary || 
                data.basic_info.description || 
                data.basic_info.self_evaluation || '',
        avatar: data.basic_info.avatar || ''
      }
      
      console.log('处理后的基本信息:', data.basic_info);
      
      // 处理教育经历，确保使用正确的字段名 educations
      let eduData = data.education || data.educations || []
      if (!Array.isArray(eduData)) {
        eduData = [eduData]
      }
      data.educations = eduData.map(edu => ({
        school: edu.school || edu.university || edu.institution || '',
        major: edu.major || edu.speciality || '',
        degree: edu.degree || edu.education_level || '',
        start_date: formatDate(edu.start_date),
        end_date: formatDate(edu.end_date),
        is_current: edu.is_current || false,
        description: edu.description || '',
        achievements: edu.achievements || ''
      }))
      // 删除旧的 education 字段
      delete data.education
      
      // 处理工作经验
      let workExp = data.work_experiences || data.work_experience || []
      if (!Array.isArray(workExp)) {
        workExp = [workExp]
      }
      data.work_experiences = workExp.map(work => ({
        company: work.company || '',
        position: work.position || '',
        department: work.department || '',
        start_date: formatDate(work.start_date),
        end_date: formatDate(work.end_date),
        is_current: work.is_current || false,
        description: work.description || '',
        achievements: work.achievements || '',
        technologies: work.technologies || ''
      }))
      
      // 处理项目经验
      let projects = data.projects || data.project || []
      if (!Array.isArray(projects)) {
        projects = [projects]
      }
      data.projects = projects.map(proj => ({
        name: proj.name || '',
        role: proj.role || '',
        start_date: formatDate(proj.start_date),
        end_date: formatDate(proj.end_date),
        is_current: proj.is_current || false,
        description: proj.description || '',
        achievement: proj.achievement || ''
      }))
      
      // 处理技能
      let skills = data.skills || data.skill || []
      if (!Array.isArray(skills)) {
        skills = [skills]
      }
      data.skills = skills.slice(0, 5).map(skill => {
        if (typeof skill === 'string') {
          return {
            name: skill.slice(0, 50),
            level: '熟练',
            description: '',
            projects: []
          }
        }
        return {
          name: (skill.name || '').slice(0, 50),
          level: skill.level || '熟练',
          description: (skill.description || '').slice(0, 500),
          projects: Array.isArray(skill.projects) ? skill.projects.slice(0, 3) : []
        }
      })
      
      console.log('最终处理后的数据:', JSON.stringify(data, null, 2))
      previewData.value = data
      importProgress.value = 100
      importing.value = false
      dialogVisible.value = false
      await nextTick()
      showPreviewDialog.value = true
      ElMessage.success('简历解析成功，请确认数据后导入')
    }
  } catch (error) {
    console.error('简历解析失败:', error)
    ElMessage.error('简历解析失败，请稍后重试')
    importing.value = false
    importProgress.value = 0
  }
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return null
  // 处理 YYYY.MM 格式
  if (/^\d{4}\.\d{2}$/.test(dateStr)) {
    return `${dateStr.replace('.', '-')}-01`
  }
  // 处理 YYYY 格式
  if (/^\d{4}$/.test(dateStr)) {
    return `${dateStr}-01-01`
  }
  return dateStr
}

// 处理所有日期字段和格式化数据
const formatDates = (data) => {
  if (!data) return data
  
  // 深拷贝数据以避免直接修改预览数据
  const formattedData = JSON.parse(JSON.stringify(data))
  
  // 处理工作经历日期
  if (formattedData.work_experiences) {
    formattedData.work_experiences = formattedData.work_experiences.map(exp => ({
      ...exp,
      start_date: formatDate(exp.start_date),
      end_date: formatDate(exp.end_date)
    }))
  }
  
  // 处理教育经历日期
  if (formattedData.educations) {
    formattedData.educations = formattedData.educations.map(edu => ({
      ...edu,
      start_date: formatDate(edu.start_date),
      end_date: formatDate(edu.end_date)
    }))
  }
  
  // 处理项目经历日期
  if (formattedData.projects) {
    formattedData.projects = formattedData.projects.map(proj => ({
      ...proj,
      start_date: formatDate(proj.start_date),
      end_date: formatDate(proj.end_date)
    }))
  }

  // 处理技能特长格式
  if (formattedData.skills && Array.isArray(formattedData.skills)) {
    formattedData.skills = formattedData.skills.map(skill => {
      if (typeof skill === 'string') {
        return {
          name: skill.slice(0, 50),  // 限制长度为50
          level: '熟练',
          description: '',
          projects: []
        }
      }
      return {
        ...skill,
        name: skill.name.slice(0, 50),  // 限制长度为50
        description: (skill.description || '').slice(0, 500),
        projects: Array.isArray(skill.projects) ? skill.projects.slice(0, 3) : []
      }
    })
  }
  
  return formattedData
}

// 确认导入
const confirmImport = async () => {
  if (!previewData.value) {
    ElMessage.warning('没有可导入的数据')
    return
  }
  
  try {
    importing.value = true
    
    // 格式化日期后再提交
    const formattedData = formatDates(previewData.value)
    console.log('提交前的数据:', JSON.stringify(formattedData, null, 2))
    
    // 确保数据结构正确
    const submitData = {
      basic_info: {
        ...formattedData.basic_info,
        // 确保个人简介和头像字段名称正确
        personal_summary: formattedData.basic_info.personal_summary || '',
        avatar: formattedData.basic_info.avatar || ''
      },
      work_experiences: formattedData.work_experiences || [],
      educations: formattedData.educations || [],
      projects: formattedData.projects || [],
      skills: formattedData.skills || [],
      languages: formattedData.languages || [],
      social_links: formattedData.social_links || []
    }
    
    // 提交导入数据
    const response = await profile.importResumeData(submitData)
    
    if (response.data?.code === 200 || response.status === 200) {
      ElMessage.success('导入成功')
      showPreviewDialog.value = false
      dialogVisible.value = false
      // 触发数据更新事件
      eventBus.emit('profile-updated')
      // 触发完整度更新事件
      eventBus.emit('completeness-updated')
      // 刷新用户信息
      await profile.getData()
      // 触发成功回调
      emit('success')
    } else {
      throw new Error(response.data?.message || '导入失败')
    }
  } catch (error) {
    console.error('数据导入失败:', error)
    ElMessage.error({
      message: error.message || '数据导入失败，请重试',
      duration: 5000,
      showClose: true
    })
  } finally {
    importing.value = false
  }
}

// 监听预览对话框状态变化
watch(() => showPreviewDialog.value, (val) => {
  console.log('预览对话框状态变化:', val)
  console.log('当前预览数据:', previewData.value)
  if (!val) {
    // 如果预览对话框关闭，重置预览数据
    previewData.value = null
    console.log('预览数据已重置')
  }
})

// 组件卸载时清理定时器
onUnmounted(() => {
  stopProgressSimulation()
})
</script>

<style scoped>
.resume-import {
  /* 基础样式 */
}

/* 自定义对话框样式 */
:deep(.el-dialog) {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
}

:deep(.el-dialog__header) {
  margin: 0;
  padding: 20px 24px;
  border-bottom: 1px solid #f3f4f6;
}

:deep(.el-dialog__title) {
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
}

:deep(.el-dialog__headerbtn) {
  top: 20px;
  right: 20px;
}

:deep(.el-dialog__body) {
  padding: 0;
}

:deep(.el-button--primary) {
  --el-button-hover-bg-color: #2563eb;
  --el-button-hover-border-color: #2563eb;
}

/* 预览部分的样式 */
.preview-section {
  background-color: #ffffff;
  border-radius: 1rem;
  overflow: hidden;
}

/* 输入框聚焦时的样式 */
input:focus, textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

/* 添加平滑过渡效果 */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}
</style> 