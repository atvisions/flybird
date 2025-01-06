<template>
  <div class="py-16 lg:py-16 mt-8 lg:mt-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 顶部横幅 -->
      <PageBanner theme="violet">
        <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">社区</h1>
        <p class="text-gray-600 text-lg max-w-2xl">发现优秀作品，交流学习经验</p>
      </PageBanner>

      <!-- 使用导航组件 -->
      <CommunityNavigation v-model:currentCategory="currentCategory" />

      <!-- 首页内容概览 -->
      <div class="flex flex-col lg:flex-row gap-3 lg:gap-6">
        <!-- 左侧内容：话题 + 文章 -->
        <div class="lg:w-2/3 space-y-3 lg:space-y-6">
          <!-- 热门话题 -->
          <div class="bg-white rounded-lg lg:rounded-xl border border-gray-100 p-4 lg:p-6">
            <div class="flex items-center justify-between mb-3 lg:mb-4">
              <h2 class="text-lg font-bold text-gray-900">热门话题</h2>
              <router-link 
                to="/community/topics"
                class="text-sm font-medium text-gray-500 hover:text-gray-900"
              >
                更多
              </router-link>
            </div>
            <!-- 显示一个话题 -->
            <div v-if="hotTopics[0]" class="group cursor-pointer">
              <!-- 标题和作者信息 -->
              <div class="flex items-center justify-between mb-6">
                <h3 class="text-lg font-bold text-gray-900">{{ hotTopics[0].title }}</h3>
                <div class="flex items-center gap-3">
                  <div class="text-right">
                    <div class="text-sm font-medium text-gray-900">{{ hotTopics[0].author.name }}</div>
                    <div class="text-xs text-gray-500">{{ hotTopics[0].createTime }}</div>
                  </div>
                  <img :src="hotTopics[0].author.avatar" class="w-10 h-10 rounded-full ring-2 ring-gray-50">
                </div>
              </div>
              
              <!-- VS选项对比区域 -->
              <div class="relative mb-6">
                <!-- 进度条背景 -->
                <div class="absolute inset-0 flex">
                  <!-- 左侧进度 -->
                  <div 
                    class="h-full bg-gradient-to-r from-blue-50 to-blue-100 rounded-l-lg"
                    :style="{ width: `${(hotTopics[0].votesA / (hotTopics[0].votesA + hotTopics[0].votesB)) * 100}%` }"
                  ></div>
                  <!-- 右侧进度 -->
                  <div 
                    class="h-full bg-gradient-to-l from-purple-50 to-purple-100 rounded-r-lg"
                    :style="{ width: `${(hotTopics[0].votesB / (hotTopics[0].votesA + hotTopics[0].votesB)) * 100}%` }"
                  ></div>
                </div>

                <!-- 选项内容 -->
                <div class="relative flex items-center min-h-[80px]">
                  <!-- 选项A -->
                  <div class="flex-1 p-4">
                    <div class="text-center">
                      <!-- 百分比指示器 -->
                      <div class="absolute -top-3 left-[25%] -translate-x-1/2 px-3 py-1 bg-blue-600 rounded-full text-white text-xs font-medium">
                        {{ Math.round((hotTopics[0].votesA / (hotTopics[0].votesA + hotTopics[0].votesB)) * 100) }}%
                      </div>
                      <div class="font-medium text-blue-600 mb-1">{{ hotTopics[0].optionA }}</div>
                      <div class="text-sm text-gray-500 mb-4">{{ hotTopics[0].votesA }} 票</div>
                      <!-- 投票按钮 -->
                      <button 
                        class="w-20 h-10 rounded-full border-2 border-blue-200 bg-white hover:bg-blue-50 transition-colors mx-auto flex items-center justify-center cursor-pointer"
                      >
                        <HandThumbUpIcon class="w-4 h-4 text-blue-600" />
                        <span class="ml-2 text-sm font-medium text-blue-600">投票</span>
                      </button>
                    </div>
                  </div>

                  <!-- VS标志 -->
                  <div class="w-12 h-12 rounded-full bg-white shadow-md border border-gray-100 flex items-center justify-center z-10">
                    <span class="text-sm font-bold bg-gradient-to-r from-blue-600 to-purple-600 text-transparent bg-clip-text">VS</span>
                  </div>

                  <!-- 选项B -->
                  <div class="flex-1 p-4">
                    <div class="text-center">
                      <!-- 百分比指示器 -->
                      <div class="absolute -top-3 right-[25%] translate-x-1/2 px-3 py-1 bg-purple-600 rounded-full text-white text-xs font-medium">
                        {{ Math.round((hotTopics[0].votesB / (hotTopics[0].votesA + hotTopics[0].votesB)) * 100) }}%
                      </div>
                      <div class="font-medium text-purple-600 mb-1">{{ hotTopics[0].optionB }}</div>
                      <div class="text-sm text-gray-500 mb-4">{{ hotTopics[0].votesB }} 票</div>
                      <!-- 投票按钮 -->
                      <button 
                        class="cursor-pointer w-20 h-10 rounded-full border-2 border-purple-200 bg-white hover:bg-purple-50 transition-colors mx-auto flex items-center justify-center"
                      >
                        <HandThumbUpIcon class="w-4 h-4 text-purple-600" />
                        <span class="ml-2 text-sm font-medium text-purple-600">投票</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 底部信息 -->
              <div class="flex items-center justify-between pt-4 border-t border-gray-100">
                <!-- 参与者头像组 -->
                <div class="flex items-center">
                  <!-- 当没有人参与时 -->
                  <div v-if="hotTopics[0].votesA + hotTopics[0].votesB === 0" 
                    class="text-sm text-gray-400"
                  >
                    暂无人参与
                  </div>
                  <!-- 当只有1人参与时 -->
                  <div v-else-if="hotTopics[0].votesA + hotTopics[0].votesB === 1" 
                    class="flex items-center gap-2"
                  >
                    <img :src="`https://picsum.photos/32/32?random=${hotTopics[0].id}`"
                      class="w-8 h-8 rounded-full border-2 border-white"
                    >
                    <span class="text-sm text-gray-500">第一个参与者</span>
                  </div>
                  <!-- 当有多人参与时 -->
                  <div v-else class="flex items-center gap-2">
                    <div class="flex -space-x-2">
                      <img v-for="i in Math.min(5, Math.floor((hotTopics[0].votesA + hotTopics[0].votesB) / 10))" :key="i"
                        :src="`https://picsum.photos/32/32?random=${hotTopics[0].id * 10 + i}`"
                        class="w-8 h-8 rounded-full border-2 border-white hover:scale-110 transition-transform duration-300"
                      >
                      <div v-if="hotTopics[0].votesA + hotTopics[0].votesB > 50" 
                        class="w-8 h-8 rounded-full border-2 border-white bg-gray-50 flex items-center justify-center hover:bg-gray-100 transition-colors"
                      >
                        <span class="text-xs text-gray-500">+{{ hotTopics[0].votesA + hotTopics[0].votesB - 50 }}</span>
                      </div>
                    </div>
                    <span class="text-sm text-gray-500">{{ hotTopics[0].votesA + hotTopics[0].votesB }} 人参与</span>
                  </div>
                </div>
                <div class="flex items-center space-x-3 text-sm text-gray-500">
                  <span class="flex items-center">
                    <ChatBubbleLeftIcon class="w-4 h-4 mr-1" />{{ hotTopics[0].comments }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- 热门文章 -->
          <div class="bg-white rounded-lg lg:rounded-xl border border-gray-100 p-4 lg:p-6">
            <div class="flex items-center justify-between mb-3 lg:mb-6">
              <h2 class="text-lg font-bold text-gray-900">热门文章</h2>
              <router-link 
                to="/community/articles"
                class="text-sm font-medium text-gray-500 hover:text-gray-900 flex items-center group"
              >
                更多
                <ChevronRightIcon class="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
              </router-link>
            </div>
            <div class="space-y-3 lg:space-y-5">
              <div v-for="(article, index) in hotArticles" :key="article.id"
                class="group cursor-pointer rounded-lg lg:rounded-xl hover:bg-gray-50 transition-colors"
              >
                <!-- 使用flex-col在移动端垂直布局，lg:flex-row在大屏幕水平布局 -->
                <div class="flex flex-col lg:flex-row gap-3 lg:gap-4 p-3 lg:p-4">
                  <!-- 序号和内容容器 -->
                  <div class="flex flex-1 gap-4">
                    <!-- 序号 -->
                    <div class="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center"
                      :class="{
                        'bg-orange-100 text-orange-600': index === 0,
                        'bg-blue-100 text-blue-600': index === 1,
                        'bg-purple-100 text-purple-600': index === 2,
                        'bg-gray-100 text-gray-600': index > 2
                      }"
                    >
                      <span class="text-sm font-medium">{{ index + 1 }}</span>
                    </div>

                    <!-- 文章信息 -->
                    <div class="flex-1 min-w-0">
                      <h3 class="text-base font-medium text-gray-900 group-hover:text-blue-600 transition-colors line-clamp-1 mb-2">
                        {{ article.title }}
                      </h3>
                      <!-- 在移动端隐藏描述 -->
                      <p class="text-sm text-gray-500 line-clamp-1 mb-3 hidden lg:block">{{ article.description }}</p>
                      <div class="flex flex-wrap items-center gap-4">
                        <div class="flex items-center space-x-2">
                          <img :src="article.author.avatar" class="w-5 h-5 rounded-full">
                          <span class="text-sm text-gray-600">{{ article.author.name }}</span>
                        </div>
                        <div class="flex items-center text-xs text-gray-500 space-x-3">
                          <span class="flex items-center">
                            <EyeIcon class="w-3 h-3 mr-1" />{{ article.views }}
                          </span>
                          <span class="flex items-center">
                            <ChatBubbleLeftIcon class="w-3 h-3 mr-1" />{{ article.comments }}
                          </span>
                          <span class="hidden sm:inline">{{ article.createTime }}</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- 文章封面图 -->
                  <div class="flex-shrink-0 w-full lg:w-24 h-32 lg:h-24 rounded-lg overflow-hidden order-first lg:order-last">
                    <img 
                      :src="article.cover" 
                      class="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-500"
                      alt=""
                    >
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧内容：问答 -->
        <div class="lg:w-1/3">
          <div class="bg-white rounded-lg lg:rounded-xl border border-gray-100 p-4 lg:p-6">
            <div class="flex items-center justify-between mb-3 lg:mb-6">
              <h2 class="text-lg font-bold text-gray-900">热门问答</h2>
              <router-link 
                to="/community/questions"
                class="text-sm font-medium text-gray-500 hover:text-gray-900 flex items-center group"
              >
                更多
                <ChevronRightIcon class="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
              </router-link>
            </div>
            <div class="space-y-3 lg:space-y-5">
              <div v-for="(question, index) in hotQuestions" :key="question.id"
                class="group cursor-pointer p-3 lg:p-4 rounded-lg lg:rounded-xl hover:bg-gray-50 transition-colors"
              >
                <!-- 问题标题和回答数 -->
                <div class="flex items-start space-x-3">
                  <div class="flex-shrink-0 w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center">
                    <QuestionMarkCircleIcon class="w-5 h-5 text-blue-500" />
                  </div>
                  <div class="flex-1 min-w-0">
                    <h3 class="text-base font-medium text-gray-900 group-hover:text-blue-600 transition-colors line-clamp-2 mb-2">
                      {{ question.title }}
                    </h3>
                    <div class="flex items-center space-x-4">
                      <div class="flex items-center text-xs text-gray-500">
                        <ChatBubbleLeftIcon class="w-3 h-3 mr-1" />
                        <span class="text-blue-600 font-medium">{{ question.answers }}</span>
                        <span class="ml-1">回答</span>
                      </div>
                      <div class="text-xs text-gray-500">{{ question.createTime }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useStore } from 'vuex'
