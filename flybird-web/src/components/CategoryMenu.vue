<template>
  <div v-if="show" class="fixed inset-0 bg-black/50 z-[100] sm:hidden flex items-end" @click="$emit('update:show', false)">
    <div class="absolute bottom-0 left-0 right-0 bg-white rounded-t-2xl p-6 max-h-[85vh] overflow-y-auto"
      @click.stop
    >
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center space-x-2">
          <button 
            v-if="currentLevel !== 'main'"
            @click="handleBack"
            class="text-gray-400 hover:text-gray-500"
          >
            <ChevronLeftIcon class="w-5 h-5" />
          </button>
          <h3 class="text-lg font-medium text-gray-900">
            {{ getMenuTitle }}
          </h3>
        </div>
        <button @click="$emit('update:show', false)" class="text-gray-400 hover:text-gray-500">
          <XMarkIcon class="w-5 h-5" />
        </button>
      </div>
      <div class="grid grid-cols-2 gap-3 pb-6">
        <!-- 主分类导航 -->
        <template v-if="currentLevel === 'main'">
          <button
            v-for="category in categories"
            :key="category.id"
            @click="handleMainCategoryClick(category)"
            class="flex items-center justify-center px-4 py-4 rounded-xl text-sm font-medium transition-colors"
            :class="[
              currentMainCategory === category.id
                ? 'bg-blue-50 text-blue-600'
                : 'bg-gray-50 text-gray-600 hover:bg-gray-100'
            ]"
          >
            <component :is="category.icon" class="w-4 h-4 mr-2 flex-shrink-0" />
            {{ category.name }}
          </button>
        </template>

        <!-- 页面内分类 -->
        <template v-else-if="currentLevel === 'sub'">
          <button
            v-for="category in currentSubCategories"
            :key="category.id"
            @click="handleSubCategoryClick(category)"
            class="flex items-center justify-center px-4 py-4 rounded-xl text-sm font-medium transition-colors"
            :class="[
              currentSubCategory === category.id
                ? 'bg-blue-50 text-blue-600'
                : 'bg-gray-50 text-gray-600 hover:bg-gray-100'
            ]"
          >
            <component :is="category.icon" class="w-4 h-4 mr-2 flex-shrink-0" />
            {{ category.name }}
          </button>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { ChevronLeftIcon, XMarkIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  show: Boolean,
  currentLevel: String,
  currentMainCategory: String,
  currentSubCategory: String,
  currentThirdCategory: String,
  categories: {
    type: Array,
    required: true
  }
})

const emit = defineEmits([
  'update:show',
  'update:currentLevel',
  'update:currentMainCategory',
  'update:currentSubCategory',
  'update:currentThirdCategory',
  'category-change'
])

// 获取菜单标题
const getMenuTitle = computed(() => {
  if (props.currentLevel === 'main') return '选择分类'
  if (props.currentLevel === 'sub') {
    const mainCategory = props.categories.find(c => c.id === props.currentMainCategory)
    return mainCategory?.name || '选择分类'
  }
  return ''
})

// 获取当前子分类
const currentSubCategories = computed(() => {
  const mainCategory = props.categories.find(c => c.id === props.currentMainCategory)
  return mainCategory?.children || []
})

// 处理主分类点击
const handleMainCategoryClick = (category) => {
  emit('category-change', category.id, 'main')
  if (category.id !== 'all') {
    emit('update:currentLevel', 'sub')
  } else {
    emit('update:show', false)
  }
}

// 处理页面内分类点击
const handleSubCategoryClick = (category) => {
  emit('category-change', category.id, 'sub')
  emit('update:show', false)
}

const handleBack = () => {
  if (props.currentLevel === 'third') {
    emit('update:currentLevel', 'sub')
    emit('update:currentSubCategory', '')
  } else if (props.currentLevel === 'sub') {
    emit('update:currentLevel', 'main')
    emit('update:currentMainCategory', 'all')
  }
}
</script> 