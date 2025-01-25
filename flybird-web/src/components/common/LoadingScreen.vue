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
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAccountStore } from '@/stores/account'
import { useRoute, useRouter } from 'vue-router'
import { templateApi } from '@/api/template'
import { ElMessage } from 'element-plus'
import profileApi from '@/api/profile'
import { useAuthStore } from '@/stores/auth'

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

// 加载用户信息
const loadUserInfo = async () => {
  loadingText.value = '正在获取用户信息...'
  try {
    await accountStore.fetchUserInfo()
    if (!accountStore.userInfo?.id) {
      throw new Error('无法获取用户信息')
    }
    return accountStore.userInfo.id
  } catch (error) {
    console.error('加载用户信息失败:', error)
    throw new Error('无法获取用户信息')
  }
}

// 加载用户档案数据
const loadProfileData = async () => {
  loadingText.value = '正在获取用户档案数据...'
  try {
    console.log('【LoadingScreen】开始获取用户档案数据')
    const response = await profileApi.getData()
    
    console.log('【LoadingScreen】获取档案数据响应:', {
      status: response?.status,
      hasData: !!response?.data,
      dataStructure: response?.data ? {
        code: response.data.code,
        message: response.data.message,
        hasData: !!response.data.data,
        dataKeys: response.data.data ? Object.keys(response.data.data) : []
      } : null
    })
    
    // 检查响应状态
    if (!response || !response.data) {
      console.error('【LoadingScreen】档案数据响应无效:', response)
      throw new Error('档案数据请求失败')
    }
    
    console.log('【LoadingScreen】加载的档案数据:', response.data)
    
    // 将档案数据存储到 localStorage
    localStorage.setItem('user_profile_data', JSON.stringify(response.data))
    
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

// 加载模板数据
const loadTemplateData = async () => {
  loadingText.value = '正在加载模板数据...'
  
  // 检查模板ID
  if (!props.templateId) {
    console.error('模板ID未定义')
    throw new Error('模板ID不能为空')
  }
  
  try {
    const response = await templateApi.getDetail(props.templateId)
    const templateData = response.data
    
    // 仅在编辑模式下检查权限
    if (props.mode === 'edit') {
      const creator = templateData.creator
      if (Number(creator) !== Number(accountStore.userInfo?.id)) {
        console.log('权限检查:', { creator, userId: accountStore.userInfo?.id })
        throw new Error('没有权限编辑此模板')
      }
    }

    return templateData
  } catch (error) {
    if (error.response?.status === 404) {
      throw new Error('模板不存在')
    }
    throw error
  }
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
  
  // 构造标准格式的模板数据
  let formattedTemplateData = null
  if (templateData.value) {
    console.log('【LoadingScreen】开始格式化模板数据:', templateData.value)
    
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

            // 获取字段配置
            const fieldKey = (() => {
              // 基于字段类型和标签推断key
              switch(element.props?.type) {
                case 'avatar': return 'avatar'
                case 'text':
                  switch(element.props?.label) {
                    case '姓名': return 'name'
                    case '性别': return 'gender'
                    case '出生日期': return 'birth_date'
                    case '电话': return 'phone'
                    case '邮箱': return 'email'
                    case '所在城市': return 'location'
                    default: return ''
                  }
                case 'textarea':
                  if (element.props?.label === '个人简介') return 'personal_summary'
                  return ''
                default: return ''
              }
            })()

            console.log('【LoadingScreen】处理后的field属性:', {
              hasField: !!element.field,
              fieldDataPath: `basic_info.${fieldKey}`,
              fieldType: element.props?.type || '',
              fieldKey,
              fieldLabel: element.props?.label || '',
              propsContent: element.props
            })

            return {
              id: element.id || `element-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
              type: element.type || 'text',
              x: element.position?.x || 0,
              y: element.position?.y || 0,
              width: element.width || 100,
              height: element.height || 100,
              content: element.content || '',
              style: element.style || {},
              props: element.props || {},
              field: element.field,
              dataPath: `basic_info.${fieldKey}`,
              mappingType: element.props?.type || '',
              // 添加可拖拽相关的属性
              draggable: true,
              resizable: true,
              rotatable: true,
              lockAspectRatio: false,
              selected: false,
              zIndex: element.zIndex || 1,
              // 添加变换相关的属性
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
    
    console.log('【LoadingScreen】模板数据格式化完成:', {
      id: formattedTemplateData.id,
      canvasCount: formattedTemplateData.canvases.length,
      firstCanvasElements: formattedTemplateData.canvases[0]?.elements?.length
    })
  }
  
  const eventData = {
    templateData: formattedTemplateData,
    profileData: profileData.value
  }
  
  console.log('【LoadingScreen】事件数据:', {
    hasTemplateData: !!eventData.templateData,
    templateDataStructure: eventData.templateData ? {
      id: eventData.templateData.id,
      canvasCount: eventData.templateData.canvases?.length
    } : null,
    hasProfileData: !!eventData.profileData,
    profileDataKeys: eventData.profileData?.data ? Object.keys(eventData.profileData.data) : []
  })
  
  emit('load-complete', eventData)
  
  console.log('【LoadingScreen】load-complete事件已触发')
}

// 初始化加载
const initialize = async () => {
  error.value = ''
  updateLoadingText()
  
  try {
    console.log('【LoadingScreen】开始初始化:', {
      mode: props.mode,
      templateId: props.templateId
    })

    // 加载用户信息
    console.log('【LoadingScreen】开始加载用户信息')
    const userId = await loadUserInfo()
    console.log('【LoadingScreen】用户信息加载完成:', { userId })
    
    // 如果是使用模式，加载用户档案数据
    if (props.mode === 'use') {
      console.log('【LoadingScreen】开始加载用户档案数据')
      profileData.value = await loadProfileData()
      console.log('【LoadingScreen】用户档案数据加载完成:', {
        hasData: !!profileData.value,
        dataKeys: profileData.value?.data ? Object.keys(profileData.value.data) : []
      })
    }
    
    // 如果有模板ID，加载模板数据
    if (props.templateId) {
      console.log('【LoadingScreen】开始加载模板数据:', props.templateId)
      templateData.value = await loadTemplateData()
      console.log('【LoadingScreen】模板数据加载完成:', {
        hasData: !!templateData.value,
        pages: templateData.value?.pages?.length
      })
    }
    
    console.log('【LoadingScreen】所有数据加载完成，准备触发事件')
    
    // 发送加载完成事件，传递模板数据和用户档案数据
    handleLoadComplete()
    
  } catch (err) {
    console.error('【LoadingScreen】初始化失败:', {
      error: err,
      message: err.message,
      stack: err.stack,
      mode: props.mode,
      templateId: props.templateId
    })
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
</style> 