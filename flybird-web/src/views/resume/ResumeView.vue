<template>
  <div class="min-h-screen bg-gray-50 pb-16 md:pb-0">
    <HeadView />
    <router-view></router-view>
    <FootView class="hidden md:block" />
    
    <MobileTabBar 
      :menu-groups="menuGroups"
      :unread-messages="unreadMessagesCount"
    />

    <!-- 移动端浮动创建按钮 -->
    <button 
      class="fixed right-4 bottom-20 md:hidden bg-rose-500 text-white rounded-full p-3 shadow-lg hover:bg-rose-600 transition-colors z-50"
      @click="handleCreate"
    >
      <PlusIcon class="w-6 h-6" />
    </button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import HeadView from '@/components/HeadView.vue'
import FootView from '@/components/FootView.vue'
import MobileTabBar from '@/components/MobileTabBar.vue'
import { 
  PlusIcon,
  DocumentIcon,
  AcademicCapIcon,
  BriefcaseIcon,
  LanguageIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const route = useRoute()
const unreadMessagesCount = ref(0)

// 获取当前导航名称
const getCurrentNavName = computed(() => {
  const navMap = {
    '/templates': '全部模板',
    '/templates/resume': '简历模板',
    '/templates/cover-letter': '求职信',
    '/templates/bio': '个人简介'
  }
  return navMap[route.path] || '全部模板'
})

// 获取横幅描述
const getBannerDescription = computed(() => {
  const descriptions = {
    '/templates': '精选优质简历模板，助你打造完美简历',
    '/templates/resume': '为在校生和应届生量身定制的简历模板',
    '/templates/cover-letter': '专业的求职信模板，助力职业发展',
    '/templates/bio': '专业的个人简介模板，展现个人魅力'
  }
  return descriptions[route.path] || ''
})

// 更多菜单中的选项分组
const menuGroups = [
  {
    title: '简历模板',
    items: [
      { name: '全部模板', path: '/templates', icon: DocumentIcon },
      { name: '简历模板', path: '/templates/resume', icon: AcademicCapIcon },
      { name: '求职信', path: '/templates/cover-letter', icon: BriefcaseIcon },
      { name: '个人简介', path: '/templates/bio', icon: LanguageIcon }
    ]
  }
]

// 处理创建按钮点击
const handleCreate = () => {
  router.push('/templates/create')
}
</script> 