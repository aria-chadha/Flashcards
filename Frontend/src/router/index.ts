import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../components/Login.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../components/Register.vue')
    },
    {
      path: '/',
      name: 'home',
      component: () => import('../components/Home.vue')
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../components/boutApp.vue')
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../components/Dash.vue')
    },{
      path: '/cards/',
      name: 'cards',
      component: () => import('../components/Cards.vue')
    },
    {
      path: '/card/',
      name: 'card',
      component: () => import('../components/EditCard.vue')
    }
    ,{
      path: '/review/',
      name: 'review',
      component: () => import('../components/Review.vue')
    },
    

  ]
})

export default router
