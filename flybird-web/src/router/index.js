import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ResetPasswordView from '../views/ResetPasswordView.vue'
import ProView from '../views/ProView.vue'
import FAQView from '../views/FAQView.vue'
import ResourcesView from '../views/ResourcesView.vue'
import UserCenter from '@/views/user/UserCenter.vue'
import store from '../store'
import AboutView from '@/views/AboutView.vue'
import PrivacyView from '@/views/PrivacyView.vue'
import TermsView from '@/views/TermsView.vue'
import ContactView from '@/views/ContactView.vue'
import CommunityView from '@/views/community/CommunityView.vue'
import CommunityHomeView from '@/views/community/HomeView.vue'
import UserPageView from '../views/user/UserPageView.vue'
import SearchView from '@/views/search/SearchView.vue'
import PortfolioHomeView from '@/views/portfolio/HomeView.vue'

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
    component: () => import('@/views/resume/ResumeView.vue'),
    children: [
      {
        path: '',
        name: 'templates-home',
        component: () => import('@/views/resume/TemplatesView.vue')
      },
      {
        path: 'resume',
        name: 'templates-resume',
        component: () => import('@/views/resume/ResumeTemplatesView.vue')
      },
      {
        path: 'cover-letter',
        name: 'templates-cover-letter',
        component: () => import('@/views/resume/CoverLetterView.vue')
      },
      {
        path: 'bio',
        name: 'templates-bio',
        component: () => import('@/views/resume/BioView.vue')
      }
    ]
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
  },
  {
    path: '/u/:username',
    name: 'UserPage',
    component: UserPageView,
    props: true,
    meta: {
      title: '个人主页'
    }
  },
  {
    path: '/community',
    component: CommunityView,
    children: [
      {
        path: '',
        name: 'CommunityHome',
        component: CommunityHomeView
      },
      {
        path: 'articles',
        name: 'Articles',
        component: () => import('@/views/community/ArticlesView.vue')
      },
      {
        path: 'questions',
        name: 'Questions',
        component: () => import('@/views/community/QuestionsView.vue')
      },
      {
        path: 'topics',
        name: 'Topics',
        component: () => import('@/views/community/TopicsView.vue')
      },
      {
        path: 'profile',
        component: () => import('@/views/user/MyProfile/index.vue')
      },
      {
        path: 'resumes',
        component: () => import('@/views/user/MyResumes.vue')
      },
      {
        path: 'messages',
        component: () => import('@/views/user/MyProfile/components/MyMessages.vue')
      },
      {
        path: 'settings',
        component: () => import('@/views/user/AccountSettings.vue')
      }
    ]
  },
  {
    path: '/portfolio',
    name: 'portfolio',
    component: () => import('@/views/portfolio/PortfolioView.vue'),
    children: [
      {
        path: '',
        name: 'portfolio-home',
        component: PortfolioHomeView
      },
      {
        path: 'design',
        name: 'portfolio-design',
        component: () => import('@/views/portfolio/DesignView.vue')
      },
      {
        path: 'video',
        name: 'portfolio-video',
        component: () => import('@/views/portfolio/VideoView.vue')
      },
      {
        path: 'animation',
        name: 'portfolio-animation',
        component: () => import('@/views/portfolio/AnimationView.vue')
      },
      {
        path: 'photo',
        name: 'portfolio-photo',
        component: () => import('@/views/portfolio/PhotoView.vue')
      }
    ]
  },
  {
    path: '/search',
    component: SearchView,
    children: [
      {
        path: '',
        name: 'SearchAll',
        component: SearchView
      },
      {
        path: 'articles',
        name: 'SearchArticles',
        component: SearchView
      },
      {
        path: 'portfolio',
        name: 'SearchPortfolio',
        component: SearchView
      },
      {
        path: 'users',
        name: 'SearchUsers',
        component: SearchView
      }
    ]
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