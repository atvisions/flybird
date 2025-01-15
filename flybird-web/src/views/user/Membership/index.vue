<template>
  <div class="space-y-8">
    <!-- 会员状态卡片 -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <div class="px-6 py-8 bg-gradient-to-br from-[#1A56DB] via-blue-600 to-blue-500 relative overflow-hidden">
        <!-- 装饰背景 -->
        <div class="absolute inset-0">
          <div class="absolute right-0 top-0 w-64 h-64 bg-white bg-opacity-10 rounded-full blur-3xl transform -translate-y-1/2 translate-x-1/2"></div>
          <div class="absolute left-0 bottom-0 w-32 h-32 bg-white bg-opacity-5 rounded-full blur-2xl"></div>
        </div>
        <!-- 内容 -->
        <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between relative space-y-4 lg:space-y-0">
          <div class="text-white">
            <h3 class="text-2xl font-bold tracking-tight">{{ vipTypeText }}</h3>
            <p class="mt-2 text-white text-opacity-80 font-medium">{{ vipExpireText }}</p>
          </div>
          <button 
            @click="handleVipButton"
            class="w-full lg:w-auto px-6 py-2.5 bg-white bg-opacity-10 backdrop-blur-sm text-white border border-white border-opacity-20 rounded-full text-sm font-medium hover:bg-opacity-20 transition-all duration-300"
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
            class="flex lg:flex-col items-center lg:text-center p-3 lg:p-0 bg-gray-50 bg-opacity-50 lg:bg-transparent rounded-lg lg:rounded-none"
          >
            <div class="w-10 lg:w-12 h-10 lg:h-12 rounded-full bg-gradient-to-br from-blue-50 to-blue-100 bg-opacity-50 flex items-center justify-center">
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
      <div class="px-6 py-8 relative">
        <!-- 装饰背景 -->
        <div class="absolute inset-0 opacity-10">
          <div class="absolute right-0 top-0 w-64 h-64 bg-gradient-to-br from-violet-100 to-purple-100 bg-opacity-20 rounded-full transform -translate-y-1/3 translate-x-1/3"></div>
        </div>
        
        <!-- 积分和等级概览 -->
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
          <div>
            <h3 class="text-lg lg:text-xl font-semibold text-gray-900">我的积分</h3>
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
                <span class="text-xl font-bold text-[#1A56DB]">{{ signInInfo.sign_in_days || 0 }}</span>
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
          <div v-if="!pointsRecords?.length" class="py-8 text-center text-gray-500">
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
                {{ formatDate(record.created_at, dateFormat) }}
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

    <!-- Tab 导航 -->
    <div class="bg-white rounded-lg shadow">
      <!-- Tab 头部 -->
      <div class="border-b border-gray-200">
        <nav class="-mb-px flex" aria-label="Tabs">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            @click="currentTab = tab.key"
            :class="[
              currentTab === tab.key
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
              'w-1/3 py-4 px-1 text-center border-b-2 font-medium text-sm transition-colors duration-200'
            ]"
          >
            {{ tab.name }}
          </button>
        </nav>
      </div>

      <!-- Tab 内容 -->
      <div class="p-6">
        <!-- 积分规则 -->
        <div v-if="currentTab === 'points'" class="space-y-6">
          <h3 class="text-lg font-medium text-gray-900">积分获取规则</h3>
          <div class="space-y-3">
            <div class="flex items-center p-4 bg-white border rounded-lg transition-all hover:shadow-sm border-blue-100">
              <div class="w-10 h-10 rounded-lg flex items-center justify-center bg-blue-50">
                <CalendarDaysIcon class="w-5 h-5 text-blue-500" />
              </div>
              <div class="ml-4 flex-1">
                <div class="flex items-center justify-between">
                  <div class="font-medium text-gray-900">每日签到</div>
                  <button
                    @click="handleSignIn"
                    :disabled="!canSignIn"
                    class="px-4 py-1.5 rounded-full text-sm font-medium transition-colors cursor-pointer"
                    :class="[
                      canSignIn 
                        ? 'bg-primary-600 text-white hover:bg-primary-700 hover:shadow-sm active:bg-primary-800' 
                        : 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    ]"
                  >
                    {{ canSignIn ? '立即签到' : '今日已签到' }}
                  </button>
                </div>
                <div class="mt-1 text-sm text-gray-500">
                  已连续签到 {{ signInInfo.sign_in_days || 0 }} 天
                  <template v-if="signInInfo.nextReward">
                    <span class="ml-2">
                      再签到 {{ signInInfo.nextReward.days }} 天可获得 
                      {{ signInInfo.nextReward.points }} 积分奖励
                    </span>
                  </template>
                </div>
              </div>
            </div>
            <div v-for="rule in pointRules.slice(1)" :key="rule.action" 
              class="flex items-center p-4 bg-white border rounded-lg transition-all hover:shadow-sm"
              :class="rule.borderColor"
            >
              <div :class="[
                'w-10 h-10 rounded-lg flex items-center justify-center',
                rule.bgColor
              ]">
                <component :is="rule.icon" class="w-5 h-5" :class="rule.iconColor" />
              </div>
              <div class="ml-4 flex-1">
                <div class="flex items-center justify-between">
                  <div class="font-medium text-gray-900">{{ rule.action }}</div>
                  <div class="text-sm font-medium" :class="rule.textColor">{{ rule.points }}</div>
                </div>
                <div class="mt-1 text-sm text-gray-500">{{ rule.description }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 等级权益 -->
        <div v-if="currentTab === 'privileges'" class="space-y-6">
          <h3 class="text-lg font-medium text-gray-900">等级特权</h3>
          <div class="space-y-6">
            <div v-for="level in 5" :key="level" 
              class="bg-white border rounded-lg overflow-hidden transition-all hover:shadow-sm"
              :class="[
                level === pointsInfo.level ? 'border-primary-500' : 'border-gray-100',
              ]"
            >
              <!-- 等级头部 -->
              <div class="px-6 py-4 flex items-center justify-between border-b border-gray-100"
                :class="level === pointsInfo.level ? 'bg-primary-50' : 'bg-gray-50'"
              >
                <div class="flex items-center space-x-3">
                  <div class="w-10 h-10 rounded-lg flex items-center justify-center"
                    :class="level === pointsInfo.level ? 'bg-primary-100' : 'bg-white'"
                  >
                    <TrophyIcon 
                      class="w-6 h-6"
                      :class="level === pointsInfo.level ? 'text-primary-500' : 'text-gray-400'"
                    />
                  </div>
                  <div>
                    <div class="flex items-center">
                      <span class="text-lg font-semibold text-gray-900">
                        Lv.{{ level }} {{ getLevelTitle(level) }}
                      </span>
                      <span v-if="level === pointsInfo.level"
                        class="ml-2 px-2 py-0.5 text-xs font-medium text-primary-600 bg-primary-100 rounded-full"
                      >
                        当前等级
                      </span>
                    </div>
                    <div class="text-sm text-gray-500 mt-0.5">{{ getLevelRange(level) }}</div>
                  </div>
                </div>
                <div class="text-sm text-gray-500">
                  {{ level < 5 ? `距离下一级还需 ${getNextLevelPoints(level, pointsInfo.total_earned)} 积分` : '已达到最高等级' }}
                </div>
              </div>

              <!-- 等级特权列表 -->
              <div class="p-6">
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div v-for="(privilege, index) in getLevelPrivileges(level)" 
                    :key="index"
                    class="flex items-start space-x-3 p-3 rounded-lg"
                    :class="level === pointsInfo.level ? 'bg-primary-50' : 'bg-gray-50'"
                  >
                    <div class="flex-shrink-0">
                      <CheckCircleIcon 
                        class="w-5 h-5"
                        :class="level === pointsInfo.level ? 'text-primary-500' : 'text-gray-400'"
                      />
                    </div>
                    <div>
                      <div class="text-sm font-medium text-gray-900">{{ privilege.title }}</div>
                      <div class="text-xs text-gray-500 mt-0.5">{{ privilege.description }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 订单记录 -->
        <div v-if="currentTab === 'orders'" class="space-y-4">
          <div v-if="orders.length === 0" class="text-center py-8 text-gray-500">
            暂无订单记录
          </div>
          
          <!-- 订单列表 -->
          <div v-else class="space-y-4">
            <div v-for="order in orders" :key="order.order_no" 
              class="bg-white border rounded-lg overflow-hidden transition-all hover:border-gray-300"
            >
              <!-- 订单基本信息 -->
              <div class="px-4 py-3 flex items-center justify-between border-b border-gray-100">
                <div class="flex items-center space-x-4">
                  <div class="text-sm text-gray-500">订单号：{{ order.order_no }}</div>
                  <div :class="[
                    'px-2 py-1 text-xs font-medium rounded-full',
                    {
                      'bg-yellow-100 text-yellow-800': order.status === 'pending',
                      'bg-green-100 text-green-800': order.status === 'paid',
                      'bg-gray-100 text-gray-800': order.status === 'cancelled',
                      'bg-red-100 text-red-800': order.status === 'refunded'
                    }
                  ]">
                    {{ formatOrderStatus(order.status) }}
                  </div>
                </div>
                <button 
                  class="text-sm text-gray-500 hover:text-gray-700"
                  @click="toggleOrderDetail(order.order_no)"
                >
                  {{ expandedOrders.includes(order.order_no) ? '收起' : '展开' }}
                  <ChevronDownIcon 
                    class="w-4 h-4 inline-block ml-1 transition-transform"
                    :class="{ 'rotate-180': expandedOrders.includes(order.order_no) }"
                  />
                </button>
              </div>
              
              <!-- 订单主要信息 -->
              <div class="px-4 py-3 flex items-center justify-between bg-gray-50">
                <div class="flex items-center space-x-3">
                  <div class="w-10 h-10 rounded-lg bg-violet-100 flex items-center justify-center">
                    <SparklesIcon class="w-5 h-5 text-violet-600" />
                  </div>
                  <div>
                    <div class="font-medium">{{ formatMembershipType(order) }}</div>
                    <div class="text-sm text-gray-500">{{ formatOrderDate(order.created_at) }}</div>
                  </div>
                </div>
                <div class="text-lg font-medium text-gray-900">
                  ¥{{ order.amount }}
                </div>
              </div>
              
              <!-- 展开的详细信息 -->
              <div v-show="expandedOrders.includes(order.order_no)"
                class="px-4 py-3 space-y-3 bg-gray-50 border-t border-gray-100"
              >
                <div class="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <div class="text-gray-500">支付方式</div>
                    <div class="mt-1">{{ formatPaymentMethod(order.payment_method) }}</div>
                  </div>
                  <div>
                    <div class="text-gray-500">支付时间</div>
                    <div class="mt-1">{{ order.paid_at ? formatDate(order.paid_at) : '-' }}</div>
                  </div>
                  <div>
                    <div class="text-gray-500">订单创建时间</div>
                    <div class="mt-1">{{ formatDate(order.created_at) }}</div>
                  </div>
                  <div>
                    <div class="text-gray-500">订单更新时间</div>
                    <div class="mt-1">{{ formatDate(order.updated_at) }}</div>
                  </div>
                </div>
                
                <!-- 如果有备注信息 -->
                <div v-if="order.remarks" class="text-sm">
                  <div class="text-gray-500">备注信息</div>
                  <div class="mt-1 text-gray-700">{{ order.remarks }}</div>
                </div>
                
                <!-- 订单操作按钮 -->
                <div class="flex justify-end space-x-3 pt-2">
                  <button v-if="order.status === 'pending'"
                    class="px-3 py-1 text-sm text-violet-600 hover:text-violet-700 border border-violet-200 rounded-md hover:bg-violet-50"
                    @click="handlePayment(order)"
                  >
                    立即支付
                  </button>
                  <button v-if="['pending', 'paid'].includes(order.status)"
                    class="px-3 py-1 text-sm text-gray-600 hover:text-gray-700 border border-gray-200 rounded-md hover:bg-gray-50"
                    @click="showOrderDetail(order)"
                  >
                    查看详情
                  </button>
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
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  CalendarDaysIcon, 
  StarIcon,
  TrophyIcon,
  CheckCircleIcon,
  ChevronDownIcon,
  SparklesIcon
} from '@heroicons/vue/24/outline'
import { useRouter } from 'vue-router'
import * as membership from '@/api/membership'
import { formatDate } from '@/utils/date'
import { useAccountStore } from '@/stores/account'