import {
  DocumentTextIcon,
  QuestionMarkCircleIcon,
  ScaleIcon,
  UsersIcon,
  UserIcon,
  ChevronRightIcon,
  EyeIcon,
  ChatBubbleLeftIcon,
  HandThumbUpIcon,
  PlusIcon,
} from '@heroicons/vue/24/outline'
import PageBanner from '@/components/common/PageBanner.vue'
import CommunityNavigation from '@/components/community/CommunityNavigation.vue'

const router = useRouter()
const route = useRoute()
const store = useStore()

// 使用 Vuex store 的 isAuthenticated 状态
const isAuthenticated = computed(() => store.state.isAuthenticated)

// 添加主导航数据
const mainNavs = [
  { name: '首页', path: '/community' },
  { name: '文章', path: '/community/articles' },
  { name: '问答', path: '/community/questions' },
  { name: '话题', path: '/community/topics' }
]

// 修改热门文章数据
const hotArticles = ref([
  {
    id: 1,
    title: '2024年前端开发趋势展望：AI驱动开发将成为主流',
    description: '探讨新的前端框架、工具和最佳实践，帮助开发者在新的一年保持技术领先。',
    cover: 'https://picsum.photos/600/300?random=1',
    author: {
      name: '张小明',
      avatar: 'https://picsum.photos/32/32?random=1'
    },
    views: 3102,
    comments: 56,
    createTime: '8小时前'
  },
  {
    id: 2,
    title: 'Spring Boot 3.0 新特性详解：性能提升与开发体验优化',
    description: '深入解析Spring Boot 3.0的重要更新，包括原生支持GraalVM、HTTP接口等特性。',
    cover: 'https://picsum.photos/600/300?random=2',
    author: {
      name: '李大山',
      avatar: 'https://picsum.photos/32/32?random=2'
    },
    views: 2456,
    comments: 45,
    createTime: '1天前'
  },
  {
    id: 3,
    title: '微服务架构实践：从单体到微服务的演进之路',
    description: '分享一个大型企业级应用从单体架构迁移到微服务的实践经验。',
    cover: 'https://picsum.photos/600/300?random=3',
    author: {
      name: '王大力',
      avatar: 'https://picsum.photos/32/32?random=3'
    },
    views: 1987,
    comments: 89,
    createTime: '1天前'
  },
  {
    id: 4,
    title: 'Flutter vs React Native：2024移动开发框架对比',
    description: '详细对比两大主流跨平台开发框架的优劣，从性能、生态、开发效率等多个维度进行分析。',
    cover: 'https://picsum.photos/600/300?random=4',
    author: {
      name: '赵明',
      avatar: 'https://picsum.photos/32/32?random=4'
    },
    views: 1654,
    comments: 67,
    createTime: '2天前'
  },
  {
    id: 5,
    title: 'MongoDB 性能优化实战指南',
    description: '深入探讨 MongoDB 在大规模应用场景下的性能优化策略，包括索引设计、查询优化等。',
    cover: 'https://picsum.photos/600/300?random=5',
    author: {
      name: '李云',
      avatar: 'https://picsum.photos/32/32?random=5'
    },
    views: 1432,
    comments: 34,
    createTime: '2天前'
  }
])

