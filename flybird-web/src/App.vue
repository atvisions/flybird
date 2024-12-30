<template>
  <div class="app-wrapper">
    <div class="bg-image" :style="bgStyle"></div>
    <router-view></router-view>
  </div>
</template>

<script setup>
import {  onMounted } from 'vue'
import { useStore } from 'vuex'
import bgImage from '@/assets/images/bg.png'
const store = useStore()
const bgStyle = {
  backgroundImage: `url(${bgImage})`,
  backgroundSize: '100% 100%',
  backgroundPosition: 'center top',
  backgroundRepeat: 'no-repeat'
}
onMounted(async () => {
  try {
    // 先检查认证状态
    const isAuthenticated = await store.dispatch('checkAuth')
    
    if (isAuthenticated) {
      // 如果认证成功但没有用户信息，重新获取
      if (!store.state.userInfo || !store.state.userInfo.profile?.avatar) {
        await store.dispatch('fetchUserInfo')
      }
    }
  } catch (error) {
    console.error('初始化用户信息失败:', error)
  }
})
</script>
<style>
.app-wrapper {
  position: relative;
  min-height: 100vh;
}

.bg-image {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
  pointer-events: none;
}

/* 可选：添加一个半透明遮罩让内容更易读 */
.bg-image::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
}

/* 确保内容在背景之上 */
.app-wrapper > *:not(.bg-image) {
  position: relative;
  z-index: 1;
}
</style>