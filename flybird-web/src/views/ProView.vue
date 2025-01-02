<template>
  <div>
    <HeadView />
    <div class="min-h-screen relative overflow-hidden" style="padding-top: calc(var(--navbar-height) + 2rem);">
      <!-- 页面标题区域 -->
      <div class="text-center mb-12">
        <h2 class="text-4xl font-bold text-gray-900 mb-4">选择会员计划</h2>
        <p class="text-xl text-gray-600">Select the best membership plan for you</p>
      </div>

      <!-- Tab 导航 -->
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-8">
        <div class="flex justify-center">
          <div class="inline-flex rounded-full bg-white p-1 shadow-sm">
            <button v-for="tab in tabs" :key="tab.id" @click="handleTabClick(tab.id)" :class="[
              'px-6 py-2 text-sm font-medium rounded-full whitespace-nowrap',
              activeTab === tab.id
                ? 'bg-black text-white'
                : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
            ]">
              {{ tab.name }}
            </button>
          </div>
        </div>
      </div>

      <!-- 内容区域 -->
      <div class="relative z-20">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <!-- 会员计划部分 -->
          <div v-if="activeTab === 'purchase'" class="max-w-7xl mx-auto">
            <!-- 会员卡片列表 -->
            <div class="grid grid-cols-1 gap-6 sm:grid-cols-3 mt-12">
              <div 
                v-for="plan in plans" 
                :key="plan.id"
                class="relative bg-white rounded-xl transition-all duration-300 hover:-translate-y-1"
                :class="[
                  plan.hot 
                    ? 'border-2 border-black shadow-lg' 
                    : 'border border-gray-200 hover:border-black'
                ]"
              >
                <!-- 热门标签 -->
                <div 
                  v-if="plan.hot"
                  class="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-black text-white text-xs px-4 py-1 rounded-full font-medium"
                >
                  热门 / Popular
                </div>

                <div class="p-6">
                  <!-- 标题 -->
                  <div class="text-center mb-6">
                    <component :is="plan.icon" class="w-8 h-8 mx-auto mb-3 text-gray-900" />
                    <h3 class="text-xl font-bold text-gray-900">{{ plan.name }}</h3>
                  </div>

                  <!-- 价格 -->
                  <div class="text-center mb-6">
                    <div class="text-gray-400 line-through text-sm">¥{{ plan.originalPrice }}</div>
                    <div class="flex items-center justify-center">
                      <span class="text-sm">¥</span>
                      <span class="text-4xl font-bold mx-1">{{ plan.price }}</span>
                      <span class="text-gray-500">/{{ plan.period }}</span>
                    </div>
                  </div>

                  <!-- 功能列表 -->
                  <ul class="space-y-3 mb-6">
                    <li 
                      v-for="feature in plan.features" 
                      :key="feature"
                      class="flex items-start text-sm text-gray-600"
                    >
                      <CheckIcon class="h-5 w-5 text-black shrink-0 mr-2" />
                      <span>{{ feature }}</span>
                    </li>
                  </ul>

                  <!-- 按钮 -->
                  <button
                    @click="openPaymentModal(plan)"
                    class="w-full py-3 text-center rounded-lg font-medium transition-colors duration-200"
                    :class="[
                      plan.hot 
                        ? 'bg-black text-white hover:bg-gray-800' 
                        : 'border-2 border-black text-black hover:bg-black hover:text-white'
                    ]"
                  >
                    开通 / Subscribe
                  </button>
                </div>
              </div>
            </div>

            <!-- 会员特权 -->
            <div class="mt-20">
              <h3 class="text-2xl font-bold text-center mb-12">会员特权 / Benefits</h3>
              <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
                <div 
                  v-for="feature in memberFeatures"
                  :key="feature.id"
                  class="p-6 bg-white border border-gray-200 rounded-lg hover:border-black transition-colors duration-200"
                >
                  <component 
                    :is="feature.icon"
                    class="w-8 h-8 text-black mb-4"
                  />
                  <h4 class="font-bold mb-2">{{ feature.name }}</h4>
                  <p class="text-sm text-gray-600">{{ feature.description }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- 学生认证部分 -->
          <div v-else-if="activeTab === 'student'" class="max-w-3xl mx-auto px-4 sm:px-0">
            <div class="mt-12 bg-white rounded-xl p-6 sm:p-12 shadow-lg">
              <!-- 顶部区域 -->
              <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-8 sm:mb-12 border-b border-gray-100 pb-4 sm:pb-8">
                <div>
                  <h3 class="text-xl sm:text-2xl font-bold text-gray-900">学生专属特权</h3>
                  <p class="mt-2 text-gray-500">认证后即可获得 1 年会员资格</p>
                </div>
                <div class="flex items-center space-x-2 mt-4 sm:mt-0">
                  <span class="text-sm text-gray-400">认证时长</span>
                  <span class="text-xl sm:text-2xl font-bold text-black">365</span>
                  <span class="text-sm text-gray-400">天</span>
                </div>
              </div>

              <!-- 认证方式选择 -->
              <div class="space-y-4">
                <!-- 教育邮箱认证 -->
                <div 
                  class="group relative p-4 sm:p-6 border-2 rounded-xl cursor-pointer transition-all duration-300"
                  :class="[
                    selectedMethod === 'edu_email' 
                      ? 'border-black' 
                      : 'border-gray-100 hover:border-black'
                  ]"
                  @click="selectedMethod = 'edu_email'"
                >
                  <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-4">
                      <div class="w-10 sm:w-12 h-10 sm:h-12 bg-gray-50 rounded-lg flex items-center justify-center">
                        <EnvelopeIcon class="w-5 sm:w-6 h-5 sm:h-6 text-gray-900" />
                      </div>
                      <div>
                        <h4 class="font-medium text-gray-900">教育邮箱认证</h4>
                        <p class="text-sm text-gray-500 mt-1">使用学校邮箱，在线自动认证</p>
                      </div>
                    </div>
                    <div class="w-5 sm:w-6 h-5 sm:h-6 rounded-full border-2 border-gray-200 group-hover:border-black flex items-center justify-center">
                      <div 
                        class="w-2 sm:w-3 h-2 sm:h-3 rounded-full transition-all duration-300"
                        :class="selectedMethod === 'edu_email' ? 'bg-black' : 'bg-transparent'"
                      ></div>
                    </div>
                  </div>
                  <!-- 详细说明 - 默认展开 -->
                  <div class="mt-4 text-sm text-gray-500">
                    <ul class="list-disc pl-5 space-y-1">
                      <li>输入教育邮箱，系统校验域名</li>
                      <li>发送验证码到教育邮箱</li>
                      <li>输入验证码完成认证</li>
                      <li>自动化程度高，用户体验好</li>
                    </ul>
                  </div>
                </div>

                <!-- 学生证认证 -->
                <div 
                  class="group relative p-4 sm:p-6 border-2 rounded-xl cursor-pointer transition-all duration-300"
                  :class="[
                    selectedMethod === 'student_card' 
                      ? 'border-black' 
                      : 'border-gray-100 hover:border-black'
                  ]"
                  @click="selectedMethod = 'student_card'"
                >
                  <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-4">
                      <div class="w-10 sm:w-12 h-10 sm:h-12 bg-gray-50 rounded-lg flex items-center justify-center">
                        <IdentificationIcon class="w-5 sm:w-6 h-5 sm:h-6 text-gray-900" />
                      </div>
                      <div>
                        <h4 class="font-medium text-gray-900">学生证认证</h4>
                        <p class="text-sm text-gray-500 mt-1">上传学生证照片，快速完成认证</p>
                      </div>
                    </div>
                    <div class="w-5 sm:w-6 h-5 sm:h-6 rounded-full border-2 border-gray-200 group-hover:border-black flex items-center justify-center">
                      <div 
                        class="w-2 sm:w-3 h-2 sm:h-3 rounded-full transition-all duration-300"
                        :class="selectedMethod === 'student_card' ? 'bg-black' : 'bg-transparent'"
                      ></div>
                    </div>
                  </div>
                  <!-- 详细说明 -->
                  <div v-if="selectedMethod === 'student_card'" class="mt-4 text-sm text-gray-500">
                    <ul class="list-disc pl-5 space-y-1">
                      <li>上传学生证正面和手持学生证自拍照</li>
                      <li>OCR识别学生证信息</li>
                      <li>人脸识别对比自拍照与用户头像</li>
                      <li>仅认可正规高校</li>
                    </ul>
                  </div>
                </div>
              </div>

              <!-- 底部说明和按钮 -->
              <div class="mt-8 sm:mt-12 flex flex-col sm:flex-row items-center justify-between">
                <div class="flex items-center space-x-2 text-sm text-gray-500 mb-4 sm:mb-0">
                  <InformationCircleIcon class="w-5 h-5" />
                  <span>认证通过后立即生效</span>
                </div>
                <button 
                  @click="handleVerification"
                  class="w-full sm:w-auto px-8 py-3 bg-black text-white rounded-lg font-medium hover:bg-gray-800 transition-colors duration-200"
                >
                  开始认证
                </button>
              </div>
            </div>
          </div>

          <!-- 邀请好友部分 -->
          <div v-else-if="activeTab === 'invite'" class="max-w-3xl mx-auto px-4 sm:px-0">
            <div class="mt-12 bg-white rounded-xl p-6 sm:p-12 shadow-lg">
              <!-- 顶部区域 -->
              <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-8 sm:mb-12 border-b border-gray-100 pb-4 sm:pb-8">
                <div>
                  <h3 class="text-xl sm:text-2xl font-bold text-gray-900">邀请好友特权</h3>
                  <p class="mt-2 text-gray-500">邀请好友注册，双方都可获得会员奖励</p>
                </div>
                <div class="flex items-center space-x-2 mt-4 sm:mt-0">
                  <span class="text-sm text-gray-400">已邀请</span>
                  <span class="text-xl sm:text-2xl font-bold text-black">{{ inviteCount }}</span>
                  <span class="text-sm text-gray-400">人</span>
                </div>
              </div>

              <!-- 邀请方式选择 -->
              <div class="space-y-4">
                <!-- 分享链接 -->
                <div class="group relative p-4 sm:p-6 border-2 rounded-xl cursor-pointer transition-all duration-300"
                  :class="[
                    selectedInviteMethod === 'share_link' 
                      ? 'border-black' 
                      : 'border-gray-100 hover:border-black'
                  ]"
                  @click="selectedInviteMethod = 'share_link'"
                >
                  <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-4">
                      <div class="w-10 sm:w-12 h-10 sm:h-12 bg-gray-50 rounded-lg flex items-center justify-center">
                        <LinkIcon class="w-5 sm:w-6 h-5 sm:h-6 text-gray-900" />
                      </div>
                      <div>
                        <h4 class="font-medium text-gray-900">分享邀请链接</h4>
                        <p class="text-sm text-gray-500 mt-1">复制链接分享给好友</p>
                      </div>
                    </div>
                    <div class="w-5 sm:w-6 h-5 sm:h-6 rounded-full border-2 border-gray-200 group-hover:border-black flex items-center justify-center">
                      <div class="w-2 sm:w-3 h-2 sm:h-3 rounded-full transition-all duration-300"
                        :class="selectedInviteMethod === 'share_link' ? 'bg-black' : 'bg-transparent'"
                      ></div>
                    </div>
                  </div>
                  <!-- 详细说明 -->
                  <div class="mt-4">
                    <div class="flex items-center space-x-2 bg-gray-50 rounded-lg p-3">
                      <input 
                        type="text" 
                        :value="inviteLink" 
                        readonly 
                        class="flex-1 bg-transparent border-none text-sm text-gray-600 focus:ring-0"
                      >
                      <button 
                        @click.stop="handleCopyLink"
                        class="px-4 py-1.5 bg-black text-white text-sm rounded-lg hover:bg-gray-800"
                      >
                        复制链接
                      </button>
                    </div>
                  </div>
                </div>

                <!-- 社交分享 -->
                <div class="group relative p-4 sm:p-6 border-2 rounded-xl cursor-pointer transition-all duration-300"
                  :class="[
                    selectedInviteMethod === 'social_share' 
                      ? 'border-black' 
                      : 'border-gray-100 hover:border-black'
                  ]"
                  @click="selectedInviteMethod = 'social_share'"
                >
                  <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-4">
                      <div class="w-10 sm:w-12 h-10 sm:h-12 bg-gray-50 rounded-lg flex items-center justify-center">
                        <ShareIcon class="w-5 sm:w-6 h-5 sm:h-6 text-gray-900" />
                      </div>
                      <div>
                        <h4 class="font-medium text-gray-900">社交分享</h4>
                        <p class="text-sm text-gray-500 mt-1">分享到社交平台</p>
                      </div>
                    </div>
                    <div class="w-5 sm:w-6 h-5 sm:h-6 rounded-full border-2 border-gray-200 group-hover:border-black flex items-center justify-center">
                      <div class="w-2 sm:w-3 h-2 sm:h-3 rounded-full transition-all duration-300"
                        :class="selectedInviteMethod === 'social_share' ? 'bg-black' : 'bg-transparent'"
                      ></div>
                    </div>
                  </div>
                  <!-- 详细说明 -->
                  <div v-if="selectedInviteMethod === 'social_share'" class="mt-4">
                    <button 
                      @click.stop="handleShare"
                      class="w-full py-2 bg-black text-white rounded-lg hover:bg-gray-800"
                    >
                      一键分享
                    </button>
                  </div>
                </div>
              </div>

              <!-- 奖励规则 -->
              <div class="mt-8 sm:mt-12 space-y-6">
                <h4 class="font-medium text-gray-900">奖励规则</h4>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div class="p-4 bg-gray-50 rounded-lg text-center">
                    <div class="text-xl font-bold text-black mb-1">2人</div>
                    <div class="text-sm text-gray-500">获得1个月会员</div>
                  </div>
                  <div class="p-4 bg-gray-50 rounded-lg text-center">
                    <div class="text-xl font-bold text-black mb-1">5人</div>
                    <div class="text-sm text-gray-500">获得1年会员</div>
                  </div>
                  <div class="p-4 bg-gray-50 rounded-lg text-center">
                    <div class="text-xl font-bold text-black mb-1">10人</div>
                    <div class="text-sm text-gray-500">获得终身会员</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 支付弹窗 -->
    <div v-if="showPaymentModal" class="fixed inset-0 z-50">
      <!-- 遮罩层 -->
      <div class="absolute inset-0 bg-black bg-opacity-50" @click="closePaymentModal"></div>

      <!-- 弹窗内容 -->
      <div class="relative z-10 min-h-screen px-4 flex items-center justify-center">
        <div class="bg-white rounded-lg w-full max-w-md p-6">
          <!-- 关闭按钮 -->
          <button @click="closePaymentModal" class="absolute top-4 right-4 text-gray-400 hover:text-gray-500">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>

          <!-- 订单信息 -->
          <div class="text-center mb-6">
            <h3 class="text-lg font-medium text-gray-900">确认订单</h3>
            <p class="mt-2 text-sm text-gray-500">请选择支付方式完成购买</p>
          </div>

          <div class="bg-gray-50 rounded-lg p-4 mb-6">
            <div class="flex justify-between items-center">
              <span class="text-gray-600">{{ selectedPlan?.name }}</span>
              <span class="text-gray-900 font-medium">¥{{ selectedPlan?.price }}</span>
            </div>
          </div>

          <!-- 支付方式选择 -->
          <div class="space-y-4">
            <button v-for="method in paymentMethods" :key="method.id" @click="selectPaymentMethod(method)" :class="[
              'w-full flex items-center justify-between px-4 py-3 border rounded-lg',
              selectedPaymentMethod?.id === method.id
                ? 'border-primary-600 bg-primary-50'
                : 'border-gray-200 hover:border-primary-600'
            ]">
              <div class="flex items-center">
                <img :src="method.icon" :alt="method.name" class="h-6 w-6">
                <span class="ml-3 font-medium text-gray-900">{{ method.name }}</span>
              </div>
              <div class="flex-shrink-0 text-primary-600">
                <svg v-if="selectedPaymentMethod?.id === method.id" class="h-5 w-5" viewBox="0 0 20 20"
                  fill="currentColor">
                  <path fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clip-rule="evenodd" />
                </svg>
              </div>
            </button>
          </div>

          <!-- 按钮组 -->
          <div class="mt-6 flex space-x-4">
            <!-- 取消按钮 -->
            <button @click="closePaymentModal"
              class="flex-1 px-4 py-3 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md font-medium transition-colors duration-200">
              取消支付
            </button>

            <!-- 确认支付按钮 -->
            <button @click="handlePayment" :disabled="!selectedPaymentMethod"
              class="flex-1 px-4 py-3 text-white bg-primary-600 hover:bg-primary-700 disabled:bg-gray-300 disabled:cursor-not-allowed rounded-md font-medium transition-colors duration-200">
              确认支付
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 二维码弹窗 -->
    <div v-if="showQRCode" class="fixed inset-0 z-50">
      <div class="absolute inset-0 bg-black bg-opacity-50" @click="closeQRCode"></div>
      <div class="relative z-10 min-h-screen px-4 flex items-center justify-center">
        <div class="bg-white rounded-lg w-full max-w-sm p-6 text-center">
          <button @click="closeQRCode" class="absolute top-4 right-4 text-gray-400 hover:text-gray-500">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>

          <h3 class="text-lg font-medium text-gray-900 mb-4">
            {{ selectedPaymentMethod?.name }}扫码支付
          </h3>

          <div class="bg-white p-4 inline-block rounded-lg">
            <img :src="qrCodeUrl" alt="支付二维码" class="w-48 h-48">
          </div>

          <p class="mt-4 text-sm text-gray-500">
            请使用{{ selectedPaymentMethod?.name }}扫描二维码完成支付
          </p>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="isLoading" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 flex flex-col items-center">
        <div class="animate-spin rounded-full h-12 w-12 border-4 border-primary-500 border-t-transparent"></div>
        <span class="mt-4 text-gray-700">处理中...</span>
      </div>
    </div>

    <FootView />
  </div>
