<!-- src/views/user/MyProfile/components/ModuleList.vue -->
<template>
  <div class="space-y-4">
    <!-- 未激活的模块按钮组 -->
    <div v-if="inactiveModules.length > 0" class="bg-white rounded-lg shadow">
      <div class="px-4 py-3">
        <h3 class="text-sm font-medium text-gray-900">添加更多模块</h3>
        <div class="mt-3 flex flex-wrap gap-2">
          <button
            v-for="module in inactiveModules"
            :key="module.type"
            @click="handleAdd(module.type)"
            class="inline-flex items-center px-3 py-1.5 text-sm text-gray-600 bg-gray-50 hover:bg-gray-100 rounded border border-gray-200"
          >
            {{ module.name }}
            <PlusIcon class="w-4 h-4 ml-1 text-gray-400" />
          </button>
        </div>
      </div>
    </div>

    <!-- 激活的模块列表 -->
    <div v-for="module in activeModules" :key="module.type" class="bg-white rounded-lg shadow">
      <div class="flex items-center justify-between px-4 py-3">
        <h3 class="text-base font-medium text-gray-900">
          {{ module.name }}
        </h3>
        <div class="flex items-center space-x-2">
          <!-- 展开/关闭按钮 -->
          <button
            @click="toggleModule(module.type)"
            class="p-1 hover:bg-gray-100 rounded-full"
          >
            <ChevronUpIcon
              v-if="!collapsedModules[module.type]"
              class="w-5 h-5 text-gray-400"
            />
            <ChevronDownIcon
              v-else
              class="w-5 h-5 text-gray-400"
            />
          </button>
          <!-- 添加按钮 -->
          <button
            v-if="shouldShowAddButton(module.type)"
            @click="handleAdd(module.type)"
            class="p-1 hover:bg-gray-100 rounded-full"
          >
            <PlusIcon class="w-5 h-5 text-gray-400" />
          </button>
          <!-- 编辑按钮 -->
          <button
            v-if="module.type === 'job_intention'"
            @click="handleModuleEdit(module.type)"
            class="p-1 hover:bg-gray-100 rounded-full"
          >
            <PencilSquareIcon class="w-5 h-5 text-gray-400" />
          </button>
          <!-- 删除按钮 -->
          <button
            @click="handleModuleRemove(module.type)"
            class="p-1 hover:bg-gray-100 rounded-full"
          >
            <TrashIcon class="w-5 h-5 text-gray-400" />
          </button>
        </div>
      </div>
      
      <!-- 使用 v-show 控制内容显示/隐藏 -->
      <div class="px-4 pb-4" v-show="!collapsedModules[module.type]">
        <!-- 求职意向模块 -->
        <template v-if="module.type === 'job_intention' && module.data">
          <div class="text-gray-600">
            <!-- 求职状态标识 -->
            <div class="flex items-center space-x-2 mb-3">
              <div 
                class="w-2 h-2 rounded-full"
                :class="getJobStatusColor(module.data.job_status)"
              ></div>
              <span class="text-sm font-medium">
                {{ getJobStatusLabel(module.data.job_status) }}
              </span>
            </div>

            <!-- 主要信息卡片 -->
            <div class="bg-gray-50 rounded-lg p-4 space-y-4">
              <!-- 工作类型和薪资 -->
              <div class="flex justify-between items-start">
                <div class="flex items-start space-x-3">
                  <BriefcaseIcon class="w-5 h-5 text-blue-500 mt-0.5" />
                  <div>
                    <div class="text-sm text-gray-500">期望职位</div>
                    <div class="font-medium mt-1">{{ getJobTypeLabel(module.data.job_type) }}</div>
                  </div>
                </div>
                <div class="flex items-start space-x-3">
                  <BanknotesIcon class="w-5 h-5 text-emerald-500 mt-0.5" />
                  <div class="text-right">
                    <div class="text-sm text-gray-500">期望薪资</div>
                    <div class="font-medium mt-1 text-emerald-600">
                      {{ module.data.expected_salary }}
                    </div>
                  </div>
                </div>
              </div>

              <!-- 期望城市 -->
              <div class="flex items-start space-x-3">
                <MapPinIcon class="w-5 h-5 text-red-500 mt-0.5" />
                <div>
                  <div class="text-sm text-gray-500">期望城市</div>
                  <div class="font-medium mt-1">
                    {{ formatCity(module.data.expected_city) }}
                  </div>
                </div>
              </div>

              <!-- 期望行业 -->
              <div v-if="module.data.industries" class="flex items-start space-x-3">
                <BuildingOfficeIcon class="w-5 h-5 text-purple-500 mt-0.5" />
                <div class="flex-1">
                  <div class="text-sm text-gray-500 mb-2">期望行业</div>
                  <div class="flex flex-wrap gap-2">
                    <span 
                      v-for="industry in formatIndustries(module.data.industries)" 
                      :key="industry"
                      class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-purple-50 text-purple-700"
                    >
                      {{ industry }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>

        <!-- 工作经历模块 -->
        <template v-else-if="module.type === 'work_experience' && module.data">
          <div class="relative space-y-0">
            <!-- 时间线 -->
            <div class="absolute left-[0.5625rem] top-3 bottom-3 w-px bg-gray-200"></div>

            <!-- 工作经历列表 -->
            <div 
              v-for="(exp, index) in module.data" 
              :key="index" 
              class="relative pl-12 pb-6"
            >
              <!-- 时间节点 -->
              <div class="absolute left-[0.5625rem] -translate-x-1/2 top-2 w-3 h-3 rounded-full bg-white border-2 border-blue-500"></div>
              
              <!-- 内容卡片 -->
              <div class="bg-gray-50 rounded-lg border border-gray-100 p-4 hover:shadow-sm transition-shadow">
                <!-- 头部信息 -->
                <div class="flex items-center justify-between mb-3">
                  <div class="flex-1">
                    <div class="text-sm text-gray-500">
                      {{ formatDate(exp.start_date) }} - {{ exp.end_date ? formatDate(exp.end_date) : '至今' }}
                    </div>
                    <div class="flex items-center justify-between mt-1.5">
                      <span class="text-base font-medium text-gray-900">{{ exp.company }}</span>
                      <div class="flex items-center space-x-2">
                        <button
                          @click="handleEdit(module.type, exp)"
                          class="p-1 hover:bg-white rounded-full transition-colors"
                        >
                          <PencilSquareIcon class="w-4 h-4 text-gray-400" />
                        </button>
                        <button
                          @click="handleItemDelete(module.type, exp.id)"
                          class="p-1 hover:bg-white rounded-full transition-colors"
                        >
                          <TrashIcon class="w-4 h-4 text-gray-400" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 职位 -->
                <div class="text-sm font-medium text-blue-600 mb-3">
                  {{ exp.position }}
                </div>

                <!-- 工作内容 -->
                <div class="space-y-2">
                  <div class="flex items-center space-x-2">
                    <DocumentTextIcon class="w-4 h-4 text-gray-400" />
                    <span class="text-sm text-gray-500">工作内容</span>
                  </div>
                  <div class="text-sm leading-relaxed text-gray-600 pl-6">
                    {{ exp.description }}
                  </div>
                </div>

                <!-- 工作成果 -->
                <div v-if="exp.achievements" class="mt-3 space-y-2">
                  <div class="flex items-center space-x-2">
                    <TrophyIcon class="w-4 h-4 text-yellow-500" />
                    <span class="text-sm text-gray-500">工作成果</span>
                  </div>
                  <div class="text-sm leading-relaxed text-gray-600 pl-6">
                    {{ exp.achievements }}
                  </div>
                </div>
              </div>
            </div>

            <!-- 添加按钮 -->
            <div class="relative pl-12">
              <div class="absolute left-[0.5625rem] -translate-x-1/2 top-2 w-3 h-3 rounded-full bg-white border-2 border-gray-300"></div>
              <button
                @click="handleAdd(module.type)"
                class="w-full flex items-center justify-center px-4 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-all"
              >
                <PlusIcon class="w-4 h-4 mr-2" />
                添加工作经历
              </button>
            </div>
          </div>
        </template>

        <!-- 教育经历模块 -->
        <template v-else-if="module.type === 'education' && module.data">
          <EducationContent 
            :key="educationKey"
            :data="module.data"
            @edit="item => handleEdit('education', item)"
            @delete="id => handleItemDelete('education', id)"
            @add="() => handleEdit('education', null)"
          />
        </template>

        <!-- 专业技能模块 -->
        <template v-else-if="module.type === 'skill' && module.data">
          <div class="text-gray-600 px-4 pb-4">
            <!-- 添加调试信息 -->
            <pre class="text-xs text-gray-500 mb-2">{{ JSON.stringify(module.data, null, 2) }}</pre>
            
            <!-- 原有的模块内容 -->
            <div class="space-y-4">
              <div v-for="(skill, index) in module.data" :key="index" 
                class="bg-gray-50 rounded-lg p-4">
                <div class="flex items-center justify-between">
                  <div class="font-medium">{{ skill.name }}</div>
                  <div class="flex items-center space-x-2">
                    <button
                      @click="handleEdit(module.type, skill)"
                      class="p-1 hover:bg-white rounded-full transition-colors"
                    >
                      <PencilSquareIcon class="w-4 h-4 text-gray-400" />
                    </button>
                    <button
                      @click="handleDelete(module.type, skill.id)"
                      class="p-1 hover:bg-white rounded-full transition-colors"
                    >
                      <TrashIcon class="w-4 h-4 text-gray-400" />
                    </button>
                  </div>
                </div>
                <div class="mt-2 text-sm text-gray-500">{{ skill.description }}</div>
              </div>
            </div>
            
            <!-- 添加按钮 -->
            <button
              @click="handleAdd(module.type)"
              class="mt-4 w-full flex items-center justify-center px-4 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-all"
            >
              <PlusIcon class="w-4 h-4 mr-2" />
              添加专业技能
            </button>
          </div>
        </template>

        <!-- 项目经历模块 -->
        <template v-else-if="module.type === 'project' && module.data">
          <ProjectContent
            :data="module.data"
            @edit="item => handleEdit('project', item)"
            @delete="id => handleItemDelete('project', id)"
            @add="() => handleAdd('project')"
          />
        </template>

        <!-- 证书奖项模块 -->
        <template v-else-if="module.type === 'certificate' && module.data">
          <div class="text-gray-600 px-4 pb-4">
            <div class="space-y-4">
              <div v-for="(cert, index) in module.data" :key="index" 
                class="bg-gray-50 rounded-lg p-4">
                <div class="flex items-center justify-between mb-2">
                  <div class="font-medium">{{ cert.name }}</div>
                  <div class="flex items-center space-x-2">
                    <button
                      @click="handleEdit(module.type, cert)"
                      class="p-1 hover:bg-white rounded-full transition-colors"
                    >
                      <PencilSquareIcon class="w-4 h-4 text-gray-400" />
                    </button>
                    <button
                      @click="handleDelete(module.type, cert.id)"
                      class="p-1 hover:bg-white rounded-full transition-colors"
                    >
                      <TrashIcon class="w-4 h-4 text-gray-400" />
                    </button>
                  </div>
                </div>
                <div class="text-sm text-gray-500">{{ cert.date }}</div>
                <div class="mt-2 text-sm text-gray-600">{{ cert.description }}</div>
              </div>
            </div>
            
            <button
              @click="handleAdd(module.type)"
              class="mt-4 w-full flex items-center justify-center px-4 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-all"
            >
              <PlusIcon class="w-4 h-4 mr-2" />
              添加证书奖项
            </button>
          </div>
        </template>

        <!-- 语言能力模块 -->
        <template v-else-if="module.type === 'language' && module.data">
          <div class="text-gray-600 px-4 pb-4">
            <div class="space-y-4">
              <div v-for="(lang, index) in module.data" :key="index" 
                class="bg-gray-50 rounded-lg p-4">
                <div class="flex items-center justify-between">
                  <div>
                    <div class="font-medium">{{ lang.name }}</div>
                    <div class="text-sm text-gray-500 mt-1">{{ lang.level }}</div>
                  </div>
                  <div class="flex items-center space-x-2">
                    <button
                      @click="handleEdit(module.type, lang)"
                      class="p-1 hover:bg-white rounded-full transition-colors"
                    >
                      <PencilSquareIcon class="w-4 h-4 text-gray-400" />
                    </button>
                    <button
                      @click="handleDelete(module.type, lang.id)"
                      class="p-1 hover:bg-white rounded-full transition-colors"
                    >
                      <TrashIcon class="w-4 h-4 text-gray-400" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
            
            <button
              @click="handleAdd(module.type)"
              class="mt-4 w-full flex items-center justify-center px-4 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-all"
            >
              <PlusIcon class="w-4 h-4 mr-2" />
              添加语言能力
            </button>
          </div>
        </template>

        <!-- 作品展示模块 -->
        <template v-else-if="module.type === 'portfolio' && module.data">
          <div class="text-gray-600 px-4 pb-4">
            <div class="space-y-4">
              <div v-for="(work, index) in module.data" :key="index" 
                class="bg-gray-50 rounded-lg p-4">
                <div class="flex items-center justify-between mb-2">
                  <div class="font-medium">{{ work.name }}</div>
                  <div class="flex items-center space-x-2">
                    <button
                      @click="handleEdit(module.type, work)"
                      class="p-1 hover:bg-white rounded-full transition-colors"
                    >
                      <PencilSquareIcon class="w-4 h-4 text-gray-400" />
                    </button>
                    <button
                      @click="handleDelete(module.type, work.id)"
                      class="p-1 hover:bg-white rounded-full transition-colors"
                    >
                      <TrashIcon class="w-4 h-4 text-gray-400" />
                    </button>
                  </div>
                </div>
                <div class="mt-2 text-sm text-gray-600">{{ work.description }}</div>
                <a 
                  v-if="work.link" 
                  :href="work.link" 
                  target="_blank"
                  class="inline-flex items-center mt-2 text-sm text-blue-600 hover:text-blue-800"
                >
                  查看链接
                  <ArrowTopRightOnSquareIcon class="w-4 h-4 ml-1" />
                </a>
              </div>
            </div>
            
            <button
              @click="handleAdd(module.type)"
              class="mt-4 w-full flex items-center justify-center px-4 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-all"
            >
              <PlusIcon class="w-4 h-4 mr-2" />
              添加作品展示
            </button>
          </div>
        </template>

        <!-- 社交主页模块 -->
        <template v-else-if="module.type === 'social_link' && module.data">
          <div class="text-gray-600 px-4 pb-4">
            <div class="space-y-4">
              <div v-for="(social, index) in module.data" :key="index" 
                class="bg-gray-50 rounded-lg p-4">
                <div class="flex items-center justify-between">
                  <div>
                    <div class="font-medium">{{ social.platform }}</div>
                    <a 
                      :href="social.url" 
                      target="_blank"
                      class="text-sm text-blue-600 hover:text-blue-800 mt-1 inline-flex items-center"
                    >
                      {{ social.username }}
                      <ArrowTopRightOnSquareIcon class="w-4 h-4 ml-1" />
                    </a>
                  </div>
                  <div class="flex items-center space-x-2">
                    <button
                      @click="handleEdit(module.type, social)"
                      class="p-1 hover:bg-white rounded-full transition-colors"
                    >
                      <PencilSquareIcon class="w-4 h-4 text-gray-400" />
                    </button>
                    <button
                      @click="handleDelete(module.type, social.id)"
                      class="p-1 hover:bg-white rounded-full transition-colors"
                    >
                      <TrashIcon class="w-4 h-4 text-gray-400" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
            
            <button
              @click="handleAdd(module.type)"
              class="mt-4 w-full flex items-center justify-center px-4 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-all"
            >
              <PlusIcon class="w-4 h-4 mr-2" />
              添加社交主页
            </button>
          </div>
        </template>

        <!-- 默认显示 -->
        <div v-else-if="!module.data" class="text-center text-gray-400 py-4">
          暂无内容，点击编辑添加
        </div>
        <div v-else class="text-gray-600">
          {{ module.data }}
        </div>
      </div>
    </div>
  </div>

  <!-- 删除确认弹窗 -->
  <TransitionRoot :show="showDeleteConfirm" as="template">
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
                      确认删除教育经历？
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

  <!-- 添加教育经历编辑弹窗 -->
  <EditEducationDialog
    v-if="currentModule?.type === 'education'"
    v-model="showEditModal"
    :initial-data="editFormData"
    :loading="loading"
    @submit="handleSubmit"
  />

  <!-- 添加所有编辑弹窗 -->
  <EditProjectDialog
    v-if="currentModule?.type === 'project'"
    v-model="showEditModal"
    :initial-data="editFormData"
    :loading="loading"
    @submit="handleSubmit"
  />

  <EditSkillDialog
    v-if="currentModule?.type === 'skill'"
    v-model="showEditModal"
    :initial-data="editFormData"
    :loading="loading"
    @submit="handleSubmit"
  />

  <EditCertificateDialog
    v-if="currentModule?.type === 'certificate'"
    v-model="showEditModal"
    :initial-data="editFormData"
    :loading="loading"
    @submit="handleSubmit"
  />

  <EditLanguageDialog
    v-if="currentModule?.type === 'language'"
    v-model="showEditModal"
    :initial-data="editFormData"
    :loading="loading"
    @submit="handleSubmit"
  />

  <EditPortfolioDialog
    v-if="currentModule?.type === 'portfolio'"
    v-model="showEditModal"
    :initial-data="editFormData"
    :loading="loading"
    @submit="handleSubmit"
  />

  <EditSocialLinkDialog
    v-if="currentModule?.type === 'social_link'"
    v-model="showEditModal"
    :initial-data="editFormData"
    :loading="loading"
    @submit="handleSubmit"
  />

  <!-- 工作经历编辑弹窗 -->
  <EditWorkExperienceDialog
    v-if="currentModule?.type === 'work_experience'"
    v-model="showEditModal"
    :initial-data="editFormData"
    :loading="loading"
    @submit="handleSubmit"
  />

  <EditJobIntentionDialog
    v-if="currentModule?.type === 'job_intention'"
    v-model="showEditModal"
    :initial-data="editFormData"
    :loading="loading"
    @submit="handleSubmit"
  />
</template>

<script setup>
import { ref, watch, onMounted, nextTick, computed } from 'vue'
import { 
  PencilSquareIcon, 
  TrashIcon,
  PlusIcon,
  ExclamationTriangleIcon,
  BriefcaseIcon,
  BanknotesIcon,
  MapPinIcon,
  BuildingOfficeIcon,
  CalendarIcon,
  DocumentTextIcon,
  TrophyIcon,
  ArrowTopRightOnSquareIcon,
  ChevronUpIcon,
  ChevronDownIcon
} from '@heroicons/vue/24/outline'
import { ALL_MODULES } from '@/constants'
import JobIntentionContent from './JobIntentionContent.vue'
import WorkExperienceContent from './WorkExperienceContent.vue'
import { JOB_TYPE_OPTIONS, JOB_STATUS_OPTIONS, SALARY_OPTIONS } from '../constants/jobOptions'
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionRoot,
  TransitionChild
} from '@headlessui/vue'
import EducationContent from './EducationContent.vue'
import EditEducationDialog from '../dialogs/EditEducationDialog.vue'
import { ElMessage } from 'element-plus'
import profile from '@/api/profile'
import { useModules } from '../composables/useModules'
import EditProjectDialog from '../dialogs/EditProjectDialog.vue'
import EditSkillDialog from '../dialogs/EditSkillDialog.vue'
import EditCertificateDialog from '../dialogs/EditCertificateDialog.vue'
import EditLanguageDialog from '../dialogs/EditLanguageDialog.vue'
import EditPortfolioDialog from '../dialogs/EditPortfolioDialog.vue'
import EditSocialLinkDialog from '../dialogs/EditSocialLinkDialog.vue'
import EditWorkExperienceDialog from '../dialogs/EditWorkExperienceDialog.vue'
import EditJobIntentionDialog from '../dialogs/EditJobIntentionDialog.vue'
import ProjectContent from './ProjectContent.vue'

