import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ResetPasswordView from '../views/ResetPasswordView.vue'
import ProView from '../views/ProView.vue'
import FAQView from '../views/FAQView.vue'
import ResourcesView from '../views/ResourcesView.vue'
import UserCenter from '@/views/user/UserCenter.vue'
import AboutView from '@/views/AboutView.vue'
import PrivacyView from '@/views/PrivacyView.vue'
import TermsView from '@/views/TermsView.vue'
import ContactView from '@/views/ContactView.vue'
import CommunityView from '@/views/community/CommunityView.vue'
import CommunityHomeView from '@/views/community/HomeView.vue'
import UserPageView from '../views/user/UserPageView.vue'
import SearchView from '@/views/search/SearchView.vue'
import PortfolioHomeView from '@/views/portfolio/HomeView.vue'
import PortfolioView from '@/views/portfolio/PortfolioView.vue'
import DesignView from '@/views/portfolio/DesignView.vue'
import PortfolioDetailView from '@/views/portfolio/PortfolioDetailView.vue'
import { useAuthStore } from '@/stores/auth'
import { useAccountStore } from '@/stores/account'

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
    component: () => import('@/views/resume/ResumeView.vue'),
    children: [
      {
        path: '',
        name: 'resume-home',
        redirect: '/templates/resume'
      },
      {
        path: 'resume',
        name: 'templates-resume',
        component: () => import('@/views/resume/TemplatesView.vue')
      },
      {
        path: 'cover-letter',
        name: 'templates-cover-letter',
        component: () => import('@/views/resume/CoverLetterView.vue')
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
        path: 'article/:id',
        name: 'ArticleDetail',
        component: () => import('@/views/community/ArticleDetail.vue')
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
        path: 'topic/:id',
        name: 'TopicDetail',
        component: () => import('@/views/community/TopicDetail.vue')
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
      },
      {
        path: 'question/:id',
        name: 'QuestionDetail',
        component: () => import('@/views/community/QuestionDetail.vue'),
        meta: { title: '问答详情' }
      },
      {
        path: 'create',
        name: 'CreateContent',
        component: () => import('@/views/community/CreateContent.vue'),
        meta: { 
          title: '发布内容',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: '/portfolio',
    component: PortfolioView,
    children: [
      {
        path: '',
        name: 'portfolio-home',
        component: PortfolioHomeView
      },
      {
        path: 'design',
        name: 'portfolio-design',
        component: DesignView
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
    path: '/portfolio/:id',
    name: 'PortfolioDetail',
    component: PortfolioDetailView,
    props: true,
    meta: {
      requiresAuth: false,
      title: '作品详情'
    }
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
  const authStore = useAuthStore()
  const accountStore = useAccountStore()

  // 检查路由是否需要认证
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  // 如果已经登录且有 token
  if (authStore.isLoggedIn && localStorage.getItem('token')) {
    // 如果没有用户信息，尝试获取
    if (!accountStore.userInfo) {
      try {
        await accountStore.fetchUserInfo()
      } catch (error) {
        console.error('Failed to fetch user info:', error)
        if (error.response?.status === 401) {
          // token 失效，清除登录状态
          authStore.clearAuth()
          next('/login')
          return
        }
      }
    }
    
    // 如果要去登录页，重定向到首页
    if (to.path === '/login') {
      next('/user?tab=home')
      return
    }
    
    next()
    return
  }

  // 如果页面需要认证且用户未登录
  if (requiresAuth && !authStore.isLoggedIn) {
    // 保存目标路由，登录后跳转
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
    return
  }

  // 其他情况放行
  next()
})

export default router