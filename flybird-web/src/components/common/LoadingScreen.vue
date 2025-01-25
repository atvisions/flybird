<template>
  <div class="fixed inset-0 bg-gradient-to-br from-gray-900 to-gray-800 flex items-center justify-center z-50">
    <div class="text-center">
      <!-- 加载动画 -->
      <div class="relative w-24 h-24 mx-auto mb-8">
        <!-- 外圈旋转光环 -->
        <div class="absolute inset-0 border-4 border-rose-500/30 rounded-full animate-[spin_3s_linear_infinite]"></div>
        <div class="absolute inset-0 border-4 border-transparent border-t-rose-500 rounded-full animate-[spin_2s_linear_infinite]"></div>
        
        <!-- 内圈脉冲 -->
        <div class="absolute inset-4 bg-rose-500 rounded-full animate-[pulse_2s_ease-in-out_infinite]">
          <div class="w-full h-full bg-gradient-to-tr from-rose-600 to-rose-400 rounded-full"></div>
        </div>
        
        <!-- 光点环绕 -->
        <div class="absolute w-2 h-2 bg-rose-400 rounded-full top-0 left-1/2 -translate-x-1/2 animate-[bounce_1s_ease-in-out_infinite]"></div>
      </div>
      
      <!-- 加载进度 -->
      <div class="w-64 h-2 bg-gray-700 rounded-full mx-auto mb-4">
        <div 
          class="h-full bg-rose-500 rounded-full transition-all duration-300"
          :style="{ width: `${loadingProgress}%` }"
        ></div>
      </div>
      
      <!-- 加载文字 -->
      <h2 class="text-2xl font-bold text-white mb-4">{{ loadingText }}</h2>
      <p class="text-rose-400 text-lg">{{ loadingDescription }}</p>
      
      <!-- 错误重试按钮 -->
      <template v-if="error">
        <p class="text-red-400 mt-4">{{ error }}</p>
        <button 
          @click="initialize"
          class="mt-4 px-6 py-2 bg-rose-500 text-white rounded-lg hover:bg-rose-600 transition-colors"
        >
          重试
        </button>
      </template>
    </div>
  </div>

  <!-- 档案完整度提示弹窗 -->
  <TransitionRoot appear :show="showCompletenessDialog" as="template">
    <Dialog as="div" @close="handleDialogClose" class="relative z-50">
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black/75" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4">
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
              <DialogTitle as="div" class="flex items-center space-x-3 mb-6">
                <div class="flex-shrink-0 w-12 h-12 bg-amber-100 rounded-full flex items-center justify-center">
                  <ExclamationTriangleIcon class="h-8 w-8 text-amber-600" />
                </div>
                <div>
                  <h3 class="text-xl font-semibold leading-6 text-gray-900">
                    档案完整度提示
                  </h3>
                  <p class="mt-1 text-sm text-gray-500">
                    完善的档案信息可以帮助您生成更专业的简历
                  </p>
                </div>
              </DialogTitle>

              <div class="mt-4">
                <!-- 总分展示 -->
                <div class="flex items-center justify-between mb-8 p-6 bg-amber-50 rounded-xl">
                  <span class="text-amber-700 font-medium">当前完整度</span>
                  <div class="text-3xl font-bold text-amber-600">{{ completenessScore }}分</div>
                </div>

                <!-- 维度得分 -->
                <div class="space-y-4">
                  <h4 class="font-medium text-gray-900">各维度得分</h4>
                  <div v-for="(score, key) in dimensionScores" :key="key"
                    class="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                    <div class="flex items-center space-x-3">
                      <div class="w-2 h-2 rounded-full" :class="{
                        'bg-red-500': score.score < 60,
                        'bg-amber-500': score.score >= 60 && score.score < 80,
                        'bg-green-500': score.score >= 80
                      }"></div>
                      <span class="text-gray-700 font-medium">{{ score.name }}</span>
                    </div>
                    <div class="flex items-center space-x-3">
                      <div class="w-32 h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div class="h-full rounded-full transition-all duration-300"
                          :class="{
                            'bg-red-500': score.score < 60,
                            'bg-amber-500': score.score >= 60 && score.score < 80,
                            'bg-green-500': score.score >= 80
                          }"
                          :style="{ width: `${score.score}%` }" />
                      </div>
                      <span class="text-gray-600 font-medium min-w-[3rem] text-right">{{ score.score }}分</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="mt-8 flex justify-end space-x-3">
                <button
                  type="button"
                  class="inline-flex justify-center rounded-lg border border-gray-300 bg-white px-5 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-rose-500 focus-visible:ring-offset-2 transition-colors"
                  @click="handleDialogClose(false)"
                >
                  暂不完善
                </button>
                <button
                  type="button"
                  class="inline-flex justify-center rounded-lg border border-transparent bg-rose-500 px-5 py-2.5 text-sm font-medium text-white hover:bg-rose-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-rose-500 focus-visible:ring-offset-2 transition-colors"
                  @click="handleDialogClose(true)"
                >
                  立即完善
                </button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useAccountStore } from '@/stores/account'