const props = defineProps({
  activeModules: {
    type: Array,
    required: true
  },
  inactiveModules: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  fetchModulesData: {
    type: Function,
    required: true
  }
})

const emit = defineEmits(['remove', 'edit', 'edit-item', 'remove-item'])

// 获取模块显示名称
const getModuleName = (type) => {
  return ALL_MODULES[type] || type
}

// 删除确认相关
const showDeleteConfirm = ref(false)
const itemToDelete = ref(null)
const moduleToDelete = ref(null)

// 处理移除模块按钮点击
const handleRemove = (moduleType) => {
  console.log('准备移除模块:', moduleType)
  moduleToDelete.value = moduleType
  showDeleteConfirm.value = true
}

// 确认移除模块
const confirmRemove = () => {
  if (moduleToDelete.value) {
    console.log('确认移除模块:', moduleToDelete.value)
    emit('remove', moduleToDelete.value)
    showDeleteConfirm.value = false
    moduleToDelete.value = null
  }
}

// 处理删除具体项目
const handleDelete = (type, itemId) => {
  console.log('【ModuleList】准备删除项目:', { type, itemId })
  itemToDelete.value = { type, id: itemId }
  showDeleteConfirm.value = true
}

// 确认删除项目
const confirmDelete = async () => {
  try {
    if (itemToDelete.value) {
      const { type, id } = itemToDelete.value
      console.log('【ModuleList】确认删除项目:', { type, id })
      
      if (type === 'work_experience') {
        console.log('【ModuleList】删除工作经历')
        await profile.workExperience.delete(id)
      } else if (type === 'education') {
        console.log('【ModuleList】删除教育经历')
        await profile.education.delete(id)
      } else if (profile[type]?.delete) {
        console.log('【ModuleList】删除其他类型项目:', type)
        await profile[type].delete(id)
      } else {
        throw new Error('不支持的模块类型')
      }
      
      await props.fetchModulesData()
      ElMessage.success('删除成功')
    }
  } catch (error) {
    console.error('【ModuleList】删除失败:', error)
    ElMessage.error(error.message || '删除失败，请稍后重试')
  } finally {
    showDeleteConfirm.value = false
    itemToDelete.value = null
  }
}

