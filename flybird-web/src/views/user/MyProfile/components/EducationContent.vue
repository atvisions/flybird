<template>
  <div class="relative space-y-0">
    <!-- 时间线 -->
    <div class="absolute left-[0.5625rem] top-3 bottom-3 w-px bg-gray-200"></div>

    <!-- 教育经历列表 -->
    <div 
      v-for="(edu, index) in data" 
      :key="index" 
      class="relative pl-12 pb-6"
    >
      <!-- 时间节点 -->
      <div class="absolute left-[0.5625rem] -translate-x-1/2 top-2 w-3 h-3 rounded-full bg-white border-2 border-blue-500"></div>
      
      <!-- 内容卡片 -->
      <div class="bg-gray-50 rounded-lg border border-gray-100 p-4 hover:shadow-sm transition-shadow">
        <div class="flex flex-col space-y-2">
          <!-- 学校和专业信息 -->
          <div class="flex items-start justify-between">
            <div class="flex-1 min-w-0">
              <h4 class="text-base font-medium text-gray-900 break-words">{{ edu.school }}</h4>
              <div class="text-sm font-medium text-blue-600 mt-1 break-words">{{ edu.major }}</div>
            </div>
          </div>

          <!-- 教育经历描述 -->
          <div class="text-sm leading-relaxed text-gray-600 break-words whitespace-pre-wrap">
            {{ edu.description }}
          </div>

          <!-- 学历 -->
          <div class="space-y-2">
            <div class="flex items-center space-x-2">
              <AcademicCapIcon class="w-4 h-4 text-gray-400" />
              <span class="text-sm text-gray-500">{{ getDegreeLabel(edu.degree) }}</span>
            </div>
          </div>

          <!-- 在校经历 -->
          <div v-if="edu.description !== undefined" class="mt-3 space-y-2">
            <div class="flex items-center space-x-2">
              <DocumentTextIcon class="w-4 h-4 text-gray-400" />
              <span class="text-sm text-gray-500">在校经历</span>
            </div>
            <div class="text-sm leading-relaxed text-gray-600 pl-6">
              {{ edu.description }}
            </div>
          </div>

          <!-- 在校成就 -->
          <div v-if="edu.achievements !== undefined" class="mt-3 space-y-2">
            <div class="flex items-center space-x-2">
              <TrophyIcon class="w-4 h-4 text-yellow-500" />
              <span class="text-sm text-gray-500">在校成就</span>
            </div>
            <div class="text-sm leading-relaxed text-gray-600 pl-6">
              {{ edu.achievements }}
            </div>
          </div>

          <!-- 调试信息 -->
          <div v-if="showDebug" class="mt-2 text-xs text-gray-400">
            <div>description: {{ typeof edu.description }} = "{{ edu.description }}"</div>
            <div>achievements: {{ typeof edu.achievements }} = "{{ edu.achievements }}"</div>
            <div>字段列表: {{ Object.keys(edu).join(', ') }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加按钮 -->
    <div class="relative pl-12">
      <div class="absolute left-[0.5625rem] -translate-x-1/2 top-2 w-3 h-3 rounded-full bg-white border-2 border-gray-300"></div>
      <button
        @click="handleAdd"
        class="w-full flex items-center justify-center px-4 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-all"
      >
        <PlusIcon class="w-4 h-4 mr-2" />
        添加教育经历
      </button>
    </div>
  </div>
</template>

<script setup>
import { 
  PencilSquareIcon,
  TrashIcon,
  PlusIcon,
  AcademicCapIcon,
  DocumentTextIcon,
  TrophyIcon
} from '@heroicons/vue/24/outline'
import { defineProps, watch, computed, ref } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    required: true,
    validator: (value) => {
      console.log('【EducationContent】数据验证:', {
        数据: value,
        类型: Array.isArray(value) ? 'Array' : typeof value,
        长度: value?.length,
        第一条: value?.[0],
        字段列表: value?.[0] ? Object.keys(value[0]) : [],
        description: value?.[0]?.description,
        achievements: value?.[0]?.achievements
      })
      return Array.isArray(value)
    }
  }
})

const emit = defineEmits(['edit', 'delete', 'add'])

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}`
}

// 获取学历标签
const getDegreeLabel = (degree) => {
  const degreeMap = {
    'high_school': '高中',
    'junior_college': '大专',
    'bachelor': '本科',
    'master': '硕士',
    'doctor': '博士',
    'other': '其他'
  }
  return degreeMap[degree] || degree
}

// 处理编辑
const handleEdit = (edu) => {
  console.log('EducationContent handleEdit:', edu)
  emit('edit', edu)
}

// 处理删除
const handleDelete = (id) => {
  emit('delete', id)
}

// 处理添加
const handleAdd = () => {
  console.log('EducationContent handleAdd')
  emit('edit', null)  // 传 null 表示新增
}

// 添加计算属性来检查字段
const hasFields = computed(() => {
  if (!props.data?.length) return false
  const firstItem = props.data[0]
  return {
    description: 'description' in firstItem,
    achievements: 'achievements' in firstItem,
    descriptionType: typeof firstItem.description,
    achievementsType: typeof firstItem.achievements,
    descriptionValue: firstItem.description,
    achievementsValue: firstItem.achievements
  }
})

// 添加调试开关
const showDebug = ref(process.env.NODE_ENV === 'development')


</script>

<style scoped>
/* 时间线渐变效果 */
.bg-gray-200 {
  background: linear-gradient(180deg, 
    transparent 0%,
    #e5e7eb 10%,
    #e5e7eb 90%,
    transparent 100%
  );
}

/* 卡片悬浮效果 */
.hover\:shadow-sm:hover {
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
}

/* 按钮悬浮效果 */
button:hover .text-gray-400 {
  @apply text-gray-500 transition-colors;
}
</style> 