import { useRoute, useRouter } from 'vue-router'
import { templateApi } from '@/api/template'
import { ElMessage } from 'element-plus'
import profileApi from '@/api/profile'
import { useAuthStore } from '@/stores/auth'
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionChild,
  TransitionRoot,
} from '@headlessui/vue'
import {
  ExclamationTriangleIcon,
  LightBulbIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  templateId: {
    type: [String, Number],
    default: null
  },
  mode: {
    type: String,
    required: true,
    validator: (value) => ['create', 'edit', 'use'].includes(value)
  }
})

const emit = defineEmits(['load-complete'])

// 添加响应式变量
const profileData = ref(null)
const templateData = ref(null)
const loadingText = ref('加载中')
const loadingDescription = ref('请稍候...')
const error = ref('')
const loadingProgress = ref(0)
const showCompletenessDialog = ref(false)
const completenessScore = ref(0)
const dimensionScores = ref([])
const suggestions = ref([])

// 获取store实例
const authStore = useAuthStore()
const accountStore = useAccountStore()
const router = useRouter()

// 根据模式设置初始文本
const updateLoadingText = () => {
  switch (props.mode) {
    case 'create':
      loadingText.value = '准备创建新模板'
      loadingDescription.value = '正在初始化编辑器...'
      break
    case 'edit':
      loadingText.value = '加载模板数据'
      loadingDescription.value = '正在加载模板内容...'
      break
    case 'use':
      loadingText.value = '准备使用模板'
      loadingDescription.value = '正在准备模板数据...'
      break
  }
}

// 添加延迟函数
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms))

// 处理弹窗关闭
const handleDialogClose = async (confirmed) => {
  showCompletenessDialog.value = false
  if (confirmed) {
    console.log('【LoadingScreen】用户选择完善档案，准备跳转')
    router.replace('/user?tab=profile')
  } else {
    console.log('【LoadingScreen】用户选择暂不完善，跳转到模板页面')
    router.replace('/templates/resume')
  }
  return !confirmed
}

// 检查缓存的档案完整度数据
const checkCachedCompleteness = () => {
  try {
    const cachedData = localStorage.getItem('profile_completeness')
    if (cachedData) {
      const { data, timestamp } = JSON.parse(cachedData)
      // 检查缓存是否在30分钟内
      if (Date.now() - timestamp < 30 * 60 * 1000) {
        return data
      }
    }
    return null
  } catch (error) {
    console.error('【LoadingScreen】读取缓存数据失败:', error)
    return null
  }
}

