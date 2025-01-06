<template>
  <div>
    <HeadView />
    <div class="min-h-screen relative ">
      <!-- 主标题区域 -->
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 min-h-[calc(100vh-var(--navbar-height))] flex items-center relative">
        <!-- 底部曲线和飞机动画 -->
        <div class="absolute left-0 right-0 h-32 pointer-events-none sm:bottom-0 bottom-[-2rem]">
          <!-- 曲线路径 -->
          <svg class="w-full h-full" preserveAspectRatio="none">
            <defs>
              <path 
                id="motionPath"
                class="curve-path"
                :d="curvePath"
                fill="none"
                stroke="#00000020"
                stroke-width="2"
                stroke-dasharray="8,8"
              />
            </defs>
            
            <!-- 使用 use 元素显示路径 -->
            <use href="#motionPath" />
            
            <!-- 节点 -->
            <g class="step-nodes">
              <circle cx="20%" cy="20" r="6" class="node-circle node-circle-blue" />
              <text x="20%" y="55" text-anchor="middle" class="text-sm fill-gray-600 font-medium">填写信息</text>
              
              <circle cx="50%" cy="30" r="6" class="node-circle node-circle-purple" />
              <text x="50%" y="65" text-anchor="middle" class="text-sm fill-gray-600 font-medium">选择模板</text>
              
              <circle cx="80%" cy="40" r="6" class="node-circle node-circle-green" />
              <text x="80%" y="75" text-anchor="middle" class="text-sm fill-gray-600 font-medium">保存导出</text>
            </g>
            
            <!-- 飞机动画 -->
            <g class="plane">
              <path 
                d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5"
                class="fill-none stroke-black stroke-2"
              >
                <animateMotion
                  :dur="isDesktop ? '10s' : '6s'"
                  repeatCount="indefinite"
                  rotate="auto"
                  keyPoints="0;0.3;0.6;1"
                  keyTimes="0;0.4;0.7;1"
                  calcMode="linear"
                >
                  <mpath href="#motionPath" />
                </animateMotion>
              </path>
            </g>
          </svg>
        </div>

        <div class="grid lg:grid-cols-2 gap-12 items-center w-full py-12 lg:py-0">
          <div class="relative">
            <!-- 装饰图标 -->
            <div class="absolute right-0 lg:-right-8 top-0 animate-float-slow hidden md:block">
              <div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
                <DocumentTextIcon class="w-6 h-6 text-blue-600" />
              </div>
            </div>
            
            <div class="absolute left-0 lg:-left-[200px] top-20 animate-float-normal hidden lg:block">
              <div class="w-10 h-10 bg-rose-100 rounded-lg flex items-center justify-center">
                <PencilIcon class="w-5 h-5 text-rose-600" />
              </div>
            </div>
            
            <div class="absolute right-0 lg:-right-[50px] top-[140px] animate-float-fast hidden md:block">
              <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <CheckIcon class="w-6 h-6 text-green-600" />
              </div>
            </div>

            <!-- 原有的标题内容 -->
            <h1 class="text-5xl sm:text-7xl font-bold leading-tight">
              <div class="typing-container text-gray-900" :key="typingKey">
                <div class="typing-line">
                  <span class="typing-text-1">制作简历</span>
                  <span class="typing-cursor-1">|</span>
                </div>
                <br/>
                <div class="typing-line">
                  <span class="typing-text-2">其实很简单</span>
                  <span class="typing-cursor-2">|</span>
                </div>
              </div>
            </h1>
            <p class="mt-8 text-xl text-gray-600 max-w-lg">
              3分钟快速创建专业简历，让你的求职之路更加出彩
            </p>
            <div class="mt-10 flex flex-col sm:flex-row gap-4 sm:gap-6">
              <button 
                class="group px-8 py-4 bg-black text-white rounded-full text-lg font-medium hover:bg-gray-900 transition-all hover:scale-105 flex items-center justify-center"
              >
                开始创建简历
               
              </button>
              <button 
                class="px-8 py-4 border-2 border-black text-black rounded-full text-lg font-medium hover:bg-black hover:text-white transition-all flex items-center justify-center"
              >
                导入简历
              </button>
            </div>
          </div>
          <div class="relative hidden lg:block">
            <img 
              src="https://resumegenius.com/wp-content/uploads/hero-resume-32-interface.webp" 
              alt="Resume Preview" 
              class="relative z-10 w-full h-auto rounded-2xl shadow-2xl transform hover:-rotate-2 transition-transform duration-500"
            >
          </div>
        </div>
      </div>

      <!-- 特点展示 -->
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="bg-white rounded-3xl p-8 sm:p-12 shadow-[0_0_40px_-15px_rgba(0,0,0,0.1)] hover:shadow-[0_0_50px_-15px_rgba(0,0,0,0.15)] transition-shadow duration-300">
          <div class="grid md:grid-cols-3 gap-12">
            <!-- 快速创建 -->
            <div class="group">
              <div class="mb-6">
                <div class="w-16 h-16 rounded-full bg-blue-50 flex items-center justify-center transform transition-all duration-300 group-hover:scale-110 group-hover:rotate-6">
                  <ClockIcon class="w-8 h-8 text-blue-600" />
                </div>
              </div>
              <h3 class="text-xl font-bold text-gray-900 mb-3">快速创建简历</h3>
              <p class="text-gray-600">我们的简历生成器让您能在几分钟内制作出完全定制化的简历，加快求职进度。</p>
            </div>

            <!-- 智能生成 -->
            <div class="group">
              <div class="mb-6">
                <div class="w-16 h-16 rounded-full bg-rose-50 flex items-center justify-center transform transition-all duration-300 group-hover:scale-110 group-hover:-rotate-6">
                  <DocumentTextIcon class="w-8 h-8 text-rose-600" />
                </div>
              </div>
              <h3 class="text-xl font-bold text-gray-900 mb-3">智能生成要点</h3>
              <p class="text-gray-600">工作经验是雇主最关注的部分。自动生成经验要点，突出您的工作能力。</p>
            </div>

            <!-- 自动格式化 -->
            <div class="group">
              <div class="mb-6">
                <div class="w-16 h-16 rounded-full bg-green-50 flex items-center justify-center transform transition-all duration-300 group-hover:scale-110 group-hover:rotate-12">
                  <AdjustmentsHorizontalIcon class="w-8 h-8 text-green-600" />
                </div>
              </div>
              <h3 class="text-xl font-bold text-gray-900 mb-3">自动格式调整</h3>
              <p class="text-gray-600">无需担心排版问题，填写您的内容，简历生成器会自动调整格式和间距。</p>
            </div>

            <!-- 即时下载 -->
            <div class="group">
              <div class="mb-6">
                <div class="w-16 h-16 rounded-full bg-purple-50 flex items-center justify-center transform transition-all duration-300 group-hover:scale-110 group-hover:-rotate-12">
                  <ArrowDownTrayIcon class="w-8 h-8 text-purple-600" />
                </div>
              </div>
              <h3 class="text-xl font-bold text-gray-900 mb-3">即时下载简历</h3>
              <p class="text-gray-600">支持PDF、Word等多种格式导出，使用仪表板测试不同模板，找到最适合的样式。</p>
            </div>

            <!-- 专家反馈 -->
            <div class="group">
              <div class="mb-6">
                <div class="w-16 h-16 rounded-full bg-amber-50 flex items-center justify-center transform transition-all duration-300 group-hover:scale-110 group-hover:rotate-6">
                  <LightBulbIcon class="w-8 h-8 text-amber-600" />
                </div>
              </div>
              <h3 class="text-xl font-bold text-gray-900 mb-3">专业建议反馈</h3>
              <p class="text-gray-600">在竞争激烈的就业市场中，获取专业的简历修改建议，让您的简历更具竞争力。</p>
            </div>

            <!-- 开启求职 -->
            <div class="group">
              <div class="mb-6">
                <div class="w-16 h-16 rounded-full bg-indigo-50 flex items-center justify-center transform transition-all duration-300 group-hover:scale-110 group-hover:-rotate-6">
                  <RocketLaunchIcon class="w-8 h-8 text-indigo-600" />
                </div>
              </div>
              <h3 class="text-xl font-bold text-gray-900 mb-3">开启求职之旅</h3>
              <p class="text-gray-600">完善的简历助您准备就绪，获得更多面试机会，收获更好的工作机会。</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 模板展示 -->
      <div class="py-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center mb-16">
            <h2 class="text-3xl font-bold text-gray-900 mb-4">精选模板</h2>
            <p class="text-xl text-gray-600">找到适合你的专业简历模板</p>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div v-for="template in featuredTemplates" :key="template.id"
              class="group relative aspect-[3/4] rounded-2xl overflow-hidden shadow-sm">
              <img 
                :src="template.preview" 
                :alt="template.name"
                class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
              >
              <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-60 transition-all duration-300 flex items-center justify-center opacity-0 group-hover:opacity-100">
                <button class="px-8 py-3 bg-white text-black rounded-full font-medium transform -translate-y-10 group-hover:translate-y-0 transition-all duration-300">
                  使用此模板
                </button>
              </div>
            </div>
          </div>
          <div class="text-center mt-12">
            <button class="px-8 py-3 border-2 border-black text-black rounded-full font-medium hover:bg-black hover:text-white transition-all">
              查看全部模板
            </button>
          </div>
        </div>
      </div>

      <!-- 简历示例展示 -->
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="bg-white rounded-3xl p-8 sm:p-12 shadow-sm">
          <!-- 标题区域 -->
          <div class="flex items-center space-x-4 mb-8">
            <div class="flex space-x-3">
              <button class="px-4 py-2 bg-gray-100 rounded-full text-gray-900 font-medium hover:bg-gray-200 transition-colors">
                <DocumentIcon class="w-5 h-5 inline-block mr-2" />
                简历
              </button>
              <button class="px-4 py-2 bg-gray-50 rounded-full text-gray-500 font-medium hover:bg-gray-100 transition-colors">
                <DocumentTextIcon class="w-5 h-5 inline-block mr-2" />
                求职信
              </button>
            </div>
          </div>

          <h2 class="text-4xl font-bold text-gray-900 mb-4">查看简历示例获取灵感</h2>
          <p class="text-gray-600 mb-8">
            我们提供超过400个专业简历示例供您参考。每个示例都经过我们的
            <a href="#" class="text-primary-600 hover:underline">职业顾问团队</a>
            审核和优化。
          </p>

          <!-- 职位标签 -->
          <div class="flex flex-wrap gap-3 mb-8">
            <button class="px-4 py-2 rounded-full text-sm font-medium inline-flex items-center space-x-2 bg-blue-50 text-blue-600">
              <UserIcon class="w-4 h-4" />
              <span>演员</span>
            </button>
            <button class="px-4 py-2 rounded-full text-sm font-medium inline-flex items-center space-x-2 bg-orange-50 text-orange-600">
              <BriefcaseIcon class="w-4 h-4" />
              <span>行政助理</span>
            </button>
            <button class="px-4 py-2 rounded-full text-sm font-medium inline-flex items-center space-x-2 bg-green-50 text-green-600">
              <BuildingOfficeIcon class="w-4 h-4" />
              <span>建筑设计</span>
            </button>
            <button class="px-4 py-2 rounded-full text-sm font-medium inline-flex items-center space-x-2 bg-pink-50 text-pink-600">
              <AcademicCapIcon class="w-4 h-4" />
              <span>在校学生</span>
            </button>
            <button class="px-4 py-2 rounded-full text-sm font-medium inline-flex items-center space-x-2 bg-purple-50 text-purple-600">
              <PhoneIcon class="w-4 h-4" />
              <span>客服专员</span>
            </button>
            <button class="px-4 py-2 rounded-full text-sm font-medium inline-flex items-center space-x-2 bg-yellow-50 text-yellow-600">
              <ComputerDesktopIcon class="w-4 h-4" />
              <span>IT工程师</span>
            </button>
            <button class="px-4 py-2 rounded-full text-sm font-medium inline-flex items-center space-x-2 bg-indigo-50 text-indigo-600">
              <PaintBrushIcon class="w-4 h-4" />
              <span>平面设计</span>
            </button>
            <button class="px-4 py-2 rounded-full text-sm font-medium inline-flex items-center space-x-2 bg-red-50 text-red-600">
              <ChartBarIcon class="w-4 h-4" />
              <span>项目经理</span>
            </button>
          </div>

          <!-- 更多标签行 -->
          <div class="flex flex-wrap gap-3">
            <button class="px-4 py-2 rounded-full text-sm font-medium inline-flex items-center space-x-2 bg-emerald-50 text-emerald-600">
              <ChartPieIcon class="w-4 h-4" />
              <span>市场营销</span>
            </button>
            <button class="px-4 py-2 rounded-full text-sm font-medium inline-flex items-center space-x-2 bg-rose-50 text-rose-600">
              <HeartIcon class="w-4 h-4" />
              <span>护理人员</span>
            </button>
            <button class="px-4 py-2 rounded-full text-sm font-medium inline-flex items-center space-x-2 bg-violet-50 text-violet-600">
              <AcademicCapIcon class="w-4 h-4" />
              <span>教师</span>
            </button>
            <button class="px-4 py-2 rounded-full text-sm font-medium inline-flex items-center space-x-2 bg-amber-50 text-amber-600">
              <BookOpenIcon class="w-4 h-4" />
              <span>高中生</span>
            </button>
          </div>

          <!-- 查看更多按钮 -->
          <div class="mt-8">
            <a href="/resume-examples" class="inline-flex items-center text-gray-900 font-medium hover:text-gray-600 transition-colors">
              查看更多示例
              <ArrowRightIcon class="w-5 h-5 ml-2" />
            </a>
          </div>
        </div>
      </div>



      <!-- 新闻资讯区域 -->
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">职场资源</h2>
          <p class="text-xl text-gray-600">获取最新的职场动态和求职技巧</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- 文章卡片 -->
          <div v-for="notice in notices.slice(0, 3)" :key="notice.id" 
            class="group bg-white rounded-2xl overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
            <div class="aspect-[16/9] bg-gradient-to-br from-blue-50 to-indigo-50 relative overflow-hidden">
              <div class="absolute inset-0 bg-gradient-to-br from-blue-500/10 to-indigo-500/10 group-hover:scale-110 transition-transform duration-500"></div>
              <div class="absolute bottom-4 left-4">
                <span class="px-3 py-1 bg-white/90 rounded-full text-sm font-medium text-gray-700">
                  {{ notice.category }}
                </span>
              </div>
            </div>
            <div class="p-6">
              <div class="flex items-center space-x-2 mb-4">
                <CalendarIcon class="w-4 h-4 text-gray-400" />
                <span class="text-sm text-gray-500">{{ notice.date }}</span>
              </div>
              <h3 class="text-xl font-bold text-gray-900 mb-3 group-hover:text-primary-600 transition-colors line-clamp-2">
                {{ notice.title }}
              </h3>
              <p class="text-gray-600 mb-4 line-clamp-2">{{ notice.content }}</p>
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <img :src="notice.author.avatar" alt="" class="w-8 h-8 rounded-full">
                  <span class="text-sm font-medium text-gray-700">{{ notice.author.name }}</span>
                </div>
                <button class="text-primary-600 hover:text-primary-700 font-medium text-sm inline-flex items-center">
                  阅读更多
                  <ArrowRightIcon class="w-4 h-4 ml-1" />
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 查看更多按钮 -->
        <div class="text-center mt-12">
          <a href="/resources" class="inline-block px-6 py-3 bg-gray-900 text-white rounded-full font-medium hover:bg-gray-800 transition-colors">
            查看更多资讯
          </a>
        </div>
      </div>

      <!-- 帮助中心区域 -->
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">帮助中心</h2>
          <p class="text-xl text-gray-600">解答您的疑问，助您轻松制作简历</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <!-- 常见问题 -->
          <div class="bg-white rounded-2xl p-6 hover:shadow-lg transition-shadow duration-300 group">
            <div class="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
              <QuestionMarkCircleIcon class="w-6 h-6 text-blue-600" />
            </div>
            <h3 class="text-lg font-bold text-gray-900 mb-2">常见问题</h3>
            <p class="text-gray-600 mb-4">查看用户最常遇到的问题和解答</p>
            <a href="/faq" class="text-blue-600 hover:text-blue-700 font-medium inline-flex items-center">
              了解更多
              <ArrowRightIcon class="w-4 h-4 ml-1" />
            </a>
          </div>

          <!-- 使用教程 -->
          <div class="bg-white rounded-2xl p-6 hover:shadow-lg transition-shadow duration-300 group">
            <div class="w-12 h-12 bg-green-50 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
              <BookOpenIcon class="w-6 h-6 text-green-600" />
            </div>
            <h3 class="text-lg font-bold text-gray-900 mb-2">使用教程</h3>
            <p class="text-gray-600 mb-4">详细的功能介绍和操作指南</p>
            <a href="/tutorials" class="text-green-600 hover:text-green-700 font-medium inline-flex items-center">
              查看教程
              <ArrowRightIcon class="w-4 h-4 ml-1" />
            </a>
          </div>

          <!-- 简历技巧 -->
          <div class="bg-white rounded-2xl p-6 hover:shadow-lg transition-shadow duration-300 group">
            <div class="w-12 h-12 bg-purple-50 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
              <LightBulbIcon class="w-6 h-6 text-purple-600" />
            </div>
            <h3 class="text-lg font-bold text-gray-900 mb-2">简历技巧</h3>
            <p class="text-gray-600 mb-4">专业的简历写作建议和技巧</p>
            <a href="/tips" class="text-purple-600 hover:text-purple-700 font-medium inline-flex items-center">
              获取建议
              <ArrowRightIcon class="w-4 h-4 ml-1" />
            </a>
          </div>

          <!-- 联系我们 -->
          <div class="bg-white rounded-2xl p-6 hover:shadow-lg transition-shadow duration-300 group">
            <div class="w-12 h-12 bg-rose-50 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
              <ChatBubbleLeftRightIcon class="w-6 h-6 text-rose-600" />
            </div>
            <h3 class="text-lg font-bold text-gray-900 mb-2">联系我们</h3>
            <p class="text-gray-600 mb-4">有问题？我们随时为您解答</p>
            <a href="/contact" class="text-rose-600 hover:text-rose-700 font-medium inline-flex items-center">
              联系客服
              <ArrowRightIcon class="w-4 h-4 ml-1" />
            </a>
          </div>
        </div>
      </div>


            <!-- CTA区域 -->
            <div class="relative py-12 overflow-hidden">
        <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
          <h2 class="text-4xl font-bold text-gray-900 mb-6">准备好开始了吗？</h2>
          <p class="text-xl text-gray-600 mb-10">3分钟完成简历创建，提升求职竞争力</p>
          <button class="px-12 py-4 bg-black text-white rounded-full text-lg font-medium hover:bg-gray-900 transition-all hover:scale-105">
            免费创建简历
          </button>
        </div>
      </div>
    </div>
    <FootView />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import HeadView from '../components/HeadView.vue'
