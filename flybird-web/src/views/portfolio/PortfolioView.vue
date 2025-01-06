<template>
  <div class="min-h-screen">
    <HeadView />
    <router-view></router-view>
    <FootView class="hidden md:block" />
    <MobileTabBar 
      :menu-groups="menuGroups"
      :unread-messages="unreadMessagesCount"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from 'vuex'
import HeadView from '@/components/HeadView.vue'
import FootView from '@/components/FootView.vue'
import MobileTabBar from '@/components/MobileTabBar.vue'
import {
  PaintBrushIcon,
  HomeIcon,
  UserIcon,
  PlusIcon,
  VideoCameraIcon,
  CameraIcon,
  FilmIcon
} from '@heroicons/vue/24/outline'

const route = useRoute()
const router = useRouter()
const store = useStore()

// 使用 Vuex store 的 isAuthenticated 状态
const isAuthenticated = computed(() => store.state.isAuthenticated)

// 未读消息数量
const unreadMessagesCount = ref(0)

// 主导航数据
const mainNavs = [
  { name: '发现', path: '/portfolio' },
  { name: '设计', path: '/portfolio/design' },
  { name: '视频', path: '/portfolio/video' },
  { name: '动画', path: '/portfolio/animation' },
  { name: '摄影', path: '/portfolio/photo' }
]

// 移动端菜单组
const menuGroups = [
  {
    title: '作品分类',
    items: [
      {
        name: '作品集',
        path: '/portfolio',
        icon: HomeIcon
      },
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
        name: '动画',
        path: '/portfolio/animation',
        icon: FilmIcon
      },
      {
        name: '摄影',
        path: '/portfolio/photo',
        icon: CameraIcon
      }
    ]
  }
]
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