const router = useRouter()

const accountStore = useAccountStore()

// 会员状态数据
const vipTypeText = computed(() => {
  const userInfo = accountStore.userInfo
  if (!userInfo?.is_vip) return '免费用户'
  return userInfo.vip_status
})

const vipExpireText = computed(() => {
  const userInfo = accountStore.userInfo
  if (!userInfo?.is_vip) return '开通会员享受更多权益'
  if (userInfo.vip_type === 'lifetime') return '终身会员'
  if (userInfo.vip_expire_time) {
    const expireDate = new Date(userInfo.vip_expire_time)
    const now = new Date()
    const diffDays = Math.floor((expireDate - now) / (1000 * 60 * 60 * 24))
    if (diffDays > 0) {
      return `剩余 ${diffDays} 天 (${formatDate(userInfo.vip_expire_time, 'YYYY-MM-DD')})`
    } else {
      return '会员已过期'
    }
  }
  return '开通会员享受更多权益'
})

const vipButtonText = computed(() => {
  const userInfo = accountStore.userInfo
  if (!userInfo?.is_vip) return '立即开通'
  if (userInfo.vip_type === 'lifetime') return '查看权益'
  return '立即续费'
})

// 积分相关数据
const pointsInfo = ref({
  balance: 0,
  level: 1,
  sign_in_days: 0,
  total_earned: 0
})

