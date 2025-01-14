<!-- src/views/user/MyProfile/index.vue -->
<template>
  <div class="container mx-auto pb-6">
    <div class="max-w-4xl mx-auto space-y-4">
      <!-- 顶部提示横幅 -->
      <div v-if="!hideWelcomeBanner" class="bg-gradient-to-r from-blue-500 to-indigo-600 rounded-lg shadow-lg overflow-hidden relative">
        <div class="px-4 py-5 sm:p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <DocumentTextIcon class="h-6 w-6 text-white" />
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-medium text-white">欢迎来到简历档案</h3>
              <div class="mt-1">
                <p class="text-sm text-blue-100">
                  这里是您的专业简历信息管理中心，完善的档案信息将帮助您生成更出色的简历。请注意，这里的信息与您在社区中展示的个人主页是分开的，专注于求职场景使用。
                </p>
              </div>
            </div>
          </div>
        </div>
        <!-- 关闭按钮 -->
        <button 
          @click="closeWelcomeBanner"
          class="absolute top-2 right-2 p-1 text-white/80 hover:text-white transition-colors"
        >
          <XMarkIcon class="w-5 h-5" />
        </button>
      </div>

      <!-- 基本信息 -->
      <BasicInfo
        :resumeData="profileData?.basic_info"
        :loading="profileLoading"
        :bioExpanded="bioExpanded"
        :showBioExpandButton="showBioExpandButton"
        @edit="handleEdit"
        @update="handleUpdate"
        @toggleBioExpand="toggleBioExpand"
      />


      <!-- 简历状态 -->
      <ResumeStatus
        :completion-data="completionData"
        :profile-data="profileData"
        :loading="profileLoading"
      />

      <!-- 激活的模块列表 -->
      <ModuleList
        :active-modules="activeModules"
        :inactive-modules="inactiveModules"
        :loading="modulesLoading"
        :fetch-modules-data="fetchModulesData"
        @edit="handleEdit"
        @add="handleAdd"
        @remove="handleModuleRemove"
        @delete="handleDelete"
      />

      <!-- 未激活的模块按钮组 -->
      <div v-if="inactiveModules.length > 0" class="bg-white rounded-lg shadow">
        <div class="px-4 py-3">
          <h3 class="text-sm font-medium text-gray-900">添加更多模块</h3>
          <div class="mt-3 flex flex-wrap gap-2">
            <button
              v-for="module in inactiveModules"
              :key="module.type"
              @click="handleAddModule(module.type)"
              class="inline-flex items-center px-3 py-1.5 text-sm text-gray-600 bg-gray-50 hover:bg-gray-100 rounded border border-gray-200"
            >
              {{ getModuleName(module.type) }}
              <PlusIcon class="w-4 h-4 ml-1 text-gray-400" />
            </button>
          </div>
        </div>
      </div>

      <!-- 工作经历编辑弹窗 -->
      <EditWorkExperienceDialog
        v-model="showWorkExperienceDialog"
        :initial-data="editWorkExperienceData"
        :loading="profileLoading"
        @submit="handleWorkExperienceSubmit"
      />

      <!-- 求职意向编辑弹窗 -->
      <EditJobIntentionDialog
        v-model="showJobIntentionDialog"
        :initial-data="editJobIntentionData"
        :loading="profileLoading"
        @submit="handleJobIntentionSubmit"
      />

      <!-- 基本信息编辑弹窗 -->
      <EditBasicDialog
        v-if="currentModule?.type === 'basic_info'"
        v-model="showEditModal"
        :initial-data="editFormData"
        :loading="profileLoading"
        @submit="handleSubmit"
      />

      <!-- AI 优化弹窗 -->
      <AIOptimizeDialog
        v-model="showAIOptimizeDialog"
        :profile-data="profileData"
        @apply="handleAIOptimize"
      />

      <!-- 删除确认弹窗 -->
      <TransitionRoot appear :show="!!showDeleteConfirmDialog" as="div">
        <Dialog as="div" class="relative z-50" @close="closeDeleteConfirm">
          <TransitionChild
            as="div"
            :show="true"
            enter="duration-300 ease-out"
            enter-from="opacity-0"
            enter-to="opacity-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100"
            leave-to="opacity-0"
          >
            <div class="fixed inset-0 bg-black/25" />
          </TransitionChild>

          <div class="fixed inset-0 overflow-y-auto">
            <div class="flex min-h-full items-center justify-center p-4 text-center">
              <TransitionChild
                as="div"
                :show="true"
                enter="duration-300 ease-out"
                enter-from="opacity-0 scale-95"
                enter-to="opacity-100 scale-100"
                leave="duration-200 ease-in"
                leave-from="opacity-100 scale-100"
                leave-to="opacity-0 scale-95"
              >
                <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-xl bg-white text-left align-middle shadow-xl transition-all">
                  <div class="p-6">
                    <div class="flex items-start space-x-3">
                      <div class="p-2 bg-red-50 rounded-full flex-shrink-0">
                        <ExclamationTriangleIcon class="w-6 h-6 text-red-600" />
                      </div>
                      <div class="flex-1">
                        <DialogTitle as="h3" class="text-lg font-medium text-gray-900">
                          确认删除工作经历？
                        </DialogTitle>
                        <p class="mt-2 text-sm text-gray-500">
                          删除后将无法恢复，请确认是否继续。
                        </p>
                      </div>
                    </div>
                    
                    <div class="mt-6 flex justify-end space-x-3">
                      <button
                        type="button"
                        @click="closeDeleteConfirm"
                        class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
                      >
                        取消
                      </button>
                      <button
                        type="button"
                        @click="confirmDelete"
                        class="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                      >
                        确认删除
                      </button>
                    </div>
                  </div>
                </DialogPanel>
              </TransitionChild>
            </div>
          </div>
        </Dialog>
      </TransitionRoot>

      <!-- 教育经历编辑弹窗 -->
      <EditEducationDialog
        v-model="showEducationDialog"
        :initial-data="editEducationData"
        :loading="profileLoading"
        @submit="handleEducationSubmit"
      />

      <!-- 项目经历编辑弹窗 -->
      <EditProjectDialog
        v-model="showProjectDialog"
        :initial-data="editProjectData"
        :loading="profileLoading"
        @submit="handleProjectSubmit"
      />

      <!-- 证书奖项编辑弹窗 -->
      <EditCertificateDialog
        v-model="showCertificateDialog"
        :initial-data="editCertificateData"
        :loading="profileLoading"
        @submit="handleCertificateSubmit"
      />

      <!-- 专业技能编辑弹窗 -->
      <EditSkillDialog
        v-model="showSkillDialog"
        :initial-data="editSkillData"
        :loading="profileLoading"
        @submit="handleSkillSubmit"
      />

      <!-- 语言能力编辑弹窗 -->
      <EditLanguageDialog
        v-model="showLanguageDialog"
        :initial-data="editLanguageData"
        :loading="profileLoading"
        @submit="handleLanguageSubmit"
      />

      <!-- 社交主页编辑弹窗 -->
      <EditSocialLinkDialog
        v-if="currentModule?.type === 'social_link'"
        v-model="showEditModal"
        :initial-data="editFormData"
        :loading="loading"
        @submit="handleSubmit"
      />
      
      <!-- 作品展示编辑弹窗 -->
      <EditPortfolioDialog
        v-if="currentModule?.type === 'portfolio'"
        v-model="showEditModal"
        :initial-data="editFormData"
        :loading="loading"
        @submit="handleSubmit"
      />

      <!-- 确认对话框 -->
      <TransitionRoot appear :show="showConfirmDialog" as="template">
        <Dialog as="div" class="relative z-50" @close="showConfirmDialog = false">
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0"
            enter-to="opacity-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100"
            leave-to="opacity-0"
          >
            <div class="fixed inset-0 bg-black/25" />
          </TransitionChild>

          <div class="fixed inset-0 overflow-y-auto">
            <div class="flex min-h-full items-center justify-center p-4 text-center">
              <TransitionChild
                as="template"
                enter="duration-300 ease-out"
                enter-from="opacity-0 scale-95"
                enter-to="opacity-100 scale-100"
                leave="duration-200 ease-in"
                leave-from="opacity-100 scale-100"
                leave-to="opacity-0 scale-95"
              >
                <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                  <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900">
                    确认操作
                  </DialogTitle>
                  <div class="mt-2">
                    <p class="text-sm text-gray-500">
                      {{ confirmMessage }}
                    </p>
                  </div>

                  <div class="mt-4 flex justify-end space-x-3">
                    <button
                      type="button"
                      class="inline-flex justify-center rounded-md border border-transparent bg-gray-100 px-4 py-2 text-sm font-medium text-gray-900 hover:bg-gray-200"
                      @click="showConfirmDialog = false"
                    >
                      取消
                    </button>
                    <button
                      type="button"
                      class="inline-flex justify-center rounded-md border border-transparent bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700"
                      @click="handleConfirm"
                    >
                      确认
                    </button>
                  </div>
                </DialogPanel>
              </TransitionChild>
            </div>
          </div>
        </Dialog>
      </TransitionRoot>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, nextTick, onUnmounted } from 'vue'