</template>
<script setup>

import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import HeadView from '../components/HeadView.vue'
import FootView from '../components/FootView.vue'
import { showToast } from '@/components/ToastMessage'
import {
  CalendarIcon,
  StarIcon,
  SparklesIcon,
  CheckIcon,
  DocumentArrowDownIcon,
  DocumentTextIcon,
  UserGroupIcon,
  ChartBarIcon,
  DocumentDuplicateIcon,
  AcademicCapIcon,
  ChatBubbleLeftRightIcon,
  InformationCircleIcon,
  GiftIcon,
  IdentificationIcon,
  EnvelopeIcon,
  LinkIcon,
  ShareIcon
} from '@heroicons/vue/24/outline'
const router = useRouter()
const store = useStore()

// 状态管理
const showPaymentModal = ref(false)
const showQRCode = ref(false)
const selectedPaymentMethod = ref(null)
const qrCodeUrl = ref('')
const selectedPlan = ref(null)
const inviteCount = ref(0)
const requiredInvites = ref(5)
const isLoading = ref(false)
const inviteLink = ref('https://example.com/invite/123456')

// 标签页配置
const tabs = [
  {
    id: 'purchase',
    name: '直接购买'
  },
  {
    id: 'student',
    name: '学生认证'
  },
  {
    id: 'invite',
    name: '邀请好友'
  }
]

