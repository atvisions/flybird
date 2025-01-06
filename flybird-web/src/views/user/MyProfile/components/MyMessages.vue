<template>
  <div class="messages-container">
    <!-- 消息类型切换 -->
    <div class="bg-white rounded-lg shadow mb-4">
      <div class="flex border-b">
        <button
          v-for="tab in messageTabs"
          :key="tab.key"
          @click="currentMessageTab = tab.key"
          class="flex-1 px-4 py-3 text-sm font-medium relative"
          :class="[
            currentMessageTab === tab.key
              ? 'text-blue-600'
              : 'text-gray-500 hover:text-gray-700'
          ]"
        >
          {{ tab.label }}
          <span 
            v-if="tab.unread" 
            class="absolute top-2 right-2 bg-red-500 text-white text-xs rounded-full min-w-[16px] h-4 flex items-center justify-center px-1"
          >
            {{ tab.unread }}
          </span>
        </button>
      </div>
    </div>

    <!-- 消息列表 -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <!-- 空状态 -->
      <div v-if="!currentMessages.length" class="p-8 text-center">
        <div class="w-16 h-16 mx-auto mb-4">
          <InboxIcon class="w-full h-full text-gray-400" />
        </div>
        <p class="text-gray-500">暂无消息</p>
      </div>

      <!-- 消息列表 -->
      <div v-else class="divide-y divide-gray-100">
        <div 
          v-for="message in currentMessages" 
          :key="message.id"
          class="p-4 hover:bg-gray-50 transition-colors cursor-pointer"
          :class="{ 'bg-blue-50': message.unread }"
          @click="handleMessageClick(message)"
        >
          <div class="flex items-start space-x-3">
            <img 
              :src="message.avatar" 
              :alt="message.sender"
              class="w-10 h-10 rounded-full flex-shrink-0"
            />
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between">
                <p class="text-sm font-medium text-gray-900">{{ message.sender }}</p>
                <span class="text-xs text-gray-500">{{ message.time }}</span>
              </div>
              <p class="text-sm text-gray-500 truncate mt-1">{{ message.content }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 加载更多 -->
      <div 
        v-if="currentMessages.length && hasMore" 
        class="p-4 text-center border-t"
      >
        <button 
          @click="loadMore"
          class="text-sm text-blue-600 hover:text-blue-700"
          :disabled="loading"
        >
          {{ loading ? '加载中...' : '加载更多' }}
        </button>
      </div>
    </div>

    <!-- 新消息按钮 -->
    <button
      class="fixed right-4 bottom-20 lg:bottom-4 bg-blue-600 text-white rounded-full p-3 shadow-lg hover:bg-blue-700 transition-colors"
      @click="openNewMessage"
    >
      <PencilSquareIcon class="w-6 h-6" />
    </button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { InboxIcon, PencilSquareIcon } from '@heroicons/vue/24/outline'
import { showToast } from '@/components/ToastMessage'

// 消息类型标签
const messageTabs = [
  { key: 'all', label: '全部消息', unread: 5 },
  { key: 'system', label: '系统通知', unread: 2 },
  { key: 'private', label: '私信', unread: 3 }
]

const currentMessageTab = ref('all')
const loading = ref(false)
const hasMore = ref(true)

// 模拟消息数据
const messages = ref([
  {
    id: 1,
    sender: '系统通知',
    avatar: 'https://picsum.photos/32/32?random=1',
    content: '欢迎加入飞鸟社区！',
    time: '刚刚',
    unread: true,
    type: 'system'
  },
  {
    id: 2,
    sender: '张三',
    avatar: 'https://picsum.photos/32/32?random=2',
    content: '你好，我看了你的文章很受启发',
    time: '10分钟前',
    unread: true,
    type: 'private'
  },
  // 添加更多消息...
])

// 根据当前标签筛选消息
const currentMessages = computed(() => {
  if (currentMessageTab.value === 'all') {
    return messages.value
  }
  return messages.value.filter(msg => msg.type === currentMessageTab.value)
})

// 处理消息点击
const handleMessageClick = (message) => {
  // 标记消息为已读
  message.unread = false
  // TODO: 打开消息详情
  showToast('消息功能开发中...', 'info')
}

// 加载更多消息
const loadMore = async () => {
  if (loading.value) return
  loading.value = true
  try {
    // TODO: 调用API加载更多消息
    await new Promise(resolve => setTimeout(resolve, 1000))
    // 模拟加载完成
    hasMore.value = false
  } catch (error) {
    showToast('加载失败，请重试', 'error')
  } finally {
    loading.value = false
  }
}

// 打开新消息对话框
const openNewMessage = () => {
  showToast('新消息功能开发中...', 'info')
}
</script>

<style scoped>
.messages-container {
  min-height: calc(100vh - 64px - 56px); /* 减去头部和底部导航的高度 */
  padding-bottom: 80px; /* 为新消息按钮预留空间 */
}

@media (min-width: 1024px) {
  .messages-container {
    min-height: calc(100vh - 64px);
    padding-bottom: 60px;
  }
}
</style> 