import FootView from '../components/FootView.vue'
import { StarIcon } from '@heroicons/vue/20/solid'
import { 
  DocumentDuplicateIcon, 
  SparklesIcon,
  CloudArrowDownIcon,
  ShieldCheckIcon,
  PaintBrushIcon,
  DocumentTextIcon,
  UserGroupIcon,
  ClockIcon,
  AdjustmentsHorizontalIcon,
  ArrowDownTrayIcon,
  LightBulbIcon,
  RocketLaunchIcon,
  DocumentIcon,
  UserIcon,
  BriefcaseIcon,
  BuildingOfficeIcon,
  AcademicCapIcon,
  PhoneIcon,
  ComputerDesktopIcon,
  ChartBarIcon,
  ChartPieIcon,
  HeartIcon,
  BookOpenIcon,
  ArrowRightIcon,
  PencilIcon,
  CheckIcon,
  QuestionMarkCircleIcon,
  ChatBubbleLeftRightIcon,
  CalendarIcon,
  PaperAirplaneIcon
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
    title: "如何在面试中展现你的领导力",
    content: "在当今竞争激烈的职场中，领导力已经成为许多职位的必备技能...",
    date: "2024-03-15",
    category: "面试技巧",
    author: {
      name: "Sarah Chen",
      avatar: "https://picsum.photos/32/32?random=1"
    }
  },
  {
    id: 2,
    title: "2024年最受欢迎的职业技能",
    content: "随着技术的快速发展，雇主们正在寻找具备这些关键技能的人才...",
    date: "2024-03-14",
    category: "职业发展",
    author: {
      name: "Mike Johnson",
      avatar: "https://picsum.photos/32/32?random=2"
    }
  },
  {
    id: 3,
    title: "远程工作：如何提高工作效率",
    content: "远程工作已经成为新常态，这里有一些提高效率的实用技巧...",
    date: "2024-03-13",
    category: "工作指南",
    author: {
      name: "Lisa Wang",
      avatar: "https://picsum.photos/32/32?random=3"
    }
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

// 精选模板数据
const featuredTemplates = [
  {
    id: 1,
    name: 'Stockholm',
    preview: 'https://picsum.photos/300/400?random=1'
  },
  {
    id: 2,
    name: 'New York',
    preview: 'https://picsum.photos/300/400?random=2'
  },
  {
    id: 3,
    name: 'Toronto',
    preview: 'https://picsum.photos/300/400?random=3'
  }
]

// 用户评价数据
const userReviews = [
  {
    id: 1,
    name: '张明',
    title: '使用体验',
    content: '使用这个平台制作的简历帮助我成功应聘到理想的工作。模板很专业，操作也很简单。',
    avatar: 'https://picsum.photos/40/40?random=1'
  },
  {
    id: 2,
    name: '李华',
    title: 'AI建议',
    content: '平台提供的AI建议对优化简历内容很有帮助，让我的简历更有竞争力。',
    avatar: 'https://picsum.photos/40/40?random=2'
  },
  {
    id: 3,
    name: '王芳',
    title: '多种导出格式',
    content: '多种导出格式很实用，简历的排版和样式都很专业，强烈推荐！',
    avatar: 'https://picsum.photos/40/40?random=3'
  }
]

// 打字动画控制
const typingKey = ref(0)
let typingTimer = null

const restartTyping = () => {
  clearTimeout(typingTimer)
  typingTimer = setTimeout(() => {
    typingKey.value++
  }, 6000) // 6秒后重新开始打字（3秒打字动画 + 3秒等待）
}

watch(typingKey, () => {
  restartTyping()
})

onMounted(() => {
  restartTyping()
})

onUnmounted(() => {
  clearTimeout(typingTimer)
})

// 添加响应式曲线路径
const curvePath = ref('')

// 更新曲线路径的函数
const updateCurvePath = () => {
  if (typeof window !== 'undefined') {
    const container = document.querySelector('.max-w-7xl')
    if (container) {
      const width = container.clientWidth
      curvePath.value = `M0,30 Q${width/4},5 ${width/2},30 T${width},30`
    }
  }
}

// 生命周期钩子
onMounted(() => {
  updateCurvePath() // 初始化路径
  window.addEventListener('resize', updateCurvePath)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateCurvePath)
})

