<template>
  <div class="min-h-screen ">
    <HeadView />
    <router-view></router-view>
    <FootView class="hidden md:block" />
    
    <MobileTabBar 
      :menu-groups="menuGroups"
      :unread-messages="unreadMessagesCount"
    />

    <!-- 移动端浮动发布按钮 -->
    <button 
      class="fixed right-4 bottom-20 md:hidden bg-blue-500 text-white rounded-full p-3 shadow-lg hover:bg-blue-600 transition-colors z-50"
      @click="handlePublish"
    >
      <PlusIcon class="w-6 h-6" />
    </button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import HeadView from '@/components/HeadView.vue'
import FootView from '@/components/FootView.vue'
import MobileTabBar from '@/components/MobileTabBar.vue'
import {
  DocumentTextIcon,
  QuestionMarkCircleIcon,
  ScaleIcon,
  UserIcon,
  Bars3Icon,
  XMarkIcon,
  PlusIcon,
  DocumentIcon,
  EnvelopeIcon,
  Cog6ToothIcon,
  UserCircleIcon,
  PaintBrushIcon,
  VideoCameraIcon,
  CameraIcon,
  FilmIcon,
  UsersIcon
} from '@heroicons/vue/24/outline'

const route = useRoute()
const router = useRouter()
const isMobileMenuOpen = ref(false)
const unreadMessagesCount = ref(0)
const messageBadge = computed(() => unreadMessagesCount.value)

// 更多菜单中的选项分组
const menuGroups = [
  {
    title: '社区',
    items: [
      { 
        name: '文章', 
        path: '/community/articles', 
        icon: DocumentTextIcon 
      },
      { 
        name: '问答', 
        path: '/community/questions', 
        icon: QuestionMarkCircleIcon 
      },
      { 
        name: '话题', 
        path: '/community/topics', 
        icon: ScaleIcon 
      }
    ]
  },
  {
    title: '创作集',
    items: [
      {
        name: '设计',
        path: '/portfolio/design',
        icon: PaintBrushIcon
      },
      {
        name: '视频',
        path: '/portfolio/video',
        icon: VideoCameraIcon
      },
      {
        name: '摄影',
        path: '/portfolio/photography',
        icon: CameraIcon
      },
      {
        name: '动画',
        path: '/portfolio/animation',
        icon: FilmIcon
      }
    ]
  }
]

// 处理发布按钮点击
const handlePublish = () => {
  const path = route.path
  if (path.includes('articles')) {
    router.push('/community/articles/publish')
  } else if (path.includes('questions')) {
    router.push('/community/questions/publish')
  } else {
    router.push('/community/articles/publish')
  }
}
</script>

<style scoped>
.safe-area-inset-bottom {
  padding-bottom: env(safe-area-inset-bottom);
}

@supports (padding-bottom: env(safe-area-inset-bottom)) {
  .pb-16 {
    padding-bottom: calc(4rem + env(safe-area-inset-bottom));
  }
}
</style> 