<template>
  <div class="space-y-8">
    <!-- 会员状态卡片 -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <div class="px-6 py-8 bg-gradient-to-br from-[#1A56DB] via-blue-600 to-blue-500 relative overflow-hidden">
        <!-- 装饰背景 -->
        <div class="absolute inset-0">
          <div class="absolute right-0 top-0 w-64 h-64 bg-white/10 rounded-full blur-3xl transform translate-x-1/2 -translate-y-1/2"></div>
          <div class="absolute left-0 bottom-0 w-32 h-32 bg-white/5 rounded-full blur-2xl"></div>
        </div>
        <!-- 内容 -->
        <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between relative space-y-4 lg:space-y-0">
          <div class="text-white">
            <h3 class="text-2xl font-bold tracking-tight">{{ vipTypeText }}</h3>
            <p class="mt-2 text-white/80 font-medium">{{ vipExpireText }}</p>
          </div>
          <button 
            @click="handleVipButton"
            class="w-full lg:w-auto px-6 py-2.5 bg-white/10 backdrop-blur-sm text-white border border-white/20 rounded-full text-sm font-medium hover:bg-white/20 transition-all duration-300"
          >
            {{ vipButtonText }}
          </button>
        </div>
      </div>
      
      <!-- 会员权益 -->
      <div class="px-6 py-4">
        <h4 class="text-base font-medium text-gray-900 mb-4">专属会员权益</h4>
        <div class="grid grid-cols-1 lg:grid-cols-5 gap-4 lg:gap-6">
          <div v-for="benefit in memberBenefits" :key="benefit.key" 
            class="flex lg:flex-col items-center lg:text-center p-3 lg:p-0 bg-gray-50/50 lg:bg-transparent rounded-lg lg:rounded-none"
          >
            <div class="w-10 lg:w-12 h-10 lg:h-12 rounded-full bg-gradient-to-br from-blue-50 to-blue-100/50 flex items-center justify-center">
              <component :is="benefit.icon" class="w-6 h-6 text-[#1A56DB]" />
            </div>
            <div class="ml-3 lg:ml-0 lg:mt-3">
              <div class="text-sm font-medium text-gray-900">{{ benefit.name }}</div>
              <div class="text-xs text-gray-600 mt-1">{{ benefit.desc }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 积分信息 -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <!-- 积分和等级概览 -->
      <div class="relative px-4 lg:px-8 py-6 lg:py-10 overflow-hidden bg-gradient-to-br from-gray-50 to-white border-b border-gray-100">
        <!-- 装饰背景 -->
        <div class="absolute inset-0 opacity-10">
          <div class="absolute right-0 top-0 w-64 h-64 bg-gradient-to-br from-violet-100/20 to-purple-100/20 rounded-full transform translate-x-1/3 -translate-y-1/3"></div>
        </div>
        
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
          <div>
            <div class="flex items-center">
              <h3 class="text-lg lg:text-xl font-semibold text-gray-900">我的积分</h3>
            </div>
            <div class="mt-3">
              <span class="text-4xl lg:text-5xl font-bold bg-gradient-to-r from-[#1A56DB] to-blue-500 bg-clip-text text-transparent">{{ pointsInfo.balance || 0 }}</span>
              <span class="text-sm text-gray-600 ml-1">积分</span>
            </div>
          </div>
          
          <!-- 等级展示 -->
          <div class="text-right">
            <div class="inline-flex items-center px-4 py-2 rounded-full bg-blue-50 border border-blue-100">
              <StarIcon class="w-5 h-5 text-[#1A56DB] mr-2" />
              <span class="text-base font-semibold text-[#1A56DB]">Lv.{{ pointsInfo.level || 1 }}</span>
            </div>
            <div class="mt-2 text-sm font-medium text-gray-600">{{ getLevelTitle(pointsInfo.level) }}</div>
          </div>
        </div>
        
        <!-- 等级进度条 -->
        <div class="mt-6">
          <div class="flex items-center justify-between mb-2">
            <div class="text-sm text-gray-700">
              距离 Lv.{{ Math.min((pointsInfo.level || 1) + 1, 5) }} 还需 
              <span class="font-medium text-violet-600">{{ getNextLevelPoints(pointsInfo.level, pointsInfo.balance) }}</span> 分
            </div>
            <div class="text-sm text-gray-600">
              {{ pointsInfo.balance || 0 }}/{{ getLevelThreshold(pointsInfo.level) }}
            </div>
          </div>
          <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
            <div 
              class="h-full bg-gradient-to-r from-[#1A56DB] to-blue-500 transition-all duration-500"
              :style="{ width: `${getLevelProgress(pointsInfo.level, pointsInfo.balance)}%` }"
            ></div>
          </div>
        </div>

        <!-- 签到信息 -->
        <div class="mt-6 flex items-center">
          <div class="flex flex-wrap lg:flex-nowrap items-center space-x-2 lg:space-x-3 px-3 lg:px-4 py-2 bg-blue-50 rounded-lg border border-blue-100">
            <CalendarDaysIcon class="w-5 h-5 text-[#1A56DB]" />
            <div>
              <div class="text-sm font-medium text-blue-900">连续签到</div>
              <div class="flex items-baseline space-x-1">
                <span class="text-xl font-bold text-[#1A56DB]">{{ pointsInfo.sign_in_days || 0 }}</span>
                <span class="text-sm text-[#1A56DB]">天</span>
              </div>
            </div>
            <button 
              v-if="canSignIn"
              @click="handleSignIn"
              class="mt-2 lg:mt-0 w-full lg:w-auto lg:ml-4 px-3 py-1.5 bg-blue-100 hover:bg-blue-200 text-[#1A56DB] text-sm font-medium rounded-full transition-colors"
            >
              立即签到
            </button>
            <div v-else class="mt-2 lg:mt-0 w-full lg:w-auto lg:ml-4 text-center lg:text-left text-sm text-violet-600">
              今日已签到
            </div>
          </div>
          
          <div class="hidden lg:block ml-auto text-sm text-gray-500">
            {{ getSignInTip() }}
          </div>
        </div>
      </div>

      <!-- 积分明细 -->
      <div class="px-4 lg:px-6 py-4">
        <div class="flex items-center justify-between mb-3">
          <h4 class="text-base font-medium text-gray-900">积分明细</h4>
          <div class="flex space-x-1 lg:space-x-2">
            <button 
              v-for="filter in pointsFilters" 
              :key="filter.value"
              @click="currentFilter = filter.value"
              class="px-1.5 lg:px-2 py-1 text-xs rounded-full transition-colors whitespace-nowrap"
              :class="[
                currentFilter === filter.value 
                  ? 'bg-gray-100 text-gray-800' 
                  : 'text-gray-500 hover:text-gray-700'
              ]"
            >
              {{ filter.label }}
            </button>
          </div>
        </div>
        <div class="divide-y divide-gray-100 max-h-[400px] overflow-y-auto">
          <div v-if="pointsRecords.length === 0" class="py-8 text-center text-gray-500">
            暂无积分记录
          </div>
          <div 
            v-else
            v-for="record in filteredRecords" 
            :key="record.id" 
            class="py-3 lg:py-3.5 flex items-center justify-between hover:bg-gray-50 transition-colors px-2"
          >
            <div>
              <div class="text-xs lg:text-sm font-medium text-gray-900">{{ record.description }}</div>
              <div class="text-[10px] lg:text-xs text-gray-500 mt-0.5">
                {{ formatDate(record.created_at, window.innerWidth < 640 ? 'MM-DD HH:mm' : 'YYYY-MM-DD HH:mm') }}
              </div>
            </div>
            <div :class="[
              'text-xs lg:text-sm font-medium ml-2 lg:ml-4',
              record.points > 0 ? 'text-gray-800' : 'text-red-600'
            ]">
              {{ record.points > 0 ? '+' : '' }}{{ record.points }}
            </div>
          </div>
        </div>
        <!-- 加载更多按钮 -->
        <div v-if="hasMore" class="mt-4 text-center">
          <button 
            @click="loadMore"
            class="text-xs lg:text-sm text-gray-500 hover:text-gray-700 px-3 lg:px-4 py-1.5 lg:py-2 rounded-full hover:bg-gray-100 transition-colors"
            :disabled="loading"
          >
            {{ loading ? '加载中...' : '加载更多' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 积分和等级说明区域 -->
    <div class="space-y-4">
      <div class="space-y-8">
        <!-- 积分获取规则 -->
        <div class="bg-white rounded-lg shadow overflow-hidden">
          <div class="px-6 py-4 bg-gray-50 border-b border-gray-100">
            <h3 class="text-base font-medium text-gray-900">积分获取规则</h3>
            <p class="mt-1 text-sm text-gray-500">参与社区互动，赚取积分升级</p>
          </div>
          <div class="p-6">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 lg:gap-8 mt-6 lg:mt-8">
              <!-- 内容创作 -->
              <div class="p-4 lg:p-5 bg-gradient-to-br from-gray-50 to-white rounded-lg border border-gray-100/80 shadow-sm">
                <div class="flex items-center space-x-3 mb-4">
                  <div class="w-7 lg:w-8 h-7 lg:h-8 rounded-full bg-violet-100 flex items-center justify-center">
                    <PencilSquareIcon class="w-4 h-4 text-violet-600" />
                  </div>
                  <span class="text-sm lg:text-base font-semibold text-gray-900">内容创作</span>
                </div>
                <ul class="space-y-3">
                  <li class="flex items-center justify-between text-sm">
                    <span class="text-gray-600">发布原创文章</span>
                    <span class="font-medium text-violet-600 bg-violet-50 px-3 py-1 rounded-full">+30分</span>
                  </li>
                  <li class="flex items-center justify-between text-sm">
                    <span class="text-gray-600">发布作品集</span>
                    <span class="font-medium text-gray-900 bg-gray-100 px-2 py-0.5 rounded">+35分</span>
                  </li>
                  <li class="flex items-center justify-between text-sm">
                    <span class="text-gray-600">发布问答</span>
                    <span class="font-medium text-gray-900 bg-gray-100 px-2 py-0.5 rounded">+20分</span>
                  </li>
                  <li class="flex items-center justify-between text-sm">
                    <span class="text-gray-600">发布话题</span>
                    <span class="font-medium text-gray-900 bg-gray-100 px-2 py-0.5 rounded">+20分</span>
                  </li>
                </ul>
              </div>
              
              <!-- 社区互动 -->
              <div class="p-4 lg:p-5 bg-gradient-to-br from-gray-50 to-white rounded-lg border border-gray-100/80 shadow-sm">
                <div class="flex items-center space-x-3 mb-4">
                  <div class="w-7 lg:w-8 h-7 lg:h-8 rounded-full bg-blue-100 flex items-center justify-center">
                    <ChatBubbleLeftRightIcon class="w-4 h-4 text-blue-600" />
                  </div>
                  <span class="text-sm lg:text-base font-semibold text-gray-900">社区互动</span>
                </div>
                <ul class="space-y-3">
                  <li class="flex items-center justify-between text-sm">
                    <span class="text-gray-600">回答问题</span>
                    <span class="font-medium text-blue-600 bg-blue-50 px-3 py-1 rounded-full">+8分</span>
                  </li>
                  <li class="flex items-center justify-between text-sm">
                    <span class="text-gray-600">评论文章/作品</span>
                    <span class="font-medium text-gray-900 bg-gray-100 px-2 py-0.5 rounded">+3分</span>
                  </li>
                  <li class="flex items-center justify-between text-sm">
                    <span class="text-gray-600">回答被采纳</span>
                    <span class="font-medium text-gray-900 bg-gray-100 px-2 py-0.5 rounded">悬赏分</span>
                  </li>
                </ul>
              </div>
              
              <!-- 每日签到 -->
              <div class="p-4 lg:p-5 bg-gradient-to-br from-gray-50 to-white rounded-lg border border-gray-100/80 shadow-sm">
                <div class="flex items-center space-x-3 mb-4">
                  <div class="w-7 lg:w-8 h-7 lg:h-8 rounded-full bg-amber-100 flex items-center justify-center">
                    <GiftIcon class="w-4 h-4 text-amber-600" />
                  </div>
                  <span class="text-sm lg:text-base font-semibold text-gray-900">每日签到</span>
                </div>
                <ul class="space-y-3">
                  <li class="flex items-center justify-between text-sm">
                    <span class="text-gray-600">每日签到</span>
                    <span class="font-medium text-amber-600 bg-amber-50 px-3 py-1 rounded-full">+3分</span>
                  </li>
                  <li class="flex items-center justify-between text-sm">
                    <span class="text-gray-600">连续签到7天</span>
                    <span class="font-medium text-gray-900 bg-gray-100 px-2 py-0.5 rounded">+10分</span>
                  </li>
                  <li class="flex items-center justify-between text-sm">
                    <span class="text-gray-600">连续签到30天</span>
                    <span class="font-medium text-gray-900 bg-gray-100 px-2 py-0.5 rounded">+50分</span>
                  </li>
                </ul>
              </div>
              
              <!-- 额外奖励 -->
              <div class="p-4 lg:p-5 bg-gradient-to-br from-gray-50 to-white rounded-lg border border-gray-100/80 shadow-sm">
                <div class="flex items-center space-x-3 mb-4">
                  <div class="w-7 lg:w-8 h-7 lg:h-8 rounded-full bg-emerald-100 flex items-center justify-center">
                    <StarIcon class="w-4 h-4 text-emerald-600" />
                  </div>
                  <span class="text-sm lg:text-base font-semibold text-gray-900">额外奖励</span>
                </div>
                <ul class="space-y-3">
                  <li class="flex items-center justify-between text-sm">
                    <div class="flex items-center">
                      <span class="text-gray-600">会员双倍积分</span>
                      <span class="ml-1.5 text-xs px-1.5 py-0.5 rounded bg-amber-100 text-amber-600">VIP</span>
                    </div>
                    <span class="font-medium text-emerald-600 bg-emerald-50 px-3 py-1 rounded-full">×2</span>
                  </li>
                  <li class="flex items-center justify-between text-sm">
                    <span class="text-gray-600">内容被收藏</span>
                    <span class="font-medium text-emerald-600 bg-emerald-50 px-3 py-1 rounded-full">+2分/次</span>
                  </li>
                  <li class="flex items-center justify-between text-sm">
                    <span class="text-gray-600">内容被推荐</span>
                    <span class="font-medium text-emerald-600 bg-emerald-50 px-3 py-1 rounded-full">+100分</span>
                  </li>
                  <li class="text-xs text-gray-500 mt-2 pl-1">
                    注：会员用户参与所有积分活动可获得双倍积分奖励
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 等级特权说明 -->
        <div class="bg-white rounded-lg shadow overflow-hidden">
          <div class="px-6 py-4 bg-gray-50 border-b border-gray-100">
            <h3 class="text-lg font-semibold text-gray-900">会员等级特权</h3>
            <p class="mt-1 text-sm text-gray-600">解锁更多等级，享受更多尊享权益</p>
          </div>
          <div class="p-6">
            <div class="space-y-4 lg:space-y-8 mt-6 lg:mt-8">
              <div v-for="level in 5" :key="level" 
                class="p-4 lg:p-5 bg-gradient-to-br from-gray-50 to-white rounded-lg border transition-all duration-300 hover:shadow-md"
                :class="[
                  level <= pointsInfo.level 
                    ? 'border-blue-200' 
                    : 'border-gray-100',
                ]"
              >
                <div class="flex flex-col lg:flex-row lg:items-center justify-between mb-4 space-y-2 lg:space-y-0">
                  <div class="flex items-center space-x-3">
                    <div class="relative">
                      <div class="w-8 lg:w-10 h-8 lg:h-10 rounded-full flex items-center justify-center"
                        :class="[
                          level <= pointsInfo.level 
                            ? 'bg-gradient-to-br from-[#1A56DB] to-blue-500 text-white' 
                            : 'bg-gray-100 text-gray-400'
                        ]"
                      >
                        <span class="text-lg font-bold">{{ level }}</span>
                      </div>
                      <div v-if="level <= pointsInfo.level" 
                        class="absolute -right-1 -bottom-1 w-4 h-4 bg-green-500 rounded-full border-2 border-white flex items-center justify-center"
                      >
                        <CheckIcon class="w-2.5 h-2.5 text-white" />
                      </div>
                    </div>
                    <div>
                      <div class="text-base lg:text-lg font-semibold text-gray-900">{{ getLevelTitle(level) }}</div>
                      <div class="text-sm text-gray-500">{{ getLevelRange(level) }}</div>
                    </div>
                  </div>
                  <div class="flex items-center space-x-2">
                    <div class="text-xs px-2 py-0.5 rounded-full"
                      :class="[
                        level <= pointsInfo.level 
                          ? 'bg-green-100 text-green-600' 
                          : 'bg-gray-100 text-gray-500'
                      ]"
                    >
                      {{ level <= pointsInfo.level ? '已解锁' : '未解锁' }}
                    </div>
                  </div>
                </div>
                <div class="mt-4 grid grid-cols-1 lg:grid-cols-2 gap-3 lg:gap-4">
                  <div v-for="privilege in getLevelPrivileges(level)" :key="privilege"
                    class="flex items-start space-x-2">
                    <CheckCircleIcon class="w-5 h-5 mt-0.5 flex-shrink-0" />
                    <span class="text-xs lg:text-sm">{{ privilege }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 订单记录 -->
    <div class="space-y-4">
      <h2 class="text-lg font-medium text-gray-900">订单记录</h2>
      <div class="bg-white rounded-lg shadow overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-medium text-gray-900">会员订单</h3>
            <button 
              class="text-sm text-gray-500 hover:text-gray-700"
              @click="router.push('/orders')"
            >
              查看全部
            </button>
          </div>
        </div>
        <div class="divide-y divide-gray-200">
          <div v-if="orders.length === 0" class="py-8 text-center text-gray-500">
            暂无订单记录
          </div>
          <div v-else v-for="order in orders" :key="order.order_no" class="px-6 py-4">
            <div class="flex items-center justify-between">
              <div>
                <div class="text-sm text-gray-500">订单号：{{ order.order_no }}</div>
                <div class="mt-1 text-base font-medium text-gray-900">{{ order.vip_type_display }}</div>
              </div>
              <div class="text-right">
                <div class="text-lg font-medium text-gray-900">¥{{ order.amount }}</div>
                <div class="mt-1 text-sm" :class="{
                  'text-green-500': order.status === 'paid',
                  'text-gray-500': order.status === 'pending',
                  'text-red-500': ['cancelled', 'refunded'].includes(order.status)
                }">
                  {{ order.status_display }}
                </div>
              </div>
            </div>
            <div class="mt-2 text-sm text-gray-500">
              {{ formatDate(order.created_at) }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/account'
import { 
  SparklesIcon, CloudArrowUpIcon, 
  ChatBubbleLeftRightIcon, QuestionMarkCircleIcon, CheckCircleIcon, 
  GiftIcon, ClipboardDocumentListIcon, StarIcon, PencilSquareIcon, 
  CalendarDaysIcon,
  DocumentTextIcon,
  CloudIcon,
  DocumentChartBarIcon,
  UserGroupIcon,
  CheckIcon,
  DocumentIcon,
  BoltIcon,
  HeartIcon
} from '@heroicons/vue/24/outline'
import { formatDate, formatRemainingTime } from '@/utils/date'

const router = useRouter()
const accountStore = useAccountStore()

// 会员权益
const memberBenefits = [
  { 
    key: 'template', 
    name: '会员模板', 
    desc: '进阶模板无限用',
    icon: DocumentIcon
  },
  { 
    key: 'points', 
    name: '双倍积分', 
    desc: '所有活动双倍奖',
    icon: StarIcon
  },
  { 
    key: 'ai', 
    name: 'AI助手', 
    desc: '智能档案优化',
    icon: BoltIcon
  },
  { 
    key: 'storage', 
    name: '超大空间', 
    desc: '100G专属云盘',
    icon: CloudIcon
  },
  {
    key: 'support',
    name: '专属客服',
    desc: '7×24小时服务',
    icon: HeartIcon
  }
]

// 积分信息
const pointsInfo = ref({
  balance: 0,
  total_earned: 0,
  total_spent: 0,
  level: 1
})

// 订单记录
const orders = ref([])

// 积分记录相关
const currentFilter = ref('all')
const pointsRecords = ref([])
const currentPage = ref(1)
const hasMore = ref(true)
const loading = ref(false)

const pointsFilters = [
  { label: '全部', value: 'all' },
  { label: '获得', value: 'earned' },
  { label: '使用', value: 'spent' }
]

// 过滤后的记录
const filteredRecords = computed(() => {
  if (currentFilter.value === 'all') return pointsRecords.value
  
  return pointsRecords.value.filter(record => 
    currentFilter.value === 'earned' 
      ? record.points > 0 
      : record.points < 0
  )
})

// 获取积分信息
const fetchPointsInfo = async () => {
  try {
    const response = await membership.getPointsInfo()
    if (response?.data?.code === 200) {
      pointsInfo.value = response.data.data
    }
  } catch (error) {
    console.error('获取积分信息失败:', error)
  }
}

// 获取订单记录
const fetchOrders = async () => {
  try {
    const response = await membership.getOrders()
    if (response?.data?.code === 200) {
      orders.value = response.data.data
    }
  } catch (error) {
    console.error('获取订单记录失败:', error)
  }
}

// 获取积分记录
const fetchPointsRecords = async (page = 1) => {
  if (loading.value) return
  
  loading.value = true
  try {
    const response = await membership.getPointsRecords({ 
      page,
      page_size: 10
    })
    if (response?.data?.code === 200) {
      const { records, has_more } = response.data.data
      if (page === 1) {
        pointsRecords.value = records
      } else {
        pointsRecords.value.push(...records)
      }
      hasMore.value = has_more
      currentPage.value = page
    }
  } catch (error) {
    console.error('获取积分记录失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载更多
const loadMore = () => {
  fetchPointsRecords(currentPage.value + 1)
}

// 监听筛选变化
watch(currentFilter, () => {
  // 切换筛选时重置到第一页
  currentPage.value = 1
  fetchPointsRecords(1)
})

// 会员类型文本
const vipTypeText = computed(() => {
  const userInfo = accountStore.userInfo
  if (!userInfo?.is_vip) return '普通用户'
  return userInfo.vip_status
})

// 会员到期文本
const vipExpireText = computed(() => {
  const userInfo = accountStore.userInfo
  if (!userInfo?.is_vip) return '开通会员享专属权益'
  if (userInfo.vip_type === 'lifetime') return '终身会员'
  if (userInfo.vip_expire_time) {
    const expireDate = new Date(userInfo.vip_expire_time)
    const now = new Date()
    const diffDays = Math.floor((expireDate - now) / (1000 * 60 * 60 * 24))
    return diffDays > 0 ? `剩余 ${diffDays} 天` : '已过期'
  }
  return ''
})

// 会员按钮文本和处理
const vipButtonText = computed(() => {
  const userInfo = accountStore.userInfo
  if (!userInfo?.is_vip) return '立即开通'
  if (userInfo.vip_type === 'lifetime') return '查看权益'
  return '立即续费'
})

const handleVipButton = () => {
  const userInfo = accountStore.userInfo
  if (!userInfo?.is_vip) {
    router.push('/pro')
  } else if (userInfo.vip_type === 'lifetime') {
    // 显示会员权益详情
  } else {
    router.push('/pro')
  }
}

// 获取等级称号
const getLevelTitle = (level) => {
  const levelConfig = {
    1: { title: '初级会员', range: '0-1000积分' },
    2: { title: '进阶会员', range: '1001-3000积分' },
    3: { title: '高级会员', range: '3001-8000积分' },
    4: { title: '精英会员', range: '8001-15000积分' },
    5: { title: '至尊会员', range: '15000+积分' }
  }
  return levelConfig[level]?.title || '普通会员'
}

const showTooltip = ref(false)

// 提示框位置
const tooltipPosition = ref({ x: 0, y: 0 })

// 计算提示框位置
const calculateTooltipPosition = (event) => {
  const iconRect = event.target.getBoundingClientRect()
  const tooltipWidth = 320 // w-80 = 20rem = 320px
  const tooltipHeight = 480 // 预估高度
  
  // 水平居中于图标
  const x = iconRect.left + (iconRect.width / 2) - (tooltipWidth / 2)
  // 位于图标上方，留出足够空间
  const y = iconRect.top - tooltipHeight - 10
  
  // 确保不超出视窗边界
  const adjustedX = Math.max(16, Math.min(x, window.innerWidth - tooltipWidth - 16))
  const adjustedY = Math.max(16, y)
  
  tooltipPosition.value = {
    x: adjustedX,
    y: adjustedY
  }
}

// 修改鼠标进入事件处理
const handleMouseEnter = (event) => {
  calculateTooltipPosition(event)
  showTooltip.value = true
}

// 获取下一等级所需积分
const getNextLevelPoints = (currentLevel, currentPoints) => {
  const levelThresholds = {
    1: 1000,
    2: 3000,
    3: 8000,
    4: 15000,
    5: Infinity
  }
  
  if (currentLevel >= 5) return 0
  
  const nextLevelThreshold = levelThresholds[currentLevel + 1]
  return nextLevelThreshold - currentPoints
}

// 获取当前等级进度
const getLevelProgress = (currentLevel, currentPoints) => {
  const levelRanges = {
    1: { min: 0, max: 1000 },
    2: { min: 1001, max: 3000 },
    3: { min: 3001, max: 8000 },
    4: { min: 8001, max: 15000 },
    5: { min: 15001, max: 15001 } // 最高等级
  }
  
  const range = levelRanges[currentLevel]
  if (!range) return 0
  
  const total = range.max - range.min
  const current = currentPoints - range.min
  return Math.min(100, Math.max(0, (current / total) * 100))
}

// 是否可以签到
const canSignIn = computed(() => !pointsInfo.value.signed_today)

// 处理签到
const handleSignIn = async () => {
  if (!canSignIn.value) return
  
  try {
    const response = await membership.signIn()
    if (response?.data?.code === 200) {
      await fetchPointsInfo() // 刷新积分信息
      showToast('签到成功', 'success')
    }
  } catch (error) {
    console.error('签到失败:', error)
    showToast('签到失败，请重试', 'error')
  }
}

// 获取等级阈值
const getLevelThreshold = (level) => {
  const thresholds = {
    1: 1000,
    2: 3000,
    3: 8000,
    4: 15000,
    5: Infinity
  }
  return thresholds[level] || 1000
}

// 获取签到提示
const getSignInTip = () => {
  if (!pointsInfo.value.signed_today) {
    return '今日签到可获得3积分'
  }
  if (pointsInfo.value.sign_in_days % 7 === 6) {
    return '明日签到可获得额外10积分奖励'
  }
  if (pointsInfo.value.sign_in_days % 30 === 29) {
    return '明日签到可获得额外50积分奖励'
  }
  return `已连续签到 ${pointsInfo.value.sign_in_days} 天`
}

// 获取等级范围说明
const getLevelRange = (level) => {
  const ranges = {
    1: '0-1,000积分',
    2: '1,001-3,000积分',
    3: '3,001-8,000积分',
    4: '8,001-15,000积分',
    5: '15,000+积分'
  }
  return ranges[level] || ''
}

// 获取等级特权说明
const getLevelPrivileges = (level) => {
  const privileges = {
    1: [
      '发布简历动态',
      '参与社区讨论',
      '基础积分奖励',
      '个人主页展示'
    ],
    2: [
      '简历曝光加成',
      '简历动态置顶',
      '积分加速成长',
      '社区徽章展示'
    ],
    3: [
      '专属等级标识',
      '简历优先推荐',
      '开通打赏功能',
      '高级积分特权'
    ],
    4: [
      '内容免审发布',
      '简历优先投递',
      '打赏特权加成',
      '社区荣誉称号'
    ],
    5: [
      '资深用户认证',
      '内容审核特权',
      '打赏收益加成',
      '专属成就徽章'
    ]
  }
  return privileges[level] || []
}

onMounted(async () => {
  await Promise.all([
    fetchPointsInfo(),
    fetchOrders(),
    fetchPointsRecords()
  ])
  
  // 添加窗口大小变化监听
  window.addEventListener('resize', () => {
    if (showTooltip.value) {
      showTooltip.value = false
    }
  })
})

// 在 onUnmounted 中清理
onUnmounted(() => {
  window.removeEventListener('resize', () => {
    if (showTooltip.value) {
      showTooltip.value = false
    }
  })
})
</script> 