// 热门话题数据
const hotTopics = ref([
  {
    id: 1,
    title: '开发移动应用选择哪个方案？',
    optionA: 'Flutter',
    optionB: 'React Native',
    votesA: 234,
    votesB: 187,
    author: {
      name: '王大力',
      avatar: 'https://picsum.photos/32/32?random=1'
    },
    comments: 45
  },
  {
    id: 2,
    title: '前端状态管理选型？',
    optionA: 'Pinia',
    optionB: 'Redux',
    votesA: 445,
    votesB: 300,
    author: {
      name: '李小明',
      avatar: 'https://picsum.photos/32/32?random=2'
    },
    comments: 67
  },
  {
    id: 3,
    title: '选择哪个UI组件库？',
    optionA: 'Element Plus',
    optionB: 'Ant Design Vue',
    votesA: 567,
    votesB: 432,
    author: {
      name: '张前端',
      avatar: 'https://picsum.photos/32/32?random=3'
    },
    comments: 89
  }
])

// 热门问答数据
const hotQuestions = ref([
  {
    id: 1,
    title: '如何优雅地处理Vue3项目中的全局状态管理？',
    answers: 12,
    createTime: '2小时前'
  },
  {
    id: 2,
    title: 'Vue3性能优化的最佳实践有哪些？',
    answers: 8,
    createTime: '4小时前'
  },
  {
    id: 3,
    title: '如何实现高性能的无限滚动列表？',
    answers: 15,
    createTime: '6小时前'
  }
])

// 当前选中的分类
const currentCategory = ref('all')
</script> 