// 签到相关数据
const signInInfo = ref({
  can_sign_in: false,
  sign_in_days: 0,
  next_reward: null
})

const loading = ref(false)
const currentFilter = ref('all')
const currentTab = ref('points')
const pointsRecords = ref([])
const hasMore = ref(false)
const page = ref(1)
const expandedOrders = ref([])

// 会员权益列表
const memberBenefits = [
  {
    key: 'unlimited',
    name: '无限使用',
    desc: '无限制使用所有功能',
    icon: SparklesIcon
  },
  // ... 其他权益配置
]

// 积分筛选选项
const pointsFilters = [
  { label: '全部', value: 'all' },
  { label: '获得', value: 'earned' },
  { label: '使用', value: 'used' }
]

// tabs配置
const tabs = [
  { key: 'points', name: '积分规则' },
  { key: 'privileges', name: '等级权益' },
  { key: 'orders', name: '订单记录' }
]

// 积分规则
const pointRules = [
  {
    action: '每日签到',
    points: '+1~10',
    description: '连续签到可获得更多积分奖励',
    icon: CalendarDaysIcon,
    bgColor: 'bg-blue-50',
    iconColor: 'text-blue-500',
    borderColor: 'border-blue-100',
    textColor: 'text-blue-600'
  },
  // ... 其他规则配置
]

