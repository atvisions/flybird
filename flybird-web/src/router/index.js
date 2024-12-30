import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ResetPasswordView from '../views/ResetPasswordView.vue'
import ProView from '../views/ProView.vue'
import FAQView from '../views/FAQView.vue'
import ResourcesView from '../views/ResourcesView.vue'
import ResumeTemplateView from '../views/ResumeTemplateView.vue'
import UserCenter from '@/views/user/UserCenter.vue'
import store from '../store'
import AboutView from '@/views/AboutView.vue'
import PrivacyView from '@/views/PrivacyView.vue'
import TermsView from '@/views/TermsView.vue'
import ContactView from '@/views/ContactView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: {
      guest: true
    }
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: {
      guest: true
    }
  },
  {
    path: '/reset-password',
    name: 'reset-password',
    component: ResetPasswordView,
    meta: {
      guest: true
    }
  },
  {
    path: '/pro',
    name: 'pro',
    component: ProView,
  },
  {
    path: '/faq',
    name: 'faq',
    component: FAQView,
  },
  {
    path: '/resources',
    name: 'resources',
    component: ResourcesView,
  },
  {
    path: '/templates',
    name: 'templates',
    component: ResumeTemplateView,
  },
  {
    path: '/user',
    name: 'UserCenter',
    component: UserCenter,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView,
    meta: { title: '关于我们' }
  },
  {
    path: '/privacy',
    name: 'privacy',
    component: PrivacyView,
    meta: { title: '隐私政策' }
  },
  {
    path: '/terms',
    name: 'terms',
    component: TermsView,
    meta: { title: '服务条款' }
  },
  {
    path: '/contact',
    name: 'contact',
    component: ContactView,
    meta: { title: '联系我们' }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

/// 路由守卫
router.beforeEach(async (to, from, next) => {
  // 检查是否需要认证
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 检查认证状态
    const isAuthenticated = await store.dispatch('checkAuth')
    
    if (!isAuthenticated) {
      // 未认证，跳转到登录页
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } 
  // 检查是否是游客专用页面（如登录页）
  else if (to.matched.some(record => record.meta.requiresGuest)) {
    const isAuthenticated = store.getters.isAuthenticated
    
    if (isAuthenticated) {
      // 已登录用户不能访问游客页面
      next({ path: '/' })
    } else {
      next()
    }
  } 
  else {
    next()
  }
})

export default router