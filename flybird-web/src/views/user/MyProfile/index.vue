<!-- src/views/user/MyProfile/index.vue -->
<template>
  <div class="container mx-auto pb-6">
    <div class="max-w-4xl mx-auto space-y-4">
      <BasicInfo
        :resumeData="basicInfo"
        :loading="profileLoading"
        :bioExpanded="bioExpanded"
        :showBioExpandButton="showBioExpandButton"
        @edit="handleEdit"
        @update="handleUpdate"
        @toggleBioExpand="toggleBioExpand"
      />

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
        @edit="handleEdit"
        @remove="handleModuleRemove"
        @edit-item="handleEditItem"
        @remove-item="handleRemoveItem"
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
        :initial-data="currentEditData"
        :loading="profileLoading"
        @submit="handleWorkExperienceSubmit"
      />

      <!-- 求职意向编辑弹窗 -->
      <EditJobIntentionDialog
        v-if="currentModule?.type === 'job_intention'"
        v-model="showEditModal"
        :initial-data="editFormData"
        :loading="profileLoading"
        @submit="handleSubmit"
      />

      <!-- 基本信息编辑弹窗 -->
      <EditBasicDialog
        v-if="currentModule?.type === 'basic_info'"
        v-model="showEditModal"
        :initial-data="editFormData"
        :loading="profileLoading"
        @submit="handleSubmit"
      />

      <AIOptimizeDialog
        v-model="showAIOptimizeDialog"
        :profile-data="profileData"
        @apply="handleAIOptimize"
      />

      <!-- 删除确认弹窗 -->
      <TransitionRoot appear :show="showDeleteConfirm" as="template">
        <Dialog as="div" class="relative z-50" @close="showDeleteConfirm = false">
          <!-- 背景遮罩 -->
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

          <!-- 对话框 -->
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
                        @click="showDeleteConfirm = false"
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
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useModules } from './composables/useModules'
import { useProfileData } from './composables/useProfileData'
import profile from '@/api/profile'
import { ElMessage, ElMessageBox } from 'element-plus'
import { PlusIcon, ExclamationTriangleIcon } from '@heroicons/vue/24/outline'
import { ALL_MODULES } from '@/constants'
import { useLoading } from './composables/useLoading'
import { TransitionRoot, TransitionChild, Dialog, DialogPanel, DialogTitle } from '@headlessui/vue'

// 组件引入
import BasicInfo from './components/BasicInfo.vue'
import ResumeStatus from './components/ResumeStatus.vue'
import ModuleList from './components/ModuleList.vue'
import AddModule from './components/AddModule.vue'
import EditBasicDialog from './dialogs/EditBasicDialog.vue'
import EditJobIntentionDialog from './dialogs/EditJobIntentionDialog.vue'
import EditWorkExperienceDialog from './dialogs/EditWorkExperienceDialog.vue'
import AIOptimizeDialog from './dialogs/AIOptimizeDialog.vue'

// 使用模块管理
const { 
  loading: modulesLoading,
  activeModules,
  inactiveModules,
  fetchModulesData,
  addModule,
  removeModule
} = useModules()

const {
  loading: profileLoading,
  basicInfo,
  profileData,
  completionData,
  fetchBasicInfo,
  fetchModuleData,
  fetchCompletionData
} = useProfileData()

// 当前编辑的模块
const currentModule = ref(null)

// 基本状态
const showEditModal = ref(false)
const editFormData = ref({})

// 基本信息控制
const bioExpanded = ref(false)
const showBioExpandButton = ref(false)

// 添加缺失的响应式变量
const showAIOptimizeDialog = ref(false)

// 处理 Bio 展开/收起
const toggleBioExpand = () => {
  bioExpanded.value = !bioExpanded.value
}

// 定义组件的 emits
defineEmits([
  'update:modelValue',
  'edit',
  'add',
  'remove',
  'edit-item',
  'remove-item'
])

// 初始化数据
onMounted(async () => {
  
  try {
    // 获取基本信息
    await fetchBasicInfo()
    
    // 获取模块数据
    await fetchModulesData()
  
    // 获取完整度数据
    await fetchCompletionData()
  
  } catch (error) {
    console.error('初始化数据失败:', error)
    if (error.response) {
      console.error('API 错误响应:', error.response)
    } else if (error.request) {
      console.error('未收到响应:', error.request)
    } else {
      console.error('请求配置错误:', error.message)
    }
  }
})

// 工作经历相关
const showWorkExperienceDialog = ref(false)
const currentEditData = ref({})
const { loading: submitLoading, withLoading } = useLoading()

