<template>
  <HeadView />
  <div class="min-h-screen py-4 lg:py-6">
    <div v-if="loading" class="flex justify-center items-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent"></div>
    </div>
    <div v-else class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 面包屑导航 -->
      <nav class="flex items-center space-x-2 text-sm text-gray-500 mb-6">
        <router-link to="/portfolio" class="hover:text-gray-900">作品集</router-link>
        <ChevronRightIcon class="w-4 h-4" />
        <span class="text-gray-900">{{ portfolio?.title || '加载中...' }}</span>
      </nav>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <!-- 左侧主内容区 -->
        <div class="lg:col-span-8">
          <!-- 图片轮播 -->
          <div class="bg-white rounded-xl shadow-sm overflow-hidden mb-6">
            <Swiper
              :modules="modules"
              :slides-per-view="1"
              :space-between="0"
              :pagination="{ clickable: true }"
              :navigation="true"
              :autoplay="{ delay: 5000 }"
              class="aspect-video"
            >
              <SwiperSlide v-for="(image, index) in portfolio.images" :key="index">
                <img 
                  :src="image.url" 
                  :alt="image.description"
                  class="w-full h-full object-cover"
                >
              </SwiperSlide>
            </Swiper>
          </div>

          <!-- 作品信息 -->
          <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
            <h1 class="text-2xl font-bold text-gray-900 mb-4">{{ portfolio.title }}</h1>
            
            <!-- 作者信息 -->
            <div class="flex items-center justify-between mb-6">
              <div class="flex items-center space-x-3">
                <img 
                  :src="author.avatar || defaultAvatar" 
                  class="w-10 h-10 rounded-full"
                  alt=""
                  @error="handleImageError"
                >
                <div>
                  <div class="text-sm font-medium text-gray-900">{{ author.name || '未知作者' }}</div>
                  <div class="text-sm text-gray-500">{{ formatTime(portfolio.createTime) }}</div>
                </div>
              </div>
              <button 
                class="px-4 py-2 text-sm font-medium text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                @click="handleFollow"
              >
                {{ portfolio.author.isFollowing ? '已关注' : '+ 关注' }}
              </button>
            </div>

            <!-- 作品描述 -->
            <div class="prose prose-blue max-w-none">
              <div v-html="portfolio.description"></div>
            </div>

            <!-- 标签 -->
            <div class="flex flex-wrap gap-2 mt-6">
              <span 
                v-for="tag in portfolio.tags" 
                :key="tag"
                class="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm"
              >
                {{ tag }}
              </span>
            </div>
          </div>

          <!-- 评论区 -->
          <div class="bg-white rounded-xl shadow-sm p-6">
            <h2 class="text-lg font-medium text-gray-900 mb-4">评论 ({{ portfolio.comments }})</h2>
            <CommentList 
              :comments="comments"
              @reply="handleReply"
              @like="handleLikeComment"
            />
          </div>
        </div>

        <!-- 右侧信息栏 -->
        <div class="lg:col-span-4 space-y-6">
          <!-- 统计信息 -->
          <div class="bg-white rounded-xl shadow-sm p-6">
            <div class="grid grid-cols-3 gap-4 text-center">
              <div>
                <div class="text-2xl font-bold text-gray-900">{{ portfolio.views }}</div>
                <div class="text-sm text-gray-500">浏览</div>
              </div>
              <div>
                <div class="text-2xl font-bold text-gray-900">{{ portfolio.likes }}</div>
                <div class="text-sm text-gray-500">点赞</div>
              </div>
              <div>
                <div class="text-2xl font-bold text-gray-900">{{ portfolio.collects }}</div>
                <div class="text-sm text-gray-500">收藏</div>
              </div>
            </div>
            
            <!-- 操作按钮 -->
            <div class="grid grid-cols-2 gap-4 mt-6">
              <button 
                class="flex items-center justify-center px-4 py-2 border rounded-lg text-sm font-medium transition-colors"
                :class="[
                  portfolio.isLiked 
                    ? 'border-pink-200 text-pink-600 bg-pink-50 hover:bg-pink-100'
                    : 'border-gray-200 text-gray-700 hover:bg-gray-50'
                ]"
                @click="handleLike"
              >
                <HeartIcon 
                  class="w-5 h-5 mr-2"
                  :class="portfolio.isLiked ? 'text-pink-600' : 'text-gray-400'"
                />
                {{ portfolio.isLiked ? '已点赞' : '点赞' }}
              </button>
              <button 
                class="flex items-center justify-center px-4 py-2 border rounded-lg text-sm font-medium transition-colors"
                :class="[
                  portfolio.isCollected
                    ? 'border-yellow-200 text-yellow-600 bg-yellow-50 hover:bg-yellow-100'
                    : 'border-gray-200 text-gray-700 hover:bg-gray-50'
                ]"
                @click="handleCollect"
              >
                <StarIcon 
                  class="w-5 h-5 mr-2"
                  :class="portfolio.isCollected ? 'text-yellow-600' : 'text-gray-400'"
                />
                {{ portfolio.isCollected ? '已收藏' : '收藏' }}
              </button>
            </div>
          </div>

          <!-- 作者其他作品 -->
          <div class="bg-white rounded-xl shadow-sm p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">更多作品</h3>
            <div class="space-y-4">
              <router-link
                v-for="work in relatedWorks"
                :key="work.id"
                :to="`/portfolio/${work.id}`"
                class="block group"
              >
                <div class="aspect-video rounded-lg overflow-hidden mb-2">
                  <img 
                    :src="work.cover" 
                    class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                    alt=""
                  >
                </div>
                <h4 class="text-sm font-medium text-gray-900 group-hover:text-blue-600 transition-colors">
                  {{ work.title }}
                </h4>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <FootView />
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { Swiper, SwiperSlide } from 'swiper/vue'
import 'swiper/css'
import 'swiper/css/pagination'
import 'swiper/css/navigation'
import {
  ChevronRightIcon,
  HeartIcon,
  StarIcon
} from '@heroicons/vue/24/outline'
import CommentList from '@/components/comments/CommentList.vue'
import { formatTime } from '@/utils/time'
import { showToast } from '@/components/ToastMessage'
import defaultAvatar from '@/assets/images/default-avatar.png'
import { Navigation, Pagination, Autoplay } from 'swiper/modules'
import HeadView from '@/components/HeadView.vue'
import FootView from '@/components/FootView.vue'

