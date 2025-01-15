<template>
  <div class="resume-import">
    <!-- 导入对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="导入简历"
      width="500px"
      :close-on-click-modal="false"
    >
      <div class="p-4">
        <!-- 上传区域 -->
        <div
          class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center"
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
          <div class="space-y-2">
            <DocumentArrowUpIcon class="w-12 h-12 mx-auto text-gray-400" />
            <div class="text-sm text-gray-600">
              <span class="font-medium text-blue-600 hover:text-blue-500">
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
        <div v-if="selectedFile" class="mt-4">
          <div class="flex items-center justify-between p-2 bg-gray-50 rounded">
            <div class="flex items-center space-x-2">
              <DocumentIcon class="w-5 h-5 text-gray-400" />
              <span class="text-sm text-gray-900">{{ selectedFile.name }}</span>
            </div>
            <button
              @click="clearFile"
              class="text-gray-400 hover:text-gray-500"
            >
              <XMarkIcon class="w-5 h-5" />
            </button>
          </div>
        </div>

        <!-- 导入进度 -->
        <div v-if="importing" class="mt-4">
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-500">正在解析文件...</span>
            <span class="text-sm text-gray-500">{{ importProgress }}%</span>
          </div>
          <div class="mt-2 h-2 bg-gray-200 rounded-full">
            <div
              class="h-2 bg-blue-600 rounded-full transition-all duration-300"
              :style="{ width: importProgress + '%' }"
            ></div>
          </div>
        </div>
      </div>

      <!-- 对话框底部按钮 -->
      <template #footer>
        <div class="flex justify-end space-x-3">
          <el-button @click="closeDialog">取消</el-button>
          <el-button
            type="primary"
            @click="handleImport(selectedFile)"
            :loading="importing"
            :disabled="!selectedFile"
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
    >
      <div class="p-4">
        <div class="space-y-6">
          <!-- 基本信息 -->
          <div v-if="previewData?.basic_info">
            <h3 class="text-sm font-medium text-gray-900 mb-3">基本信息</h3>
            <div class="grid grid-cols-2 gap-4">
              <!-- 头像显示 -->
              <div v-if="previewData.basic_info.avatar" class="col-span-2 mb-4">
                <label class="block text-xs text-gray-500">头像</label>
                <div class="mt-1">
                  <img 
                    :src="previewData.basic_info.avatar" 
                    class="w-32 h-32 object-cover rounded-lg border border-gray-200"
                    alt="用户头像"
                  />
                </div>
              </div>
              <!-- 个人简介 -->
              <div v-if="previewData.basic_info.personal_summary" class="col-span-2">
                <label class="block text-xs text-gray-500">个人简介</label>
                <div class="mt-1">
                  <textarea
                    v-model="previewData.basic_info.personal_summary"
                    rows="3"
                    class="block w-full border-gray-300 rounded-md shadow-sm text-sm"
                  ></textarea>
                </div>
              </div>
              <!-- 其他基本信息 -->
              <div v-for="(value, key) in previewData.basic_info" :key="key">
                <template v-if="!['avatar', 'personal_summary'].includes(key)">
                  <label class="block text-xs text-gray-500">{{ getFieldLabel('basic_info', key) }}</label>
                  <div class="mt-1">
                    <input
                      type="text"
                      v-model="previewData.basic_info[key]"
                      class="block w-full border-gray-300 rounded-md shadow-sm text-sm"
                    />
                  </div>
                </template>
              </div>
            </div>
          </div>

          <!-- 工作经历 -->
          <div v-if="previewData?.work_experiences?.length">
            <h3 class="text-sm font-medium text-gray-900 mb-3">工作经历</h3>
            <div v-for="(exp, index) in previewData.work_experiences" :key="index" class="mb-4 p-4 border rounded-lg">
              <div class="grid grid-cols-2 gap-4">
                <div v-for="(value, key) in exp" :key="key">
                  <label class="block text-xs text-gray-500">{{ getFieldLabel('work_experience', key) }}</label>
                  <div class="mt-1">
                    <input
                      v-if="!['description', 'achievements', 'technologies'].includes(key)"
                      type="text"
                      v-model="previewData.work_experiences[index][key]"
                      class="block w-full border-gray-300 rounded-md shadow-sm text-sm"
                    />
                    <textarea
                      v-else
                      v-model="previewData.work_experiences[index][key]"
                      rows="3"
                      class="block w-full border-gray-300 rounded-md shadow-sm text-sm"
                    ></textarea>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 教育经历 -->
          <div v-if="previewData?.educations?.length">
            <h3 class="text-sm font-medium text-gray-900 mb-3">教育经历</h3>
            <div v-for="(edu, index) in previewData.educations" :key="index" class="mb-4 p-4 border rounded-lg">
              <div class="grid grid-cols-2 gap-4">
                <div v-for="(value, key) in edu" :key="key">
                  <label class="block text-xs text-gray-500">{{ getFieldLabel('education', key) }}</label>
                  <div class="mt-1">
                    <input
                      v-if="!['description', 'achievements'].includes(key)"
                      type="text"
                      v-model="previewData.educations[index][key]"
                      class="block w-full border-gray-300 rounded-md shadow-sm text-sm"
                    />
                    <textarea
                      v-else
                      v-model="previewData.educations[index][key]"
                      rows="3"
                      class="block w-full border-gray-300 rounded-md shadow-sm text-sm"
                    ></textarea>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 项目经历 -->
          <div v-if="previewData?.projects?.length">
            <h3 class="text-sm font-medium text-gray-900 mb-3">项目经历</h3>
            <div v-for="(proj, index) in previewData.projects" :key="index" class="mb-4 p-4 border rounded-lg">
              <div class="grid grid-cols-2 gap-4">
                <div v-for="(value, key) in proj" :key="key">
                  <label class="block text-xs text-gray-500">{{ getFieldLabel('project', key) }}</label>
                  <div class="mt-1">
                    <input
                      v-if="!['description', 'achievement'].includes(key)"
                      type="text"
                      v-model="previewData.projects[index][key]"
                      class="block w-full border-gray-300 rounded-md shadow-sm text-sm"
                    />
                    <textarea
                      v-else
                      v-model="previewData.projects[index][key]"
                      rows="3"
                      class="block w-full border-gray-300 rounded-md shadow-sm text-sm"
                    ></textarea>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 技能特长 -->
          <div v-if="previewData?.skills?.length">
            <h3 class="text-sm font-medium text-gray-900 mb-3">技能特长</h3>
            <div class="p-4 border rounded-lg">
              <div class="flex flex-wrap gap-2">
                <div v-for="(skill, index) in previewData.skills" :key="index" 
                  class="inline-flex items-center px-3 py-1 rounded-full text-sm bg-gray-100">
                  {{ skill.name }}
                </div>
              </div>
            </div>
          </div>

          <!-- 学习经历 -->
          <div v-if="previewData?.studies?.length">
            <h3 class="text-sm font-medium text-gray-900 mb-3">学习经历</h3>
            <div v-for="(study, index) in previewData.studies" :key="index" class="mb-4 p-4 border rounded-lg">
              <div class="grid grid-cols-2 gap-4">
                <div v-for="(value, key) in study" :key="key">
                  <label class="block text-xs text-gray-500">{{ getFieldLabel('study', key) }}</label>
                  <div class="mt-1">
                    <input
                      v-if="!['description'].includes(key)"
                      type="text"
                      v-model="previewData.studies[index][key]"
                      class="block w-full border-gray-300 rounded-md shadow-sm text-sm"
                    />
                    <textarea
                      v-else
                      v-model="previewData.studies[index][key]"
                      rows="3"
                      class="block w-full border-gray-300 rounded-md shadow-sm text-sm"
                    ></textarea>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 语言能力 -->
          <div v-if="previewData?.languages?.length">
            <h3 class="text-sm font-medium text-gray-900 mb-3">语言能力</h3>
            <div v-for="(lang, index) in previewData.languages" :key="index" class="mb-4 p-4 border rounded-lg">
              <div class="grid grid-cols-2 gap-4">
                <div v-for="(value, key) in lang" :key="key">
                  <label class="block text-xs text-gray-500">{{ getFieldLabel('language', key) }}</label>
                  <div class="mt-1">
                    <input
                      type="text"
                      v-model="previewData.languages[index][key]"
                      class="block w-full border-gray-300 rounded-md shadow-sm text-sm"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 社交主页 -->
          <div v-if="previewData?.social_links?.length">
            <h3 class="text-sm font-medium text-gray-900 mb-3">社交主页</h3>
            <div v-for="(link, index) in previewData.social_links" :key="index" class="mb-4 p-4 border rounded-lg">
              <div class="grid grid-cols-2 gap-4">
                <div v-for="(value, key) in link" :key="key">
                  <label class="block text-xs text-gray-500">{{ getFieldLabel('social_link', key) }}</label>
                  <div class="mt-1">
                    <input
                      v-if="!['description'].includes(key)"
                      type="text"
                      v-model="previewData.social_links[index][key]"
                      class="block w-full border-gray-300 rounded-md shadow-sm text-sm"
                    />
                    <textarea
                      v-else
                      v-model="previewData.social_links[index][key]"
                      rows="3"
                      class="block w-full border-gray-300 rounded-md shadow-sm text-sm"
                    ></textarea>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 预览对话框底部按钮 -->
      <template #footer>
        <div class="flex justify-end space-x-3">
          <el-button @click="showPreviewDialog = false">取消</el-button>
          <el-button
            type="primary"
            @click="confirmImport"
            :loading="importing"
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
  XMarkIcon
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
  /* 添加需要的样式 */
}
</style> 