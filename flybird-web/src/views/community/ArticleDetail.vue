<template>
  <div class="py-4 pb-24 lg:py-6 mt-[28px] md:mt-[72px]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 面包屑导航 -->
      <nav class="flex items-center space-x-2 text-sm mb-6" aria-label="Breadcrumb">
        <router-link 
          to="/community" 
          class="text-gray-500 hover:text-gray-700"
        >
          社区
        </router-link>
        <ChevronRightIcon class="w-4 h-4 text-gray-400" />
        <router-link 
          to="/community/articles" 
          class="text-gray-500 hover:text-gray-700"
        >
          文章
        </router-link>
        <ChevronRightIcon class="w-4 h-4 text-gray-400" />
        <span 
          class="text-gray-900 font-medium truncate max-w-[200px]"
          :title="article.title"
        >
          {{ article.title }}
        </span>
      </nav>

      <!-- 内容区域两栏布局 -->
      <div class="flex flex-col lg:flex-row gap-4 lg:gap-6">
        <!-- 左侧主要内容 -->
        <div class="lg:flex-1 lg:max-w-[calc(100%-320px-24px)]">
          <!-- 文章内容卡片 -->
          <div class="bg-white rounded-xl border border-gray-100 p-4 lg:p-6">
            <!-- 文章头部 -->
            <header class="mb-6">
              <h1 class="text-2xl lg:text-3xl font-bold text-gray-900 mb-4">
                {{ article.title }}
              </h1>
              
              <!-- 作者信息和文章数据 -->
              <div class="flex flex-wrap items-center gap-4">
                <!-- 作者信息 -->
                <div class="flex items-center">
                  <img 
                    :src="article.author.avatar" 
                    :alt="article.author.name"
                    class="w-10 h-10 rounded-full mr-3"
                  >
                  <div>
                    <div class="font-medium text-gray-900">{{ article.author.name }}</div>
                    <div class="text-sm text-gray-500">{{ article.createTime }}</div>
                  </div>
                </div>

                <!-- 分隔线 -->
                <div class="hidden sm:block w-px h-8 bg-gray-200"></div>
                
                <!-- 文章数据 -->
                <div class="flex items-center gap-4 text-sm text-gray-500">
                  <span class="flex items-center">
                    <EyeIcon class="w-4 h-4 mr-1" />
                    {{ article.views }} 阅读
                  </span>
                  <span class="flex items-center">
                    <ChatBubbleLeftIcon class="w-4 h-4 mr-1" />
                    {{ article.comments }} 评论
                  </span>
                  <span class="flex items-center">
                    <HeartIcon class="w-4 h-4 mr-1" />
                    {{ article.likes }} 点赞
                  </span>
                </div>
              </div>
            </header>

            <!-- 文章内容 -->
            <article class="prose prose-lg max-w-none mb-8">
              <div v-html="renderContent(article.content)"></div>
            </article>

            <!-- 文章标签 -->
            <div class="flex items-center gap-2 mb-6 flex-wrap">
              <span 
                v-for="tag in article.tags" 
                :key="tag"
                class="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm"
              >
                {{ tag }}
              </span>
            </div>

            <!-- 点赞和分享 -->
            <div class="flex items-center justify-between py-4 border-t border-gray-100">
              <button 
                class="flex items-center px-4 py-2 rounded-lg transition-colors"
                :class="isLiked ? 'text-red-500 bg-red-50' : 'text-gray-600 hover:bg-gray-50'"
                @click="toggleLike"
              >
                <HeartIcon 
                  class="w-5 h-5 mr-2"
                  :class="{ 'fill-current': isLiked }"
                />
                {{ isLiked ? '已点赞' : '点赞' }}
              </button>
              
              <!-- 分享按钮组 -->
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

          <!-- 评论区 -->
          <div class="mt-6 bg-white rounded-xl border border-gray-100 p-4 lg:p-6">
            <h2 class="text-lg font-bold text-gray-900 mb-4">
              评论 ({{ article.comments }})
            </h2>

            <!-- 评论输入框 -->
            <div class="mb-6">
              <textarea
                v-model="commentContent"
                rows="3"
                class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-violet-500 focus:ring-violet-500"
                placeholder="写下你的评论..."
              ></textarea>
              <div class="mt-2 flex justify-end">
                <button 
                  class="px-4 py-2 bg-violet-600 text-white rounded-lg hover:bg-violet-700 transition-colors"
                  @click="submitComment"
                >
                  发表评论
                </button>
              </div>
            </div>

            <!-- 评论列表 -->
            <div class="space-y-4">
              <div 
                v-for="comment in comments" 
                :key="comment.id"
                class="flex gap-4"
              >
                <img 
                  :src="comment.author.avatar"
                  :alt="comment.author.name"
                  class="w-10 h-10 rounded-full flex-shrink-0"
                >
                <div class="flex-1">
                  <div class="bg-gray-50 rounded-lg p-4">
                    <div class="flex items-center justify-between mb-2">
                      <span class="font-medium text-gray-900">{{ comment.author.name }}</span>
                      <span class="text-sm text-gray-500">{{ comment.time }}</span>
                    </div>
                    <p class="text-gray-600">{{ comment.content }}</p>
                  </div>
                  <div class="flex items-center gap-4 mt-2 text-sm">
                    <button 
                      class="text-gray-500 hover:text-gray-700"
                      @click="replyToComment(comment)"
                    >
                      回复
                    </button>
                    <button 
                      class="flex items-center text-gray-500 hover:text-gray-700"
                      @click="toggleCommentLike(comment)"
                    >
                      <HeartIcon 
                        class="w-4 h-4 mr-1"
                        :class="{ 'fill-current text-red-500': comment.isLiked }"
                      />
                      {{ comment.likes }}
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
                :src="article.author.avatar" 
                :alt="article.author.name"
                class="w-12 h-12 rounded-full"
              >
              <div>
                <div class="font-medium text-gray-900">{{ article.author.name }}</div>
                <div class="text-sm text-gray-500">{{ article.author.title || '社区作者' }}</div>
              </div>
            </div>
            <p class="text-sm text-gray-600 mb-4">{{ article.author.bio || '这个作者很懒，还没有写简介' }}</p>
            <div class="flex items-center justify-between text-sm text-gray-500">
              <div>文章 {{ article.author.articles || 0 }}</div>
              <div>关注者 {{ article.author.followers || 0 }}</div>
            </div>
            <button 
              class="mt-4 w-full h-9 rounded-lg border border-violet-600 text-violet-600 hover:bg-violet-50 transition-colors text-sm font-medium"
            >
              关注作者
            </button>
          </div>

          <!-- 相关文章 -->
          <div class="bg-white rounded-xl border border-gray-100 p-4 lg:p-6">
            <h2 class="text-lg font-bold text-gray-900 mb-4">相关文章</h2>
            <div class="space-y-4">
              <div v-for="article in relatedArticles" :key="article.id"
                class="group cursor-pointer"
              >
                <h3 class="text-sm font-medium text-gray-900 group-hover:text-blue-600 transition-colors line-clamp-2 mb-2">
                  {{ article.title }}
                </h3>
                <div class="flex items-center text-xs text-gray-500">
                  <span class="flex items-center">
                    <EyeIcon class="w-3 h-3 mr-1" />{{ article.views }}
                  </span>
                  <span class="mx-2">·</span>
                  <span>{{ article.createTime }}</span>
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
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'
import { marked } from 'marked'
import { 
  HeartIcon, 
  ShareIcon,
  QrCodeIcon,
  LinkIcon,
  ChatBubbleLeftIcon,
  EyeIcon,
  ChevronRightIcon,
  ClipboardIcon,
  CheckIcon
} from '@heroicons/vue/24/outline'
import { showToast } from '@/components/ToastMessage'