// 添加桌面检测
const isDesktop = ref(false)

const checkDesktop = () => {
  isDesktop.value = window.innerWidth >= 1024 // lg breakpoint
}

onMounted(() => {
  checkDesktop()
  window.addEventListener('resize', checkDesktop)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkDesktop)
})
</script>

<style scoped>
/* 移除之前的样式，保持简洁 */

/* 添加浮动动画 */
@keyframes float-slow {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

@keyframes float-normal {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-15px); }
}

@keyframes float-fast {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-8px); }
}

.animate-float-slow {
  animation: float-slow 4s ease-in-out infinite;
}

.animate-float-normal {
  animation: float-normal 3s ease-in-out infinite;
}

.animate-float-fast {
  animation: float-fast 2.5s ease-in-out infinite;
}

/* 打字动画效果 */
.typing-container {
  display: inline-block;
  position: relative;
}

.typing-line {
  display: inline-flex;
  position: relative;
}

.typing-text-1 {
  display: inline-block;
  overflow: hidden;
  white-space: nowrap;
  width: 0;
  animation: typing1 1.5s steps(4, end) forwards;
}

.typing-text-2 {
  display: inline-block;
  overflow: hidden;
  white-space: nowrap;
  width: 0;
  animation: typing2 1.5s steps(5, end) forwards;
  animation-delay: 1.5s;
}

