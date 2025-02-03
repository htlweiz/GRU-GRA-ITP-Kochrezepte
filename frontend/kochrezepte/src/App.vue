<template>
  <div>
    <div class="nav">
      <NavBar />
    </div>
    <div class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue';

export default {
  name: 'App',
  components: {
    NavBar
  }
};
</script>

<style>
html
{
  width: 100%;
}

.nav {
  position: fixed;
  top: 0;
  left: 0;
  background-color: #333;
  z-index: 1000;
}

.content {
  padding-top: 60px;
}
</style>
