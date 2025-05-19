// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { menuConfig } from './menuConfig.js'
import TheWelcomeView from '@/views/HomeView.vue'
import FinanceTrackerView from '@/views/ExpensesView.vue'
import BudgetView from '@/views/BudgetView.vue'
import SavingsView from '@/views/SavingsView.vue'

// Example
// const routes = [
//   { path: '/', component: HomeView },
//   { path: '/expense-tracker', component: ExpensesView },
//   { path: '/budget', component: BudgetView },
//   { path: '/savings', component: SavingsView },
// ]

// Dynamically add routes based on menuConfig
const routes = menuConfig.map(item => {
  return {path: item.path, component: () => import(`@/views/${item.label}View.vue`)}})

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router