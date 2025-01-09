<template>
  <div class="space-y-6">
    <!-- 评论输入框 -->
    <div class="flex space-x-4">
      <img 
        :src="userAvatar" 
        class="w-10 h-10 rounded-full flex-shrink-0"
        alt=""
      >
      <div class="flex-1">
        <textarea
          v-model="commentContent"
          rows="3"
          class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm"
          placeholder="写下你的评论..."
        ></textarea>
        <div class="mt-2 flex justify-end">
          <button
            @click="handleSubmit"
            class="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            发表评论
          </button>
        </div>
      </div>
    </div>

    <!-- 评论列表 -->
    <div class="space-y-6">
      <div v-for="comment in comments" :key="comment.id" class="flex space-x-4">
        <img 
          :src="comment.author.avatar" 
          class="w-10 h-10 rounded-full flex-shrink-0"
          alt=""
        >
        <div class="flex-1">
          <div class="bg-gray-50 rounded-lg px-4 py-3">
            <div class="flex items-center justify-between mb-1">
              <span class="font-medium text-gray-900">{{ comment.author.name }}</span>
              <span class="text-sm text-gray-500">{{ formatTime(comment.createTime) }}</span>
            </div>
            <p class="text-gray-600">{{ comment.content }}</p>
          </div>
          
          <!-- 评论操作 -->
          <div class="mt-2 flex items-center space-x-4">
            <button 
              @click="handleLike(comment)"
              class="flex items-center text-sm text-gray-500 hover:text-blue-600"
            >
              <HeartIcon 
                class="w-4 h-4 mr-1"
                :class="comment.isLiked ? 'text-pink-600' : 'text-gray-400'"
              />
              {{ comment.likes }}
            </button>
            <button 
              @click="handleReply(comment)"
              class="flex items-center text-sm text-gray-500 hover:text-blue-600"
            >
              <ChatBubbleLeftIcon class="w-4 h-4 mr-1" />
              回复
            </button>
          </div>

          <!-- 回复列表 -->
          <div v-if="comment.replies?.length" class="mt-3 space-y-3 pl-4">
            <div v-for="reply in comment.replies" :key="reply.id" class="flex space-x-3">
              <img 
                :src="reply.author.avatar" 
                class="w-8 h-8 rounded-full flex-shrink-0"
                alt=""
              >
              <div class="flex-1">
                <div class="bg-gray-50 rounded-lg px-3 py-2">
                  <div class="flex items-center justify-between mb-1">
                    <span class="font-medium text-gray-900">{{ reply.author.name }}</span>
                    <span class="text-sm text-gray-500">{{ formatTime(reply.createTime) }}</span>
                  </div>
                  <p class="text-gray-600">{{ reply.content }}</p>
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
import { ref, computed } from 'vue'
import { HeartIcon, ChatBubbleLeftIcon } from '@heroicons/vue/24/outline'
import { formatTime } from '@/utils/time'
import { useStore } from 'vuex'

const store = useStore()
const props = defineProps({
  comments: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['reply', 'like'])
const commentContent = ref('')
const userAvatar = computed(() => store.getters.userAvatar)

const handleSubmit = () => {
  if (!commentContent.value.trim()) return
  // TODO: 提交评论
  commentContent.value = ''
}

const handleLike = (comment) => {
  emit('like', comment)
}

const handleReply = (comment) => {
  emit('reply', comment)
}
</script> 