<!-- src/views/user/MyProfile/components/ModuleList.vue -->
<template>
  <div class="space-y-4">
    <!-- 激活的模块列表 -->
    <div 
      v-for="module in sortedActiveModules" 
      :key="module.type" 
      class="bg-white rounded-lg shadow"
    >
      <!-- 模块头部 -->
      <div 
        class="flex items-center justify-between px-4 py-3"
      >
        <h3 class="text-base font-medium text-gray-900">
          {{ getModuleName(module.type) }}
        </h3>
        <div class="flex items-center space-x-2">
          <!-- 添加按钮 -->
          <button
            v-if="shouldShowAddButton(module.type)"
            @click="$emit('add', module.type)"
            class="p-1 rounded-full hover:bg-gray-100 transition-colors duration-200 group relative"
          >
            <PlusIcon class="w-5 h-5 text-gray-500 hover:text-gray-700" />
            <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 px-2 py-1 text-xs text-white bg-gray-800 rounded opacity-0 group-hover:opacity-100 whitespace-nowrap pointer-events-none transition-opacity duration-150">
              添加
            </div>
          </button>
          <!-- 编辑按钮 -->
          <button
            v-if="module.type === 'basic_info' || module.type === 'job_intention'"
            @click="$emit('edit', module.type, module.data)"
            class="p-1 rounded-full hover:bg-gray-100 transition-colors duration-200 group relative"
          >
            <PencilSquareIcon class="w-5 h-5 text-gray-500 hover:text-gray-700" />
            <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 px-2 py-1 text-xs text-white bg-gray-800 rounded opacity-0 group-hover:opacity-100 whitespace-nowrap pointer-events-none transition-opacity duration-150">
              编辑
            </div>
          </button>
          <!-- 删除按钮 -->
          <button
            v-if="shouldShowDeleteButton(module.type)"
            @click="$emit('remove', module.type)"
            class="p-1 rounded-full hover:bg-gray-100 transition-colors duration-200 group relative"
          >
            <MinusCircleIcon class="w-5 h-5 text-gray-500 hover:text-gray-700" />
            <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 px-2 py-1 text-xs text-white bg-gray-800 rounded opacity-0 group-hover:opacity-100 whitespace-nowrap pointer-events-none transition-opacity duration-150">
              删除
            </div>
          </button>
          <!-- 展开/收起按钮 -->
          <button
            @click="toggleModule(module)"
            class="p-1 rounded-full hover:bg-gray-100 transition-colors duration-200 group relative cursor-pointer"
          >
            <ChevronUpIcon
              v-if="expandedModules[module.type]"
              class="w-5 h-5 text-gray-500 hover:text-gray-700 transition-transform duration-200"
            />
            <ChevronDownIcon
              v-else
              class="w-5 h-5 text-gray-500 hover:text-gray-700 transition-transform duration-200"
            />
            <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 px-2 py-1 text-xs text-white bg-gray-800 rounded opacity-0 group-hover:opacity-100 whitespace-nowrap pointer-events-none transition-opacity duration-150">
              {{ expandedModules[module.type] ? '收起' : '展开' }}
            </div>
          </button>
        </div>
      </div>

      <!-- 模块内容 -->
      <div 
        v-show="expandedModules[module.type]"
        class="px-4 pb-4 transition-all duration-200"
      >
        <keep-alive>
          <component
            v-if="module.type"
            :is="getComponentByType(module.type)"
            v-bind="getComponentProps(module)"
            @edit="(data) => $emit('edit', module.type, data)"
            @delete="(id) => handleItemDelete(module.type, id)"
            @add="() => $emit('add', module.type)"
          />
        </keep-alive>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import {
  PlusIcon,
  PencilSquareIcon,
  MinusCircleIcon,
  ChevronUpIcon,
  ChevronDownIcon
} from '@heroicons/vue/24/outline'
import { ElMessage } from 'element-plus'
import profile from '@/api/profile'

// 导入各个模块的内容组件
import BasicInfo from './BasicInfo.vue'
import JobIntentionContent from './JobIntentionContent.vue'
import WorkExperienceContent from './WorkExperienceContent.vue'
import EducationContent from './EducationContent.vue'
import ProjectContent from './ProjectContent.vue'
import SkillContent from './SkillContent.vue'
import CertificateContent from './CertificateContent.vue'
import LanguageContent from './LanguageContent.vue'
import PortfolioContent from './PortfolioContent.vue'
import SocialLinkContent from './SocialLinkContent.vue'

