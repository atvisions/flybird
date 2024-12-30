<template>
    <div>
      <HeadView />
      <div class="min-h-screen" style="padding-top: calc(var(--navbar-height));">
        <!-- 头部搜索区 -->
        <div class="bg-gradient-to-r from-primary-500 to-primary-600">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
            <div class="text-center max-w-3xl mx-auto">
              <h1 class="text-4xl font-bold mb-4 text-gray-900">您好，需要帮助吗？</h1>
              <p class="text-lg text-gray-900 mb-8">搜索您想了解的问题，获取即时帮助</p>
              <div class="relative">
                <input type="text" 
                       placeholder="输入关键词搜索..." 
                       class="w-full px-6 py-4 rounded-full text-gray-900 text-lg shadow-lg focus:ring-4 focus:ring-white/30 focus:outline-none" />
                <button class="absolute right-2 top-1/2 -translate-y-1/2 px-6 py-2 gradient-bg rounded-full text-white font-medium hover:opacity-90 transition-opacity">
                  搜索
                </button>
              </div>
            </div>
          </div>
        </div>
  
        <!-- 快速导航区 -->
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-8">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div v-for="nav in quickNavs" 
                 :key="nav.id" 
                 class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow cursor-pointer">
              <div class="flex items-start gap-4">
                <div class="p-3 rounded-lg" :class="nav.bgColor">
                  <component :is="nav.icon" class="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 class="text-lg font-semibold text-gray-900 mb-1">{{ nav.title }}</h3>
                  <p class="text-gray-600">{{ nav.description }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- 主要内容区 -->
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- 左侧主要内容 -->
            <div class="lg:col-span-2 space-y-8">
              <!-- 常见问题 -->
              <section>
                <h2 class="text-2xl font-bold text-gray-900 mb-6">常见问题</h2>
                <div class="space-y-4">
                  <div v-for="faq in faqs" 
                       :key="faq.id" 
                       class="border border-gray-200 rounded-lg overflow-hidden bg-white">
                    <button @click="faq.isOpen = !faq.isOpen"
                            class="w-full flex items-center justify-between p-4 text-left hover:bg-gray-50">
                      <span class="font-medium text-gray-900">{{ faq.question }}</span>
                      <ChevronDownIcon class="w-5 h-5 text-gray-500 transition-transform"
                                     :class="{ 'rotate-180': faq.isOpen }" />
                    </button>
                    <div v-show="faq.isOpen" class="p-4 bg-gray-50 border-t border-gray-200">
                      <p class="text-gray-600">{{ faq.answer }}</p>
                    </div>
                  </div>
                </div>
              </section>
  
              <!-- 视频教程 -->
              <section>
                <h2 class="text-2xl font-bold text-gray-900 mb-6">视频教程</h2>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                  <div v-for="video in videos" 
                       :key="video.id" 
                       class="group cursor-pointer">
                    <div class="relative aspect-video rounded-lg overflow-hidden mb-3">
                      <img :src="video.thumbnail" :alt="video.title" class="w-full h-full object-cover" />
                      <div class="absolute inset-0 bg-black/30 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                        <PlayCircleIcon class="w-16 h-16 text-white" />
                      </div>
                    </div>
                    <h3 class="font-medium text-gray-900 group-hover:text-primary-600 transition-colors">{{ video.title }}</h3>
                    <p class="text-sm text-gray-500">{{ video.duration }}</p>
                  </div>
                </div>
              </section>
            </div>
  
            <!-- 右侧边栏 -->
            <div class="lg:col-span-1 space-y-8">
              <!-- 快速联系 -->
              <div class="bg-white rounded-xl shadow-sm p-6">
                <h3 class="text-lg font-bold text-gray-900 mb-4">联系我们</h3>
                <div class="space-y-4">
                  <a href="#" class="flex items-center gap-3 text-gray-600 hover:text-primary-600">
                    <EnvelopeIcon class="w-5 h-5" />
                    <span>support@example.com</span>
                  </a>
                  <a href="#" class="flex items-center gap-3 text-gray-600 hover:text-primary-600">
                    <PhoneIcon class="w-5 h-5" />
                    <span>400-123-4567</span>
                  </a>
                  <div class="flex items-center gap-3 text-gray-600">
                    <ClockIcon class="w-5 h-5" />
                    <span>周一至周日 9:00-18:00</span>
                  </div>
                </div>
              </div>
  
              <!-- 热门文档 -->
              <div class="bg-white rounded-xl shadow-sm p-6">
                <h3 class="text-lg font-bold text-gray-900 mb-4">热门文档</h3>
                <div class="space-y-3">
                  <a v-for="doc in popularDocs" 
                     :key="doc.id"
                     href="#" 
                     class="flex items-start gap-3 group">
                    <DocumentTextIcon class="w-5 h-5 text-gray-400 group-hover:text-primary-600" />
                    <div>
                      <p class="text-gray-900 group-hover:text-primary-600">{{ doc.title }}</p>
                      <span class="text-sm text-gray-500">{{ doc.views }}次阅读</span>
                    </div>
                  </a>
                </div>
              </div>
  
              <!-- 反馈建议 -->
              <div class="bg-gradient-to-br from-primary-50 to-primary-100 rounded-xl p-6 bg-white">
                <h3 class="text-lg font-bold text-gray-900 mb-2">帮助我们改进</h3>
                <p class="text-gray-600 mb-4">您的反馈对我们很重要</p>
                <button class="w-full px-4 py-2 gradient-bg text-white rounded-lg hover:opacity-90 transition-opacity">
                  提供建议
                </button>
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
    AcademicCapIcon
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