import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: () => import('../views/HomepageView.vue') },
    { path: '/login', name: 'auth', component: () => import('../views/AuthView.vue') },
    { path: '/dashboard', name: 'dashboard', component: () => import('../views/DashboardView.vue') },
  ]
})

export default router