// 定义模块组件映射
const moduleComponents = {
  job_intention: JobIntentionContent,
  work_experience: WorkExperienceContent,
  education: EducationContent,
  // 在这里添加其他模块组件的映射
}

// 监听模块变化
watch(() => props.activeModules, (newModules) => {
  console.log('ModuleList - 活动模块更新:', {
    active: newModules,
    workExperience: newModules.find(m => m.type === 'work_experience')?.data,
    jobIntention: newModules.find(m => m.type === 'job_intention')?.data
  })
}, { deep: true })

// 格式化薪资显示
const formatSalary = (salary) => {
  if (!salary) return '未设置'
  const [min, max] = salary.split('-')
  if (min && max) {
    return `${min}-${max}K/月`
  }
  return `${salary}K/月`
}

// 获取到岗时间显示
const getArrivalTime = (time) => {
  const timeMap = {
    'immediately': '随时到岗',
    'within_1_week': '1周内',
    'within_1_month': '1个月内',
    'within_3_months': '3个月内',
    'negotiable': '待商议'
  }
  return timeMap[time] || '未设置'
}

// 获取工作性质显示
const getJobNature = (nature) => {
  const natureMap = {
    'full_time': '全职',
    'part_time': '兼职',
    'internship': '实习',
    'freelance': '自由职业'
  }
  return natureMap[nature] || '未设置'
}

