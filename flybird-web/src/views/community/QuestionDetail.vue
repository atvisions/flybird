<template>
  <div class="py-4 pb-24 lg:py-6 mt-[28px] md:mt-[72px]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 面包屑导航 -->
      <nav class="flex items-center space-x-2 text-sm mb-6" aria-label="Breadcrumb">
        <router-link to="/community" class="text-gray-500 hover:text-gray-700">
          社区
        </router-link>
        <ChevronRightIcon class="w-4 h-4 text-gray-400" />
        <router-link to="/community/questions" class="text-gray-500 hover:text-gray-700">
          问答
        </router-link>
        <ChevronRightIcon class="w-4 h-4 text-gray-400" />
        <span class="text-gray-900 font-medium truncate max-w-[200px]" :title="question.title">
          {{ question.title }}
        </span>
      </nav>

      <!-- 内容区域两栏布局 -->
      <div class="flex flex-col lg:flex-row gap-4 lg:gap-6">
        <!-- 左侧主要内容 -->
        <div class="lg:flex-1 lg:max-w-[calc(100%-320px-24px)]">
          <!-- 问题内容卡片 -->
          <div class="bg-white rounded-xl border border-gray-100 p-4 lg:p-6">
            <!-- 问题头部 -->
            <header class="mb-6">
              <div class="flex items-center gap-2 mb-3">
                <span class="px-2.5 py-1 bg-violet-100 text-violet-600 rounded-full text-xs font-medium">
                  {{ question.category }}
                </span>
                <span class="px-2.5 py-1 bg-amber-100 text-amber-600 rounded-full text-xs font-medium flex items-center">
                  <CurrencyYenIcon class="w-3.5 h-3.5 mr-0.5" />
                  {{ question.bounty }} 悬赏
                </span>
                <span v-if="question.solved" class="px-2.5 py-1 bg-green-100 text-green-600 rounded-full text-xs font-medium">
                  已解决
                </span>
              </div>
              <h1 class="text-xl font-bold text-gray-900 mb-4">
                {{ question.title }}
              </h1>
              
              <!-- 作者信息和问题数据 -->
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <img 
                    :src="question.author.avatar" 
                    :alt="question.author.name"
                    class="w-10 h-10 rounded-full mr-3"
                  >
                  <div>
                    <div class="font-medium text-gray-900">{{ question.author.name }}</div>
                    <div class="text-sm text-gray-500">{{ question.createTime }}</div>
                  </div>
                </div>

                <div class="flex items-center gap-4 text-sm text-gray-500">
                  <span class="flex items-center">
                    <EyeIcon class="w-4 h-4 mr-1" />
                    {{ question.views }} 浏览
                  </span>
                  <span class="flex items-center">
                    <ChatBubbleLeftIcon class="w-4 h-4 mr-1" />
                    {{ question.answers }} 回答
                  </span>
                </div>
              </div>
            </header>

            <!-- 问题内容 -->
            <div class="prose prose-sm max-w-none text-gray-600 mb-6">
              {{ question.content }}
            </div>

            <!-- 问题标签 -->
            <div class="flex items-center gap-2 mb-6 flex-wrap">
              <span 
                v-for="tag in question.tags" 
                :key="tag"
                class="px-2 py-0.5 bg-gray-100 text-gray-600 rounded-full text-xs hover:bg-gray-200 cursor-pointer transition-colors"
              >
                {{ tag }}
              </span>
            </div>

            <!-- 操作按钮 -->
            <div class="flex items-center justify-between py-4 border-t border-gray-100">
              <div class="flex items-center gap-2">
                <button 
                  class="flex items-center px-4 py-2 rounded-lg transition-colors"
                  :class="isLiked ? 'text-red-500 bg-red-50' : 'text-gray-600 hover:bg-gray-50'"
                  @click="toggleLike"
                >
                  <HeartIcon class="w-5 h-5 mr-2" :class="{ 'fill-current': isLiked }" />
                  {{ isLiked ? '已点赞' : '点赞' }}
                </button>
                <button 
                  class="flex items-center px-4 py-2 text-gray-600 hover:bg-gray-50 rounded-lg transition-colors"
                  @click="handleCollect"
                >
                  <BookmarkIcon class="w-5 h-5 mr-2" :class="{ 'fill-current': isCollected }" />
                  {{ isCollected ? '已收藏' : '收藏' }}
                </button>
              </div>
              
              <div class="flex items-center gap-2">
                <button 
                  v-for="(item, index) in shareOptions" 
                  :key="index"
                  class="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-50"
                  @click="item.action"
                >
                  <component :is="item.icon" class="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>

          <!-- 回答列表 -->
          <div class="mt-6 bg-white rounded-xl border border-gray-100 p-4 lg:p-6">
            <h2 class="text-lg font-bold text-gray-900 mb-4">
              {{ question.answers }} 个回答
            </h2>

            <!-- 回答输入框 -->
            <div class="mb-6">
              <textarea
                v-model="answerContent"
                rows="3"
                class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-violet-500 focus:ring-violet-500"
                placeholder="写下你的回答..."
              ></textarea>
              <div class="mt-2 flex justify-end">
                <button 
                  class="px-4 py-2 bg-violet-600 text-white rounded-lg hover:bg-violet-700 transition-colors"
                  @click="submitAnswer"
                >
                  发表回答
                </button>
              </div>
            </div>

            <!-- 回答列表 -->
            <div class="space-y-6">
              <div 
                v-for="answer in answers" 
                :key="answer.id"
                class="flex gap-4"
              >
                <img 
                  :src="answer.author.avatar"
                  :alt="answer.author.name"
                  class="w-10 h-10 rounded-full flex-shrink-0"
                >
                <div class="flex-1">
                  <div class="bg-gray-50 rounded-lg p-4" :class="{'ring-2 ring-green-500': answer.isAccepted}">
                    <div class="flex items-center justify-between mb-2">
                      <div class="flex items-center gap-2">
                        <span class="font-medium text-gray-900">{{ answer.author.name }}</span>
                        <span v-if="answer.isAccepted" class="flex items-center px-2 py-0.5 bg-green-100 text-green-600 rounded text-xs font-medium">
                          <CheckCircleIcon class="w-3.5 h-3.5 mr-1" />
                          最佳答案
                        </span>
                      </div>
                      <span class="text-sm text-gray-500">{{ answer.time }}</span>
                    </div>
                    <p class="text-gray-600">{{ answer.content }}</p>
                    <!-- 悬赏金额提示 - 仅在被采纳的回答显示 -->
                    <div v-if="answer.isAccepted && question.bounty" class="mt-3 pt-3 border-t border-gray-200">
                      <div class="flex items-center text-amber-600 text-sm">
                        <CurrencyYenIcon class="w-4 h-4 mr-1" />
                        <span>获得 {{ question.bounty }} 悬赏金额</span>
                      </div>
                    </div>
                  </div>
                  <div class="flex items-center gap-4 mt-2 text-sm">
                    <!-- 采纳为最佳答案按钮 -->
                    <button 
                      v-if="isAuthor && !question.solved && !answer.isAccepted"
                      class="flex items-center px-3 py-1.5 bg-green-50 text-green-600 hover:bg-green-100 rounded-full text-sm font-medium transition-colors"
                    >
                      <CheckCircleIcon class="w-4 h-4 mr-1.5" />
                      采纳为最佳答案
                    </button>
                    <button 
                      class="text-gray-500 hover:text-gray-700"
                      @click="replyToUser(answer)"
                    >
                      回复
                    </button>
                    <button 
                      class="flex items-center text-gray-500 hover:text-gray-700"
                      @click="toggleAnswerLike(answer)"
                    >
                      <HeartIcon 
                        class="w-4 h-4 mr-1"
                        :class="{ 'fill-current text-red-500': answer.isLiked }"
                      />
                      {{ answer.likes }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧边栏 -->
        <div class="lg:w-[320px] space-y-6">
          <!-- 悬赏信息 -->
          <div class="bg-white rounded-xl border border-gray-100 p-4 lg:p-6">
            <div class="relative">
              <!-- 悬赏金额 -->
              <div class="flex flex-col items-center p-6 bg-gradient-to-br from-amber-50 to-orange-50 rounded-lg border border-amber-100">
                <span class="text-amber-600 text-sm mb-1">悬赏金额</span>
                <div class="text-3xl font-bold text-amber-600 flex items-center">
                  <span class="text-xl mr-0.5">¥</span>
                  <span>{{ question.bounty }}</span>
                </div>
                <!-- 状态标识 -->
                <div class="absolute -top-2 -right-2">
                  <span v-if="question.solved" 
                    class="inline-flex items-center px-2.5 py-1 bg-green-100 text-green-600 rounded-full text-xs font-medium"
                  >
                    <CheckCircleIcon class="w-3.5 h-3.5 mr-1" />
                    已解决
                  </span>
                  <span v-else 
                    class="inline-flex items-center px-2.5 py-1 bg-amber-100 text-amber-600 rounded-full text-xs font-medium"
                  >
                    <ClockIcon class="w-3.5 h-3.5 mr-1" />
                    进行中
                  </span>
                </div>
              </div>
              <!-- 截止时间 -->
              <div class="mt-4 flex items-center justify-center text-sm text-gray-500">
                <ClockIcon class="w-4 h-4 mr-1.5 text-amber-500" />
                <span>截止时间：{{ question.bountyEndTime }}</span>
              </div>
            </div>
          </div>

          <!-- 作者信息卡片 -->
          <div class="bg-white rounded-xl border border-gray-100 p-4 lg:p-6">
            <div class="flex items-center space-x-4 mb-4">
              <img 
                :src="question.author.avatar" 
                :alt="question.author.name"
                class="w-12 h-12 rounded-full"
              >
              <div>
                <div class="font-medium text-gray-900">{{ question.author.name }}</div>
                <div class="text-sm text-gray-500">{{ question.author.title || '社区成员' }}</div>
              </div>
            </div>
            <p class="text-sm text-gray-600 mb-4">{{ question.author.bio || '这个作者很懒，还没有写简介' }}</p>
            <div class="flex items-center justify-between text-sm text-gray-500">
              <div>提问 {{ question.author.questions || 0 }}</div>
              <div>回答 {{ question.author.answers || 0 }}</div>
            </div>
            <button 
              class="mt-4 w-full h-9 rounded-lg border border-violet-600 text-violet-600 hover:bg-violet-50 transition-colors text-sm font-medium"
            >
              关注作者
            </button>
          </div>

          <!-- 相关问题 -->
          <div class="bg-white rounded-xl border border-gray-100 p-4 lg:p-6">
            <h2 class="text-lg font-bold text-gray-900 mb-4">相关问题</h2>
            <div class="space-y-4">
              <div v-for="question in relatedQuestions" :key="question.id"
                class="group"
              >
                <h3 
                  class="text-sm font-medium text-gray-900 group-hover:text-violet-600 transition-colors line-clamp-2 mb-2 cursor-pointer"
                  @click="$router.push(`/community/question/${question.id}`)"
                >
                  {{ question.title }}
                </h3>
                <div class="flex items-center text-xs text-gray-500">
                  <span class="flex items-center">
                    <ChatBubbleLeftIcon class="w-3 h-3 mr-1" />{{ question.answers }}
                  </span>
                  <span class="mx-2">·</span>
                  <span>{{ question.createTime }}</span>
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
import { useRoute } from 'vue-router'
import { useStore } from 'vuex'
import { 
  HeartIcon,
  ChatBubbleLeftIcon,
  EyeIcon,
  ChevronRightIcon,
  BookmarkIcon,
  ShareIcon,
  LinkIcon,
  QrCodeIcon,
  CurrencyYenIcon,
  ClockIcon,
  CheckBadgeIcon,
  CheckCircleIcon
} from '@heroicons/vue/24/outline'
import { showToast } from '@/components/ToastMessage'

const route = useRoute()
const store = useStore()

// 判断是否是问题作者
const isAuthor = computed(() => {
  return store.state.user?.id === question.value.author.id
})

// 问题数据
const question = ref({
  id: 1,
  title: 'Vue 3 组合式 API 中如何优雅地处理异步请求？',
  category: '技术问答',
  bounty: 50,
  bountyEndTime: '2024-03-20 23:59:59',
  solved: true,
  content: `在使用 Vue 3 的组合式 API 开发时，遇到了一些关于异步请求处理的问题：

1. 如何优雅地处理加载状态？
2. 请求失败后如何进行错误处理？
3. 如何避免重复请求？
4. 如何处理请求竞态问题？

希望有经验的同学分享一下最佳实践。`,
  author: {
    id: 1,
    name: '张三',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=author',
    title: '前端工程师',
    bio: '热爱技术，专注前端开发',
    questions: 12,
    answers: 34
  },
  createTime: '2024-03-15',
  views: 1234,
  answers: 2,
  likes: 45,
  tags: ['Vue.js', '异步编程', '最佳实践']
})

// 回答相关
const answerContent = ref('')
const answers = ref([
  {
    id: 1,
    author: {
      name: '李四',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=user1'
    },
    content: '建议使用 vue-query 或 swrv 这类请求库，它们提供了很多开箱即用的功能，比如缓存、重试、请求竞态处理等。',
    time: '2小时前',
    likes: 5,
    isLiked: false,
    isAccepted: true
  },
  {
    id: 2,
    author: {
      name: '王五',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=user2'
    },
    content: `关于异步请求处理，我建议以下最佳实践：

1. 使用 async/await 配合 try/catch 处理异步流程
2. 将请求逻辑封装在 composables 中，便于复用
3. 使用 ref 或 reactive 管理加载状态和错误状态
4. 实现请求取消机制，避免竞态问题
5. 使用 loading 和 error 状态控制 UI 展示

示例代码：
\`\`\`js
const useAsyncRequest = () => {
  const data = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const execute = async () => {
    loading.value = true
    error.value = null
    
    try {
      data.value = await api.getData()
    } catch (err) {
      error.value = err
    } finally {
      loading.value = false
    }
  }

  return { data, loading, error, execute }
}
\`\`\`

这样可以优雅地处理异步流程中的各种状态。`,
    time: '1小时前',
    likes: 12,
    isLiked: false,
    isAccepted: false
  },
  {
    id: 3,
    author: {
      name: '赵六',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=user3'
    },
    content: '可以考虑使用 Suspense 组件配合异步组件，这样可以更优雅地处理加载状态。',
    time: '30分钟前',
    likes: 3,
    isLiked: false,
    isAccepted: false
  }
])

// 点赞和收藏状态
const isLiked = ref(false)
const isCollected = ref(false)

// 分享选项
const shareOptions = [
  {
    icon: LinkIcon,
    action: () => {
      navigator.clipboard.writeText(window.location.href)
      showToast('链接已复制', 'success')
    }
  },
  {
    icon: ShareIcon,
    action: () => {
      showToast('分享功能开发中', 'info')
    }
  },
  {
    icon: QrCodeIcon,
    action: () => {
      showToast('二维码分享功能开发中', 'info')
    }
  }
]

// 相关问题
const relatedQuestions = ref([
  {
    id: 1,
    title: 'Vue 3 + TypeScript 项目最佳实践分享',
    answers: 12,
    createTime: '2天前'
  },
  {
    id: 2,
    title: '如何处理 Vue 3 组件中的副作用？',
    answers: 8,
    createTime: '3天前'
  },
  {
    id: 3,
    title: 'Vue 3 性能优化技巧总结',
    answers: 15,
    createTime: '4天前'
  }
])

// 点赞问题
const toggleLike = () => {
  if (!isLiked.value) {
    question.value.likes++
  } else {
    question.value.likes--
  }
  isLiked.value = !isLiked.value
}

// 收藏问题
const handleCollect = () => {
  isCollected.value = !isCollected.value
  showToast(isCollected.value ? '收藏成功' : '已取消收藏', 'success')
}

// 点赞回答
const toggleAnswerLike = (answer) => {
  if (!answer.isLiked) {
    answer.likes++
  } else {
    answer.likes--
  }
  answer.isLiked = !answer.isLiked
}

// 采纳回答
const acceptAnswer = (answer) => {
  if (question.value.solved) {
    showToast('该问题已采纳答案', 'warning')
    return
  }
  
  // TODO: 调用接口采纳回答
  answer.isAccepted = true
  question.value.solved = true
  showToast('已采纳该回答', 'success')
}

// 回复用户
const replyToUser = (answer) => {
  answerContent.value = `@${answer.author.name} `
}

// 提交回答
const submitAnswer = () => {
  if (!answerContent.value.trim()) {
    showToast('请输入回答内容', 'warning')
    return
  }

  answers.value.push({
    id: Date.now(),
    author: {
      name: '当前用户',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=current'
    },
    content: answerContent.value,
    time: '刚刚',
    likes: 0,
    isLiked: false,
    isAccepted: false
  })

  question.value.answers++
  answerContent.value = ''
  showToast('回答发表成功', 'success')
}
</script> 