.typing-cursor-1 {
  position: absolute;
  display: inline-block;
  animation: blink 1s step-end infinite,
           cursor1 1.5s steps(4, end) forwards,
           fadeOut 0.1s forwards 1.5s;
  font-weight: 300;
}

.typing-cursor-2 {
  position: absolute;
  display: inline-block;
  animation: blink 1s step-end infinite,
           cursor2 1.5s steps(5, end) forwards;
  animation-delay: 1.5s;
  font-weight: 300;
  opacity: 0;
}

@keyframes typing1 {
  from { width: 0 }
  to { width: 4.1em }
}

@keyframes typing2 {
  from { width: 0 }
  to { width: 5em }
}

@keyframes cursor1 {
  from { left: 0 }
  to { left: 4.1em }
}

@keyframes cursor2 {
  0% { 
    left: 0;
    opacity: 1;
  }
  100% { 
    left: 5em;
    opacity: 1;
  }
}

@keyframes fadeOut {
  to { opacity: 0 }
}

@keyframes blink {
  50% { opacity: 0 }
}

/* 光标样式 */
.typing-cursor-1,
.typing-cursor-2 {
  color: currentColor;
  position: absolute;
  display: inline-block;
}

.plane {
  transform-origin: center;
  transform: scale(1.2);
}

