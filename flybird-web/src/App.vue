<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 主要内容区域 -->
    <main>
      <router-view></router-view>
    </main>
    
    
    <!-- Toast 消息组件 -->
    <ToastMessage 
      v-if="toastMessage"
      :message="toastMessage"
      :type="toastType"
      :duration="toastDuration"
      @destroy="handleToastDestroy"
    />
  </div>
</template>

<script setup>
import { ref, defineAsyncComponent } from 'vue'

// Toast 相关状态
const toastMessage = ref('')
const toastType = ref('info')
const toastDuration = ref(3000)

// 处理 Toast 销毁
const handleToastDestroy = () => {
  toastMessage.value = ''
  toastType.value = 'info'
}

// 异步导入组件
const ToastMessage = defineAsyncComponent(() => import('@/components/ToastMessage.vue'))
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
