<template>
  <div>
    <HeadView />
    <div class="min-h-screen  relative overflow-hidden"
      style="padding-top: calc(var(--navbar-height) + 2rem);">
      <!-- 标题部分 -->
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold tracking-tight text-gray-900">选择会员方案</h2>
        <p class="mt-4 text-lg text-gray-600">根据您的需求选择合适的会员类型</p>
      </div>

      <!-- Tab 导航 -->
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8 relative z-20">
        <div class="flex justify-center">
          <div class="inline-flex rounded-full bg-white p-1 shadow-sm">
            <button v-for="tab in tabs" :key="tab.id" @click="handleTabClick(tab.id)" :class="[
              'px-6 py-2 text-sm font-medium rounded-full whitespace-nowrap',
              activeTab === tab.id
                ? 'gradient-bg text-white'
                : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
            ]">
              {{ tab.name }}
            </button>
          </div>
        </div>
      </div>
  
      <!-- 内容区域 -->
      <div class="relative z-20">
        <div class="max-w-7xl mx-auto px-4 py-12 sm:px-6 lg:px-8">
          <!-- 直接购买会员面板 -->
          <div v-if="activeTab === 'purchase'">
            <div class="grid grid-cols-1 gap-4 sm:grid-cols-3 sm:gap-6 mt-8">
              <div
                v-for="plan in plans"
                :key="plan.id"
                class="relative rounded-lg bg-white hover-card" 
                :class="[
                  plan.hot 
                    ? 'card-gradient-border' 
                    : 'border-2 border-gray-200'
                ]"
              >
                <!-- 热门标签 -->
                <div v-if="plan.hot"
                  class="absolute -top-3 left-1/2 transform -translate-x-1/2 text-white text-xs px-3 py-1 rounded-full gradient-bg">
                  最热门选择
                </div>

                <div class="p-6">
                  <!-- 图标 -->
                  <div class="flex justify-center mb-4">
                    <component :is="plan.icon" class="w-10 h-10 text-[#F85072]" />
                  </div>

                  <!-- 标题 -->
                  <h3 class="text-lg font-medium text-center text-gray-900 mb-2">{{ plan.name }}</h3>

                  <!-- 价格 -->
                  <div class="text-center mb-4">
                    <div class="text-gray-400 line-through text-sm">¥{{ plan.originalPrice }}</div>
                    <div class="text-2xl font-bold text-[#F85072]">¥{{ plan.price }}</div>
                    <div class="text-sm text-gray-500">{{ plan.period }}</div>
                  </div>

                  <!-- 功能列表 -->
                  <ul class="space-y-3 mb-6">
                    <li v-for="feature in plan.features" :key="feature" class="flex items-start">
                      <CheckIcon class="h-5 w-5 text-[#F85072] shrink-0 mt-0.5" />
                      <span class="ml-2 text-sm text-gray-600">{{ feature }}</span>
                    </li>
                  </ul>

                  <!-- 按钮 -->
                  <button
                    @click="openPaymentModal(plan)"
                    class="w-full px-4 py-2.5 text-sm font-medium rounded-md"
                    :class="[
                      plan.hot 
                        ? 'gradient-bg text-white' 
                        : 'border border-black'
                    ]"
                  >
                    立即开通
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- 学生认证面板 -->
          <div v-else-if="activeTab === 'student'" class="max-w-3xl mx-auto">
            <div class="text-center">
              <h2 class="text-3xl font-bold tracking-tight text-gray-900">大学生认证</h2>
              <p class="mt-4 text-lg text-gray-600">
                认证大学生身份即可获得 <span class="text-primary-600 font-medium">年会员特权</span>
              </p>
            </div>

            <div class="mt-12 bg-white rounded-lg p-8 shadow-sm">
              <!-- 认证步骤 -->
              <div class="space-y-8">
                <div class="flex items-start space-x-4">
                  <div class="flex-shrink-0">
                    <div class="h-12 w-12 rounded-full bg-primary-100 flex items-center justify-center">
                      <AcademicCapIcon class="h-6 w-6 text-primary-600" />
                    </div>
                  </div>
                  <div class="flex-1">
                    <h3 class="text-lg font-medium text-gray-900">认证方式</h3>
                    <div class="mt-4 space-y-6">
                      <!-- 学生证认证 -->
                      <div class="bg-gray-50 rounded-lg p-4">
                        <h4 class="font-medium text-gray-900">方式一：学生证认证</h4>
                        <p class="mt-2 text-sm text-gray-600">
                          上传学生证照片，包含姓名、学校、有效期等信息
                        </p>
                      </div>

                      <!-- 教育邮箱认证 -->
                      <div class="bg-gray-50 rounded-lg p-4">
                        <h4 class="font-medium text-gray-900">方式二：教育邮箱认证</h4>
                        <p class="mt-2 text-sm text-gray-600">
                          使用学校分配的教育邮箱（edu.cn）进行验证
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 认证说明 -->
                <div class="rounded-md bg-primary-50 p-4">
                  <div class="flex">
                    <InformationCircleIcon class="h-5 w-5 text-primary-400" />
                    <div class="ml-3">
                      <h3 class="text-sm font-medium text-primary-800">认证说明</h3>
                      <div class="mt-2 text-sm text-primary-700">
                        <ul class="list-disc pl-5 space-y-1">
                          <li>认证通过后即可获得年会员特权</li>
                          <li>认证有效期为一年</li>
                          <li>到期前可重新认证延长有效期</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 认证按钮 -->
                <button @click="handleVerification"
                  class="w-full flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700">
                  开始认证
                </button>
              </div>
            </div>
          </div>

          <!-- 邀请好友面板 -->
          <div v-else-if="activeTab === 'invite'" class="max-w-3xl mx-auto">
            <div class="text-center">
              <h2 class="text-3xl font-bold tracking-tight text-gray-900">邀请好友</h2>
              <p class="mt-4 text-lg text-gray-600">
                邀请好友注册使用，双方都可获得会员奖励
              </p>
            </div>

            <div class="mt-12 bg-white rounded-lg p-8 shadow-sm">
              <div class="space-y-8">
                <!-- 邀请进度 -->
                <div>
                  <div class="flex items-center justify-between text-sm font-medium text-gray-900">
                    <span>邀请进度</span>
                    <span class="text-primary-600">{{ inviteCount }}/{{ requiredInvites }} 人</span>
                  </div>
                  <div class="mt-2 relative">
                    <div class="h-2 bg-gray-100 rounded-full">
                      <div class="h-2 bg-primary-600 rounded-full transition-all duration-300"
                        :style="{ width: `${inviteProgress}%` }"></div>
                    </div>
                  </div>
                </div>

                <!-- 奖励规则 -->
                <div class="rounded-md bg-gray-50 p-6">
                  <h3 class="text-lg font-medium text-gray-900 mb-4">邀请奖励规则</h3>
                  <div class="grid grid-cols-1 gap-6 sm:grid-cols-3">
                    <!-- 月会员奖励 -->
                    <div class="text-center p-4 rounded-lg bg-white shadow-sm">
                      <div class="text-xl font-bold text-primary-600 mb-2">2人</div>
                      <div class="text-sm text-gray-600">获得1个月会员</div>
                    </div>

                    <!-- 年会员奖励 -->
                    <div class="text-center p-4 rounded-lg bg-white shadow-sm">
                      <div class="text-xl font-bold text-primary-600 mb-2">5人</div>
                      <div class="text-sm text-gray-600">获得1年会员</div>
                    </div>

                    <!-- 终身会员奖励 -->
                    <div class="text-center p-4 rounded-lg bg-white shadow-sm">
                      <div class="text-xl font-bold text-primary-600 mb-2">10人</div>
                      <div class="text-sm text-gray-600">获得终身会员</div>
                    </div>
                  </div>
                </div>

                <!-- 邀请方式 -->
                <div class="space-y-4">
                  <h3 class="text-lg font-medium text-gray-900">邀请方式</h3>
                  <!-- 复制链接 -->
                  <div class="flex items-center space-x-4">
                    <input type="text" :value="inviteLink" readonly
                      class="flex-1 min-w-0 block w-full px-3 py-2 rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm" />
                    <button @click="handleCopyLink"
                      class="inline-flex items-center px-4 py-2 border border-primary-500 text-sm font-medium rounded-md text-primary-600 bg-white hover:bg-primary-50">
                      复制链接
                    </button>
                  </div>

                  <!-- 分享按钮 -->
                  <button @click="handleShare"
                    class="w-full flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700">
                    分享给好友
                  </button>
                </div>

                <!-- 邀请记录 -->
                <div v-if="inviteHistory.length > 0">
                  <h3 class="text-lg font-medium text-gray-900 mb-4">邀请记录</h3>
                  <div class="space-y-3">
                    <div v-for="record in inviteHistory" :key="record.id"
                      class="flex items-center justify-between bg-gray-50 p-3 rounded-lg">
                      <div class="flex items-center">
                        <img :src="record.avatar" alt="" class="h-8 w-8 rounded-full">
                        <span class="ml-3 text-sm text-gray-900">{{ record.name }}</span>
                      </div>
                      <span class="text-sm text-gray-500">{{ record.date }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      <!-- 会员特权展示 -->
<div class="mb-12">
  <h3 class="text-lg font-medium text-center text-gray-900 mb-8">会员特权</h3>
  <div class="max-w-4xl mx-auto grid grid-cols-1 sm:grid-cols-2 gap-6">
    <div v-for="feature in memberFeatures" 
         :key="feature.id" 
         class="flex items-start space-x-4 bg-white rounded-lg p-6 hover:shadow-lg transition-shadow duration-300">
      <!-- 图标 -->
      <div class="flex-shrink-0">
        <component 
          :is="feature.icon" 
          class="w-8 h-8 text-[#F85072]"
        />
      </div>
      <!-- 文字内容 -->
      <div>
        <h4 class="text-gray-900 font-medium mb-1">{{ feature.name }}</h4>
        <p class="text-sm text-gray-500 leading-relaxed">{{ feature.description }}</p>
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
  InformationCircleIcon
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
    name: '月会员',
    icon: CalendarIcon,
    price: '19.9',
    originalPrice: '39.9',
    period: '月'
  },
  {
    id: 'yearly',
    name: '年会员',
    icon: StarIcon,
    price: '99',
    originalPrice: '199',
    period: '年',
    hot: true
  },
  {
    id: 'lifetime',
    name: '终身会员',
    icon: SparklesIcon,
    price: '299',
    originalPrice: '599',
    period: '终身'
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
</script>
<style>
/* 渐变背景 */
.gradient-bg {
  background: linear-gradient(135deg, #F85072, #FF9446);
}

/* 卡片基础样式 */
.hover-card {
  position: relative;
  background: white;
  border: 2px solid #e5e7eb; /* 默认边框颜色 */
  height: 100%;
}

/* 热门卡片默认样式 */
.card-gradient-border {
  border: 2px solid transparent;
  background: linear-gradient(white, white) padding-box,
              linear-gradient(135deg, #F85072, #FF9446) border-box;
}

/* hover 效果 */
.hover-card:hover {
  border: 2px solid transparent;
  background: linear-gradient(white, white) padding-box,
              linear-gradient(135deg, #F85072, #FF9446) border-box;
}

/* 按钮 hover 效果 */
.hover-card:hover button {
  background: linear-gradient(135deg, #F85072, #FF9446);
  color: white;
  border: none;
}

/* 按钮基础样式 */
.hover-card button {
  transition: background-color 0.3s ease, color 0.3s ease;
}

</style>