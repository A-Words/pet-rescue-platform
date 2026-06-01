import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes: RouteRecordRaw[] = [
  { path: '/', name: 'Home', component: () => import('@/views/Home.vue') },
  { path: '/login', name: 'Login', component: () => import('@/views/Login.vue') },
  { path: '/register', name: 'Register', component: () => import('@/views/Register.vue') },

  // Lost Pets
  { path: '/lost-pets', name: 'LostPetList', component: () => import('@/views/lost-pets/LostPetList.vue') },
  { path: '/lost-pets/publish', name: 'LostPetPublish', component: () => import('@/views/lost-pets/LostPetPublish.vue'), meta: { requiresAuth: true } },
  { path: '/lost-pets/:lostPetId', name: 'LostPetDetail', component: () => import('@/views/lost-pets/LostPetDetail.vue') },
  { path: '/lost-pets/:lostPetId/clue', name: 'FoundClueSubmit', component: () => import('@/views/found-clues/FoundClueSubmit.vue'), meta: { requiresAuth: true } },

  // Adoption
  { path: '/adoption', name: 'AdoptablePetList', component: () => import('@/views/adoption/AdoptablePetList.vue') },
  { path: '/adoption/:adoptablePetId', name: 'AdoptablePetDetail', component: () => import('@/views/adoption/AdoptablePetDetail.vue') },
  { path: '/adoption/:adoptablePetId/apply', name: 'AdoptionApplicationForm', component: () => import('@/views/adoption/AdoptionApplicationForm.vue'), meta: { requiresAuth: true } },
  { path: '/my/applications', name: 'MyApplications', component: () => import('@/views/adoption/MyApplications.vue'), meta: { requiresAuth: true } },

  // Admin
  {
    path: '/admin',
    component: () => import('@/components/layout/AppSidebar.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      { path: '', name: 'AdminDashboard', component: () => import('@/views/admin/Dashboard.vue') },
      { path: 'pets', name: 'AdminPetManagement', component: () => import('@/views/admin/PetManagement.vue') },
      { path: 'clues', name: 'AdminClueManagement', component: () => import('@/views/admin/ClueManagement.vue') },
      { path: 'applications', name: 'AdminApplicationReview', component: () => import('@/views/admin/ApplicationReview.vue') },
      { path: 'statistics', name: 'AdminStatistics', component: () => import('@/views/admin/Statistics.vue') },
      { path: 'reminders', name: 'AdminVisitReminders', component: () => import('@/views/admin/VisitReminders.vue') },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _from, next) => {
  const userStore = useUserStore()

  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.meta.requiresAdmin && userStore.user?.role !== 'admin') {
    next({ name: 'Home' })
  } else {
    next()
  }
})

export default router
