import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue';
import Home from '../components/Home.vue';

const routes = [
  {
    path: '/login',
    component: Login
  },
  {
    path: '/home',
    component: Home
  },
  {
    path: '/',
    redirect: '/login'
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;