const activeTab = ref('purchase')
// 会员特权列表
const memberFeatures = [
  {
    id: 1,
    name: '简历下载',
    description: '无限次下载简历，支持多种格式导出',
    icon: DocumentArrowDownIcon
  },
  {
    id: 2,
    name: '模板特权',
    description: '解锁所有高级模板，支持自定义风格',
    icon: DocumentTextIcon
  },
  {
    id: 3,
    name: 'AI优化',
    description: '智能分析简历内容，提供专业修改建议',
    icon: SparklesIcon
  },
  {
    id: 4,
    name: '一对一指导',
    description: '专业顾问提供简历编写和求职指导',
    icon: UserGroupIcon
  },
  {
    id: 5,
    name: '访问统计',
    description: '查看简历被浏览和下载的详细数据',
    icon: ChartBarIcon
  },
  {
    id: 6,
    name: '多份管理',
    description: '创建多份简历，针对不同职位投递',
    icon: DocumentDuplicateIcon
  },
  {
    id: 7,
    name: '求职经验',
    description: '获取行业内部求职经验和面试技巧',
    icon: AcademicCapIcon
  },
  {
    id: 8,
    name: 'VIP客服',
    description: '专属客服通道，优先响应需求',
    icon: ChatBubbleLeftRightIcon
  }
]

