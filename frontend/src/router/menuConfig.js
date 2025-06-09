// src/router/menuConfig.js
// Make sure to name the views as <label>View.vue for index.js to automatically populate the NavBar route correctly
export const menuConfig = [
  {
    path: '/',
    label: 'Home',
    icon: 'home',
    order: 1,
    group: null
  },
  {
    path: '/expense-tracker',
    label: 'Expenses',
    icon: 'receipt',
    order: 2,
    group: 'Tracker'
  },
  {
    path: '/budget',
    label: 'Budget',
    icon: 'piggy-bank',
    order: 3,
    group: 'Tracker'
  },
  {
    path: '/savings',
    label: 'Savings',
    icon: 'money-bill',
    order: 4,
    group: 'Tracker'
  }
]
