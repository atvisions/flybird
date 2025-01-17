<template>
  <div class="canvas-container">
    <div class="canvas-wrapper">
      <div 
        class="canvas-content" 
        :style="{ transform: `scale(${scale})` }"
        @dragover.prevent
        @drop.prevent="handleElementDrop"
        @dragenter.prevent="handleDragEnter"
        @dragleave.prevent="handleDragLeave"
        @click.self="handleCanvasClick"
        tabindex="0"
        @keydown.delete.prevent="handleDeleteElement"
        @keydown.backspace.prevent="handleDeleteElement"
      >
        <!-- 设计元素列表 -->
        <template v-for="element in elements" :key="element.id">
          <DesignElement
            :element="element"
            :is-selected="selectedElement?.id === element.id"
            :scale="scale"
            :data-fields="dataFields"
            @select="handleElementSelect"
            @update="handleElementUpdate"
          />
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import DesignElement from './DesignElement.vue'
import profile from '@/api/profile'
import { useAuthStore } from '@/stores/auth'
import { useAccountStore } from '@/stores/account'

const props = defineProps({
  scale: {
    type: Number,
    default: 1
  }
})

const emit = defineEmits(['element-select', 'data-fields-update'])

// 状态
const isDragOver = ref(false)
const elements = ref([])
const selectedElement = ref(null)
const dataFields = ref([])
const elementRefs = ref([])

// Store
const authStore = useAuthStore()
const accountStore = useAccountStore()

// 用户登录状态
const isAuthenticated = computed(() => {
  return authStore.isLoggedIn && accountStore.userInfo !== null
})

// 获取数据字段定义
const fetchDataFields = async () => {
  try {
    // 检查登录状态
    if (!isAuthenticated.value) {
      console.error('用户未登录')
      // 使用默认字段
      dataFields.value = [
        { label: '姓名', field: 'basic_info.name', group: '基本信息', type: 'text' },
        { label: '电话', field: 'basic_info.phone', group: '基本信息', type: 'text' },
        { label: '邮箱', field: 'basic_info.email', group: '基本信息', type: 'text' }
      ]
      emit('data-fields-update', dataFields.value)
      return
    }

    // 获取用户信息
    const response = await profile.getData()
    console.log('API完整响应:', response)
    
    // 确保使用正确的数据路径
    const profileData = response.data?.data
    console.log('用户资料数据:', profileData)
    
    if (!profileData) {
      throw new Error('获取用户资料失败')
    }

    // 将API返回的数据转换为字段定义
    const fields = [
      // 基本信息
      { label: '头像', field: 'basic_info.avatar', group: '基本信息', type: 'image' },
      { label: '姓名', field: 'basic_info.name', group: '基本信息', type: 'text' },
      { label: '性别', field: 'basic_info.gender', group: '基本信息', type: 'text' },
      { label: '出生日期', field: 'basic_info.birth_date', group: '基本信息', type: 'text' },
      { label: '电话', field: 'basic_info.phone', group: '基本信息', type: 'text' },
      { label: '邮箱', field: 'basic_info.email', group: '基本信息', type: 'text' },
      { label: '所在地', field: 'basic_info.location', group: '基本信息', type: 'text' },
      { label: '个人总结', field: 'basic_info.personal_summary', group: '基本信息', type: 'text' },

      // 求职意向
      { label: '工作类型', field: 'job_intention.job_type', group: '求职意向', type: 'text' },
      { label: '求职状态', field: 'job_intention.job_status', group: '求职意向', type: 'text' },
      { label: '期望薪资', field: 'job_intention.expected_salary', group: '求职意向', type: 'text' },
      { label: '期望城市', field: 'job_intention.expected_city', group: '求职意向', type: 'text' },
      { label: '期望行业', field: 'job_intention.industries', group: '求职意向', type: 'text' },

      // 工作经历
      ...(profileData.work_experience || []).map((_, index) => [
        { label: `公司名称${index + 1}`, field: `work_experience[${index}].company`, group: '工作经历', type: 'text' },
        { label: `职位名称${index + 1}`, field: `work_experience[${index}].position`, group: '工作经历', type: 'text' },
        { label: `部门${index + 1}`, field: `work_experience[${index}].department`, group: '工作经历', type: 'text' },
        { label: `工作描述${index + 1}`, field: `work_experience[${index}].description`, group: '工作经历', type: 'text' }
      ]).flat(),

      // 教育经历
      ...(profileData.education || []).map((_, index) => [
        { label: `学校${index + 1}`, field: `education[${index}].school`, group: '教育经历', type: 'text' },
        { label: `专业${index + 1}`, field: `education[${index}].major`, group: '教育经历', type: 'text' },
        { label: `学历${index + 1}`, field: `education[${index}].degree`, group: '教育经历', type: 'text' }
      ]).flat(),

      // 项目经历
      ...(profileData.project || []).map((_, index) => [
        { label: `项目名称${index + 1}`, field: `project[${index}].name`, group: '项目经历', type: 'text' },
        { label: `项目角色${index + 1}`, field: `project[${index}].role`, group: '项目经历', type: 'text' },
        { label: `项目描述${index + 1}`, field: `project[${index}].description`, group: '项目经历', type: 'text' }
      ]).flat(),

      // 技能特长
      ...(profileData.skill || []).map((_, index) => [
        { label: `技能名称${index + 1}`, field: `skill[${index}].name`, group: '技能特长', type: 'text' },
        { label: `掌握程度${index + 1}`, field: `skill[${index}].level`, group: '技能特长', type: 'text' },
        { label: `技能描述${index + 1}`, field: `skill[${index}].description`, group: '技能特长', type: 'text' }
      ]).flat(),

      // 语言能力
      ...(profileData.language || []).map((_, index) => [
        { label: `语言名称${index + 1}`, field: `language[${index}].name`, group: '语言能力', type: 'text' },
        { label: `掌握程度${index + 1}`, field: `language[${index}].proficiency_display`, group: '语言能力', type: 'text' },
        { label: `证书名称${index + 1}`, field: `language[${index}].certification`, group: '语言能力', type: 'text' },
        { label: `证书分数${index + 1}`, field: `language[${index}].score`, group: '语言能力', type: 'text' }
      ]).flat()
    ]

    dataFields.value = fields
    console.log('设置的字段:', dataFields.value)
    emit('data-fields-update', dataFields.value)
  } catch (error) {
    console.error('获取数据字段失败:', error)
    // 使用默认字段
    dataFields.value = [
      { label: '姓名', field: 'basic_info.name', group: '基本信息', type: 'text' },
      { label: '电话', field: 'basic_info.phone', group: '基本信息', type: 'text' },
      { label: '邮箱', field: 'basic_info.email', group: '基本信息', type: 'text' }
    ]
    emit('data-fields-update', dataFields.value)
  }
}

