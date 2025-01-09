<template>
  <div class="py-4 pb-24 lg:py-6 mt-[28px] md:mt-[72px]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 面包屑导航 -->
      <nav class="flex items-center space-x-2 text-sm mb-6" aria-label="Breadcrumb">
        <router-link to="/community" class="text-gray-500 hover:text-gray-700">
          社区
        </router-link>
        <ChevronRightIcon class="w-4 h-4 text-gray-400" />
        <router-link to="/community/topics" class="text-gray-500 hover:text-gray-700">
          话题
        </router-link>
        <ChevronRightIcon class="w-4 h-4 text-gray-400" />
        <span class="text-gray-900 font-medium truncate max-w-[200px]" :title="topic.title">
          {{ topic.title }}
        </span>
      </nav>

      <!-- 内容区域两栏布局 -->
      <div class="flex flex-col lg:flex-row gap-4 lg:gap-6">
        <!-- 左侧主要内容 -->
        <div class="lg:flex-1 lg:max-w-[calc(100%-320px-24px)]">
          <!-- 话题内容卡片 -->
          <div class="bg-white rounded-xl border border-gray-100 p-4 lg:p-6 topic-card">
            <!-- 话题头部 -->
            <header class="mb-6">
              <div class="flex items-center gap-2 mb-3">
                <span class="px-2.5 py-1 bg-violet-100 text-violet-600 rounded-full text-xs font-medium">
                  {{ topic.category }}
                </span>
                <span v-if="topic.isHot" class="px-2.5 py-1 bg-orange-100 text-orange-600 rounded-full text-xs font-medium">
                  热门
                </span>
                <span v-if="topic.isTop" class="px-2.5 py-1 bg-blue-100 text-blue-600 rounded-full text-xs font-medium">
                  置顶
                </span>
                <span class="text-xs text-gray-500">{{ topic.createTime }}</span>
              </div>
              <h1 class="text-xl font-bold text-gray-900 hover:text-violet-600 transition-colors mb-3">
                {{ topic.title }}
              </h1>
              
              <!-- 作者信息和话题数据 -->
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <img 
                    :src="topic.author.avatar" 
                    :alt="topic.author.name"
                    class="w-10 h-10 rounded-full mr-3"
                  >
                  <div>
                    <div class="font-medium text-gray-900">{{ topic.author.name }}</div>
                    <div class="text-sm text-gray-500">{{ topic.author.title }}</div>
                  </div>
                </div>

                <div class="flex items-center gap-4 text-sm text-gray-500">
                  <span class="flex items-center">
                    <EyeIcon class="w-4 h-4 mr-1" />
                    {{ topic.views }} 浏览
                  </span>
                  <span class="flex items-center">
                    <ChatBubbleLeftIcon class="w-4 h-4 mr-1" />
                    {{ topic.replies }} 回复
                  </span>
                  <span class="flex items-center">
                    <HeartIcon class="w-4 h-4 mr-1" />
                    {{ topic.likes }} 点赞
                  </span>
                </div>
              </div>
            </header>

            <!-- 话题内容 -->
            <div class="relative mb-8">
              <!-- 进度条背景 -->
              <div class="absolute inset-0 flex rounded-xl overflow-hidden">
                <!-- 左侧进度 -->
                <div 
                  class="h-full bg-gradient-to-r from-blue-50 to-blue-100"
                  :style="{ width: `${(topic.votesA / (topic.votesA + topic.votesB)) * 100}%` }"
                ></div>
                <!-- 右侧进度 -->
                <div 
                  class="h-full bg-gradient-to-l from-purple-50 to-purple-100"
                  :style="{ width: `${(topic.votesB / (topic.votesA + topic.votesB)) * 100}%` }"
                ></div>
              </div>

              <!-- 选项内容 -->
              <div class="relative flex items-center min-h-[100px]">
                <!-- 选项A -->
                <div class="flex-1 p-6">
                  <div class="text-center">
                    <!-- 百分比指示器 -->
                    <div class="absolute -top-3 left-[25%] -translate-x-1/2 px-3 py-1 bg-blue-600 rounded-full text-white text-xs font-medium">
                      {{ Math.round((topic.votesA / (topic.votesA + topic.votesB)) * 100) }}%
                    </div>
                    <div class="text-lg font-medium text-blue-600 mb-2">{{ topic.optionA }}</div>
                    <div class="text-sm text-gray-500 mb-4">{{ topic.votesA }} 票</div>
                    <!-- 投票按钮 -->
                    <button 
                      class="px-6 h-10 rounded-full bg-blue-50 hover:bg-blue-100 transition-colors mx-auto flex items-center justify-center cursor-pointer"
                    >
                      <span class="text-sm font-medium text-blue-600">投票</span>
                    </button>
                  </div>
                </div>

                <!-- VS标志 -->
                <div class="w-10 h-10 rounded-full bg-white shadow-sm flex items-center justify-center z-10">
                  <span class="text-xs font-bold text-gray-400">VS</span>
                </div>

                <!-- 选项B -->
                <div class="flex-1 p-6">
                  <div class="text-center">
                    <!-- 百分比指示器 -->
                    <div class="absolute -top-3 right-[25%] translate-x-1/2 px-3 py-1 bg-purple-600 rounded-full text-white text-xs font-medium">
                      {{ Math.round((topic.votesB / (topic.votesA + topic.votesB)) * 100) }}%
                    </div>
                    <div class="text-lg font-medium text-purple-600 mb-2">{{ topic.optionB }}</div>
                    <div class="text-sm text-gray-500 mb-4">{{ topic.votesB }} 票</div>
                    <!-- 投票按钮 -->
                    <button 
                      class="px-6 h-10 rounded-full bg-purple-50 hover:bg-purple-100 transition-colors mx-auto flex items-center justify-center cursor-pointer"
                    >
                      <span class="text-sm font-medium text-purple-600">投票</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- 话题详细说明 -->
            <div class="mt-8 mb-6">
              <h3 class="text-lg font-medium text-gray-900 mb-4">话题说明</h3>
              <div class="bg-gray-50 rounded-lg p-6">
                <div class="prose prose-sm max-w-none text-gray-600">
                  <p class="mb-4">{{ topic.description }}</p>
                  <div class="space-y-2">
                    <h4 class="text-sm font-medium text-gray-900">参与规则：</h4>
                    <ul class="list-disc list-inside text-sm space-y-1 text-gray-600">
                      <li>每个用户只能投票一次</li>
                      <li>投票后将无法更改选择</li>
                      <li>可以在评论区详细说明你的观点</li>
                      <li>请遵守社区规范，文明讨论</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            <!-- 参与者信息 -->
            <div class="flex items-center justify-between mb-6">
              <!-- 参与者头像组 -->
              <div class="flex items-center gap-2">
                <div class="flex -space-x-2">
                  <img v-for="i in Math.min(3, Math.floor((topic.votesA + topic.votesB) / 10))" :key="i"
                    :src="`https://picsum.photos/32/32?random=${topic.id * 10 + i}`"
                    class="w-6 h-6 rounded-full ring-2 ring-white"
                  >
                </div>
                <span class="text-xs text-gray-500">{{ topic.votesA + topic.votesB }} 人参与</span>
              </div>
            </div>

            <!-- 话题标签 -->
            <div class="flex items-center gap-2 mb-6 flex-wrap">
              <span 
                v-for="tag in topic.tags" 
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

          <!-- 回复列表 -->
          <div class="mt-6 bg-white rounded-xl border border-gray-100 p-4 lg:p-6">
            <h2 class="text-lg font-bold text-gray-900 mb-4">
              回复 ({{ topic.replies }})
            </h2>

            <!-- 回复输入框 -->
            <div class="mb-6">
              <textarea
                v-model="replyContent"
                rows="3"
                class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-violet-500 focus:ring-violet-500"
                placeholder="写下你的回复..."
              ></textarea>
              <div class="mt-2 flex justify-end">
                <button 
                  class="px-4 py-2 bg-violet-600 text-white rounded-lg hover:bg-violet-700 transition-colors"
                  @click="submitReply"
                >
                  发表回复
                </button>
              </div>
            </div>

            <!-- 回复列表 -->
            <div class="space-y-6">
              <div 
                v-for="reply in replies" 
                :key="reply.id"
                class="flex gap-4"
              >
                <img 
                  :src="reply.author.avatar"
                  :alt="reply.author.name"
                  class="w-10 h-10 rounded-full flex-shrink-0"
                >
                <div class="flex-1">
                  <div class="bg-gray-50 rounded-lg p-4">
                    <div class="flex items-center justify-between mb-2">
                      <div class="flex items-center gap-2">
                        <span class="font-medium text-gray-900">{{ reply.author.name }}</span>
                        <span v-if="reply.author.isOP" class="px-1.5 py-0.5 bg-violet-100 text-violet-600 rounded text-xs">
                          楼主
                        </span>
                      </div>
                      <span class="text-sm text-gray-500">{{ reply.time }}</span>
                    </div>
                    <p class="text-gray-600">{{ reply.content }}</p>
                  </div>
                  <div class="flex items-center gap-4 mt-2 text-sm">
                    <button 
                      class="text-gray-500 hover:text-gray-700"
                      @click="replyToUser(reply)"
                    >
                      回复
                    </button>
                    <button 
                      class="flex items-center text-gray-500 hover:text-gray-700"
                      @click="toggleReplyLike(reply)"
                    >
                      <HeartIcon 
                        class="w-4 h-4 mr-1"
                        :class="{ 'fill-current text-red-500': reply.isLiked }"
                      />
                      {{ reply.likes }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧边栏 -->
        <div class="lg:w-[320px] space-y-6">
          <!-- 作者信息卡片 -->
          <div class="bg-white rounded-xl border border-gray-100 p-4 lg:p-6">
            <div class="flex items-center space-x-4 mb-4">
              <img 
                :src="topic.author.avatar" 
                :alt="topic.author.name"
                class="w-12 h-12 rounded-full"
              >
              <div>
                <div class="font-medium text-gray-900">{{ topic.author.name }}</div>
                <div class="text-sm text-gray-500">{{ topic.author.title || '社区成员' }}</div>
              </div>
            </div>
            <p class="text-sm text-gray-600 mb-4">{{ topic.author.bio || '这个作者很懒，还没有写简介' }}</p>
            <div class="flex items-center justify-between text-sm text-gray-500">
              <div>话题 {{ topic.author.topics || 0 }}</div>
              <div>关注者 {{ topic.author.followers || 0 }}</div>
            </div>
            <button 
              class="mt-4 w-full h-9 rounded-lg border border-violet-600 text-violet-600 hover:bg-violet-50 transition-colors text-sm font-medium"
            >
              关注作者
            </button>
          </div>

          <!-- 相关话题 -->
          <div class="bg-white rounded-xl border border-gray-100 p-4 lg:p-6">
            <h2 class="text-lg font-bold text-gray-900 mb-4">相关话题</h2>
            <div class="space-y-4">
              <div v-for="topic in relatedTopics" :key="topic.id"
                class="group cursor-pointer"
              >
                <h3 class="text-sm font-medium text-gray-900 group-hover:text-violet-600 transition-colors line-clamp-2 mb-2">
                  {{ topic.title }}
                </h3>
                <div class="flex items-center text-xs text-gray-500">
                  <span class="flex items-center">
                    <ChatBubbleLeftIcon class="w-3 h-3 mr-1" />{{ topic.replies }}
                  </span>
                  <span class="mx-2">·</span>
                  <span>{{ topic.createTime }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 热门标签 -->
          <div class="bg-white rounded-xl border border-gray-100 p-4 lg:p-6">
            <h2 class="text-lg font-bold text-gray-900 mb-4">热门标签</h2>
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="tag in hotTags" 
                :key="tag.name"
                class="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm cursor-pointer hover:bg-gray-200 transition-colors"
              >
                {{ tag.name }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { 
  HeartIcon,
  ChatBubbleLeftIcon,
  EyeIcon,
  ChevronRightIcon,
  BookmarkIcon,
  ShareIcon,
  LinkIcon,
  QrCodeIcon
} from '@heroicons/vue/24/outline'
import { showToast } from '@/components/ToastMessage'

const route = useRoute()

// 话题数据
const topic = ref({
  id: 1,
  title: '2024年前端开发趋势讨论',
  category: '技术讨论',
  isHot: true,
  isTop: false,
  optionA: 'AI 辅助开发',
  optionB: 'WebAssembly',
  votesA: 234,
  votesB: 156,
  description: `在2024年，前端开发领域正在经历快速的变革。本次话题旨在讨论两个最受关注的技术方向：AI辅助开发和WebAssembly。

AI辅助开发正在改变我们的编码方式，从代码补全到自动化测试，AI工具正在提高开发效率。而WebAssembly则为Web应用带来了接近原生的性能，使得更多高性能应用可以在浏览器中运行。

你更看好哪个方向？欢迎投票并分享你的观点！`,
  content: `大家好，想和大家讨论一下 2024 年前端开发的趋势。

我觉得以下几个方向值得关注：

1. AI 辅助开发
2. WebAssembly 应用
3. 微前端架构
4. 边缘计算

大家觉得还有哪些值得关注的方向？欢迎讨论！`,
  author: {
    name: '张三',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=author',
    title: '高级前端工程师',
    bio: '热爱技术，专注前端开发',
    topics: 23,
    followers: 156
  },
  createTime: '2024-03-15',
  views: 1234,
  replies: 23,
  likes: 45,
  tags: ['前端开发', '技术趋势', 'AI']
})

// 回复相关
const replyContent = ref('')
const replies = ref([
  {
    id: 1,
    author: {
      name: '李四',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=user1',
      isOP: false
    },
    content: '我觉得 AI 辅助开发确实是一个很重要的方向，特别是在提高开发效率方面。',
    time: '2小时前',
    likes: 5,
    isLiked: false
  },
  {
    id: 2,
    author: {
      name: '张三',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=author',
      isOP: true
    },
    content: '确实，现在已经有很多 AI 工具可以帮助我们提高开发效率。',
    time: '1小时前',
    likes: 3,
    isLiked: false
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

// 相关话题
const relatedTopics = ref([
  {
    id: 1,
    title: '如何看待 AI 对前端开发的影响？',
    replies: 45,
    createTime: '2天前'
  },
  {
    id: 2,
    title: 'WebAssembly 在前端的实践经验分享',
    replies: 32,
    createTime: '3天前'
  },
  {
    id: 3,
    title: '微前端架构的优势与挑战',
    replies: 28,
    createTime: '4天前'
  }
])

// 热门标签
const hotTags = ref([
  { name: '前端开发', count: 234 },
  { name: 'AI', count: 189 },
  { name: 'WebAssembly', count: 156 },
  { name: '微前端', count: 145 },
  { name: '技术趋势', count: 134 }
])

// 点赞话题
const toggleLike = () => {
  if (!isLiked.value) {
    topic.value.likes = (topic.value.likes || 0) + 1
  } else {
    topic.value.likes--
  }
  isLiked.value = !isLiked.value
}

// 收藏话题
const handleCollect = () => {
  isCollected.value = !isCollected.value
  showToast(isCollected.value ? '收藏成功' : '已取消收藏', 'success')
}

// 点赞回复
const toggleReplyLike = (reply) => {
  if (!reply.isLiked) {
    reply.likes++
  } else {
    reply.likes--
  }
  reply.isLiked = !reply.isLiked
}

// 回复用户
const replyToUser = (reply) => {
  replyContent.value = `@${reply.author.name} `
}

// 提交回复
const submitReply = () => {
  if (!replyContent.value.trim()) {
    showToast('请输入回复内容', 'warning')
    return
  }

  replies.value.push({
    id: Date.now(),
    author: {
      name: '当前用户',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=current',
      isOP: false
    },
    content: replyContent.value,
    time: '刚刚',
    likes: 0,
    isLiked: false
  })

  topic.value.replies++
  replyContent.value = ''
}
</script>

<style>
/* 话题卡片样式 */
.topic-card {
  @apply transition-all duration-200 hover:border-violet-200 hover:shadow-sm;
}

.topic-card:hover {
  transform: translateY(-1px);
}
</style> 