import { useModules } from '@/composables/useModules'
import { useProfileData } from '@/composables/useProfileData'
import useLoading from '@/composables/useLoading'
import profile from '@/api/profile'
import { ElMessage } from 'element-plus'
import { eventBus } from '@/utils/eventBus'
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionChild,
  TransitionRoot
} from '@headlessui/vue'
import {
  PlusIcon,
  ExclamationTriangleIcon,
  DocumentTextIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'
import { ALL_MODULES } from '@/constants'

// 组件导入
import BasicInfo from './components/BasicInfo.vue'
import ResumeStatus from './components/ResumeStatus.vue'
import ModuleList from './components/ModuleList.vue'
import EditWorkExperienceDialog from './dialogs/EditWorkExperienceDialog.vue'
import EditBasicDialog from './dialogs/EditBasicDialog.vue'
import EditJobIntentionDialog from './dialogs/EditJobIntentionDialog.vue'
import EditSocialLinkDialog from './dialogs/EditSocialLinkDialog.vue'
import EditPortfolioDialog from './dialogs/EditPortfolioDialog.vue'
import AIOptimizeDialog from './dialogs/AIOptimizeDialog.vue'
import EditEducationDialog from './dialogs/EditEducationDialog.vue'
import EditProjectDialog from './dialogs/EditProjectDialog.vue'
import EditCertificateDialog from './dialogs/EditCertificateDialog.vue'
import EditSkillDialog from './dialogs/EditSkillDialog.vue'
import EditLanguageDialog from './dialogs/EditLanguageDialog.vue'


// 获取数据相关
const profileLoading = ref(false)
const profileData = ref(null)
const completionData = ref(null)
const bioExpanded = ref(false)
const showBioExpandButton = ref(false)

// 布局数据
const layoutData = ref({})

// 布局状态
const layoutStatus = computed(() => {
  return layoutData.value || {}
})

// 使用组合式函数
const { 
  loading: modulesLoading,
  modules,
  fetchModulesData
} = useModules(layoutData)

const {
  fetchCompletionData
} = useProfileData()

// 使用 loading 组合式函数
const { loading, withLoading } = useLoading()

// 当前编辑的模块
const currentModule = ref(null)
const editFormData = ref({})
const showEditModal = ref(false)

// 弹窗状态
const showWorkExperienceDialog = ref(false)
const showJobIntentionDialog = ref(false)
const editJobIntentionData = ref({})
const editWorkExperienceData = ref({})
const showAIOptimizeDialog = ref(false)
const showEducationDialog = ref(false)
const editEducationData = ref({})
const showProjectDialog = ref(false)
const editProjectData = ref({})
const showCertificateDialog = ref(false)
const editCertificateData = ref({})
const showSkillDialog = ref(false)
const editSkillData = ref({})
const showLanguageDialog = ref(false)
const editLanguageData = ref({})

// 确认对话框状态
const showConfirmDialog = ref(false)
const confirmMessage = ref('')
const confirmCallback = ref(null)

// 显示确认对话框
const showConfirm = (message, callback) => {
  confirmMessage.value = message
  confirmCallback.value = callback
  showConfirmDialog.value = true
}

// 处理确认
const handleConfirm = async () => {
  if (confirmCallback.value) {
    await confirmCallback.value()
  }
  showConfirmDialog.value = false
}

// 计算激活的模块
const activeModules = computed(() => {
  if (!modules.value) return []
  const active = modules.value.filter(module => {
    // 只显示布局中明确设置为 visible: true 的模块
    const layout = layoutData.value[module.type]
    return layout?.visible === true
  }).sort((a, b) => {
    const orderA = layoutData.value[a.type]?.order || 999
    const orderB = layoutData.value[b.type]?.order || 999
    return orderA - orderB
  })
  return active
})

// 计算未激活的模块
const inactiveModules = computed(() => {
  if (!modules.value) return []
  const inactive = modules.value.filter(module => {
    // 只显示布局中明确设置为 visible: false 的模块
    const layout = layoutData.value[module.type]
    return layout?.visible === false
  })
  return inactive
})

// 定义模块类型
const moduleTypes = Object.keys(ALL_MODULES)

// 初始化数据
const initData = async () => {
  await withLoading(async () => {
    try {
      // 1. 先获取布局数据
      const layoutResponse = await profile.getLayout()
      if (layoutResponse.data?.code === 200) {
        // 确保布局数据的正确结构
        const layout = layoutResponse.data.data.layout || {}
        layoutData.value = layout
      }

      // 2. 获取档案数据
      const response = await profile.getData()
      if (response.data?.code === 200) {
        console.log('档案数据:', response.data.data)
        profileData.value = response.data.data
      }

      // 3. 获取模块数据
      await fetchModulesData()

      // 4. 获取完整度数据
      const completenessResponse = await profile.getCompleteness()
      if (completenessResponse.data?.code === 200) {
        completionData.value = completenessResponse.data.data
      }
    } catch (error) {
      console.error('初始化数据失败:', error)
      ElMessage.error('获取数据失败，请刷新重试')
    }
  })
}

// 更新数据
const handleUpdate = async (updateInfo) => {
  try {
    if (updateInfo?.type === 'avatar') {
      // 直接更新头像
      if (profileData.value?.basic_info) {
        profileData.value.basic_info.avatar = updateInfo.value
        // 强制刷新
        await nextTick()
      }
      return
    }
    // 重新获取档案数据
    await initData()
  } catch (error) {
    console.error('更新失败:', error)
  }
}

// 处理编辑
const handleEdit = (type, data) => {
  // 根据类型显示对应的弹窗
  switch (type) {
    case 'basic_info':
      currentModule.value = { type }
      editFormData.value = data || {}
      showEditModal.value = true
      break
    case 'job_intention':
      editJobIntentionData.value = data || {}
      showJobIntentionDialog.value = true
      break
    case 'work_experience':
      // 确保日期格式正确
      const formattedData = {
        ...data,
        start_date: data.start_date?.split('T')[0] || null,
        end_date: data.end_date?.split('T')[0] || null
      }
      editWorkExperienceData.value = formattedData
      showWorkExperienceDialog.value = true
      break
    case 'education':
      editEducationData.value = data || {}
      showEducationDialog.value = true
      break
    case 'project':
      editProjectData.value = data || {}
      showProjectDialog.value = true
      break
    case 'certificate':
      editCertificateData.value = data || {}
      showCertificateDialog.value = true
      break
    case 'skill':
      editSkillData.value = data || {}
      showSkillDialog.value = true
      break
    case 'language':
      editLanguageData.value = data || {}
      showLanguageDialog.value = true
      break
    default:
      currentModule.value = { type }
      editFormData.value = data || {}
      showEditModal.value = true
      break
  }
}

// 处理个人简介展开/收起
const toggleBioExpand = () => {
  bioExpanded.value = !bioExpanded.value
}

// 处理工作经历提交
const handleWorkExperienceSubmit = async (data) => {
  try {
    await profile.updateModule('work_experience', data)
    ElMessage.success('保存成功')
    showWorkExperienceDialog.value = false
    await initData()
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败，请重试')
  }
}

// 获取模块显示名称
const getModuleName = (type) => {
  const moduleNames = {
    basic_info: '基本信息',
    job_intention: '求职意向',
    work_experience: '工作经历',
    education: '教育经历',
    project: '项目经历',
    skill: '专业技能',
    certificate: '证书奖项',
    language: '语言能力',
    portfolio: '作品展示',
    social_link: '社交主页'
  }
  return moduleNames[type] || type
}

// 处理提交
const handleSubmit = async (data) => {
  try {
    await withLoading(async () => {
      const type = currentModule.value?.type
      console.log('提交数据:', { type, data })

      // 使用统一的 updateModule 方法
      const response = await profile.updateModule(type, data)
      
      if (response.data?.code === 200) {
        ElMessage.success('保存成功')
        showEditModal.value = false
        // 重新获取数据
        await initData()
      } else {
        throw new Error(response.data?.message || '保存失败')
      }
    })
  } catch (error) {
    console.error('保存失败:', error)
    if (error.response?.data?.errors) {
      const errorMessages = Object.entries(error.response.data.errors)
        .map(([field, messages]) => `${field}: ${messages.join(', ')}`)
        .join('\n')
      ElMessage.error(errorMessages)
    } else {
      ElMessage.error(error.message || '保存失败，请重试')
    }
  }
}

// 处理添加
const handleAdd = (type) => {
  currentModule.value = { type }
  
  // 根据类型显示对应的弹窗并清空数据
  switch (type) {
    case 'work_experience':
      editWorkExperienceData.value = {  // 重置为空对象
        name: '',
        company: '',
        position: '',
        start_date: null,
        end_date: null,
        description: '',
        is_current: false
      }
      showWorkExperienceDialog.value = true
      break
      
    case 'education':
      editEducationData.value = {  // 重置为空对象
        school: '',
        major: '',
        degree: '',
        start_date: null,
        end_date: null,
        description: ''
      }
      showEducationDialog.value = true
      break
      
    case 'project':
      editProjectData.value = {  // 重置为空对象
        name: '',
        role: '',
        start_date: null,
        end_date: null,
        description: '',
        technologies: ''
      }
      showProjectDialog.value = true
      break
      
    case 'certificate':
      editCertificateData.value = {  // 重置为空对象
        name: '',
        issuing_authority: '',
        issue_date: null,
        expiry_date: null,
        description: ''
      }
      showCertificateDialog.value = true
      break
      
    case 'skill':
      editSkillData.value = {  // 重置为空对象
        name: '',
        level: '初级',
        description: '',
        projects: '',
        order: 0
      }
      showSkillDialog.value = true
      break
      
    case 'language':
      editLanguageData.value = {  // 重置为空对象
        language: '',
        proficiency: '',
        certificates: ''
      }
      showLanguageDialog.value = true
      break
      
    case 'job_intention':
      editJobIntentionData.value = {  // 重置为空对象
        position: '',
        industry: '',
        location: '',
        salary_range: '',
        job_type: '',
        description: ''
      }
      showJobIntentionDialog.value = true
      break
      
    default:
      editFormData.value = {}  // 其他类型直接清空
      showEditModal.value = true
      break
  }
}

// 处理移除模块
const handleModuleRemove = async (type, id) => {
  try {
    if (id) {
      // 显示删除确认对话框
      showDeleteConfirm(type, id)
    } else {
      // 获取当前所有可见模块的配置（除了要移除的）
      const updatedModules = {}
      activeModules.value
        .filter(module => module.type !== type)
        .forEach((module, index) => {
          updatedModules[module.type] = {
            visible: true,
            order: index + 1  // 重新排序剩余模块
          }
        })
      
      // 添加要移除的模块配置
      const layoutUpdate = {
        ...updatedModules,
        [type]: {
          visible: false,
          order: 999  // 移到未激活模块区域
        }
      }

      // 提交布局更新
      const response = await profile.updateLayout(layoutUpdate)
      if (response.data?.code !== 200) {
        throw new Error('保存布局失败')
      }

      ElMessage.success('模块已隐藏')
      
      // 重新获取所有数据以确保同步
      await initData()
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      if (error.response?.data?.message) {
        ElMessage.error(error.response.data.message)
      } else {
        ElMessage.error('删除失败，请重试')
      }
    }
  }
}

// 处理删除确认
const handleDeleteConfirm = async () => {
  try {
    const { type, id } = currentDeleteItem.value
    await profile.deleteModuleItem(type, id)
    ElMessage.success('删除成功')
    await initData()
  } catch (error) {
    console.error('删除失败:', error)
    ElMessage.error('删除失败，请重试')
  } finally {
    closeDeleteConfirm()
  }
}

const handleJobIntentionSubmit = async (data) => {
  try {
    await profile.updateModule('job_intention', data)
    ElMessage.success('保存成功')
    showJobIntentionDialog.value = false
    // 重新获取完整数据
    await initData()
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败，请重试')
  }
}

// 处理教育经历提交
const handleEducationSubmit = async (data) => {
  try {
    await profile.updateModule('education', data)
    ElMessage.success('保存成功')
    showEducationDialog.value = false
    await initData()
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败，请重试')
  }
}

const handleAIOptimize = async () => {
  // AI优化逻辑
}

const showDeleteConfirmDialog = ref(false)
const currentDeleteItem = ref(null)

const showDeleteConfirm = (type, id) => {
  showDeleteConfirmDialog.value = true
  currentDeleteItem.value = { type, id }
}

const closeDeleteConfirm = () => {
  showDeleteConfirmDialog.value = false
  currentDeleteItem.value = null
}

// 处理添加模块
const handleAddModule = async (type) => {
  try {
    // 获取当前所有可见模块的配置
    const visibleModules = {}
    activeModules.value.forEach((module, index) => {
      visibleModules[module.type] = {
        visible: true,
        order: index + 1  // 保持现有模块的顺序
      }
    })
    
    // 添加新模块到最后
    const layoutUpdate = {
      ...visibleModules,  // 保持现有模块的配置
      [type]: {
        visible: true,
        order: activeModules.value.length + 1  // 新模块放在最后
      }
    }

    // 提交布局更新
    const response = await profile.updateLayout(layoutUpdate)
    if (response.data?.code !== 200) {
      throw new Error('保存布局失败')
    }

    ElMessage.success('模块已添加')
    
    // 重新获取所有数据以确保同步
    await initData()
  } catch (error) {
    console.error('添加模块失败:', error)
    ElMessage.error('添加失败，请重试')
  }
}

// 处理项目经历提交
const handleProjectSubmit = async (data) => {
  try {
    await profile.updateModule('project', data)
    ElMessage.success('保存成功')
    showProjectDialog.value = false
    await initData()
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败，请重试')
  }
}

// 处理证书奖项提交
const handleCertificateSubmit = async (data) => {
  try {
    await profile.updateModule('certificate', data)
    ElMessage.success('保存成功')
    showCertificateDialog.value = false
    await initData()
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败，请重试')
  }
}

// 处理专业技能提交
const handleSkillSubmit = async (data) => {
  try {
    // 确保数据格式正确
    const skillData = {
      name: data.name?.trim(),
      level: data.level || '初级',
      description: data.description?.trim() || '',
      projects: data.projects || '',
      order: data.order || 0
    }

    if (data.id) {
      await profile.updateModule('skills', { ...skillData, id: data.id })
    } else {
      await profile.updateModule('skills', skillData)
    }
    
    ElMessage.success('保存成功')
    showSkillDialog.value = false
    await initData()
  } catch (error) {
    console.error('保存失败:', error)
    if (error.response?.data?.errors) {
      const errorMessages = Object.entries(error.response.data.errors)
        .map(([field, messages]) => `${field}: ${messages.join(', ')}`)
        .join('\n')
      ElMessage.error(errorMessages)
    } else {
      ElMessage.error('保存失败，请重试')
    }
  }
}

// 处理语言能力提交
const handleLanguageSubmit = async (data) => {
  try {
    await profile.updateModule('language', data)
    ElMessage.success('保存成功')
    showLanguageDialog.value = false
    await initData()
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败，请重试')
  }
}

// 监听数据变化
watch(() => profileData.value, (newData) => {
  if (newData) {
    updateModules(newData)
  }
}, { deep: true })

// 处理模块数据更新
const updateModules = (data) => {
  if (!data) return
  
  const activeModulesList = moduleTypes
    .filter(type => layoutStatus.value[type]?.visible)
    .map(type => ({
      type,
      data: data[type],
      name: ALL_MODULES[type].name,
      editable: true
    }))
  
  // 更新 activeModules 的引用而不是直接修改计算属性
  modules.value = activeModulesList
  
  // 处理未激活模块
  const inactiveCount = moduleTypes
    .filter(type => !layoutStatus.value[type]?.visible).length
  const inactiveModulesList = {
    count: inactiveCount,
    modules: moduleTypes
      .filter(type => !layoutStatus.value[type]?.visible)
      .map(type => ({
        type,
        name: ALL_MODULES[type].name
      }))
  }
  // 更新 inactiveModules 的引用
  modules.value = [...activeModulesList, ...inactiveModulesList.modules]
}

// 初始化
onMounted(() => {
  initData()
  // 监听完整度更新事件
  eventBus.on('completeness-updated', async () => {
    try {
      // 获取最新的完整度数据
      const completenessResponse = await profile.getCompleteness()
      if (completenessResponse.data?.code === 200) {
        completionData.value = completenessResponse.data.data
      }
    } catch (error) {
      console.error('获取完整度数据失败:', error)
    }
  })
})

// 组件卸载时移除事件监听
onUnmounted(() => {
  eventBus.off('completeness-updated')
})

// 添加删除处理函数
const handleDelete = async (type, id) => {
  try {
    console.log('MyProfile - 处理删除:', type, id)
    // 重新获取数据
    await fetchModulesData()
  } catch (error) {
    console.error('刷新数据失败:', error)
    ElMessage.error('刷新数据失败')
  }
}

// 处理模块数据保存
const handleModuleSave = async (type, data) => {
  try {
    showEditDialog.value = false
    
    let response
    if (data.id) {
      // 编辑
      response = await profile.updateModule(type, data)
    } else {
      // 新增
      response = await profile.addModuleItem(type, data)
    }

    // 确保返回数据正确
    if (response && response.data) {
      // 刷新模块数据
      await fetchModulesData()
      ElMessage.success(data.id ? '更新成功' : '添加成功')
    } else {
      throw new Error('保存失败')
    }
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error(error.message || '保存失败')
  }
}

const handleModuleEdit = async (type, data) => {
  try {
    if (type === 'basic_info') {
      await store.dispatch('updateBasicInfo', {
        type: 'basic',
        data
      })
      // 更新成功后重新获取数据
      await fetchData()
      showToast('保存成功', 'success')
    }
    // ... 其他模块的处理
  } catch (error) {
    console.error('保存失败:', error)
    showToast(error.message || '保存失败', 'error')
  }
}

// 欢迎横幅状态
const hideWelcomeBanner = ref(localStorage.getItem('hideWelcomeBanner') === 'true')

// 关闭欢迎横幅
const closeWelcomeBanner = () => {
  hideWelcomeBanner.value = true
  localStorage.setItem('hideWelcomeBanner', 'true')
}
</script>