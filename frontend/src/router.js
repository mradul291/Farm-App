import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Register',
    component: () => import('@/component/userSelection.vue'),
  },
]

let router = createRouter({
  history: createWebHistory('/signup'),
  routes,
})

export default router