// 处理画布点击
const handleCanvasClick = (e) => {
  if (e.target === e.currentTarget) {
    selectedElement.value = null
    emit('element-select', null)
  }
}

// 处理元素选择
const handleElementSelect = (element) => {
  selectedElement.value = element
  emit('element-select', element)
}

// 处理元素更新
const handleElementUpdate = (updatedElement) => {
  const index = elements.value.findIndex(el => el.id === updatedElement.id)
  if (index > -1) {
    elements.value[index] = { ...updatedElement }
    if (selectedElement.value?.id === updatedElement.id) {
      selectedElement.value = { ...updatedElement }
    }
  }
}

// 处理删除元素
const handleDeleteElement = () => {
  if (selectedElement.value) {
    const index = elements.value.findIndex(el => el.id === selectedElement.value.id)
    if (index > -1) {
      elements.value.splice(index, 1)
      selectedElement.value = null
      emit('element-select', null)
    }
  }
}

// 处理键盘事件
const handleKeyDown = (e) => {
  if ((e.key === 'Delete' || e.key === 'Backspace') && selectedElement.value) {
    e.preventDefault()
    handleDeleteElement()
  }
}

// 添加和移除全局键盘事件监听
onMounted(() => {
  document.addEventListener('keydown', handleKeyDown)
  fetchDataFields()
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyDown)
})

// 处理元素拖拽
const handleElementDrop = (event) => {
  const elementType = event.dataTransfer.getData('element-type')
  if (!elementType) return

  try {
    const elementConfig = JSON.parse(event.dataTransfer.getData('element-config'))
    const rect = event.currentTarget.getBoundingClientRect()
    const x = (event.clientX - rect.left) / props.scale
    const y = (event.clientY - rect.top) / props.scale
    
    const newElement = {
      id: Date.now().toString(),
      type: elementType,
      x,
      y,
      width: elementConfig.width || 100,
      height: elementConfig.height || 100,
      rotation: 0,
      content: elementConfig.content || '',
      ...elementConfig.styles
    }
    
    elements.value.push(newElement)
    // 自动选中新添加的元素
    selectedElement.value = newElement
    emit('element-select', newElement)
    isDragOver.value = false
  } catch (error) {
    console.error('处理元素拖放时出错:', error)
  }
}

