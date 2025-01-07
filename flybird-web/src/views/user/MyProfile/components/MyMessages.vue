<template>
  <div class="messages-container">
    <!-- 消息类型切换 -->
    <div class="bg-white rounded-lg shadow mb-4">
      <div class="flex">
        <button
          v-for="tab in messageTabs"
          :key="tab.key"
          @click="currentMessageTab = tab.key"
          class="flex-1 px-4 py-3 text-sm font-medium relative border-b-2 transition-colors"
          :class="[
            currentMessageTab === tab.key
              ? 'text-indigo-600 border-indigo-600'
              : 'text-gray-500 hover:text-gray-700 border-transparent hover:border-gray-300'
          ]"
        >
          {{ tab.label }}
          <span 
            v-if="tab.unread" 
            class="absolute -top-1 -right-1 min-w-[16px] h-4 bg-red-500 rounded-full text-[10px] font-medium text-white flex items-center justify-center px-1"
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
        <InboxIcon class="mx-auto h-12 w-12 text-gray-400" />
        <h3 class="mt-2 text-sm font-medium text-gray-900">暂无消息</h3>
        <p class="mt-1 text-sm text-gray-500">当有新消息时会在这里显示</p>
      </div>

      <!-- 消息列表 -->
      <div v-else class="divide-y divide-gray-100">
        <div 
          v-for="message in currentMessages" 
          :key="message.id"
          class="p-4 hover:bg-gray-50 transition-colors cursor-pointer group"
          :class="{ 'bg-indigo-50/50': message.unread }"
          @click="handleMessageClick(message)"
        >
          <div class="flex items-start space-x-3">
            <img 
              :src="message.avatar" 
              :alt="message.sender"
              class="w-10 h-10 rounded-full flex-shrink-0"
              @error="handleImageError"
            />
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <p class="text-sm font-medium text-gray-900">{{ message.sender }}</p>
                  <span 
                    v-if="message.type === 'system'"
                    class="px-2 py-0.5 text-xs bg-indigo-100 text-indigo-800 rounded-full"
                  >
                    系统
                  </span>
                </div>
                <span class="text-xs text-gray-500">{{ message.time }}</span>
              </div>
              <p class="text-sm text-gray-600 line-clamp-2 mt-1">{{ message.content }}</p>
              <!-- 操作按钮 -->
              <div class="mt-2 flex items-center justify-end space-x-2 opacity-0 group-hover:opacity-100 transition-opacity">
                <button
                  v-if="message.unread"
                  @click.stop="markAsRead(message)"
                  class="text-xs text-indigo-600 hover:text-indigo-700"
                >
                  标记已读
                </button>
                <button
                  @click.stop="deleteMessage(message)"
                  class="text-xs text-gray-500 hover:text-red-600"
                >
                  删除
                </button>
              </div>
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
          class="text-sm text-indigo-600 hover:text-indigo-700"
          :disabled="loading"
        >
          {{ loading ? '加载中...' : '加载更多' }}
        </button>
      </div>
    </div>

    <!-- 新消息按钮 -->
    <button
      class="fixed right-4 bottom-20 lg:bottom-4 bg-indigo-600 text-white rounded-full p-3 shadow-lg hover:bg-indigo-700 transition-colors"
      @click="openNewMessage"
    >
      <PencilSquareIcon class="w-6 h-6" />
    </button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { InboxIcon, PencilSquareIcon } from '@heroicons/vue/24/outline'
import { ElMessage } from 'element-plus'
import defaultAvatar from '@/assets/images/default-avatar.png'

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

// 处理图片加载错误
const handleImageError = (e) => {
  e.target.src = defaultAvatar
}

// 标记消息已读
const markAsRead = async (message) => {
  try {
    // TODO: 调用API标记消息已读
    message.unread = false
    ElMessage.success('已标记为已读')
  } catch (error) {
    ElMessage.error('操作失败，请重试')
  }
}

// 删除消息
const deleteMessage = async (message) => {
  try {
    // TODO: 调用API删除消息
    messages.value = messages.value.filter(msg => msg.id !== message.id)
    ElMessage.success('删除成功')
  } catch (error) {
    ElMessage.error('删除失败，请重试')
  }
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