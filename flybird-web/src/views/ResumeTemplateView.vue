<template>
    <div>
        <HeadView />
        <!-- 主要内容区域 -->
        <div class="min-h-screen "
            style="padding-top: calc(var(--navbar-height) + 2rem);">

            <!-- 页面标题区域 -->
            <div class="text-center mb-12">
                <h1 class="text-4xl font-bold text-gray-900 mb-4">专业简历模板</h1>
                <p class="text-xl text-gray-600">选择适合你的模板，快速创建专业简历</p>
            </div>

            <!-- 筛选器区域 -->
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-8">
                <div class="bg-white rounded-lg shadow-sm p-4">
                    <div class="flex flex-wrap gap-4 items-center">
                        <!-- 搜索框 -->
                        <div class="flex-1 min-w-[200px]">
                            <input type="text" placeholder="搜索模板..."
                                class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
                                v-model="searchQuery" />
                        </div>

                        <!-- 分类筛选 -->
                        <div class="flex gap-2">
                            <button v-for="category in categories" :key="category.id"
                                @click="selectCategory(category.id)"
                                class="px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 border" :class="[
                                    selectedCategory === category.id
                                        ? 'gradient-bg text-white border-transparent'
                                        : 'bg-white text-gray-700 hover:shadow-sm border-gray-200'
                                ]">
                                {{ category.name }}
                            </button>
                        </div>

                        <!-- 会员筛选 -->
                        <div class="flex items-center gap-2">
                            <button @click="toggleMemberFilter"
                                class="px-4 py-2 rounded-full text-sm font-medium transition-all duration-200"
                                :class="[
                                    showMemberOnly
                                        ? 'gradient-bg text-white shadow-sm'
                                        : 'bg-white text-gray-700 hover:shadow-sm border border-gray-200'
                                ]">
                                <div class="flex items-center gap-1">
                                    <svg xmlns="http://www.w3.org/2000/svg" 
                                         class="w-4 h-4" 
                                         viewBox="0 0 24 24" 
                                         fill="currentColor">
                                        <path d="M2.5 4.5l4.5 4.5L12 3l5 6 4.5-4.5L19 16H5L2.5 4.5z"/>
                                    </svg>
                                    会员模板
                                </div>
                            </button>
                        </div>

                        <!-- 排序选择 -->
                        <Listbox v-model="sortBy">
                            <div class="relative">
                                <ListboxButton
                                    class="relative w-full cursor-pointer rounded-lg bg-white py-2 pl-3 pr-10 text-left border border-gray-200 hover:shadow-sm">
                                    <span class="block truncate">{{ sortOptions[sortBy] }}</span>
                                    <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                                        <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                                    </span>
                                </ListboxButton>
                                <transition leave-active-class="transition duration-100 ease-in"
                                    leave-from-class="opacity-100" leave-to-class="opacity-0">
                                    <ListboxOptions
                                        class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                                        <ListboxOption v-for="[key, name] in Object.entries(sortOptions)" :key="key"
                                            :value="key" v-slot="{ active, selected }">
                                            <li :class="[
                                                active ? 'bg-primary-50 text-primary-600' : 'text-gray-900',
                                                'relative cursor-pointer select-none py-2 pl-3 pr-9'
                                            ]">
                                                <span
                                                    :class="[selected ? 'font-medium' : 'font-normal', 'block truncate']">
                                                    {{ name }}
                                                </span>
                                                <span v-if="selected" :class="[
                                                    active ? 'text-primary-600' : 'text-primary-500',
                                                    'absolute inset-y-0 right-0 flex items-center pr-4'
                                                ]">
                                                    <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                                </span>
                                            </li>
                                        </ListboxOption>
                                    </ListboxOptions>
                                </transition>
                            </div>
                        </Listbox>
                    </div>
                </div>
            </div>

            <!-- 模板网格 -->
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div v-for="template in filteredTemplates" :key="template.id"
                        class="group relative bg-white rounded-lg overflow-hidden shadow-sm hover:shadow-lg transition-shadow duration-300">
                        <!-- 模板预览图 -->
                        <div class="aspect-[3/4] relative">
                            <img :src="template.preview" :alt="template.name" class="w-full h-full object-cover" />
                            <!-- 会员标识 -->
                            <div v-if="template.isPremium" 
                                 class="absolute top-3 right-3 p-2 bg-black bg-opacity-50 rounded-full shadow-sm backdrop-blur-sm">
                                <svg xmlns="http://www.w3.org/2000/svg" 
                                     class="w-4 h-4 text-yellow-400" 
                                     viewBox="0 0 24 24" 
                                     fill="currentColor">
                                    <path d="M2.5 4.5l4.5 4.5L12 3l5 6 4.5-4.5L19 16H5L2.5 4.5z"/>
                                </svg>
                            </div>
                            <!-- 悬停时显示的操作按钮 -->
                            <div
                                class="absolute inset-0 bg-black bg-opacity-50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center gap-4">
                                <button class="px-4 py-2 bg-white text-gray-900 rounded-md hover:bg-gray-100">
                                    预览
                                </button>
                                <button class="px-4 py-2 gradient-bg text-white rounded-md hover:opacity-90 transition-opacity">
                                    使用模板
                                </button>
                            </div>
                        </div>
                        <!-- 模板信息 -->
                        <div class="p-4">
                            <div class="flex items-center justify-between">
                                <h3 class="text-lg font-medium text-gray-900">{{ template.name }}</h3>
                                <svg v-if="template.isPremium" 
                                     xmlns="http://www.w3.org/2000/svg" 
                                     class="w-5 h-5 text-yellow-500" 
                                     viewBox="0 0 24 24" 
                                     fill="currentColor">
                                    <path d="M2.5 4.5l4.5 4.5L12 3l5 6 4.5-4.5L19 16H5L2.5 4.5z"/>
                                </svg>
                            </div>
                            <p class="text-sm text-gray-500 mt-1">{{ template.description }}</p>
                        </div>
                        <!-- 标签 -->
                        <div class="px-4 pb-4 flex flex-wrap gap-2">
                            <span v-for="tag in template.tags" :key="tag"
                                class="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded-md">
                                {{ tag }}
                            </span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 分页组件 -->
            <div class="flex justify-center mt-12">
                <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                    <!-- ���一页 -->
                    <button @click="currentPage > 1 && (currentPage--)" :disabled="currentPage === 1"
                        class="relative inline-flex items-center px-3 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium"
                        :class="[
                            currentPage === 1
                                ? 'text-gray-300 cursor-not-allowed'
                                : 'text-gray-500 hover:bg-gray-50'
                        ]">
                        <ChevronLeftIcon class="h-5 w-5" />
                    </button>

                    <!-- 页码 -->
                    <template v-for="page in displayedPages" :key="page">
                        <button v-if="page !== '...'" @click="currentPage = page" :class="[
                            currentPage === page
                                ? 'z-10 bg-primary-50 border-primary-500 text-primary-600'
                                : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50',
                            'relative inline-flex items-center px-4 py-2 border text-sm font-medium'
                        ]">
                            {{ page }}
                        </button>
                        <span v-else
                            class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700">
                            ...
                        </span>
                    </template>

                    <!-- 下一页 -->
                    <button @click="currentPage < totalPages && (currentPage++)" :disabled="currentPage === totalPages"
                        class="relative inline-flex items-center px-3 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium"
                        :class="[
                            currentPage === totalPages
                                ? 'text-gray-300 cursor-not-allowed'
                                : 'text-gray-500 hover:bg-gray-50'
                        ]">
                        <ChevronRightIcon class="h-5 w-5" />
                    </button>
                </nav>
            </div>
        </div>
        <FootView />
    </div>
