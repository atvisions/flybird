import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MyFavorites from '../views/user/MyFavorites.vue'
import MyMessages from '../views/user/MyMessages.vue'
// 其他导入...

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/favorites',
    name: 'favorites',
    component: MyFavorites
  },
  {
    path: '/messages',
    name: 'messages',
    component: MyMessages
  },
  // 其他路由...
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router 