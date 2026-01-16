import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'

const routes = [
   { path: '/', name: 'Root', component: Login },
  { 
    path: '/login', 
    name: 'Login', 
    component: Login,
  },
  { 
    path: '/home', 
    name: 'Home', 
    component: Home,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router