const route = useRoute()

// 配置 marked
marked.setOptions({
  highlight: function (code, lang) {
    const language = hljs.getLanguage(lang) ? lang : 'plaintext'
    return hljs.highlight(code, { language }).value
  },
  langPrefix: 'hljs language-'
})

// 处理代码块，添加复制按钮
const processCodeBlock = (code) => {
  const div = document.createElement('div')
  div.innerHTML = code

  const preElements = div.getElementsByTagName('pre')
  for (const pre of preElements) {
    // 创建代码块容器
    const wrapper = document.createElement('div')
    wrapper.className = 'code-block-wrapper'

    // 创建顶部栏
    const header = document.createElement('div')
    header.className = 'code-block-header'

    // 添加语言标识
    const lang = pre.querySelector('code').className.replace('hljs language-', '')
    const langSpan = document.createElement('span')
    langSpan.className = 'code-block-lang'
    langSpan.textContent = lang
    header.appendChild(langSpan)

    // 添加复制按钮
    header.innerHTML += `
      <button class="code-block-copy" onclick="
        const code = this.parentElement.nextElementSibling.querySelector('code').textContent;
        const textarea = document.createElement('textarea');
        textarea.value = code;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        window.$toast('复制成功', 'success');
      ">
        <div class="flex items-center space-x-1">
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
          </svg>
          <span class="text-xs">复制代码</span>
        </div>
      </button>
    `

    // 组装代码块
    wrapper.appendChild(header)
    wrapper.appendChild(pre.cloneNode(true))
    pre.parentNode.replaceChild(wrapper, pre)
  }

  return div.innerHTML
}

