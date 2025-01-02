<template>
  <TransitionRoot appear :show="!!modelValue" as="template">
    <Dialog as="div" class="relative z-50" @close="handleClose">
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
            <DialogPanel class="w-full max-w-2xl transform overflow-hidden rounded-xl bg-white text-left align-middle shadow-xl transition-all">
              <!-- 头部 -->
              <DialogTitle as="div" class="flex items-center justify-between px-6 py-4 border-b border-gray-200">
                <div class="flex items-center space-x-2">
                  <h3 class="text-lg font-medium text-gray-900">AI 优化</h3>
                  <div v-if="isOptimizing" class="flex items-center space-x-1 text-sm text-gray-500">
                    <span>已完成</span>
                    <span class="font-medium text-blue-600">{{ completedCount }}</span>
                    <span>/</span>
                    <span>{{ totalFields }}</span>
                  </div>
                </div>
                <button
                  @click="handleClose"
                  class="rounded-full p-1 hover:bg-gray-100 transition-colors"
                >
                  <XMarkIcon class="w-5 h-5 text-gray-400" />
                </button>
              </DialogTitle>

              <!-- 内容区域 -->
              <div class="px-6 py-4 overflow-y-auto max-h-[calc(100vh-16rem)]">
                <!-- 移动端视图 -->
                <div v-if="isMobile" class="divide-y divide-gray-100">
                  <div 
                    v-for="field in displayFields" 
                    :key="field.name"
                    class="py-4 space-y-3"
                  >
                    <!-- 字段名和状态 -->
                    <div class="flex justify-between items-center">
                      <div class="font-medium text-sm text-gray-900">{{ field.label }}</div>
                      <div class="flex items-center">
                        <template v-if="field.status === 'success'">
                          <CheckCircleIcon class="w-5 h-5 text-green-500" />
                        </template>
                        <template v-else-if="field.status === 'failed'">
                          <XCircleIcon class="w-5 h-5 text-red-500" />
                        </template>
                        <template v-else-if="field.status === 'processing'">
                          <div class="animate-spin rounded-full h-5 w-5 border-2 border-gray-300 border-t-blue-600"></div>
                        </template>
                        <template v-else>
                          <MinusCircleIcon class="w-5 h-5 text-gray-300" />
                        </template>
                      </div>
                    </div>
                    
                    <!-- 当前内容 -->
                    <div class="text-sm text-gray-500">
                      <div class="font-medium text-xs text-gray-400 mb-1">当前内容</div>
                      <div class="break-words">{{ field.currentValue || '未填写' }}</div>
                    </div>
                    
                    <!-- 优化建议 -->
                    <div class="text-sm text-gray-900">
                      <div class="font-medium text-xs text-gray-400 mb-1">优化建议</div>
                      <div class="break-words">
                        <template v-if="field.status === 'processing'">
                          <div class="flex items-center space-x-2 text-gray-500">
                            <div class="animate-spin rounded-full h-4 w-4 border-2 border-gray-300 border-t-blue-600"></div>
                            <span>优化中...</span>
                          </div>
                        </template>
                        <template v-else>
                          <div class="flex items-center justify-between">
                            <div class="flex-1 pr-2">{{ field.optimizedValue || '等待优化' }}</div>
                            <button
                              v-if="field.status === 'failed'"
                              @click="retryOptimize(field)"
                              :disabled="isOptimizing"
                              class="shrink-0 px-2 py-1 text-xs text-blue-600 hover:text-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                              重新优化
                            </button>
                          </div>
                        </template>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 桌面端表格视图 -->
                <div v-else class="min-w-full">
                  <!-- 表格头部 -->
                  <div class="sticky top-0 z-10 bg-gray-50 border-b border-gray-200">
                    <div class="grid grid-cols-12 gap-0">
                      <div class="col-span-2 py-3 px-4 text-left text-sm font-medium text-gray-900">字段</div>
                      <div class="col-span-4 py-3 px-4 text-left text-sm font-medium text-gray-900">当前内容</div>
                      <div class="col-span-5 py-3 px-4 text-left text-sm font-medium text-gray-900">优化建议</div>
                      <div class="col-span-1 py-3 px-4 text-center text-sm font-medium text-gray-900">状态</div>
                    </div>
                  </div>

                  <!-- 表格内容 -->
                  <div class="bg-white">
                    <div class="transition-all duration-300">
                      <div
                        v-for="field in displayFields" 
                        :key="field.name"
                        class="grid grid-cols-12 gap-0 border-b border-gray-100 hover:bg-gray-50 field-row"
                      >
                        <!-- 字段名 -->
                        <div class="col-span-2 py-3 px-4 text-sm text-gray-900">
                          {{ field.label }}
                        </div>
                        
                        <!-- 当前内容 -->
                        <div class="col-span-4 py-3 px-4 text-sm text-gray-500">
                          <div class="break-words">
                            {{ field.currentValue || '未填写' }}
                          </div>
                        </div>
                        
                        <!-- 优化建议 -->
                        <div class="col-span-5 py-3 px-4 text-sm text-gray-900">
                          <div class="break-words">
                            <template v-if="field.status === 'processing'">
                              <div class="flex items-center space-x-2 text-gray-500">
                                <div class="animate-spin rounded-full h-4 w-4 border-2 border-gray-300 border-t-blue-600"></div>
                                <span>优化中...</span>
                              </div>
                            </template>
                            <template v-else>
                              <div class="flex items-center justify-between">
                                <div>{{ field.optimizedValue || '等待优化' }}</div>
                                <button
                                  v-if="field.status === 'failed'"
                                  @click="retryOptimize(field)"
                                  :disabled="isOptimizing"
                                  class="ml-2 px-2 py-1 text-xs text-blue-600 hover:text-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                  重新优化
                                </button>
                              </div>
                            </template>
                          </div>
                        </div>
                        
                        <!-- 状态 -->
                        <div class="col-span-1 py-3 px-4 flex items-center justify-center">
                          <template v-if="field.status === 'success'">
                            <CheckCircleIcon class="w-5 h-5 text-green-500" />
                          </template>
                          <template v-else-if="field.status === 'failed'">
                            <XCircleIcon class="w-5 h-5 text-red-500" />
                          </template>
                          <template v-else-if="field.status === 'processing'">
                            <div class="animate-spin rounded-full h-5 w-5 border-2 border-gray-300 border-t-blue-600"></div>
                          </template>
                          <template v-else>
                            <MinusCircleIcon class="w-5 h-5 text-gray-300" />
                          </template>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 底部按钮 -->
              <div class="px-6 py-4 bg-gray-50 border-t border-gray-200">
                <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center space-y-3 sm:space-y-0">
                  <div class="text-sm text-gray-500">
                    {{ footerText }}
                  </div>
                  <div class="flex justify-end space-x-3">
                    <button
                      @click="handleClose"
                      :disabled="isOptimizing"
                      class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      取消
                    </button>
                    <button v-if="!isOptimizing"
                      @click="startOptimize"
                      class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700"
                    >
                      一键优化
                    </button>
                    <button v-else-if="hasFailedFields && !hasProcessingFields"
                      @click="retryFailedOptimizations"
                      class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700"
                    >
                      继续优化
                    </button>
                    <button v-else
                      @click="handleApply"
                      :disabled="!canApply"
                      class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      应用优化
                    </button>
                  </div>
                </div>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useWindowSize } from '@vueuse/core'
