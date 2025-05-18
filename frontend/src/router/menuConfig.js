// src/router/menuConfig.js
export const menuConfig = [
  {
    path: '/',
    label: 'Home',
    icon: 'home', // string key, for future <Icon :name="…" />
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
]
