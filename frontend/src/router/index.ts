import { createRouter, createWebHistory } from 'vue-router'

// 角色 → 路由路径。AuthView 登录后与路由守卫共用。
export const ROLE_ROUTE: Record<string, string> = {
  student: '/student',
  publisher: '/publisher',
  admin: '/admin',
  student_publisher: '/student-publisher',
}

// 把后端返回的原始 role 标准化为内部 role 标识
export function normalizeRole(raw: string): string {
  const r = (raw || 'student').toLowerCase()
  const map: Record<string, string> = { user: 'student', admin: 'admin', publisher: 'publisher', student_publisher: 'student_publisher' }
  return map[r] || 'student'
}

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'auth', component: () => import('../views/AuthView.vue') },
    { path: '/student', name: 'student', meta: { role: 'student' }, component: () => import('../views/StudentDashboardView.vue') },
    { path: '/publisher', name: 'publisher', meta: { role: 'publisher' }, component: () => import('../views/PublisherDashboardView.vue') },
    { path: '/admin', name: 'admin', meta: { role: 'admin' }, component: () => import('../views/AdminDashboardView.vue') },
    { path: '/student-publisher', name: 'student-publisher', meta: { role: 'student_publisher' }, component: () => import('../views/StudentPublisherDashboardView.vue') },
  ]
})

// 路由守卫：校验登录态 + 角色与目标路由匹配
router.beforeEach((to) => {
  if (to.name === 'auth') return true
  const raw = localStorage.getItem('user')
  if (!raw) return { name: 'auth' }
  let role = 'student'
  try { role = normalizeRole(JSON.parse(raw).role) } catch { return { name: 'auth' } }
  const target = ROLE_ROUTE[role] || '/student'
  // 访问的不是自己角色对应的页面，则重定向到自己的页面
  if (to.path !== target) return { path: target }
  return true
})

export default router
