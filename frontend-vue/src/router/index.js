import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// Import views with lazy loading for better performance
import Home from '../views/Home.vue'
const Login = () => import('../views/Login.vue')
const Register = () => import('../views/Register.vue')
const Dashboard = () => import('../views/Dashboard.vue')
const Profile = () => import('../views/Profile.vue')
const Application = () => import('../views/Application.vue')
const MyApplications = () => import('../views/MyApplications.vue')
const AdminPanel = () => import('../views/AdminPanel.vue')
const NoAccess = () => import('../views/NoAccess.vue')

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresGuest: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  },
  {
    path: '/application',
    name: 'Application',
    component: Application,
    meta: { requiresAuth: true, requiresStudent: true }
  },
  {
    path: '/my-applications',
    name: 'MyApplications',
    component: MyApplications,
    meta: { requiresAuth: true, requiresStudent: true }
  },
  {
    path: '/admin',
    name: 'AdminPanel',
    component: AdminPanel,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/no-access',
    name: 'NoAccess',
    component: NoAccess
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Initialize auth store if not already done
  if (!authStore.user && authStore.token) {
    await authStore.getProfile()
  }
  
  // Check if route requires authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }
  
  // Check if route requires guest (not authenticated)
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/dashboard')
    return
  }
  
  // Check if route requires admin role
  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next('/no-access')
    return
  }
  
  // Check if route requires student role
  if (to.meta.requiresStudent && !authStore.isStudent) {
    next('/no-access')
    return
  }
  
  next()
})

export default router
