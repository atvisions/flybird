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
import config from './config'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css'

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
})

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(ElementPlus)
app.use(VueCropper)
app.use(router)
app.use(vuetify)

// 初始化应用
const initApp = async () => {
  try {
    const authStore = useAuthStore()
    await authStore.initialize()
    console.log('Auth initialized:', {
      isLoggedIn: authStore.isLoggedIn,
      token: localStorage.getItem('token')
    })
  } catch (error) {
    console.error('Auth initialization failed:', error)
  } finally {
    // 添加全局配置
    app.config.globalProperties.$toast = showToast
    window.$toast = showToast
    app.config.globalProperties.eventBus = eventBus
    app.config.globalProperties.$config = config
    
    // 最后挂载应用
    app.mount('#app')
  }
}

// 启动应用
initApp()