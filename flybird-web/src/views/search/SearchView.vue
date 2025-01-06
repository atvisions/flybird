<template>
  <div class="min-h-screen bg-gray-50">
    <HeadView />
    
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-24">
      <!-- 搜索结果头部 -->
      <div class="mb-8">
        <h1 class="text-2xl font-medium text-gray-900">
          搜索结果：{{ searchQuery }}
        </h1>
        <div class="mt-2 text-sm text-gray-500">
          共找到 {{ totalResults }} 个相关结果
        </div>
      </div>

      <!-- 搜索类型切换 -->
      <div class="mb-6 border-b border-gray-200">
        <nav class="-mb-px flex space-x-8">
          <button
            v-for="tab in searchTabs"
            :key="tab.type"
            @click="handleTabChange(tab.type)"
            class="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm"
            :class="[
              currentTab === tab.type
                ? 'border-indigo-500 text-indigo-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            {{ tab.label }}
            <span class="ml-2 rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-600">
              {{ tab.count }}
            </span>
          </button>
        </nav>
      </div>

      <!-- 搜索结果列表 -->
      <div class="space-y-6">
        <!-- 文章搜索结果 -->
        <template v-if="currentTab === 'articles'">
          <div v-for="article in articles" :key="article.id" 
            class="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow">
            <router-link :to="`/article/${article.id}`" class="block">
              <h2 class="text-xl font-medium text-gray-900 hover:text-indigo-600">
                {{ article.title }}
              </h2>
              <p class="mt-2 text-gray-600 line-clamp-2">{{ article.description }}</p>
              <div class="mt-4 flex items-center text-sm text-gray-500">
                <img :src="article.author.avatar" class="w-6 h-6 rounded-full mr-2">
                <span>{{ article.author.name }}</span>
                <span class="mx-2">·</span>
                <span>{{ article.createTime }}</span>
              </div>
            </router-link>
          </div>
        </template>

        <!-- 作品集搜索结果 -->
        <template v-if="currentTab === 'portfolio'">
          <div v-for="work in portfolios" :key="work.id" 
            class="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow overflow-hidden">
            <router-link :to="`/portfolio/${work.id}`" class="block">
              <div class="aspect-w-16 aspect-h-9">
                <img :src="work.cover" class="object-cover w-full h-full">
              </div>
              <div class="p-6">
                <h2 class="text-xl font-medium text-gray-900 hover:text-indigo-600">
                  {{ work.title }}
                </h2>
                <p class="mt-2 text-gray-600 line-clamp-2">{{ work.description }}</p>
                <div class="mt-4 flex items-center text-sm text-gray-500">
                  <img :src="work.author.avatar" class="w-6 h-6 rounded-full mr-2">
                  <span>{{ work.author.name }}</span>
                </div>
              </div>
            </router-link>
          </div>
        </template>

        <!-- 用户搜索结果 -->
        <template v-if="currentTab === 'users'">
          <div v-for="user in users" :key="user.id" 
            class="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow">
            <router-link :to="`/user/${user.id}`" class="flex items-center">
              <img :src="user.avatar" class="w-12 h-12 rounded-full">
              <div class="ml-4">
                <h2 class="text-lg font-medium text-gray-900">{{ user.name }}</h2>
                <p class="mt-1 text-sm text-gray-500">{{ user.bio }}</p>
              </div>
              <button class="ml-auto px-4 py-2 text-sm text-indigo-600 border border-indigo-600 rounded-md hover:bg-indigo-50">
                关注
              </button>
            </router-link>
          </div>
        </template>
      </div>

      <!-- 加载更多 -->
      <div v-if="hasMore" class="mt-8 text-center">
        <button 
          @click="loadMore"
          class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
        >
          加载更多
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import HeadView from '@/components/HeadView.vue'

const route = useRoute()
const router = useRouter()
const searchQuery = computed(() => route.query.q || '')
const currentTab = computed(() => {
  const path = route.path
  if (path.includes('/articles')) return 'articles'
  if (path.includes('/portfolio')) return 'portfolio'
  if (path.includes('/users')) return 'users'
  return 'articles'
})
const page = ref(1)
const hasMore = ref(true)

// 搜索结果数据
const articles = ref([])
const portfolios = ref([])
const users = ref([])

// 搜索标签配置
const searchTabs = ref([
  { 
    type: 'articles', 
    label: '文章', 
    count: 0,
    path: '/search/articles'
  },
  { 
    type: 'portfolio', 
    label: '作品集', 
    count: 0,
    path: '/search/portfolio'
  },
  { 
    type: 'users', 
    label: '用户', 
    count: 0,
    path: '/search/users'
  }
])

// 总结果数
const totalResults = computed(() => {
  return searchTabs.value.reduce((total, tab) => total + tab.count, 0)
})

// 获取搜索结果
const fetchSearchResults = async () => {
  try {
    // TODO: 调用搜索 API
    // const response = await api.search({
    //   query: searchQuery.value,
    //   type: currentTab.value,
    //   page: page.value
    // })
    
    // 模拟数据
    const mockData = {
      articles: [
        {
          id: 1,
          title: '2024年前端开发趋势',
          description: '探讨新的前端框架和工具...',
          author: {
            name: '张三',
            avatar: '/avatar1.jpg'
          },
          createTime: '2小时前'
        }
      ],
      portfolios: [
        {
          id: 1,
          title: '个人作品集',
          description: '包含最新的设计作品...',
          cover: '/cover1.jpg',
          author: {
            name: '李四',
            avatar: '/avatar2.jpg'
          }
        }
      ],
      users: [
        {
          id: 1,
          name: '王五',
          avatar: '/avatar3.jpg',
          bio: '资深UI设计师，专注用户体验'
        }
      ]
    }

    // 更新数据
    if (page.value === 1) {
      articles.value = mockData.articles
      portfolios.value = mockData.portfolios
      users.value = mockData.users
    } else {
      articles.value.push(...mockData.articles)
      portfolios.value.push(...mockData.portfolios)
      users.value.push(...mockData.users)
    }

    // 更新计数
    searchTabs.value = searchTabs.value.map(tab => ({
      ...tab,
      count: mockData[tab.type]?.length || 0
    }))

    // 模拟是否还有更多数据
    hasMore.value = page.value < 3
  } catch (error) {
    console.error('搜索失败:', error)
  }
}

// 监听搜索关键词变化
watch(() => route.query.q, async (newQuery) => {
  if (newQuery) {
    page.value = 1
    await fetchSearchResults()
  }
}, { immediate: true })

// 加载更多
const loadMore = async () => {
  page.value++
  await fetchSearchResults()
}

// 修改标签点击处理
const handleTabChange = (type) => {
  router.push({
    path: `/search/${type}`,
    query: { q: searchQuery.value }
  })
}
</script> 