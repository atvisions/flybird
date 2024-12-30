<template>
    <div>
      <HeadView />
      <div class="min-h-screen py-12" style="padding-top: calc(var(--navbar-height) + 2rem);">
        <!-- 头部横幅 -->
        <div class="text-center mb-12">
          <h1 class="text-4xl font-bold text-gray-900 mb-4">简历资讯</h1>
          <p class="text-xl text-gray-600">获取最新的求职技巧和简历撰写指南</p>
        </div>
  
        <!-- 主要内容区域 -->
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- 左侧主要文章列表 -->
            <div class="lg:col-span-2">
              <!-- 特色文章 -->
              <div class="mb-8">
                <div class="relative aspect-[16/9] rounded-xl overflow-hidden">
                  <img src="https://picsum.photos/800/450" alt="特色文章" class="w-full h-full object-cover" />
                  <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
                  <div class="absolute bottom-0 left-0 right-0 p-6 text-white">
                    <div class="flex items-center gap-2 mb-2">
                      <span class="px-3 py-1 bg-primary-500 rounded-full text-sm">求职技巧</span>
                      <span class="text-sm">5分钟阅读</span>
                    </div>
                    <h2 class="text-2xl font-bold mb-2">如何在2024年写出一份出色的简历</h2>
                    <p class="text-gray-200">学习最新的简历写作技巧和趋势，让你的简历在竞争中脱颖而出。</p>
                  </div>
                </div>
              </div>
  
              <!-- 文章列表 -->
              <div class="space-y-8">
                <article v-for="article in articles" :key="article.id" class="flex gap-6 bg-white rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow">
                  <div class="w-1/3 aspect-[4/3]">
                    <img :src="article.image" :alt="article.title" class="w-full h-full object-cover" />
                  </div>
                  <div class="w-2/3 py-4 pr-4">
                    <div class="flex items-center gap-2 mb-2">
                      <span class="px-3 py-1 bg-gray-100 rounded-full text-sm text-gray-600">{{ article.category }}</span>
                      <span class="text-sm text-gray-500">{{ article.readTime }}分钟阅读</span>
                    </div>
                    <h3 class="text-xl font-bold text-gray-900 mb-2">{{ article.title }}</h3>
                    <p class="text-gray-600 mb-4">{{ article.excerpt }}</p>
                    <div class="flex items-center gap-4">
                      <div class="flex items-center gap-2">
                        <img :src="article.author.avatar" :alt="article.author.name" class="w-8 h-8 rounded-full" />
                        <span class="text-sm text-gray-600">{{ article.author.name }}</span>
                      </div>
                      <span class="text-sm text-gray-500">{{ article.date }}</span>
                    </div>
                  </div>
                </article>
              </div>
  
              <!-- 分页 -->
              <div class="mt-8 flex justify-center">
                <nav class="flex items-center gap-2">
                  <button class="p-2 rounded-lg border hover:bg-gray-50">
                    <ChevronLeftIcon class="w-5 h-5 text-gray-600" />
                  </button>
                  <button class="px-4 py-2 rounded-lg border bg-primary-50 text-primary-600 font-medium">1</button>
                  <button class="px-4 py-2 rounded-lg border hover:bg-gray-50">2</button>
                  <button class="px-4 py-2 rounded-lg border hover:bg-gray-50">3</button>
                  <button class="p-2 rounded-lg border hover:bg-gray-50">
                    <ChevronRightIcon class="w-5 h-5 text-gray-600" />
                  </button>
                </nav>
              </div>
            </div>
  
            <!-- 右侧边栏 -->
            <div class="lg:col-span-1">
              <!-- 搜索框 -->
              <div class="mb-8">
                <div class="relative">
                  <input type="text" 
                         placeholder="搜索文章..." 
                         class="w-full px-4 py-2 pl-10 border border-gray-300 rounded-lg focus:ring-primary-500 focus:border-primary-500" />
                  <MagnifyingGlassIcon class="w-5 h-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
                </div>
              </div>
  
              <!-- 分类列表 -->
              <div class="bg-white rounded-xl shadow-sm p-6 mb-8">
                <h3 class="text-lg font-bold text-gray-900 mb-4">文章分类</h3>
                <div class="space-y-2">
                  <button v-for="category in categories" 
                          :key="category.id"
                          class="w-full flex items-center justify-between px-4 py-2 rounded-lg hover:bg-gray-50">
                    <span class="text-gray-700">{{ category.name }}</span>
                    <span class="text-sm text-gray-500">{{ category.count }}</span>
                  </button>
                </div>
              </div>
  
              <!-- 热门文章 -->
              <div class="bg-white rounded-xl shadow-sm p-6">
                <h3 class="text-lg font-bold text-gray-900 mb-4">热门文章</h3>
                <div class="space-y-4">
                  <a v-for="article in popularArticles" 
                     :key="article.id"
                     href="#" 
                     class="flex gap-4 group">
                    <div class="w-20 aspect-[4/3] rounded-lg overflow-hidden">
                      <img :src="article.image" :alt="article.title" class="w-full h-full object-cover group-hover:scale-105 transition-transform" />
                    </div>
                    <div class="flex-1">
                      <h4 class="text-gray-900 font-medium group-hover:text-primary-600 line-clamp-2">{{ article.title }}</h4>
                      <span class="text-sm text-gray-500">{{ article.date }}</span>
                    </div>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <FootView />
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import HeadView from '../components/HeadView.vue'
  import FootView from '../components/FootView.vue'
  import { ChevronLeftIcon, ChevronRightIcon, MagnifyingGlassIcon } from '@heroicons/vue/20/solid'
  
  // 文章数据
  const articles = ref([
    {
      id: 1,
      title: '2024年最受欢迎的简历模板推荐',
      excerpt: '探索当前招聘市场最受欢迎的简历模板，了解如何选择适合你的模板。',
      image: 'https://picsum.photos/400/300?random=1',
      category: '简历模板',
      readTime: 4,
      date: '2024-01-15',
      author: {
        name: '张明',
        avatar: 'https://picsum.photos/32/32?random=1'
      }
    },
    {
      id: 2,
      title: '如何在简历中突出你的核心竞争力',
      excerpt: '学习如何在简历中展示你的优势，让招聘官一眼就能看到你的价值。',
      image: 'https://picsum.photos/400/300?random=2',
      category: '简历技巧',
      readTime: 6,
      date: '2024-01-12',
      author: {
        name: '李华',
        avatar: 'https://picsum.photos/32/32?random=2'
      }
    },
    {
      id: 3,
      title: '求职信怎么写才能打动HR',
      excerpt: '一份优秀的求职信可以大大提高你的面试机会，来看看专家的建议。',
      image: 'https://picsum.photos/400/300?random=3',
      category: '求职技巧',
      readTime: 5,
      date: '2024-01-10',
      author: {
        name: '王芳',
        avatar: 'https://picsum.photos/32/32?random=3'
      }
    }
  ])
  
  // 分类数据
  const categories = ref([
    { id: 1, name: '简历模板', count: 25 },
    { id: 2, name: '求职技巧', count: 42 },
    { id: 3, name: '面试指南', count: 38 },
    { id: 4, name: '职场发展', count: 31 },
    { id: 5, name: '行业洞察', count: 27 }
  ])
  
  // 热门文章
  const popularArticles = ref([
    {
      id: 1,
      title: '十大面试常见问题及完美回答技巧',
      image: 'https://picsum.photos/160/120?random=4',
      date: '2024-01-08'
    },
    {
      id: 2,
      title: '如何写好你的第一份简历',
      image: 'https://picsum.photos/160/120?random=5',
      date: '2024-01-05'
    },
    {
      id: 3,
      title: '2024年最热门的职业发展方向',
      image: 'https://picsum.photos/160/120?random=6',
      date: '2024-01-03'
    }
  ])
  </script>