// 检查档案完整度
const checkProfileCompleteness = async () => {
  if (props.mode !== 'use') {
    return true
  }

  loadingText.value = '检查档案完整度...'
  loadingDescription.value = '正在评估您的档案信息...'
  loadingProgress.value = 10
  
  try {
    // 先检查缓存
    const cachedData = checkCachedCompleteness()
    let completenessData
    
    if (cachedData) {
      completenessData = cachedData
      await delay(200)
    } else {
      await delay(800)
      const response = await profileApi.getCompleteness()
      
      if (!response?.data?.data || typeof response.data.data.total_score !== 'number') {
        throw new Error('档案完整度数据格式错误')
      }
      
      completenessData = response.data.data
      
      // 缓存数据
      localStorage.setItem('profile_completeness', JSON.stringify({
        data: completenessData,
        timestamp: Date.now()
      }))
    }
    
    const totalScore = completenessData.total_score
    const dimensions = completenessData.dimensions
    
    // 设置弹窗数据
    completenessScore.value = totalScore
    dimensionScores.value = Object.entries(dimensions).map(([key, value]) => ({
      key,
      name: {
        basic_info: '基本信息',
        experience: '工作经验',
        capability: '能力素质',
        achievement: '个人成就'
      }[key] || key,
      score: value.score,
      weight: value.weight,
      weightedScore: value.weighted_score
    }))
    
    await delay(cachedData ? 100 : 500)
    loadingProgress.value = 25
    
    if (totalScore < 50) {
      console.log('【LoadingScreen】档案完整度不足，显示确认对话框')
      showCompletenessDialog.value = true
      
      // 使用 Promise 等待用户选择
      return new Promise((resolve) => {
        const unwatch = watch(showCompletenessDialog, async (newVal) => {
          if (!newVal) {
            unwatch()
            const result = await handleDialogClose(false)
            resolve(result)
          }
        })
      })
    }
    
    return true
  } catch (error) {
    console.error('【LoadingScreen】检查档案完整度失败:', {
      error,
      message: error.message,
      response: error.response,
      stack: error.stack
    })
    throw new Error('无法获取档案完整度信息')
  }
}

// 检查缓存的用户档案数据
const checkCachedProfileData = () => {
  try {
    const cachedData = localStorage.getItem('user_profile_data')
    if (cachedData) {
      const data = JSON.parse(cachedData)
      // 检查数据是否完整
      if (data && data.data) {
        console.log('【LoadingScreen】使用缓存的用户档案数据')
        return data
      }
    }
    return null
  } catch (error) {
    console.error('【LoadingScreen】读取缓存数据失败:', error)
    return null
  }
}

// 加载用户档案数据
const loadProfileData = async () => {
  loadingText.value = '正在获取用户档案数据...'
  loadingDescription.value = '加载档案详细信息...'
  loadingProgress.value = 65
  
  try {
    // 先检查缓存
    const cachedData = checkCachedProfileData()
    if (cachedData) {
      await delay(200) // 使用缓存数据时只需要很短的延迟
      loadingProgress.value = 80
      return cachedData
    }
    
    await delay(700)
    const response = await profileApi.getData()
    
    
    if (!response || !response.data) {
      console.error('【LoadingScreen】档案数据响应无效:', response)
      throw new Error('档案数据请求失败')
    }
    
    localStorage.setItem('user_profile_data', JSON.stringify(response.data))
    await delay(500)
    loadingProgress.value = 80
    return response.data
  } catch (error) {
    console.error('【LoadingScreen】加载用户档案数据失败:', {
      error,
      message: error.message,
      response: error.response,
      stack: error.stack
    })
    throw new Error('无法获取用户档案数据')
  }
}

// 加载用户信息
const loadUserInfo = async () => {
  loadingText.value = '正在获取用户信息...'
  loadingDescription.value = '加载基本信息...'
  loadingProgress.value = 35
  
  try {
    await delay(600) // 添加延迟
    await accountStore.fetchUserInfo()
    if (!accountStore.userInfo?.id) {
      throw new Error('无法获取用户信息')
    }
    await delay(400) // 再添加一点延迟
    loadingProgress.value = 50
    return accountStore.userInfo.id
  } catch (error) {
    console.error('加载用户信息失败:', error)
    throw new Error('无法获取用户信息')
  }
}

// 加载模板数据
const loadTemplateData = async () => {
  loadingText.value = '正在加载模板数据...'
  loadingDescription.value = '准备模板内容...'
  loadingProgress.value = 90
  
  if (!props.templateId) {
    throw new Error('模板ID不能为空')
  }
  
  try {
    await delay(600) // 添加延迟
    const response = await templateApi.getDetail(props.templateId)
    const templateData = response.data
    
    if (props.mode === 'edit') {
      const creator = templateData.creator
      if (Number(creator) !== Number(accountStore.userInfo?.id)) {
        console.log('权限检查:', { creator, userId: accountStore.userInfo?.id })
        throw new Error('没有权限编辑此模板')
      }
    }

    await delay(400) // 再添加一点延迟
    loadingProgress.value = 100
    return templateData
  } catch (error) {
    if (error.response?.status === 404) {
      throw new Error('模板不存在')
    }
    throw error
  }
}

