
<template>
  <div class="card">
    <img :src="picUrl"/>
    <h2>{{recipeName}}</h2>
    <div class="star-rating">
    <star-rating :rating="stars" :read-only="true" :round-start-rating="false" :max-rating="5" :animate="true" :star-size="20"></star-rating>
    <h5>({{ ratingsCount }})</h5>
    </div>
    <p>{{ truncate(recipeDesc, 200) }}</p>

    <div class="cooking-time">
      <Clock color="#2e3a59"/>
      <h4>{{ cookingTime }} min</h4>
    </div>

    <div class="creator">
      <User color="#2e3a59"/>
      <h4>{{ creator }}</h4>
    </div>
    
    
    </div>
</template>

<script setup>
import '../style.css'
import StarRating from 'vue-star-rating'
import { User, Clock } from 'lucide-vue-next'

defineProps({
  picUrl: String,
  recipeName: String,
  recipeDesc: String,
  creator: String,
  cookingTime: Number,
  stars: Number,
  ratingsCount: Number
})

const truncate = (text, length) => {
  return text.length > length ? text.substring(0, length) + '...' : text;
}

</script>

<style scoped>

.card img {
  width: 100%;
  border-radius: 5px;
}

.card h2
{
  padding-left: 10px;
  font-weight: 600;
  color: #2e3a59;
}

.card p
{
  padding-left: 10px;
  color: #2e3a59;
  font-style: italic;
}

.card h4
{
  padding-left: 10px;
  color: #2e3a59;
}

.star-rating
{
  padding-left: 10px;
  display: flex;
  align-items: center;
  color: #2e3a59;
  gap: 5px;
}

.creator
{
  display: flex;
  align-items: center;
  padding-left: 10px;
  color: #2e3a59;
}

.cooking-time
{
  display: flex;
  align-items: center;
  padding-left: 10px;
  color: #2e3a59;
}



</style>
