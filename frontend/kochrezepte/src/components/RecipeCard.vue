<script setup>
import '../style.css'
import StarRating from 'vue-star-rating'

defineProps({
  recipeName: String,
  recipeDesc: String,
  creator: String,
  stars: Number,
})
</script>


<template>
  <div class="card">
    <h2>{{recipeName}}</h2>
    <p>{{ recipeDesc }}</p>

    <p>{{ creator }}</p>

    <div class="stars">
      <span v-for="i in stars" :key="i">⭐</span>
    </div>
    </div>
</template>

<style scoped>


</style>
