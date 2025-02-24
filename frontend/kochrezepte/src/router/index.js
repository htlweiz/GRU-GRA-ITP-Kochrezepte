import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue';
import Home from '../components/Home.vue';
import RecipeDetailView from '../components/RecipeDetail.vue';

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
  },
  {
    path: '/recipe/:id',
    component: RecipeDetailView,
    props: true

  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;