// 会员方案 - 简化为只包含价格和周期信息
const plans = [
  {
    id: 'monthly',
    name: '月度会员',
    icon: CalendarIcon,
    price: '19.9',
    originalPrice: '39.9',
    period: '月',
    features: [
      'AI简历优化 5 次/月',
      '简历模板无限制使用',
      '求职数据分析',
      '会员专属客服'
    ]
  },
  {
    id: 'yearly',
    name: '年度会员',
    icon: StarIcon,
    price: '99',
    originalPrice: '199',
    period: '年',
    hot: true,
    features: [
      'AI简历优化无限次数',
      '简历模板无限制使用',
      '求职数据分析',
      '一对一简历指导',
      '会员专属客服',
      '优先体验新功能'
    ]
  },
  {
    id: 'lifetime',
    name: '终身会员',
    icon: SparklesIcon,
    price: '299',
    originalPrice: '599',
    period: '终身',
    features: [
      '包含年度会员所有特权',
      '终身享受会员权益',
      'VIP专属标识',
      '简历制作课程',
      '面试辅导服务',
      '会员价格锁定'
    ]
  }
]


// 支付方式
const paymentMethods = [
  {
    id: 'alipay',
    name: '支付宝支付',
    icon: '/icons/alipay.png'
  },
  {
    id: 'wechat',
    name: '微信支付',
    icon: '/icons/wechat.png'
  }
]