// 生成唯一ID的函数
const generateElementId = () => {
  return `element_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
}

// 处理元素前确保有ID
const ensureElementId = (element) => {
  if (!element.id) {
    element.id = generateElementId()
  }
  return element
}

// 在处理元素前调用
const processElement = (element) => {
  console.log('【LoadingScreen】处理元素:', ensureElementId(element))
  // ... 其他处理逻辑 ...
}

// 加载完成后触发事件
const handleLoadComplete = () => {
  console.log('【LoadingScreen】准备触发load-complete事件:', {
    mode: props.mode,
    hasTemplateData: !!templateData.value,
    templateDataType: typeof templateData.value,
    hasProfileData: !!profileData.value,
    profileDataType: typeof profileData.value,
    profileDataStructure: profileData.value ? {
      code: profileData.value.code,
      message: profileData.value.message,
      hasData: !!profileData.value.data,
      dataKeys: profileData.value.data ? Object.keys(profileData.value.data) : []
    } : null
  })
  
  let formattedTemplateData = null
  if (templateData.value) {

    formattedTemplateData = {
      id: templateData.value.id,
      name: templateData.value.name,
      description: templateData.value.description,
      category: templateData.value.category,
      is_public: templateData.value.is_public,
      status: templateData.value.status,
      canvases: templateData.value.pages.map((page, index) => {
        console.log(`【LoadingScreen】处理第${index + 1}页元素:`, page.page_data.elements)
        
        return {
          id: index,
          elements: (page.page_data.elements || []).map(element => {
            console.log('【LoadingScreen】处理元素:', {
              id: element.id,
              type: element.type,
              hasField: !!element.field,
              hasProps: !!element.props,
              propsKeys: element.props ? Object.keys(element.props) : [],
              propsContent: JSON.stringify(element.props, null, 2),
              fieldConfig: element.props?.fieldConfig,
              fieldType: element.props?.type,
              fieldLabel: element.props?.label,
              fieldKey: element.props?.key
            })

            const fieldConfig = (() => {
              const label = element.props?.label
              
              // 工作经历字段映射
              if (label === '公司名称' || label === '职位名称' || 
                  label === '所在部门' || label === '工作时间' || 
                  label === '工作描述' || label === '工作成就' ||
                  label === '技术栈') {
                const key = {
                  '公司名称': 'company',
                  '职位名称': 'position',
                  '所在部门': 'department',
                  '工作时间': 'duration',
                  '工作描述': 'description',
                  '工作成就': 'achievements',
                  '技术栈': 'technologies'
                }[label]
                
                // 根据字段类型设置合适的输入类型
                const fieldType = {
                  '工作描述': 'textarea',
                  '工作成就': 'textarea',
                  '技术栈': 'textarea',
                  '工作时间': 'dateRange'
                }[label] || 'text'
                
                // 检查用户档案数据
                console.log('【LoadingScreen】用户档案数据:', {
                  hasData: !!profileData.value?.data,
                  workExperience: profileData.value?.data?.work_experience,
                  workExperiences: profileData.value?.data?.work_experiences,
                  label,
                  key
                })
                
                // 确定正确的数据路径
                const dataPath = profileData.value?.data?.work_experiences ? 
                  `work_experiences[0].${key}` : 
                  `work_experience[0].${key}`
                
                return {
                  key,
                  dataPath,
                  type: fieldType
                }
              }
              
              // 求职意向字段映射
              if (label === '工作类型' || label === '求职状态' || 
                  label === '期望薪资' || label === '期望城市' || 
                  label === '期望行业') {
                const key = {
                  '工作类型': 'job_type',
                  '求职状态': 'job_status',
                  '期望薪资': 'expected_salary',
                  '期望城市': 'expected_city',
                  '期望行业': 'industries'
                }[label]
                
                return {
                  key,
                  dataPath: `job_intention.${key}`,
                  type: element.props?.type || 'text'
                }
              }
              
              // 基本信息字段映射
              switch(element.props?.type) {
                case 'avatar': 
                  return {
                    key: 'avatar',
                    dataPath: 'basic_info.avatar',
                    type: 'avatar'
                  }
                case 'text':
                  const basicInfoKey = {
                    '姓名': 'name',
                    '性别': 'gender',
                    '出生日期': 'birth_date',
                    '电话': 'phone',
                    '邮箱': 'email',
                    '所在城市': 'location'
                  }[label]
                  
                  if (basicInfoKey) {
                    return {
                      key: basicInfoKey,
                      dataPath: `basic_info.${basicInfoKey}`,
                      type: 'text'
                    }
                  }
                  break
                case 'textarea':
                  if (label === '个人简介') {
                    return {
                      key: 'personal_summary',
                      dataPath: 'basic_info.personal_summary',
                      type: 'textarea'
                    }
                  }
                  break
              }
              
              return {
                key: '',
                dataPath: '',
                type: element.props?.type || ''
              }
            })()

            // 构建基础属性
            const baseProps = {
              isSelected: false,
              draggable: true,
              resizable: true,
              rotatable: true,
              lockAspectRatio: false,
              zIndex: element.zIndex || 1,
            }

            // 合并所有属性
            return {
              ...baseProps,
              id: element.id || `element-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
              type: element.type || 'text',
              x: element.position?.x || 0,
              y: element.position?.y || 0,
              width: element.width || 100,
              height: element.height || 100,
              content: element.content || '',
              style: element.style || {},
              props: {
                ...element.props,
                isSelected: false, // 确保 props 中也包含 isSelected
              },
              field: element.field,
              dataPath: fieldConfig.dataPath,
              mappingType: fieldConfig.type,
              transform: element.transform || {
                rotate: 0,
                scaleX: 1,
                scaleY: 1
              }
            }
          }),
          config: {
            width: page.page_data.config?.width || 794,
            height: page.page_data.config?.height || 1123,
            backgroundColor: page.page_data.config?.backgroundColor || '#ffffff',
            showGrid: page.page_data.config?.showGrid ?? false,
            showGuideLine: page.page_data.config?.showGuideLine ?? true,
            scale: page.page_data.config?.scale || 1
          }
        }
      })
    }
    
  }
  
  const eventData = {
    templateData: formattedTemplateData,
    profileData: profileData.value
  }
  
  
  emit('load-complete', eventData)
 
}