</template>
<script setup>
import { ref, computed } from 'vue'
import HeadView from '../components/HeadView.vue'
import FootView from '../components/FootView.vue'
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from '@headlessui/vue'
import { ChevronUpDownIcon, ChevronLeftIcon, ChevronRightIcon, CheckIcon } from '@heroicons/vue/20/solid'
// 状态管理
const searchQuery = ref('')
const selectedCategory = ref('all')
const sortBy = ref('popular')
const currentPage = ref(1)

// 添加会员筛选状态
const showMemberOnly = ref(false)

// 分类数据
const categories = [
    { id: 'all', name: '全部' },
    { id: 'simple', name: '简约' },
    { id: 'professional', name: '专业' },
    { id: 'creative', name: '创意' },
    { id: 'modern', name: '现代' }
]
// 排序选项
const sortOptions = {
    popular: '最受欢迎',
    newest: '最新添加',
    name: '名称排序'
}
// 模板数据
const templates = [
  {
    id: 1,
    name: 'Modern Minimal',
    description: '简约现代的设计风格，突出重点内容',
    preview: 'https://picsum.photos/800/1000?random=1',
    tags: ['简约', '现代', '通用'],
    category: 'simple',
    popularity: 98,
    isPremium: true
  },
  {
    id: 2,
    name: 'Creative Pro',
    description: '富有创意的布局，适合设计类职位',
    preview: 'https://picsum.photos/800/1000?random=2',
    tags: ['创意', '设计', '独特'],
    category: 'creative',
    popularity: 95,
    isPremium: false,
  },
  {
    id: 3,
    name: 'Executive Clean',
    description: '专业简洁的商务风格，适合管理岗位',
    preview: 'https://picsum.photos/800/1000?random=3',
    tags: ['专业', '商务', '管理'],
    category: 'professional',
    popularity: 92,
    isPremium: true
  },
  {
    id: 4,
    name: 'Tech Innovator',
    description: '现代科技风格，适合IT领域人才',
    preview: 'https://picsum.photos/800/1000?random=4',
    tags: ['科技', '创新', 'IT'],
    category: 'modern',
    popularity: 90,
    isPremium: true
  },
  {
    id: 5,
    name: 'Classic Elite',
    description: '经典优雅的设计，适合各类职位',
    preview: 'https://picsum.photos/800/1000?random=5',
    tags: ['经典', '优雅', '通用'],
    category: 'simple',
    popularity: 88,
    isPremium: false
  },
  {
    id: 6,
    name: 'Creative Edge',
    description: '独特的边缘设计，让简历更出众',
    preview: 'https://picsum.photos/800/1000?random=6',
    tags: ['创意', '独特', '现代'],
    category: 'creative',
    popularity: 86,
    isPremium: false
  },
  {
    id: 7,
    name: 'Professional Plus',
    description: '高级专业的商务模板，突显经验',
    preview: 'https://picsum.photos/800/1000?random=7',
    tags: ['专业', '商务', '高级'],
    category: 'professional',
    popularity: 85,
    isPremium: true
  },
  {
    id: 8,
    name: 'Modern Flow',
    description: '流畅的现代设计，视觉效果出众',
    preview: 'https://picsum.photos/800/1000?random=8',
    tags: ['现代', '流畅', '视觉'],
    category: 'modern',
    popularity: 83,
    isPremium: true
  },
  {
    id: 9,
    name: 'Simple Impact',
    description: '简约但有力的设计风格',
    preview: 'https://picsum.photos/800/1000?random=9',
    tags: ['简约', '有力', '清晰'],
    category: 'simple',
    popularity: 82,
    isPremium: false
  },
  {
    id: 10,
    name: 'Tech Minimal',
    description: '极简科技风格，突出专业技能',
    preview: 'https://picsum.photos/800/1000?random=10',
    tags: ['科技', '极简', '专业'],
    category: 'modern',
    popularity: 80,
    isPremium: true
  }
]
// 计算属性
const filteredTemplates = computed(() => {
    let result = templates

    // 搜索过滤
    if (searchQuery.value) {
        result = result.filter(template =>
            template.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
            template.description.toLowerCase().includes(searchQuery.value.toLowerCase())
        )
    }

    // 分类过滤
    if (selectedCategory.value !== 'all') {
        result = result.filter(template => template.category === selectedCategory.value)
    }

    // 会员筛选
    if (showMemberOnly.value) {
        result = result.filter(template => template.isPremium)
    }

    // 排序
    result = [...result].sort((a, b) => {
        if (sortBy.value === 'popular') {
            return b.popularity - a.popularity
        } else if (sortBy.value === 'newest') {
            return b.id - a.id
        } else {
            return a.name.localeCompare(b.name)
        }
    })

    return result
})

const totalPages = computed(() => {
    return Math.ceil(filteredTemplates.value.length / 12)
})

// 方法
const selectCategory = (categoryId) => {
    selectedCategory.value = categoryId
    currentPage.value = 1
}
// 计算显示的页码
const displayedPages = computed(() => {
  const total = totalPages.value
  const current = currentPage.value
  const pages = []
  
  if (total <= 7) {
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    if (current <= 3) {
      for (let i = 1; i <= 5; i++) {
        pages.push(i)
      }
      pages.push('...', total)
    } else if (current >= total - 2) {
      pages.push(1, '...')
      for (let i = total - 4; i <= total; i++) {
        pages.push(i)
      }
    } else {
      pages.push(1, '...')
      for (let i = current - 1; i <= current + 1; i++) {
        pages.push(i)
      }
      pages.push('...', total)
    }
  }
  
  return pages
})

// 切换会员筛选
const toggleMemberFilter = () => {
    showMemberOnly.value = !showMemberOnly.value
    currentPage.value = 1  // 重置页码
}
</script>
<style>
.gradient-bg {
  background: linear-gradient(to right, #FF6B6B, #FF8E8E);
}

.gradient-bg:hover {
  background: linear-gradient(to right, #FF5E5E, #FF8181);
}
</style>