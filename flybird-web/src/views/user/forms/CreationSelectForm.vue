<template>
    <div class="space-y-4">
      <!-- 作品列表 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 max-h-[60vh] overflow-y-auto">
        <div v-for="creation in creationsList" 
             :key="creation.id"
             class="border rounded-lg p-3 cursor-pointer"
             :class="{ 'border-primary-500 ring-2 ring-primary-500': isSelected(creation.id) }"
             @click="toggleSelection(creation)">
          <!-- 作品封面 -->
          <div class="aspect-video rounded-lg overflow-hidden mb-2">
            <img :src="creation.cover" 
                 :alt="creation.title"
                 class="w-full h-full object-cover">
          </div>
          
          <!-- 作品信息 -->
          <div>
            <h4 class="text-sm font-medium text-gray-900">{{ creation.title }}</h4>
            <p class="text-xs text-gray-500 mt-1">{{ creation.description }}</p>
          </div>
        </div>
      </div>
  
      <!-- 底部按钮 -->
      <div class="flex justify-end gap-3">
        <button @click="$emit('cancel')" 
                class="px-4 py-2 border rounded-lg hover:bg-gray-50">
          取消
        </button>
        <button @click="handleSubmit"
                class="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600">
          确认
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { getCreationsList } from '@/api/creations'
  
  const props = defineProps({
    initialSelected: {
      type: Array,
      default: () => []
    },
    maxSelect: {
      type: Number,
      default: 5
    }
  })
  
  const emit = defineEmits(['cancel', 'submit'])
  
  const creationsList = ref([])
  const selectedIds = ref([...props.initialSelected])
  
  // 获取创作集列表
  const fetchCreations = async () => {
    try {
      const res = await getCreationsList()
      if (res.data.code === 200) {
        creationsList.value = res.data.data
      }
    } catch (error) {
      console.error('获取作品列表失败:', error)
    }
  }
  
  // 检查是否已选择
  const isSelected = (id) => {
    return selectedIds.value.includes(id)
  }
  
  // 切换选择状态
  const toggleSelection = (creation) => {
    const index = selectedIds.value.indexOf(creation.id)
    if (index > -1) {
      selectedIds.value.splice(index, 1)
    } else {
      if (selectedIds.value.length >= props.maxSelect) {
        alert(`最多只能选择 ${props.maxSelect} 个作品`)
        return
      }
      selectedIds.value.push(creation.id)
    }
  }
  
  // 提交选择
  const handleSubmit = () => {
    const selectedItems = creationsList.value.filter(item => 
      selectedIds.value.includes(item.id)
    )
    emit('submit', selectedItems)
  }
  
  onMounted(() => {
    fetchCreations()
  })
  </script>