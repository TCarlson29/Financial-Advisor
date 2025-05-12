// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import TheWelcomeView from '@/views/TheWelcomeView.vue'
import FinanceTrackerView from '@/views/FinanceTrackerView.vue'

const routes = [
  { path: '/', component: TheWelcomeView },
  { path: '/expense-tracker', component: FinanceTrackerView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router