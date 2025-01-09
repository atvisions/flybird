// frontend/src/main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersist from 'pinia-plugin-persist'
import App from './App.vue'
import router from './router'
import './assets/css/input.css'
import { showToast } from '@/components/ToastMessage'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { eventBus } from '@/utils/eventBus'
import axios from 'axios'

const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersist)
app.use(store)
app.use(pinia)
app.use(router)
app.use(ElementPlus)

// 添加全局 Toast 方法
app.config.globalProperties.$toast = showToast
window.$toast = showToast  // 添加到 window 对象，供内联事件使用

// 如果需要全局使用
app.config.globalProperties.eventBus = eventBus

app.mount('#app')