import { 
  XMarkIcon, 
  CheckCircleIcon, 
  XCircleIcon,
  MinusCircleIcon
} from '@heroicons/vue/24/solid'
import { ElMessageBox, ElMessage } from 'element-plus'
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionChild,
  TransitionRoot
} from '@headlessui/vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  profileData: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue', 'apply'])

// 修改字段配置，只保留需要优化的字段
const fieldConfig = [
  // 基本信息 - 只优化个人简介
  { name: 'basic_info.personal_summary', label: '个人简介', group: '基本信息' },
  
  // 求职意向 - 全部需要优化
  { name: 'job_intention.job_type', label: '工作类型', group: '求职意向' },
  { name: 'job_intention.job_status', label: '求职状态', group: '求职意向' },
  { name: 'job_intention.expected_salary', label: '期望薪资', group: '求职意向' },
  { name: 'job_intention.industries', label: '期望行业', group: '求职意向' },

  // 工作经历 - 优化职位、描述、成就和技术栈
  { name: 'work_experiences', label: '工作经历', group: '工作经历', isArray: true, fields: [
    { name: 'position', label: '职位名称' },
    { name: 'department', label: '所在部门' },
    { name: 'description', label: '工作描述' },
    { name: 'achievements', label: '工作成就' },
    { name: 'technologies', label: '技术栈' }
  ]},

  // 教育经历 - 只优化在校经历
  { name: 'educations', label: '教育经历', group: '教育经历', isArray: true, fields: [
    { name: 'description', label: '在校经历' }
  ]},

  // 技能特长 - 优化描述和等级
  { name: 'skills', label: '技能特长', group: '技能特长', isArray: true, fields: [
    { name: 'level', label: '掌握程度' },
    { name: 'description', label: '技能描述' }
  ]},

  // 证书成就 - 只优化描述
  { name: 'certificates', label: '证书成就', group: '证书成就', isArray: true, fields: [
    { name: 'description', label: '证书描述' }
  ]},

  // 项目经历 - 优化角色、描述、成就和技术栈
  { name: 'projects', label: '项目经历', group: '项目经历', isArray: true, fields: [
    { name: 'role', label: '担任角色' },
    { name: 'description', label: '项目描述' },
    { name: 'achievements', label: '项目成就' },
    { name: 'technologies', label: '使用技术' }
  ]}
]