// 转换 Markdown 内容为 HTML
const renderContent = (markdown) => {
  const html = marked.parse(markdown)
  return processCodeBlock(html)
}

const article = ref({
  title: '使用 Vue 3 和 TailwindCSS 构建现代化 UI',
  content: `
  # 使用 Vue 3 和 TailwindCSS 构建现代化 UI

  ## 介绍
  
  Vue 3 和 TailwindCSS 的组合为我们提供了强大的开发能力。

  ## 代码示例

  \`\`\`vue
  <template>
    <div class="flex items-center justify-center min-h-screen bg-gray-100">
      <div class="max-w-md w-full bg-white rounded-lg shadow-lg p-6">
        <h1 class="text-2xl font-bold text-gray-900 mb-4">
          {{ title }}
        </h1>
        <p class="text-gray-600">
          {{ description }}
        </p>
      </div>
    </div>
  </template>

  &lt;script setup&gt;
  import { ref } from 'vue'

  const title = ref('Hello World')
  const description = ref('Welcome to Vue 3!')
  &lt;/script&gt;
  \`\`\`

  ## 样式说明

  使用 TailwindCSS 的工具类可以快速构建界面：

  \`\`\`css
  .card {
    @apply bg-white rounded-lg shadow-lg p-6;
  }

  .card-title {
    @apply text-2xl font-bold text-gray-900 mb-4;
  }
  \`\`\`
  `,
  author: {
    name: '张三',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=author'
  },
  createTime: '2024-03-15',
  views: 1234,
  comments: 23,
  likes: 45,
  tags: ['Vue.js', 'TailwindCSS', '前端开发']
})

// 评论相关
const commentContent = ref('')
const comments = ref([
  {
    id: 1,
    author: {
      name: '李四',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=user1'
    },
    content: '这篇文章写得很好，学到了很多！',
    time: '2小时前',
    likes: 5,
    isLiked: false
  }
])

// 点赞状态
const isLiked = ref(false)

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

// 点赞文章
const toggleLike = () => {
  if (!isLiked.value) {
    article.value.likes++
  } else {
    article.value.likes--
  }
  isLiked.value = !isLiked.value
}