// 统一处理编辑事件
const handleEdit = (type, item = null) => {
  console.log('handleEdit - type:', type, 'item:', item)
  if (type === 'work_experience') {
    currentEditData.value = item || {}
    showWorkExperienceDialog.value = true
  } else if (type === 'basic_info') {
    currentModule.value = {
      type,
      data: item || basicInfo.value
    }
    console.log('基本信息编辑数据:', currentModule.value)
    editFormData.value = { ...currentModule.value.data }
    showEditModal.value = true
  } else {
    // 处理其他类型的编辑
    currentModule.value = {
      type,
      data: item || {}
    }
    editFormData.value = { ...currentModule.value.data }
    showEditModal.value = true
  }
}

// 处理编辑具体项目
const handleEditItem = (type, item) => {
  console.log('handleEditItem - type:', type, 'item:', item)
  handleEdit(type, item)
}

// 删除确认弹窗状态
const showDeleteConfirm = ref(false)
const itemToDelete = ref(null)

// 处理删除
const handleRemoveItem = async (type, itemId) => {
  if (type === 'work_experience') {
    itemToDelete.value = { type, id: itemId }
    showDeleteConfirm.value = true
  }
}

// 确认删除
const confirmDelete = async () => {
  try {
    await withLoading(async () => {
      await profile.workExperience.delete(itemToDelete.value.id)
      ElMessage.success('删除成功')
      await fetchModulesData()
    })
  } catch (error) {
    console.error('删除失败:', error)
    ElMessage.error('删除失败，请稍后重试')
  } finally {
    showDeleteConfirm.value = false
    itemToDelete.value = null
  }
}

// 处理工作经历提交
const handleWorkExperienceSubmit = async (data) => {
  try {
    await withLoading(async () => {
      if (data.id) {
        await profile.workExperience.update(data.id, data)
        ElMessage.success('更新成功')
      } else {
        await profile.workExperience.add(data)
        ElMessage.success('添加成功')
      }
      showWorkExperienceDialog.value = false
      await fetchModulesData()
    })
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败，请稍后重试')
  }
}

// 处理求职意向提交
const handleJobIntentionSubmit = async (data) => {
  try {
    await withLoading(async () => {
      await profile.jobIntention.update(data)
      ElMessage.success('保存成功')
      showEditModal.value = false
      await fetchModulesData()
    })
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败，请稍后重试')
  }
}

// 提交表单
const handleSubmit = async (data) => {
  try {
    if (currentModule.value?.type === 'basic_info') {
      await withLoading(async () => {
        // 基本信息保存
        const response = await profile.updateBasicInfo(data)
        if (response.data?.code === 200) {
          ElMessage.success('保存成功')
          showEditModal.value = false
          // 重新获取基本信息
          await fetchBasicInfo()
          // 刷新完整度
          await fetchCompletionData()
        } else {
          throw new Error(response.data?.message || '保存失败')
        }
      })
    } else if (currentModule.value?.type === 'job_intention') {
      await handleJobIntentionSubmit(data)
    }
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error(error.message || '保存失败，请稍后重试')
  }
}

// 处理编辑模块
const handleEditModule = (moduleId) => {
  currentModule.value = activeModules.value.find(m => m.type === moduleId)
  
  if (currentModule.value?.type === 'work_experience') {
    editFormData.value = {}
  } else if (currentModule.value?.type === 'job_intention') {
    editFormData.value = { ...currentModule.value.data }
  }
  
  showEditModal.value = true
}

// 处理 AI 优化结果
const handleAIOptimize = (optimizedData) => {
  Object.entries(optimizedData).forEach(([key, value]) => {
    const [category, field] = key.split('.')
    if (category && field) {
      if (!profileData.value[category]) {
        profileData.value[category] = {}
      }
      profileData.value[category][field] = value
    } else {
      profileData.value[key] = value
    }
  })
}

// 添加更新处理方法
const handleUpdate = async () => {
  try {
    await fetchBasicInfo()
    await fetchModulesData()
    await fetchCompletionData()
  } catch (error) {
    console.error('更新数据失败:', error)
    ElMessage.error('更新失败，请稍后重试')
  }
}

// 处理模块移除
const handleModuleRemove = async (moduleType) => {
  await removeModule(moduleType)
}

// 处理添加模块
const handleAddModule = async (moduleType) => {
  await addModule(moduleType)
}

// 获取模块显示名称
const getModuleName = (type) => {
  return ALL_MODULES[type] || type
}

</script>