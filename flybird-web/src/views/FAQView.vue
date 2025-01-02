<template>
  <div>
    <HeadView />
    <div class="min-h-screen relative overflow-hidden" style="padding-top: calc(var(--navbar-height) + 2rem);">
      <!-- 页面标题区域 -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">帮助中心</h1>
        <p class="text-xl text-gray-600">搜索您想了解的问题，获取即时帮助</p>
      </div>

      <!-- 搜索区域 -->
      <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 mb-8">
        <div class="relative">
          <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <MagnifyingGlassIcon class="h-5 w-5 text-gray-400" />
          </div>
          <input 
            type="text" 
            placeholder="搜索问题..." 
            class="w-full pl-11 pr-4 py-3 bg-white text-gray-900 rounded-xl border-0 ring-1 ring-gray-200 focus:ring-2 focus:ring-black shadow-sm transition-all" 
          />
        </div>
      </div>

      <!-- 主要内容区 -->
      <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- 快速导航 -->
        <div class="grid grid-cols-2 gap-4 mb-12">
          <div v-for="nav in quickNavs" 
            :key="nav.id" 
            class="p-6 bg-white border-2 border-gray-100 rounded-xl hover:border-black transition-colors cursor-pointer"
          >
            <div class="flex items-center space-x-4">
              <div class="w-10 h-10 bg-gray-50 rounded-lg flex items-center justify-center">
                <component :is="nav.icon" class="w-5 h-5 text-gray-900" />
              </div>
              <div>
                <h3 class="text-lg font-medium text-gray-900">{{ nav.title }}</h3>
                <p class="text-sm text-gray-600 mt-1">{{ nav.description }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 常见问题 -->
        <div class="space-y-4 mb-12">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">常见问题</h2>
          <div v-for="faq in faqs" 
            :key="faq.id" 
            class="bg-white rounded-xl overflow-hidden transition-all duration-200"
            :class="[faq.isOpen ? 'ring-2 ring-black' : 'hover:ring-2 hover:ring-gray-200']"
          >
            <button 
              @click="faq.isOpen = !faq.isOpen"
              class="w-full flex items-center justify-between p-6 text-left"
            >
              <span class="text-lg font-medium text-gray-900">{{ faq.question }}</span>
              <ChevronDownIcon 
                class="w-5 h-5 text-gray-500 transition-transform duration-200"
                :class="{ 'rotate-180': faq.isOpen }" 
              />
            </button>
            <div 
              v-show="faq.isOpen" 
              class="px-6 pb-6"
            >
              <p class="text-base text-gray-600">{{ faq.answer }}</p>
            </div>
          </div>
        </div>

        <!-- 联系我们 -->
        <div class="bg-white border-2 border-gray-100 rounded-xl p-6">
          <h3 class="text-xl font-bold text-gray-900 mb-4">联系我们</h3>
          <div class="space-y-4">
            <a href="#" class="flex items-center space-x-3 text-base text-gray-600 hover:text-black">
              <EnvelopeIcon class="w-5 h-5" />
              <span>support@example.com</span>
            </a>
            <div class="flex items-center space-x-3 text-base text-gray-600">
              <ClockIcon class="w-5 h-5" />
              <span>周一至周日 9:00-18:00</span>
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
import { 
  ChevronDownIcon, 
  PlayCircleIcon,
  DocumentTextIcon,
  EnvelopeIcon,
  PhoneIcon,
  ClockIcon,
  DocumentDuplicateIcon,
  VideoCameraIcon,
  ChatBubbleLeftRightIcon,
  AcademicCapIcon,
  MagnifyingGlassIcon
} from '@heroicons/vue/24/outline'

// 快速导航数据
const quickNavs = [
  {
    id: 1,
    title: '使用文档',
    description: '详细的功能使用说明',
    icon: DocumentDuplicateIcon,
    bgColor: 'bg-blue-500'
  },
  {
    id: 2,
    title: '视频教程',
    description: '直观的操作演示视频',
    icon: VideoCameraIcon,
    bgColor: 'bg-red-500'
  },
  {
    id: 3,
    title: '在线咨询',
    description: '实时解答您的问题',
    icon: ChatBubbleLeftRightIcon,
    bgColor: 'bg-green-500'
  },
  {
    id: 4,
    title: '学习指南',
    description: '系统的入门教程',
    icon: AcademicCapIcon,
    bgColor: 'bg-purple-500'
  }
]

// FAQ数据
const faqs = ref([
  {
    id: 1,
    question: '如何创建我的第一份简历？',
    answer: '选择一个适合的模板，点击"使用模板"按钮开始创建。系统会引导您逐步完成简历的各个部分。您可以随时预览和编辑内容，直到对结果满意为止。',
    isOpen: false
  },
  {
    id: 2,
    question: '如何下载我的简历？',
    answer: '在简历编辑页面右上角，点击"导出"按钮，选择您需要的格式（PDF、Word等）即可下载。会员用户可以使用更多高级导出选项。',
    isOpen: false
  },
  {
    id: 3,
    question: '如何修改简历模板的样式？',
    answer: '在编辑界面右侧的"样式"面板中，您可以调整字体、颜色、间距等样式选项。部分高级样式功能需要会员权限。',
    isOpen: false
  }
])

// 视频教程数据
const videos = [
  {
    id: 1,
    title: '3分钟快速创建专业简历',
    thumbnail: 'https://picsum.photos/400/225?random=1',
    duration: '3:45'
  },
  {
    id: 2,
    title: '如何优化你的简历内容',
    thumbnail: 'https://picsum.photos/400/225?random=2',
    duration: '5:20'
  },
  {
    id: 3,
    title: '简历模板高级定制技巧',
    thumbnail: 'https://picsum.photos/400/225?random=3',
    duration: '4:15'
  },
  {
    id: 4,
    title: '求职信写作完全指南',
    thumbnail: 'https://picsum.photos/400/225?random=4',
    duration: '6:30'
  }
]

// 热门文档数据
const popularDocs = [
  {
    id: 1,
    title: '简历制作完全指南 2024版',
    views: '12,354'
  },
  {
    id: 2,
    title: '如何写好工作经验',
    views: '8,721'
  },
  {
    id: 3,
    title: '简历模板使用技巧',
    views: '6,543'
  },
  {
    id: 4,
    title: '常见简历问题解答',
    views: '5,872'
  }
]
</script>

<style scoped>
.gradient-bg {
  /* 基础渐变 */
  background: linear-gradient(to right, #FB6E5F, #FF8574);
  
  /* 或者更丰富的渐变效果 */
  background: linear-gradient(
    to right,
    #FB6E5F,    /* 主色 */
    #FF8574,    /* 浅色 */
    #FA5C4B     /* 深色 */
  );
}

/* 悬浮效果 */
.gradient-bg:hover {
  opacity: 0.95;
  transition: opacity 0.3s ease;
}
</style>