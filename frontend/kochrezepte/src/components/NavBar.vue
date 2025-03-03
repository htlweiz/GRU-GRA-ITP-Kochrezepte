<template>
  <nav class="navbar">
    <router-link to="/" class="logo">Schmeckify</router-link>
    <ul>
      <li><router-link to="/home">Home</router-link></li>
      <li><router-link to="/contact">Contact</router-link></li>
      <li v-if="!isLoginPage && !loggedIn"><router-link to="/login">Login</router-link></li>
      <li v-if="loggedIn"><router-link :to="link"><User/></router-link></li>
    </ul>
  </nav>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { User } from 'lucide-vue-next';

const route = useRoute();
const isLoginPage = computed(() => route.path === '/login');
const loggedIn = computed(() => localStorage.getItem('token') !== null);
const userId = computed(() => localStorage.getItem('userId'));

const link = computed(() => {
  if (loggedIn.value) {
    return `/profile/${userId.value}`;
  }
  return '/login';
});

</script>

<style scoped>
.navbar {
  width: 100%;
  height: 60px; /* Adjust height as needed */
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #333;
  color: white;
  position: fixed;
  top: 0;
  left: 0;
}
.navbar ul {
  list-style: none;
  display: flex;
  margin-right: 10px;
  gap: 20px;
}
.navbar ul li a {
  text-decoration: none;
  color: white;
  font-weight: bold;
}
.logo {
  font-size: 24px;
  font-weight: bold;
  margin-left: 10px;
  color: white;
  text-decoration: none;
}
</style>