// 初始化加载
const initialize = async () => {
  error.value = ''
  updateLoadingText()
  loadingProgress.value = 0
  
  try {
    console.log('【LoadingScreen】开始初始化:', {
      mode: props.mode,
      templateId: props.templateId
    })

    // 1. 检查档案完整度
    const canContinue = await checkProfileCompleteness()
    if (!canContinue) {
      console.log('【LoadingScreen】档案完整度检查未通过，终止加载')
      return
    }

    // 2. 加载用户信息
    
    const userId = await loadUserInfo()
   
    
    // 3. 如果是使用模式，加载用户档案数据
    if (props.mode === 'use') {
     
      profileData.value = await loadProfileData()

    }
    
    // 4. 如果有模板ID，加载模板数据
    if (props.templateId) {

      templateData.value = await loadTemplateData()

    }

    handleLoadComplete()
    
  } catch (err) {
    error.value = err.message || '加载失败'
    ElMessage.error(error.value)
  }
}

onMounted(() => {
  updateLoadingText()
  initialize()
})
</script>

<style scoped>
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(0.8);
    opacity: 0.8;
  }
  50% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes bounce {
  0%, 100% {
    transform: translateX(-50%) translateY(0);
  }
  50% {
    transform: translateX(-50%) translateY(-20px);
  }
}

/* 添加自定义过渡效果 */
.dialog-fade-enter-active,
.dialog-fade-leave-active {
  transition: opacity 0.3s ease;
}

.dialog-fade-enter-from,
.dialog-fade-leave-to {
  opacity: 0;
}

.dialog-slide-enter-active,
.dialog-slide-leave-active {
  transition: transform 0.3s ease;
}

.dialog-slide-enter-from,
.dialog-slide-leave-to {
  transform: translateY(-20px);
}
</style> 
