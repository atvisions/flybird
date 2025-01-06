<template>
  <div class="app-wrapper">
    <div class="bg-image" :style="bgStyle"></div>
    <router-view></router-view>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useStore } from 'vuex'
import bgImage from '@/assets/images/bg.png'
import { auth } from '@/api/auth'
import { useTokenRefresh } from '@/composables/useTokenRefresh'

const store = useStore()
const bgStyle = {
  backgroundImage: `url(${bgImage})`,
  backgroundSize: '100% 100%',
  backgroundPosition: 'center top',
  backgroundRepeat: 'no-repeat'
}

// 使用 token 刷新功能
const { startTokenRefresh } = useTokenRefresh()

onMounted(async () => {
  try {
    await store.dispatch('checkAuth')
  } catch (error) {
    console.error('初始化失败:', error)
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