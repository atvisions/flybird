<template>
  <div class="main-layout">
    <router-view />
    <MobileTabBar :menu-groups="currentMenuGroups" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import MobileTabBar from '@/components/MobileTabBar.vue'

const route = useRoute()

// 根据路由路径返回对应的菜单配置
const currentMenuGroups = computed(() => {
  if (route.path.startsWith('/resume/templates')) {
    return [{
      title: '简历模板',
      items: [
        { name: '全部模板', path: '/resume/templates/all' },
        { name: '推荐模板', path: '/resume/templates/recommended' },
        { name: '最新模板', path: '/resume/templates/latest' }
      ]
    }]
  }
  
  if (route.path.startsWith('/resume/cover-letter')) {
    return [{
      title: '求职信',
      items: [
        { name: '全部模板', path: '/resume/cover-letter/all' },
        { name: '推荐模板', path: '/resume/cover-letter/recommended' },
        { name: '最新模板', path: '/resume/cover-letter/latest' }
      ]
    }]
  }
  
  return []
})
</script> 