// 获取工作类型显示
const getWorkType = (type) => {
  const typeMap = {
    'office': '办公室工作',
    'remote': '远程工作',
    'hybrid': '混合办公',
    'flexible': '灵活办公'
  }
  return typeMap[type] || '未设置'
}

// 获取求职状态显示
const getJobStatus = (status) => {
  const statusMap = {
    'actively_looking': '积极找工作',
    'open_to_offers': '考虑机会',
    'not_looking': '暂不找工作'
  }
  return statusMap[status] || '未设置'
}

// 获取求职状态颜色
const getJobStatusColor = (status) => {
  const colorMap = {
    'actively_looking': 'bg-green-500',      // 积极找工作
    'open_to_offers': 'bg-yellow-500',       // 考虑机会
    'not_looking': 'bg-gray-500'             // 暂不找工作
  }
  return colorMap[status] || 'bg-gray-300'
}

// 获取工作类型标签
const getJobTypeLabel = (value) => {
  const typeMap = {
    'full_time': '全职',
    'part_time': '兼职',
    'internship': '实习',
    'freelance': '自由职业'
  }
  return typeMap[value] || '未设置'
}

// 获取求职状态标签
const getJobStatusLabel = (value) => {
  const statusMap = {
    'actively_looking': '积极找工作',
    'open_to_offers': '考虑机会',
    'not_looking': '暂不找工作'
  }
  return statusMap[value] || '未设置'
}