// 修改模拟优化方法
const mockOptimize = async (field, value) => {
  if (!value) return null
  
  const optimizations = {
    // 基本信息优化
    personal_summary: value => `我是一名经验丰富的${value.includes('开发') ? '开发工程师' : '专业人士'}，${value}`,

    // 求职意向优化
    expected_salary: value => value.includes('面议') ? '根据经验和能力，期望薪资15k-25k' : value,
    industries: value => value.split(',').map(i => i.trim()).join('、'),
    job_type: value => value || '全职',
    job_status: value => value || '在职，考虑新机会',

    // 工作经历优化
    position: value => value.replace(/^高级/, '资深').replace(/工程师$/, '开发工程师'),
    department: value => value || '技术部',
    description: value => value.replace(/^我/, '').replace(/。$/, '，工作中注重团队协作和技术创新。'),
    achievements: value => value ? `${value}，为团队和公司创造了显著价值。` : '通过技术创新和流程优化，提升了团队工作效率，获得领导和同事的一致好评。',
    technologies: value => value ? value.split(',').sort().join(', ') : '',

    // 技能特长优化
    level: value => value === '熟悉' ? '精通' : value,
    'skills.description': value => `精通${value}，有丰富的实践经验。`,

    // 项目经历优化
    role: value => value || '核心开发工程师',
    'projects.description': value => value ? 
      value.replace(/。$/, '，负责核心功能开发和性能优化。') : 
      '负责项目核心功能开发，解决技术难点，提升系统性能。',
    'projects.achievements': value => value ? 
      `${value}，获得客户好评。` : 
      '按时完成项目交付，解决多个技术难点，提升系统性能30%以上。'
  }

  // 模拟 API 延迟
  await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000))

  // 根据字段名返回优化结果
  const fieldKey = field.name.split('.').pop()
  return optimizations[fieldKey] ? 
    optimizations[fieldKey](value) : 
    value // 如果没有优化规则，返回原值
}

// 修改处理字段数据的方法
const processFields = () => {
  if (!props.profileData) return []
  
  const allFields = []
  
  // 基本信息
  if (props.profileData.basic_info) {
    allFields.push({
      name: 'basic_info.bio',
      label: '个人简介',
      currentValue: props.profileData.basic_info.bio,
      optimizedValue: '',
      status: 'pending'
    })
  }
  
  // 工作经历
  if (props.profileData.work_experiences?.length) {
    props.profileData.work_experiences.forEach((exp, index) => {
      allFields.push({
        name: `work_experiences.${index}.description`,
        label: `工作描述 ${index + 1}`,
        currentValue: exp.description,
        optimizedValue: '',
        status: 'pending'
      })
      
      if (exp.achievements) {
        allFields.push({
          name: `work_experiences.${index}.achievements`,
          label: `工作成就 ${index + 1}`,
          currentValue: exp.achievements,
          optimizedValue: '',
          status: 'pending'
        })
      }
    })
  }
  
  // 项目经历
  if (props.profileData.projects?.length) {
    props.profileData.projects.forEach((project, index) => {
      allFields.push({
        name: `projects.${index}.description`,
        label: `项目描述 ${index + 1}`,
        currentValue: project.description,
        optimizedValue: '',
        status: 'pending'
      })
      
      if (project.achievements) {
        allFields.push({
          name: `projects.${index}.achievements`,
          label: `项目成就 ${index + 1}`,
          currentValue: project.achievements,
          optimizedValue: '',
          status: 'pending'
        })
      }
    })
  }
  
  return allFields
}