.step-nodes circle {
  transition: all 0.3s ease;
}

.step-nodes circle:hover {
  r: 8;
  fill: #000;
  stroke: #000;
  cursor: pointer;
}

.step-nodes text {
  font-size: 0.875rem;
  font-weight: 500;
}

@keyframes dash {
  to {
    stroke-dashoffset: -16;
  }
}

.curve-path {
  animation: dash 1s linear infinite;
}



/* 移除可能影响其他元素的全局样式 */
.node-circle {
  stroke-width: 3;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.node-circle-blue {
  fill: #3B82F6;
  stroke: rgba(59, 130, 246, 0.5);
}

.node-circle-purple {
  fill: #8B5CF6;
  stroke: rgba(139, 92, 246, 0.5);
}

.node-circle-green {
  fill: #10B981;
  stroke: rgba(16, 185, 129, 0.5);
}

.node-circle:hover {
  r: 8;
  stroke-width: 4;
  filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
}

.node-circle-blue:hover {
  fill: #3B82F6;
  stroke: rgba(59, 130, 246, 0.5);
}

.node-circle-purple:hover {
  fill: #8B5CF6;
  stroke: rgba(139, 92, 246, 0.5);
}

.node-circle-green:hover {
  fill: #10B981;
  stroke: rgba(16, 185, 129, 0.5);
}

.node-circle:hover + text {
  font-weight: 600;
  fill: #111827;
}
</style>