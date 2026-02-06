import { createRouter, createWebHistory } from 'vue-router'
import { auth } from '../api/models/apis'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'

const routes = [
   { path: '/', name: 'Root', component: Login },
  { 
    path: '/login', 
    name: 'Login', 
    component: Login,
    meta: { requiresAuth: false } 
  },
  { 
    path: '/home', 
    name: 'Home', 
    component: Home,
    meta: { requiresAuth: true, requiresHomeAccess: true } 
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
    if (to.name === 'Login') {
        return next();
    }

    const isAuthenticated = await auth.checkAuth();

    if (to.meta.requiresAuth && !isAuthenticated) {
        return next({ 
            name: 'Login', 
            query: { redirect: to.fullPath } 
        });
    }

    if (to.meta.requiresHomeAccess && !isAuthenticated) {
        return next({ name: 'Login' });
    }

    next();
});

export default router