// 邀请记录数据
const inviteHistory = ref([
  {
    id: 1,
    name: '张三',
    avatar: '/avatars/1.jpg',
    date: '2024-03-20'
  },
  {
    id: 2,
    name: '李四',
    avatar: '/avatars/2.jpg',
    date: '2024-03-19'
  }
])

// 计算属性
const isAuthenticated = computed(() => store.state.isAuthenticated)
const userInfo = computed(() => store.state.userInfo)
const inviteProgress = computed(() => {
  return Math.min((inviteCount.value / requiredInvites.value) * 100, 100)
})

// 方法
const handleTabClick = (tabId) => {
  activeTab.value = tabId
}

const openPaymentModal = (plan) => {
  if (!isAuthenticated.value) {
    showToast('请先登录', 'warning')
    router.push('/login')
    return
  }
  selectedPlan.value = plan
  selectedPaymentMethod.value = null
  showPaymentModal.value = true
}

const closePaymentModal = () => {
  showPaymentModal.value = false
  selectedPlan.value = null
  selectedPaymentMethod.value = null
}

const selectPaymentMethod = (method) => {
  selectedPaymentMethod.value = method
}

const handlePayment = async () => {
  if (!selectedPlan.value || !selectedPaymentMethod.value) {
    return
  }

  try {
    isLoading.value = true
    const response = await store.dispatch('createOrder', {
      planId: selectedPlan.value.id,
      paymentMethod: selectedPaymentMethod.value.id,
      amount: selectedPlan.value.price
    })

    if (selectedPaymentMethod.value.id === 'alipay') {
      window.location.href = response.payUrl
    } else {
      qrCodeUrl.value = response.qrCode
      showPaymentModal.value = false
      showQRCode.value = true
    }
  } catch (error) {
    console.error('支付失败:', error)
    showToast('支付失败，请重试', 'error')
  } finally {
    isLoading.value = false
  }
}

