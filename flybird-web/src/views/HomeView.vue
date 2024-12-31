<template>
  <div>
    <HeadView />
    <div class="min-h-screen">
      <!-- 英雄区域 -->
      <div class="bg-gradient-to-br from-gray-950 to-gray-900 overflow-hidden">
  <main>
    <div class="relative isolate">
      <!-- 背景装饰 -->
      <div class="absolute inset-0">
        <div class="absolute inset-0 bg-[radial-gradient(circle_at_top_right,#4f46e510,transparent_50%)]"></div>
        <div class="absolute inset-0 bg-[radial-gradient(circle_at_bottom_left,#6366f110,transparent_50%)]"></div>
      </div>
      
      <div class="mx-auto max-w-7xl px-6 py-16 sm:py-24 lg:px-8">
        <div class="mx-auto flex flex-col lg:flex-row gap-12 items-center">
          <!-- 左侧轮播区域 -->
          <div class="lg:w-2/3 relative">
            <div class="relative h-[480px] perspective-[1500px]">
              <TransitionGroup 
                name="carousel"
                tag="div"
                class="relative h-full"
              >
                <div v-for="(slide, index) in slides" 
                     :key="slide.id"
                     v-show="currentSlide === index"
                     class="absolute inset-0 w-full h-full"
                     :style="{
                       transform: `rotateY(${currentSlide === index ? 0 : -90}deg)`,
                       transformOrigin: 'center center',
                       backfaceVisibility: 'hidden',
                       transition: 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)'
                     }"
                >
                  <div class="relative h-full overflow-hidden rounded-2xl shadow-2xl shadow-gray-950/50">
                    <img :src="slide.image" 
                         :alt="slide.title"
                         class="w-full h-full object-cover" />
                    <div class="absolute inset-0 bg-gradient-to-t from-gray-950 via-gray-950/50 to-transparent">
                      <div class="absolute bottom-0 left-0 right-0 p-10">
                        <div class="max-w-xl">
                          <h2 class="text-5xl font-bold text-white mb-4 leading-tight">
                            {{ slide.title }}
                          </h2>
                          <p class="text-xl text-gray-300">{{ slide.description }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </TransitionGroup>

              <!-- 轮播控制器 -->
              <div class="absolute -right-4 top-1/2 -translate-y-1/2 flex flex-col gap-3">
                <button v-for="(_, index) in slides" 
                        :key="index"
                        @click="currentSlide = index"
                        class="w-2 h-12 rounded-full transition-all duration-300 relative group"
                        :class="currentSlide === index ? 'bg-white' : 'bg-gray-700 hover:bg-gray-600'">
                  <span class="absolute right-full mr-4 py-1 px-2 rounded bg-gray-800 text-white text-sm opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                    {{ slides[index].title }}
                  </span>
                </button>
              </div>
            </div>
          </div>

          <!-- 右侧新闻公告 -->
          <div class="lg:w-1/3 h-[480px]">
            <div class="bg-gray-900/50 backdrop-blur rounded-2xl h-full border border-gray-800">
              <div class="p-8">
                <div class="flex items-center justify-between mb-8">
                  <h2 class="text-2xl font-bold text-white">最新动态</h2>
                  <a href="#" class="text-gray-400 text-sm hover:text-white transition-colors flex items-center gap-1">
                    全部
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                  </a>
                </div>
                <div class="space-y-6 overflow-auto max-h-[360px] pr-2 custom-scrollbar">
                  <a v-for="notice in notices" 
                     :key="notice.id"
                     href="#"
                     class="block group p-4 rounded-xl transition-all duration-300 hover:bg-gray-800">
                    <div class="flex flex-col">
                      <h3 class="text-gray-100 group-hover:text-white transition-colors text-lg font-medium">
                        {{ notice.title }}
                      </h3>
                      <p class="text-gray-400 mt-2 line-clamp-2 group-hover:text-gray-300">
                        {{ notice.content }}
                      </p>
                      <span class="text-sm text-gray-500 mt-3 group-hover:text-gray-400">
                        {{ notice.date }}
                      </span>
                    </div>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</div>

      <!-- 模板展示 -->
      <div class="bg-gray-50 py-20">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center mb-12">
            <h2 class="text-3xl font-bold text-gray-900 mb-4">精美的简历模板</h2>
            <p class="text-xl text-gray-600">
              使用经过招聘官验证的专业模板，快速制作一份出色的简历
            </p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div v-for="template in templates" 
                 :key="template.id"
                 class="group relative bg-white rounded-lg shadow-sm overflow-hidden">
              <div class="aspect-[3/4]">
                <img :src="template.image" 
                     :alt="template.name"
                     class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105" />
              </div>
              <div class="absolute bottom-0 left-0 right-0 bg-white/90 backdrop-blur-sm p-4">
                <h3 class="text-lg font-medium text-gray-900">{{ template.name }}</h3>
                <p class="text-sm text-gray-500">{{ template.users }}+ 用户选择</p>
              </div>
            </div>
          </div>

          <div class="text-center mt-12">
            <button class="px-6 py-3 border border-primary-600 text-primary-600 rounded-lg hover:bg-primary-50 transition-colors">
              查看更多模板
            </button>
          </div>
        </div>
      </div>

      <!-- 功能特点 -->
      <div class="py-20 bg-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center mb-16">
            <h2 class="text-3xl font-bold text-gray-900 mb-4">专业的简历制作工具</h2>
            <p class="text-xl text-gray-600">让简历制作变得简单高效</p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div v-for="feature in features" 
                 :key="feature.id"
                 class="p-6 bg-gray-50 rounded-xl">
              <component :is="feature.icon" 
                        class="w-12 h-12 text-primary-600 mb-4" />
              <h3 class="text-xl font-medium text-gray-900 mb-2">
                {{ feature.title }}
              </h3>
              <p class="text-gray-600">{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 用户评价 -->
      <div class="bg-gray-50 py-20">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center mb-12">
            <div class="flex items-center justify-center gap-1 mb-4">
              <span class="text-2xl font-bold">4.5</span>
              <div class="flex text-yellow-400">
                <StarIcon v-for="i in 5" :key="i" class="w-6 h-6" />
              </div>
            </div>
            <p class="text-gray-600">基于 52,566 条用户评价</p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div v-for="review in reviews" 
                 :key="review.id"
                 class="bg-white p-6 rounded-lg shadow-sm">
              <p class="text-gray-600 mb-4">{{ review.content }}</p>
              <div class="flex items-center gap-3">
                <img :src="review.avatar" 
                     :alt="review.name"
                     class="w-10 h-10 rounded-full" />
                <div>
                  <div class="font-medium text-gray-900">{{ review.name }}</div>
                  <div class="text-sm text-gray-500">{{ review.date }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CTA 区域 -->
      <div class="bg-primary-600 py-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 class="text-3xl font-bold text-white mb-4">
            准备好开始了吗？
          </h2>
          <p class="text-xl text-primary-100 mb-8">
            立即创建你的专业简历，开启职业新篇章
          </p>
          <button class="px-8 py-4 bg-white text-primary-600 rounded-lg text-lg font-medium hover:bg-primary-50 transition-colors">
            免费使用
          </button>
        </div>
      </div>
    </div>
    <FootView />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import HeadView from '../components/HeadView.vue'
import FootView from '../components/FootView.vue'
import { StarIcon } from '@heroicons/vue/20/solid'
import { 
  DocumentDuplicateIcon, 
  SparklesIcon,
  CloudArrowDownIcon,
  ShieldCheckIcon,
  PaintBrushIcon,
  DocumentTextIcon
} from '@heroicons/vue/24/outline'



// 模板数据
const templates = [
  {
    id: 1,
    name: 'Stockholm',
    users: '9,700,000',
    image: 'https://picsum.photos/300/400?random=1'
  },
  {
    id: 2,
    name: 'New York',
    users: '4,400,000',
    image: 'https://picsum.photos/300/400?random=2'
  },
  {
    id: 3,
    name: 'Toronto',
    users: '2,500,000',
    image: 'https://picsum.photos/300/400?random=3'
  }
]

// 功能特点
const features = [
  {
    id: 1,
    title: '在线简历制作',
    description: '简单直观的编辑界面，随时随地修改内容',
    icon: DocumentDuplicateIcon
  },
  {
    id: 2,
    title: 'AI 智能助手',
    description: '智能优化建议，帮助创建更专业的简历',
    icon: SparklesIcon
  },
  {
    id: 3,
    title: '多种导出格式',
    description: '支持 PDF、Word 等多种格式导出',
    icon: CloudArrowDownIcon
  },
  {
    id: 4,
    title: '数据安全',
    description: '使用强大的256位加密保护您的数据',
    icon: ShieldCheckIcon
  },
  {
    id: 5,
    title: '专业模板',
    description: '经过招聘官验证的简历模板',
    icon: PaintBrushIcon
  },
  {
    id: 6,
    title: 'ATS优化',
    description: '确保简历能通过筛选系统',
    icon: DocumentTextIcon
  }
]

// 用户评价
const reviews = [
  {
    id: 1,
    content: '使用这个平台制作的简历帮助我成功应聘到理想的工作。模板很专业，操作也很简单。',
    name: '张明',
    date: '2天前',
    avatar: 'https://picsum.photos/40/40?random=1'
  },
  {
    id: 2,
    content: '平台提供的AI建议对优化简历内容很有帮助，让我的简历更有竞争力。',
    name: '李华',
    date: '3天前',
    avatar: 'https://picsum.photos/40/40?random=2'
  },
  {
    id: 3,
    content: '多种导出格式很实用，简历的排版和样式都很专业，强烈推荐！',
    name: '王芳',
    date: '4天前',
    avatar: 'https://picsum.photos/40/40?random=3'
  }
]

// 轮播图数据
const slides = [
  {
    id: 1,
    title: "简历制作新体验",
    description: "AI驱动的智能简历生成器",
    image: "https://picsum.photos/800/450?random=1"
  },
  {
    id: 2,
    title: "专业模板库更新",
    description: "新增多个行业定制模板",
    image: "https://picsum.photos/800/450?random=2"
  },
  {
    id: 3,
    title: "求职季特别活动",
    description: "限时优惠，助力求职成功",
    image: "https://picsum.photos/800/450?random=3"
  }
]

// 新闻公告数据
const notices = [
  {
    id: 1,
    title: "系统升级公告：新增AI简历优化功能",
    content: "为提供更好的服务体验，我们新增了AI驱动的简历优化建议功能...",
    date: "2024-03-15"
  },
  {
    id: 2,
    title: "简历制作技巧分享会即将开始",
    content: "3月20日晚8点，资深HR将在线分享简历制作要点和注意事项...",
    date: "2024-03-14"
  },
  {
    id: 3,
    title: "新增多个行业简历模板",
    content: "针对IT、金融、教育等行业新增20+专业简历模板...",
    date: "2024-03-13"
  },
  {
    id: 4,
    title: "求职季活动开启",
    content: "春季求职黄金期，会员服务限时优惠...",
    date: "2024-03-12"
  }
]

// 轮播图当前索引
const currentSlide = ref(0)

// 自动轮播
onMounted(() => {
  setInterval(() => {
    currentSlide.value = (currentSlide.value + 1) % slides.length
  }, 5000)
})
</script>

<style scoped>
.perspective-[1500px] {
  perspective: 1500px;
}

.carousel-enter-active,
.carousel-leave-active {
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.carousel-enter-from {
  opacity: 0;
  transform: rotateY(-90deg);
}

.carousel-leave-to {
  opacity: 0;
  transform: rotateY(90deg);
}

.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.1) transparent;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 255, 255, 0.2);
}
</style>