// 获取薪资标签
const getSalaryLabel = (value) => {
  const option = SALARY_OPTIONS.find(opt => opt.value === value)
  return option ? option.label : '未设置'
}

// 格式化城市显示
const formatCity = (city) => {
  if (!city) return '未设置'
  return city.split(',').join('、')
}

// 格式化行业显示
const formatIndustries = (industries) => {
  if (!industries) return []
  return typeof industries === 'string' ? industries.split(',') : industries
}

// 格式化日期显示
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}`
}

// 处理编辑
const handleEdit = (type, item) => {
  console.log('【ModuleList】处理编辑:', { type, item })
  currentModule.value = { type }
  
  // 如果是求职意向模块，直接使用数据对象
  if (type === 'job_intention') {
    editFormData.value = item || props.activeModules.find(m => m.type === type)?.data || {}
  } else {
    editFormData.value = item || {}
  }
  
  showEditModal.value = true
}

// 处理顶部编辑按钮点击
const handleModuleEdit = (type) => {
  console.log('【ModuleList】处理模块编辑:', { type })
  currentModule.value = { type }
  
  // 获取当前模块的数据
  const currentModuleData = props.activeModules.find(m => m.type === type)?.data
  console.log('【ModuleList】当前模块数据:', currentModuleData)
  
  // 如果是求职意向模块，直接使用数据对象
  if (type === 'job_intention') {
    editFormData.value = currentModuleData || {}
  } else {
    editFormData.value = {}
  }
  
  showEditModal.value = true
}

// 处理添加按钮点击
const handleAdd = (type) => {
  console.log('【ModuleList】处理添加:', {
    type,
    时间: new Date().toISOString(),
    当前模块类型: type
  })
  
  // 根据不同类型设置不同的初始值
  let initialData = {}
  if (type === 'skill') {
    initialData = {
      name: '',
      level: '',
      description: ''
    }
  } else if (type === 'project') {
    initialData = {
      name: '',
      role: '',
      start_date: '',
      end_date: '',
      is_current: false,
      description: '',
      achievement: ''
    }
  }
  
  currentModule.value = { type }
  editFormData.value = initialData
  showEditModal.value = true
}

// 添加一个 key 来强制更新教育组件
const educationKey = ref(0)

// 修改提交处理
const handleSubmit = async (data) => {
  try {
    if (currentModule.value?.type) {
      loading.value = true
      const type = currentModule.value.type
      
      try {
        let response
        
        // 根据不同模块类型处理
        switch (type) {
          case 'job_intention':
            response = await profile.jobIntention.update(data)
            break
            
          case 'work_experience':
            if (data.id) {
              response = await profile.workExperience.update(data.id, data)
            } else {
              response = await profile.workExperience.add(data)
            }
            break
            
          case 'project':
            console.log('【ModuleList】提交项目数据:', data)
            if (data.id) {
              response = await profile.project.update(data.id, data)
            } else {
              response = await profile.project.add(data)
            }
            console.log('【ModuleList】项目保存响应:', response)
            break
            
          case 'education':
            if (data.id) {
              response = await profile.education.update(data.id, data)
            } else {
              response = await profile.education.add(data)
            }
            break
            
          case 'skill':
            if (data.id) {
              response = await profile.skill.update(data.id, data)
            } else {
              response = await profile.skill.add(data)
            }
            break
            
          default:
            // 其他模块的处理
            if (profile[type]) {
              if (data.id) {
                response = await profile[type].update(data.id, data)
              } else {
                response = await profile[type].add(data)
              }
            } else {
              throw new Error(`未知的模块类型: ${type}`)
            }
        }

        if (response?.status === 200 || response?.status === 201) {
          showEditModal.value = false
          console.log('【ModuleList】准备重新获取数据')
          await props.fetchModulesData()
          console.log('【ModuleList】数据重新获取完成')
          ElMessage.success(data.id ? '更新成功' : '添加成功')
        } else {
          throw new Error(response?.data?.message || '保存失败')
        }
      } catch (error) {
        console.error('保存失败:', error)
        ElMessage.error(error.message || '保存失败，请稍后重试')
        return false
      }
    }
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error(error.message || '保存失败，请稍后重试')
    return false
  } finally {
    loading.value = false
  }
  return true
}

// 在 script setup 的开头添加这些变量
const currentModule = ref(null)
const editFormData = ref({})
const showEditModal = ref(false)
const loading = ref(false)

// 添加初始化数据的调用
onMounted(async () => {
  // 调用父组件的 fetchModulesData
  await props.fetchModulesData()
  // 添加调试日志
  console.log('【ModuleList】模块数据:', props.activeModules)
})

// 监听对话框关闭
watch(showEditModal, (newVal) => {
  if (!newVal) {
    // 清理状态
    currentModule.value = null
    editFormData.value = {}
  }
})

// 监听模块数据变化
watch(() => props.activeModules, async (newModules) => {
  console.log('【ModuleList】模块数据变化:', {
    时间: new Date().toISOString(),
    模块数量: newModules?.length,
    模块列表: newModules?.map(m => ({
      类型: m.type,
      名称: m.name,
      数据长度: Array.isArray(m.data) ? m.data.length : (m.data ? 1 : 0)
    }))
  })
}, { deep: true, immediate: true })

// 处理模块项目的删除
const handleItemDelete = async (type, itemId) => {
  itemToDelete.value = { type, id: itemId }
  showDeleteConfirm.value = true
}

// 处理整个模块的移除
const handleModuleRemove = (type) => {
  emit('remove', type)
}

// 监听对话框关闭
watch(showDeleteConfirm, (newVal) => {
  if (!newVal) {
    moduleToDelete.value = null
    itemToDelete.value = null
  }
})

// 添加调试日志
watch(() => props.activeModules, (newModules) => {
  console.log('【ModuleList】模块数据变化详情:', {
    时间: new Date().toISOString(),
    模块数量: newModules?.length,
    模块列表: newModules?.map(m => ({
      类型: m.type,
      名称: m.name,
      数据: m.data,
      可见性: m.visible
    }))
  })
}, { deep: true, immediate: true })

// 添加调试代码
watch(() => showEditModal.value, (val) => {
  console.log('【ModuleList】编辑弹窗状态变化:', {
    显示: val,
    当前模块: currentModule.value,
    编辑数据: editFormData.value
  })
})

// 添加折叠状态管理
const collapsedModules = ref({})

// 切换模块展开/关闭状态
const toggleModule = (type) => {
  collapsedModules.value[type] = !collapsedModules.value[type]
}

// 初始化时从 localStorage 读取折叠状态
onMounted(() => {
  try {
    const savedState = localStorage.getItem('moduleCollapseState')
    if (savedState) {
      collapsedModules.value = JSON.parse(savedState)
    }
  } catch (error) {
    console.error('读取模块折叠状态失败:', error)
  }
})

// 监听折叠状态变化并保存到 localStorage
watch(collapsedModules, (newState) => {
  try {
    localStorage.setItem('moduleCollapseState', JSON.stringify(newState))
  } catch (error) {
    console.error('保存模块折叠状态失败:', error)
  }
}, { deep: true })

// 判断是否显示添加按钮
const shouldShowAddButton = (type) => {
  // 求职意向不显示添加按钮，因为只能有一条记录
  if (type === 'job_intention') {
    return false
  }
  // 其他模块都显示添加按钮
  return true
}
</script>
<style scoped>
.delete-confirm-dialog :deep(.el-dialog__body) {
  @apply p-0;
}

/* 移动端适配 */
@media (max-width: 640px) {
  .delete-confirm-dialog {
    margin: 0 !important;
  }
  
  .p-6 {
    @apply p-4;
  }
}

/* 添加渐变效果 */
.bg-gray-50 {
  background: linear-gradient(to right, #f9fafb, #f3f4f6);
}

/* 悬停效果 */
.hover\:bg-gray-200:hover {
  @apply bg-gray-200 transition-colors duration-200;
}

/* 优化卡片样式 */
.border-gray-100 {
  border-color: rgba(229, 231, 235, 0.5);
}

/* 优化阴影效果 */
.hover\:shadow-sm:hover {
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

/* 优化文本行高 */
.leading-relaxed {
  line-height: 1.625;
}

/* 优化按钮悬停效果 */
button:hover .text-gray-400 {
  @apply text-gray-500 transition-colors;
}

/* 优化时间线节点效果 */
.border-blue-500 {
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

/* 优化卡片阴影效果 */
.hover\:shadow-sm:hover {
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
}

/* 优化文本行高 */
.leading-relaxed {
  line-height: 1.625;
}

/* 时间线渐变效果 */
.bg-gray-200 {
  background: linear-gradient(180deg, 
    transparent 0%,
    #e5e7eb 10%,
    #e5e7eb 90%,
    transparent 100%
  );
}

/* 添加展开/关闭按钮动画 */
.transition-transform {
  transition: transform 0.2s ease-in-out;
}

button:hover .text-gray-400 {
  @apply text-gray-600;
}
</style>