const fields = ref(processFields())

// 计算属性
const displayFields = computed(() => {
  return fields.value.sort((a, b) => {
    if (a.status === 'pending' && b.status !== 'pending') return 1
    if (a.status !== 'pending' && b.status === 'pending') return -1
    return 0
  })
})

const completedCount = computed(() => 
  fields.value.filter(f => ['success', 'failed'].includes(f.status)).length
)

const totalFields = computed(() => fields.value.length)

const hasOptimized = computed(() => 
  fields.value.some(f => f.status === 'success')
)

// 添加优化状态标志
const isOptimizing = ref(false)

// 添加新的计算属性
const hasFailedFields = computed(() => 
  fields.value.some(f => f.status === 'failed')
)

const hasProcessingFields = computed(() => 
  fields.value.some(f => f.status === 'processing')
)

// 修改 canApply 计算属性的逻辑
const canApply = computed(() => {
  // 不能有正在处理的字段
  if (hasProcessingFields.value) return false
  
  // 至少要有一个成功优化的字段
  const hasSuccessFields = fields.value.some(f => 
    f.status === 'success' && f.optimizedValue !== f.currentValue
  )
  
  // 所有有内容的字段都必须完成优化（成功或失败）
  const allFieldsProcessed = fields.value.every(f => 
    !f.currentValue || // 未填写的字段可以跳过
    f.status === 'success' || 
    f.status === 'failed'
  )
  
  return hasSuccessFields && allFieldsProcessed
})

// 修改底部文本
const footerText = computed(() => {
  if (!isOptimizing.value) return '点击"一键优化"开始AI优化'
  if (hasProcessingFields.value) return '正在优化中，请稍候...'
  if (hasFailedFields.value) return '部分优化失败，您可以选择继续优化或应用已优化的内容'
  if (canApply.value) return '优化完成，您可以选择应用建议的内容'
  return '正在准备优化...'
})

// 添加滚动容器的引用
const scrollContainer = ref(null)

// 修改开始优化方法
const startOptimize = async () => {
  isOptimizing.value = true
  // 只优化有内容的待处理字段
  const pendingFields = fields.value.filter(f => 
    f.currentValue && f.status === 'pending'
  )
  
  for (let i = 0; i < pendingFields.length; i++) {
    const field = pendingFields[i]
    field.status = 'processing'
    
    try {
      const optimized = await mockOptimize(field, field.currentValue)
      if (optimized) {
        field.optimizedValue = optimized
        field.status = 'success'
      } else {
        field.status = 'failed' // 改为失败而不是重置为 pending
      }
      
      // 等待DOM更新后滚动
      await nextTick()
      if (i < pendingFields.length - 1) {
        const container = scrollContainer.value
        const itemHeight = 60
        const scrollAmount = itemHeight * (i + 1)
        container.scrollTo({
          top: scrollAmount,
          behavior: 'smooth'
        })
      }
    } catch (error) {
      console.error('优化失败:', error)
      field.status = 'failed'
    }
    
    await new Promise(resolve => setTimeout(resolve, 500))
  }
}

// 修改处理关闭方法
const handleClose = () => {
  if (isOptimizing.value) {
    // 如果正在优化，提示用户是否确认关闭
    if (confirm('正在优化中，确定要关闭吗？')) {
      isOptimizing.value = false
      dialogVisible.value = false
    }
  } else {
    dialogVisible.value = false
  }
}

