<!-- src/views/user/MyProfile/dialogs/CreationDialog.vue -->
<template>
    <el-dialog
      v-model="visible"
      title="选择作品"
      width="720px"
    >
      <div v-loading="loading">
        <el-tabs v-model="activeTab">
          <el-tab-pane label="我的作品" name="my">
            <div class="grid grid-cols-2 gap-4">
              <div
                v-for="item in myCreations"
                :key="item.id"
                class="border rounded-lg p-3 cursor-pointer"
                :class="isSelected(item.id) ? 'border-primary-500 bg-primary-50' : 'border-gray-200'"
                @click="toggleSelection(item.id)"
              >
                <div class="flex items-start space-x-3">
                  <el-checkbox v-model="selectedIds" :label="item.id" />
                  <div class="flex-1 min-w-0">
                    <h4 class="text-sm font-medium text-gray-900 truncate">
                      {{ item.title }}
                    </h4>
                    <p class="mt-1 text-xs text-gray-500 truncate">
                      {{ item.description }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="平台作品" name="platform">
            <div class="text-center py-8 text-gray-500">
              功能开发中...
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
  
      <template #footer>
        <div class="flex justify-between items-center">
          <span class="text-sm text-gray-500">
            已选择 {{ selectedIds.length }} 个作品
          </span>
          <div class="space-x-3">
            <el-button @click="handleCancel">取消</el-button>
            <el-button 
              type="primary"
              :disabled="!selectedIds.length"
              @click="handleConfirm"
            >
              确认
            </el-button>
          </div>
        </div>
      </template>
    </el-dialog>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  
  const props = defineProps({
    modelValue: {
      type: Boolean,
      required: true
    },
    selectedIds: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    }
  })
  
  const emit = defineEmits(['update:modelValue', 'submit', 'cancel'])
  
  const visible = computed({
    get: () => props.modelValue,
    set: (val) => emit('update:modelValue', val)
  })
  
  const activeTab = ref('my')
  const selectedIds = ref(props.selectedIds)
  
  // 模拟数据
  const myCreations = [
    {
      id: '1',
      title: '个人博客系统',
      description: 'Vue3 + Node.js 开发的博客系统'
    },
    {
      id: '2',
      title: '电商小程序',
      description: 'uni-app 开发的电商小程序'
    }
  ]
  
  const isSelected = (id) => {
    return selectedIds.value.includes(id)
  }
  
  const toggleSelection = (id) => {
    const index = selectedIds.value.indexOf(id)
    if (index > -1) {
      selectedIds.value.splice(index, 1)
    } else {
      selectedIds.value.push(id)
    }
  }
  
  const handleConfirm = () => {
    emit('submit', selectedIds.value)
  }
  
  const handleCancel = () => {
    emit('cancel')
  }
  </script>