const closeQRCode = () => {
  showQRCode.value = false
  selectedPlan.value = null
  selectedPaymentMethod.value = null
  qrCodeUrl.value = ''
}

const handleVerification = async () => {
  if (!isAuthenticated.value) {
    showToast('请先登录', 'warning')
    router.push('/login')
    return
  }

  if (userInfo.value?.isStudent) {
    showToast('您已经是学生会员了', 'info')
    return
  }

  router.push('/verification')
}

const handleShare = async () => {
  if (!isAuthenticated.value) {
    showToast('请先登录', 'warning')
    router.push('/login')
    return
  }

  try {
    isLoading.value = true
    const { inviteLink, inviteCode } = await store.dispatch('generateInviteCode')

    const shareText = `使用我的邀请码 ${inviteCode} 注册，即可获得会员优惠！`

    if (navigator.share) {
      await navigator.share({
        title: '邀请好友加入泡泡智造',
        text: shareText,
        url: inviteLink
      })
    } else {
      await navigator.clipboard.writeText(`${shareText}\n${inviteLink}`)
      showToast('邀请链接已复制到剪贴板', 'success')
    }
  } catch (error) {
    console.error('分享失败:', error)
    showToast('分享失败，请重试', 'error')
  } finally {
    isLoading.value = false
  }
}