const props = defineProps({
  activeModules: {
    type: Array,
    default: () => []
  },
  inactiveModules: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['remove', 'edit', 'edit-item', 'delete'])

// 添加布局相关的计算属性
const sortedActiveModules = computed(() => {
  return [...props.activeModules].sort((a, b) => {
    const orderA = a.order || 999
    const orderB = b.order || 999
    return orderA - orderB
  })
})

// 获取组件映射
const getComponentByType = (type) => {
  const componentMap = {
    'basic_info': BasicInfo,
    'job_intention': JobIntentionContent,
    'work_experience': WorkExperienceContent,
    'education': EducationContent,
    'project': ProjectContent,
    'skill': SkillContent,
    'certificate': CertificateContent,
    'language': LanguageContent,
    'portfolio': PortfolioContent,
    'social_link': SocialLinkContent
  }
  return componentMap[type]
}

// 获取模块名称
const getModuleName = (type) => {
  const moduleNames = {
    'basic_info': '基本信息',
    'job_intention': '求职意向',
    'work_experience': '工作经历',
    'education': '教育经历',
    'project': '项目经历',
    'skill': '专业技能',
    'certificate': '证书奖项',
    'language': '语言能力',
    'portfolio': '作品展示',
    'social_link': '社交主页'
  }
  return moduleNames[type] || type
}

// 判断是否显示添加按钮
const shouldShowAddButton = (type) => {
  // 基本信息和求职意向只能有一条记录
  if (type === 'basic_info' || type === 'job_intention') {
    return false
  }
  return true
}

// 获取组件 props 的方法
const getComponentProps = (module) => {
  switch (module.type) {
    case 'basic_info':
      return {
        resumeData: module.data,
        loading: props.loading,
        bioExpanded: false,
        showBioExpandButton: false
      }
    case 'job_intention':
      return {
        data: module.data
      }
    case 'work_experience':
    case 'education':
    case 'project':
    case 'skill':
    case 'certificate':
    case 'language':
    case 'portfolio':
    case 'social_link':
      return {
        data: module.data
      }
    default:
      return {
        data: module.data
      }
  }
}

// 模块展开状态管理
const expandedModules = ref({})

// 从 localStorage 获取保存的状态
const getStoredState = () => {
  try {
    const stored = localStorage.getItem('moduleExpandedState')
    return stored ? JSON.parse(stored) : {}
  } catch (e) {
    console.error('Error reading from localStorage:', e)
    return {}
  }
}

// 保存状态到 localStorage
const saveState = (state) => {
  try {
    localStorage.setItem('moduleExpandedState', JSON.stringify(state))
  } catch (e) {
    console.error('Error saving to localStorage:', e)
  }
}

// 初始化所有模块状态
const initExpandedState = (modules) => {
  const storedState = getStoredState()
  modules.forEach(module => {
    // 如果有存储的状态就使用存储的，否则默认展开
    expandedModules.value[module.type] = storedState[module.type] ?? true
  })
}

// 切换模块展开状态
const toggleModule = (module) => {
  const type = module.type
  expandedModules.value[type] = !expandedModules.value[type]
  // 保存新状态
  saveState(expandedModules.value)
}

// 监听 activeModules 变化，初始化展开状态
watch(() => props.activeModules, (newModules) => {
  if (newModules) {
    initExpandedState(newModules)
  }
}, { immediate: true })

// 组件卸载时保存状态
onUnmounted(() => {
  saveState(expandedModules.value)
})

// 处理模块项目的删除
const handleItemDelete = async (type, itemId) => {
  try {
    console.log('开始删除:', type, itemId)
    await profile.deleteModuleItem(type, itemId)
    // 通知父组件数据已更新
    emit('delete', type, itemId)
    ElMessage.success('删除成功')
    }  catch (error) {
    console.error('删除失败:', error)
    ElMessage.error(error.message || '删除失败')
  }
}

// 处理添加按钮点击
const handleAdd = (type) => {
  console.log('【ModuleList】处理添加:', type)
  
  // 根据不同类型设置不同的初始值
  let initialData = {}
  if (type === 'work_experience') {
    initialData = {
      company: '',
      position: '',
      department: '',
      start_date: '',
      end_date: '',
      is_current: false,
      description: '',
      achievements: '',
      technologies: ''
    }
  } else if (type === 'skill') {
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
  
  // 触发父组件的添加事件
  emit('edit', type, initialData)
}

// 添加删除按钮的判断逻辑
const shouldShowDeleteButton = (type) => {
  return ['work_experience', 'education', 'project', 'skill', 'certificate', 'language', 'social_link', 'portfolio'].includes(type)
}

// 处理删除按钮点击
const handleDelete = (type, id) => {
  // 触发父组件的删除事件
  emit('remove', type, id)
}
</script>

<style scoped>
/* 添加过渡动画 */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}
</style>
