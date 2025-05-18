// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import CategorySelect from '@/components/CategorySelect.vue'

const app = createApp(App)
app.use(router)
app.component('CategorySelect', CategorySelect)
app.mount('#app')