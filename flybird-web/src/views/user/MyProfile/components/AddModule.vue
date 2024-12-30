<!-- src/views/user/MyProfile/components/AddModule.vue -->
<template>
    <div class="bg-white rounded-lg shadow">
      <div class="p-4">
        <h3 class="text-sm font-medium text-gray-900 mb-3">添加更多模块</h3>
        
        <div class="grid grid-cols-3 gap-3">
          <button
            v-for="module in filteredModules"
            :key="module.id"
            @click="$emit('activate', module.id)"
            class="flex items-center justify-between px-3 py-2 text-xs text-gray-700 bg-gray-50 hover:bg-gray-100 rounded border border-gray-200"
          >
            <span>{{ module.name }}</span>
            <PlusIcon class="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue'  // 添加这行
  import { PlusIcon } from '@heroicons/vue/24/outline'
  const props = defineProps({
    inactiveModules: {
        type: Array,
        default: () => []
    },
    loading: {
        type: Boolean,
        default: false
    }
    })

    // 过滤掉基本信息模块
    const filteredModules = computed(() => 
    props.inactiveModules.filter(module => module.id !== 'basic')
    )
</script>