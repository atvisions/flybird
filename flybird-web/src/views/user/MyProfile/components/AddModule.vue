<!-- src/views/user/MyProfile/components/AddModule.vue -->
<template>
  <div class="bg-white rounded-lg shadow">
    <div class="px-4 py-3">
      <h3 class="text-sm font-medium text-gray-900">更多模块</h3>
      
      <div class="mt-3 flex flex-wrap gap-2">
        <div v-if="loading" class="text-center text-gray-500 text-sm">
          加载中...
        </div>
        <div v-else-if="inactiveModules.length === 0" class="text-center text-gray-500 text-sm">
          暂无可添加的模块
        </div>
        <template v-else>
          <el-dropdown
            v-for="module in inactiveModules"
            :key="module.type"
            trigger="click"
            @command="handleAdd"
          >
            <button
              class="inline-flex items-center px-3 py-1.5 text-sm text-gray-600 bg-gray-50 hover:bg-gray-100 rounded border border-gray-200"
            >
              {{ getModuleName(module.type) }}
              <PlusIcon class="w-4 h-4 ml-1 text-gray-400" />
            </button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item :command="module.type">添加到简历</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { PlusIcon } from '@heroicons/vue/24/outline'
import { ALL_MODULES, OPTIONAL_MODULES } from '@/constants'

const props = defineProps({
  activeModules: {
    type: Array,
    default: () => []
  },
  allModules: {
    type: Object,
    default: () => ({})
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['add'])

// 获取模块显示名称
const getModuleName = (type) => {
  return ALL_MODULES[type] || type
}

// 计算可添加的模块
const inactiveModules = computed(() => {
  // 获取当前激活的模块类型
  const activeTypes = props.activeModules.map(m => m.type)
  
  // 从可选模块中过滤出未激活的模块
  return OPTIONAL_MODULES
    .filter(type => !activeTypes.includes(type))
    .map(type => ({
      type,
      order: props.allModules[type]?.order || 0
    }))
    .sort((a, b) => a.order - b.order)
})

// 处理添加模块
const handleAdd = (moduleType) => {
  if (props.loading) return
  emit('add', moduleType)
}
</script>

<style scoped>
.el-dropdown {
  @apply inline-block;
}
</style>