const route = useRoute()
const portfolio = ref({})
const comments = ref([])
const relatedWorks = ref([])
const loading = ref(true)
const portfolioId = computed(() => route.params.id)

// 添加计算属性来处理作者信息
const author = computed(() => {
  return portfolio.value?.author || {
    name: '',
    avatar: '',
    isFollowing: false
  }
})

// 定义 Swiper 模块
const modules = [Navigation, Pagination, Autoplay]

// 获取作品详情
const fetchPortfolioDetail = async () => {
  loading.value = true
  try {
    // 使用路由参数中的 ID 获取作品详情
    console.log('获取作品详情:', portfolioId.value)
    // TODO: 调用API获取作品详情
    portfolio.value = {
      id: portfolioId.value,
      title: '2024春节主题插画设计',
      description: '这是一组以春节为主题的插画设计作品...',
      createTime: new Date().toISOString(),
      images: [
        { url: 'https://picsum.photos/1200/800', description: '图片1' },
        { url: 'https://picsum.photos/1200/801', description: '图片2' },
        { url: 'https://picsum.photos/1200/802', description: '图片3' }
      ],
      author: {
        name: '张小明',
        avatar: 'https://picsum.photos/200',
        isFollowing: false
      },
      tags: ['插画设计', '春节', '中国风'],
      views: 1234,
      likes: 56,
      collects: 23,
      comments: 12,
      isLiked: false,
      isCollected: false
    }
  } catch (error) {
    console.error('获取作品详情失败:', error)
    showToast('获取作品详情失败', 'error')
  } finally {
    loading.value = false
  }
}

// 获取相关作品
const fetchRelatedWorks = async () => {
  try {
    // 使用当前作品的 ID 获取相关作品
    console.log('获取相关作品:', portfolioId.value)
    // TODO: 调用API获取相关作品
    relatedWorks.value = [
      {
        id: 2,
        title: '元宵节主题插画',
        cover: 'https://picsum.photos/400/300'
      },
      {
        id: 3,
        title: '新年贺卡设计',
        cover: 'https://picsum.photos/400/301'
      }
    ]
  } catch (error) {
    console.error('获取相关作品失败:', error)
  }
}

// 处理关注
const handleFollow = async () => {
  try {
    // TODO: 调用关注API
    portfolio.value.author.isFollowing = !portfolio.value.author.isFollowing
    showToast(
      portfolio.value.author.isFollowing ? '关注成功' : '已取消关注',
      'success'
    )
  } catch (error) {
    console.error('关注操作失败:', error)
    showToast('操作失败，请稍后重试', 'error')
  }
}

// 处理点赞
const handleLike = async () => {
  try {
    // TODO: 调用点赞API
    portfolio.value.isLiked = !portfolio.value.isLiked
    portfolio.value.likes += portfolio.value.isLiked ? 1 : -1
    showToast(portfolio.value.isLiked ? '点赞成功' : '已取消点赞', 'success')
  } catch (error) {
    console.error('点赞操作失败:', error)
    showToast('操作失败，请稍后重试', 'error')
  }
}

// 处理收藏
const handleCollect = async () => {
  try {
    // TODO: 调用收藏API
    portfolio.value.isCollected = !portfolio.value.isCollected
    portfolio.value.collects += portfolio.value.isCollected ? 1 : -1
    showToast(
      portfolio.value.isCollected ? '收藏成功' : '已取消收藏',
      'success'
    )
  } catch (error) {
    console.error('收藏操作失败:', error)
    showToast('操作失败，请稍后重试', 'error')
  }
}

// 处理评论回复
const handleReply = (comment) => {
  // TODO: 实现评论回复逻辑
  console.log('回复评论:', comment)
}

// 处理评论点赞
const handleLikeComment = (comment) => {
  // TODO: 实现评论点赞逻辑
  console.log('点赞评论:', comment)
}

// 处理图片加载错误
const handleImageError = (e) => {
  e.target.src = defaultAvatar
}

onMounted(() => {
  fetchPortfolioDetail()
  fetchRelatedWorks()
})
</script>

<style scoped>
:deep(.swiper-button-next),
:deep(.swiper-button-prev) {
  color: white;
  background: rgba(0, 0, 0, 0.3);
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

:deep(.swiper-button-next:after),
:deep(.swiper-button-prev:after) {
  font-size: 20px;
}

:deep(.swiper-pagination-bullet) {
  background: white;
  opacity: 0.7;
}

:deep(.swiper-pagination-bullet-active) {
  background: white;
  opacity: 1;
}
</style> 