// 点赞评论
const toggleCommentLike = (comment) => {
  if (!comment.isLiked) {
    comment.likes++
  } else {
    comment.likes--
  }
  comment.isLiked = !comment.isLiked
}

// 回复评论
const replyToComment = (comment) => {
  commentContent.value = `@${comment.author.name} `
}

// 提交评论
const submitComment = () => {
  if (!commentContent.value.trim()) {
    showToast('请输入评论内容', 'warning')
    return
  }

  comments.value.unshift({
    id: Date.now(),
    author: {
      name: '当前用户',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=current'
    },
    content: commentContent.value,
    time: '刚刚',
    likes: 0,
    isLiked: false
  })

  article.value.comments++
  commentContent.value = ''
  showToast('评论发表成功', 'success')
}

// 添加相关文章数据
const relatedArticles = ref([
  {
    id: 1,
    title: 'Vue 3 组合式 API 最佳实践',
    views: 1234,
    createTime: '2天前'
  },
  {
    id: 2,
    title: '使用 TailwindCSS 构建响应式界面',
    views: 987,
    createTime: '3天前'
  },
  {
    id: 3,
    title: '前端项目工程化实践',
    views: 876,
    createTime: '4天前'
  }
])

// 添加热门标签数据
const hotTags = ref([
  { name: 'Vue.js', count: 234 },
  { name: 'React', count: 189 },
  { name: 'TailwindCSS', count: 156 },
  { name: '前端开发', count: 145 },
  { name: 'TypeScript', count: 134 },
  { name: 'Node.js', count: 123 }
])

onMounted(() => {
  // TODO: 根据路由参数加载文章数据
  console.log('Article ID:', route.params.id)
})
</script>

<style>
/* Tailwind Typography 样式覆盖 */
.prose img {
  margin: 2rem auto;
  border-radius: 0.5rem;
}

/* 代码块样式 */
.prose pre {
  margin: 0;
  padding: 1rem;
  background: transparent;
  overflow-x: auto;
}

.prose pre code {
  padding: 0;
  background: transparent;
  border-radius: 0;
  color: inherit;
  @apply font-mono text-sm leading-relaxed;
}

/* 行内代码样式 */
.prose code:not(pre code) {
  color: #e83e8c;
  background-color: #f8f9fa;
  padding: 0.2em 0.4em;
  border-radius: 0.25rem;
  font-size: 0.875em;
  @apply font-mono;
}

/* 代码高亮主题自定义 */
.hljs {
  background: transparent !important;
  padding: 0 !important;
  @apply text-gray-800;
}

/* 文章内容基础样式 */
.prose {
  @apply text-gray-800;
}

.prose h1 {
  @apply text-2xl font-bold text-gray-900 mb-6 mt-8;
}

.prose h2 {
  @apply text-xl font-bold text-gray-900 mb-4 mt-6;
}

.prose p {
  @apply mb-4 leading-relaxed;
}

/* 代码块容器 */
.code-block-wrapper {
  @apply relative rounded-lg overflow-hidden my-6;
  background: #f8fafc;  /* 使用更浅的背景色 */
}

/* 代码块顶部栏 */
.code-block-header {
  @apply flex items-center justify-between px-4 py-2 bg-gray-100/80 text-gray-600 border-b border-gray-200;
}

/* 语言标识 */
.code-block-lang {
  @apply text-xs font-mono uppercase;
}

/* 复制按钮 */
.code-block-copy {
  @apply p-1.5 hover:text-gray-900 hover:bg-gray-200/50 transition-colors rounded cursor-pointer;
}

/* 滚动条美化 */
.prose pre::-webkit-scrollbar {
  height: 6px;
}

.prose pre::-webkit-scrollbar-track {
  background: transparent;
}

.prose pre::-webkit-scrollbar-thumb {
  @apply bg-gray-300 rounded;
}

.prose pre::-webkit-scrollbar-thumb:hover {
  @apply bg-gray-400;
}
</style> 