// 处理拖拽进入
const handleDragEnter = (event) => {
  event.preventDefault()
  isDragOver.value = true
}

// 处理拖拽离开
const handleDragLeave = (event) => {
  event.preventDefault()
  isDragOver.value = false
}

// 导出布局数据
const exportLayoutData = () => {
  return {
    elements: elements.value.map(element => ({
      ...element,
      dataBinding: element.dataBinding
    }))
  }
}

// 加载模板
const loadTemplate = async (template) => {
  try {
    // 检查登录状态
    if (!isAuthenticated.value) {
      console.error('用户未登录，无法加载数据')
      return
    }

    // 获取用户数据
    const response = await profile.getData()
    console.log('模板加载 - API响应:', response)
    
    if (!response?.data?.data) {
      console.error('API响应数据为空')
      return
    }

    // 使用正确的数据路径
    const profileData = response.data.data
    console.log('模板加载 - 用户资料数据:', profileData)

    // 加载设计元素
    elements.value = (template.elements || []).map(element => {
      const newElement = { ...element }
      
      // 如果元素有数据绑定,注入实际数据
      if (element.dataBinding?.field) {
        console.log('处理数据绑定:', element.dataBinding)
        const { field } = element.dataBinding
        let value = null
        
        try {
          // 处理嵌套字段
          const fieldParts = field.split('.')
          console.log('字段路径:', fieldParts)
          
          // 处理特殊字段，比如basic_info中的字段
          if (!fieldParts[0].includes('basic_info') && !field.includes('[')) {
            fieldParts.unshift('basic_info')
          }
          
          value = fieldParts.reduce((obj, key) => {
            console.log('当前字段:', key, '当前对象:', obj)
            if (!obj) return null
            
            // 处理数组索引
            const match = key.match(/(\w+)\[(\d+)\]/)
            if (match) {
              const [_, arrayName, index] = match
              const array = obj[arrayName]
              console.log('数组字段:', arrayName, '索引:', index, '数组:', array)
              return array?.[parseInt(index)]
            }
            return obj[key]
          }, profileData)
          
          console.log('获取到的字段值:', field, value)
        } catch (error) {
          console.error('获取字段值失败:', field, error)
          value = null
        }

        // 根据元素类型设置实际内容
        switch (element.type) {
          case 'image':
            if (field.includes('avatar') && value) {
              newElement.content = `http://192.168.3.16:8000${value}`
              console.log('设置头像图片:', newElement.content)
            } else {
              newElement.content = value || '/images.jpeg'
              console.log('设置默认图片:', newElement.content)
            }
            break
          case 'text':
            // 处理特殊字段的显示
            if (value !== null && value !== undefined) {
              if (typeof value === 'object') {
                // 如果是对象，尝试获取display值或name值
                value = value.display || value.name || JSON.stringify(value)
              }
              newElement.content = String(value)
            } else {
              newElement.content = element.content || `{{${field}}}`
            }
            console.log('设置文本内容:', newElement.content)
            break
        }
      }
      
      return newElement
    })
    
    console.log('更新后的元素列表:', elements.value)
  } catch (error) {
    console.error('加载模板数据失败:', error)
  }
}

// 更新元素数据绑定
const updateElementDataBinding = (elementId, binding) => {
  const element = elements.value.find(el => el.id === elementId)
  if (element) {
    element.dataBinding = binding
    // 更新选中元素的状态
    if (selectedElement.value?.id === elementId) {
      selectedElement.value = { ...element }
    }
  }
}

// 获取画布数据
const getCanvasData = () => {
  return {
    elements: elements.value.map(element => ({
      ...element,
      config: {
        fields: element.dataBinding || {},
        styles: {
          width: element.width,
          height: element.height,
          left: element.x,
          top: element.y,
          borderRadius: element.borderRadius,
          backgroundColor: element.backgroundColor,
          padding: element.padding || '0px',
          margin: element.margin || '0px',
          zIndex: element.zIndex || 1
        }
      }
    }))
  }
}

// 暴露方法给父组件
defineExpose({
  loadTemplate,
  getCanvasData,
  handleElementUpdate
})
</script>

<style scoped>
.canvas-container {
  flex: 1;
  overflow: hidden;
  background: #f5f5f5;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100%;
  width: 100%;
}

.canvas-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.canvas-content {
  width: 794px; /* A4 纸宽度 */
  min-height: 1123px; /* A4 纸高度 */
  background: #ffffff;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  position: relative;
  transform-origin: center;
  outline: none;
  flex-shrink: 0;
}

/* 移除滚动条相关样式 */
</style> 