// 修改处理应用优化的方法
const handleApply = async () => {
  try {
    // 获取已优化的字段数量
    const optimizedCount = fields.value.filter(f => 
      f.status === 'success' && f.optimizedValue !== f.currentValue
    ).length

    // 构建确认消息
    const message = `确定要应用 ${optimizedCount} 条优化建议吗？此操作将覆盖原有内容且不可撤销。`

    // 显示确认对话框
    const confirmed = await ElMessageBox.confirm(
      message,
      '应用优化建议',
      {
        confirmButtonText: '确定应用',
        cancelButtonText: '取消',
        type: 'warning',
        closeOnClickModal: false,
        closeOnPressEscape: false,
        distinguishCancelAndClose: true,
        confirmButtonClass: 'el-button--danger',
      }
    )

    if (confirmed === 'confirm') {
      const optimizedData = {}
      fields.value.forEach(field => {
        if (field.status === 'success' && field.optimizedValue !== field.currentValue) {
          // 解析字段路径
          const pathParts = field.name.split('.')
          
          if (pathParts.length === 4) { // 数组字段，例如: work_experiences.0.description
            const [collection, index, key] = pathParts.slice(1)
            if (!optimizedData[pathParts[0]]) {
              optimizedData[pathParts[0]] = []
            }
            if (!optimizedData[pathParts[0]][parseInt(index)]) {
              optimizedData[pathParts[0]][parseInt(index)] = {}
            }
            optimizedData[pathParts[0]][parseInt(index)][key] = field.optimizedValue
          } else { // 普通字段
            const [category, key] = pathParts
            if (category && key) {
              if (!optimizedData[category]) {
                optimizedData[category] = {}
              }
              optimizedData[category][key] = field.optimizedValue
            } else {
              optimizedData[field.name] = field.optimizedValue
            }
          }
        }
      })

      emit('apply', optimizedData)
      ElMessage.success('优化内容已保存')
      dialogVisible.value = false
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('应用优化失败:', error)
      ElMessage.error('应用优化失败，请重试')
    }
  }
}

// 添加回对话框控制代码
const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 响应式布局
const { width } = useWindowSize()
const isMobile = computed(() => width.value < 640)
const dialogWidth = computed(() => {
  if (isMobile.value) return '100%'
  return '1000px'  // 增加宽度以适应内容
})

// 移除 onMounted 中的自动处理
onMounted(() => {
  if (props.profileData) {
    fields.value = processFields()
  }
})

// 监听对话框显示状态
watch(() => dialogVisible.value, (visible) => {
  if (visible) {
    fields.value = processFields()
  }
})

// 修改表格列宽度
const columnWidths = {
  label: 'w-[120px] min-w-[120px]',
  content: 'w-[200px] min-w-[200px]',
  suggestion: 'min-w-[300px] flex-1',
  status: 'w-[60px] min-w-[60px]'
}

// 添加 watch 来监控数据变化
watch(() => props.profileData, (newVal) => {
  if (newVal) {
    fields.value = processFields()
  }
}, { immediate: true, deep: true })

// 添加重试优化方法
const retryOptimize = async (field) => {
  field.status = 'processing'
  try {
    const optimized = await mockOptimize(field, field.currentValue)
    if (optimized) {
      field.optimizedValue = optimized
      field.status = 'success'
    } else {
      field.status = 'failed'
    }
  } catch (error) {
    console.error('重新优化失败:', error)
    field.status = 'failed'
  }
}

// 添加重试所有失败的优化方法
const retryFailedOptimizations = async () => {
  const failedFields = fields.value.filter(f => f.status === 'failed')
  isOptimizing.value = true
  
  for (const field of failedFields) {
    await retryOptimize(field)
    // 添加短暂延迟
    await new Promise(resolve => setTimeout(resolve, 500))
  }
  
  isOptimizing.value = false
}
</script>

<style scoped>
/* 动画效果 */
.list-move,
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.list-leave-active {
  position: absolute;
}

/* 滚动条美化 */
.overflow-y-auto {
  scrollbar-width: thin;
  scrollbar-color: rgba(0, 0, 0, 0.2) transparent;
}

.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

/* 文本换行 */
.break-words {
  word-break: break-word;
  overflow-wrap: break-word;
}

/* 添加平滑滚动 */
.overflow-y-auto {
  scroll-behavior: smooth;
}

/* 优化滚动体验 */
.field-row {
  scroll-margin: 100px; /* 确保滚动时有足够的上下文 */
}

/* 优化滚动行为 */
.scroll-smooth {
  scroll-behavior: smooth;
}

/* 确保每个字段行高一致 */
.field-row {
  min-height: 60px; /* 与 itemHeight 对应 */
}

/* 移动端优化 */
@media (max-width: 640px) {
  .field-row {
    min-height: auto;
  }
  
  .optimize-dialog {
    margin: 0;
  }
}
</style> 