// 计算属性
const filteredRecords = computed(() => {
  if (!pointsRecords.value) return []
  if (currentFilter.value === 'all') return pointsRecords.value
  return pointsRecords.value.filter(record => 
    currentFilter.value === 'earned' ? record.points > 0 : record.points < 0
  )
})

// 添加会员信息的响应式数据
const membershipInfo = ref({
  is_active: false,
  tier: null,
  expire_at: null
})

// 修改 handleVipButton 方法
const handleVipButton = () => {
  const userInfo = accountStore.userInfo
  if (!userInfo?.is_vip) {
    router.push('/pro')
  } else if (userInfo.vip_type === 'lifetime') {
    // 显示会员权益详情
    currentTab.value = 'privileges'
  } else {
    router.push('/pro')
  }
}

// 获取签到状态
const fetchSignInStatus = async () => {
  try {
    const response = await membership.getSignInStatus()
    if (response?.data?.code === 200) {
      signInInfo.value = response.data.data
    }
  } catch (error) {
    console.error('获取签到状态失败:', error)
  }
}

// 处理签到
const handleSignIn = async () => {
  if (!signInInfo.value.can_sign_in) return
  
  try {
    const response = await membership.signIn()
    if (response?.data?.code === 200) {
      ElMessage.success('签到成功')
      await Promise.all([
        fetchSignInStatus(),
        fetchPointsInfo()
      ])
    }
  } catch (error) {
    console.error('签到失败:', error)
    ElMessage.error('签到失败，请稍后重试')
  }
}

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

const fetchPointsRecords = async () => {
  if (loading.value) return
  
  loading.value = true
  try {
    const response = await membership.getPointsRecords({ page: page.value })
    if (response?.data?.code === 200) {
      const records = response.data.data?.records || []
      const has_more = response.data.data?.has_more || false
      
      if (page.value === 1) {
        pointsRecords.value = records
      } else {
        pointsRecords.value.push(...records)
      }
      hasMore.value = has_more
    }
  } catch (error) {
    console.error('获取积分记录失败:', error)
  } finally {
    loading.value = false
  }
}

const loadMore = () => {
  page.value++
  fetchPointsRecords()
}

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

const toggleOrderDetail = (orderNo) => {
  const index = expandedOrders.value.indexOf(orderNo)
  if (index > -1) {
    expandedOrders.value.splice(index, 1)
  } else {
    expandedOrders.value.push(orderNo)
  }
}