const handleCopyLink = async () => {
  try {
    await navigator.clipboard.writeText(inviteLink.value)
    showToast('邀请链接已复制到剪贴板', 'success')
  } catch (error) {
    showToast('复制失败，请重试', 'error')
  }
}

const fetchInviteData = async () => {
  try {
    const data = await store.dispatch('fetchInviteStats')
    inviteCount.value = data.inviteCount
    requiredInvites.value = data.requiredInvites
  } catch (error) {
    console.error('获取邀请数据失败:', error)
  }
}

// 生命周期钩子
onMounted(async () => {
  if (activeTab.value === 'invite') {
    await fetchInviteData()
  }
})

// 监听标签页变化
watch(activeTab, async (newTab) => {
  if (newTab === 'invite') {
    await fetchInviteData()
  }
})

// 添加选择方式的状态
const selectedMethod = ref('edu_email')

// 添加邀请方式的状态
const selectedInviteMethod = ref('share_link')
</script>
<style>
/* 渐变背景 */
.gradient-bg {
  background: linear-gradient(135deg, #000000, #1a1a1a);
}

/* 卡片悬浮效果 */
.hover-card {
  transition: all 0.3s ease;
}

.hover-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

/* 按钮样式 */
.btn-hover-effect {
  position: relative;
  overflow: hidden;
}

.btn-hover-effect:after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
  transform: translateX(-100%);
  transition: transform 0.6s ease;
}

.btn-hover-effect:hover:after {
  transform: translateX(0);
}
</style>