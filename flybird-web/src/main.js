// frontend/src/main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/css/input.css'
import { showToast } from '@/components/ToastMessage'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { eventBus } from '@/utils/eventBus'
import VueCropper from 'vue-cropper'
import 'vue-cropper/dist/index.css'
import { useAuthStore } from '@/stores/auth'
import store from './store'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(ElementPlus)
app.use(VueCropper)
app.use(store)

// 初始化认证状态
await (async () => {
  
  const authStore = useAuthStore()
  await authStore.initialize()
  
})()

// 在认证初始化后再设置路由
app.use(router)

// 添加全局 Toast 方法
app.config.globalProperties.$toast = showToast
window.$toast = showToast  // 添加到 window 对象，供内联事件使用

// 如果需要全局使用
app.config.globalProperties.eventBus = eventBus

app.mount('#app')