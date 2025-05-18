// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import TheWelcomeView from '@/views/TheWelcomeView.vue'
import FinanceTrackerView from '@/views/FinanceTrackerView.vue'
import BudgetView from '@/views/BudgetView.vue'

const routes = [
  { path: '/', component: TheWelcomeView },
  { path: '/expense-tracker', component: FinanceTrackerView },
  { path: '/budget', component: BudgetView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router