const getLevelThreshold = (level) => {
  const thresholds = {
    1: 1000,    // 0-1000
    2: 3000,    // 1001-3000
    3: 8000,    // 3001-8000
    4: 15000,   // 8001-15000
    5: Infinity // 15000+
  }
  return thresholds[level] || 1000
}

// 获取签到提示
const getSignInTip = () => {
  const nextReward = signInInfo.value.next_reward
  if (!nextReward) return ''
  
  if (nextReward.days === 1) {
    return `明日签到可获得 ${nextReward.points} 积分奖励`
  }
  return `再签到 ${nextReward.days} 天可获得 ${nextReward.points} 积分奖励`
}

// 获取等级特权
const getLevelPrivileges = (level) => {
  const privileges = {
    1: [
      { title: '基础功能', description: '可使用所有基础功能' },
      { title: '每日签到', description: '每日签到获取积分' }
    ],
    2: [
      { title: '高级功能', description: '解锁部分高级功能' },
      { title: '积分加速', description: '签到积分1.2倍' }
    ],
    3: [
      { title: '专业功能', description: '解锁全部高级功能' },
      { title: '积分加速', description: '签到积分1.5倍' }
    ],
    4: [
      { title: '特权服务', description: '享受专属客服服务' },
      { title: '积分加速', description: '签到积分2倍' }
    ],
    5: [
      { title: 'VIP特权', description: '享受最高级别服务' },
      { title: '积分加速', description: '签到积分3倍' }
    ]
  }
  return privileges[level] || privileges[1]
}

// 格式化订单状态
const formatOrderStatus = (status) => {
  const statusMap = {
    pending: '待支付',
    paid: '已支付',
    cancelled: '已取消',
    refunded: '已退款'
  }
  return statusMap[status] || status
}

// 格式化支付方式
const formatPaymentMethod = (method) => {
  const methodMap = {
    alipay: '支付宝',
    wechat: '微信支付',
    balance: '余额支付'
  }
  return methodMap[method] || method
}

// 格式化会员类型
const formatMembershipType = (order) => {
  // 打印原始数据，用于调试
  console.log('订单数据:', order)
  
  // 优先使用 tier_name
  const tierName = order.tier_name || order.tier?.name || '普通会员'
  
  // 如果是终身会员
  if (order.type === 'lifetime' || order.duration === 'lifetime') {
    return `${tierName} (终身)`
  }
  
  // 如果有时长
  if (order.duration) {
    return `${tierName} (${order.duration}个月)`
  }
  
  return tierName
}

// 格式化日期
const formatOrderDate = (dateString) => {
  if (!dateString) return '-'
  return formatDate(dateString, 'YYYY-MM-DD')
}

// 处理支付
const handlePayment = (order) => {
  // 处理支付逻辑
  console.log('处理支付:', order)
}

// 显示订单详情
const showOrderDetail = (order) => {
  // 显示订单详情逻辑
  console.log('显示订单详情:', order)
}

// 添加 orders 数据
const orders = ref([])

// 添加窗口宽度的响应式引用
const windowWidth = ref(window?.innerWidth || 1024)

// 添加窗口大小变化的处理函数
const handleResize = () => {
  windowWidth.value = window.innerWidth
}

// 获取订单记录
const fetchOrders = async () => {
  try {
    const response = await membership.getOrders()
    console.log('订单接口返回:', response.data)
    if (response?.data?.code === 200) {
      orders.value = response.data.data || []
    }
  } catch (error) {
    console.error('获取订单记录失败:', error)
    orders.value = []
  }
}

// 修改组件挂载时的数据获取
onMounted(async () => {
  window.addEventListener('resize', handleResize)
  try {
    await accountStore.fetchUserInfo()
    await Promise.all([
      fetchPointsInfo(),
      fetchPointsRecords(),
      fetchSignInStatus(),
      fetchOrders()  // 添加获取订单记录
    ])
  } catch (error) {
    console.error('初始化数据失败:', error)
    pointsRecords.value = []
    orders.value = []
  }
})

// 在组件卸载时移除事件监听
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

// 添加格式化日期的计算属性
const dateFormat = computed(() => windowWidth.value < 640 ? 'MM-DD HH:mm' : 'YYYY-MM-DD HH:mm')

// 计算属性：是否可以签到
const canSignIn = computed(() => signInInfo.value.can_sign_in)
</script>

