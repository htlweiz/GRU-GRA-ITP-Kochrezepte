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

    <button class="button" @click="navigateToRecipe">View Recipe</button>

    <template v-if="isCreator">
      <button class="button delete-button" @click="deleteRecipe">Delete</button>
      <button class="button update-button" @click="updateRecipe">Update</button>
    </template>

  </div>
</template>

<script setup>
import '../style.css'
import StarRating from 'vue-star-rating'
import { User, Clock } from 'lucide-vue-next'
import axios from 'axios';

const APIURL = import.meta.env.VITE_BACKEND_API_URL + `/recipes/`;

const props = defineProps({
  uuid: String,
  picUrl: String,
  recipeName: String,
  recipeDesc: String,
  creator: String,
  cookingTime: Number,
  preparationTime: Number,
  stars: Number,
  ratingsCount: Number,
  isCreator: Boolean
});

const truncate = (text, length) => {
  return text.length > length ? text.substring(0, length) + '...' : text;
}

const navigateToRecipe = () => {
  window.location.href = '/recipe/' + props.uuid;

}

const deleteRecipe = () => {
  if (confirm('Are you sure you want to delete this recipe?')) {

    const response = axios.delete(APIURL + props.uuid, {
      headers: { "Authorization": `Bearer ${localStorage.getItem('token')}` }
    })
      .then(response => {
        console.log('Recipe deleted:', response.data);
        window.location.reload();
      })
      .catch(error => {
        console.error('Error deleting recipe:', error);
      });
    console.log('Recipe deleted:', props.uuid);
  }
};

const updateRecipe = () => {
  // Logic to navigate to the update recipe page
  window.location.href = '/update-recipe/' + props.uuid;
};
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

.button {
  background-color: #2e3a59;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  margin-top: 10px;
  margin-left: 10px;
  margin-bottom: 5px;
}

.delete-button {
  background-color: #dc3545;
  margin-left: 10px;
}

.delete-button:hover {
  background-color: #c82333;
}

.update-button {
  background-color: #ffc107;
  margin-left: 10px;
}

.update-button:hover {
  background-color: #e0a800;
}

</style>
