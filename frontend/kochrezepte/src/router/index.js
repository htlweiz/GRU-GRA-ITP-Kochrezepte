import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue';
import Home from '../components/Home.vue';
import RecipeDetailView from '../components/RecipeDetail.vue';
import Profile from '../components/Profile.vue';
import AddRecipe from '../components/AddRecipe.vue';
import UpdateRecipe from '../components/UpdateRecipe.vue';

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

  },
  {
    path: '/profile/:id',
    component: Profile,
    props: true

  },
  {
    path: '/add-recipe',
    component: AddRecipe

  },
  {
    path: '/update-recipe/:id',
    component: UpdateRecipe,
    props: true
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;