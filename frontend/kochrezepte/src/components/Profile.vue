<template>
    <div class="profile-container">
      <div class="profile">
        <User size="50" />
        <h2>{{ user.firstName }} {{ user.lastName }}</h2>
        <p>{{ user.email }}</p>
        <button class="logout-btn" @click="LogOut">Log Out</button>
      </div>
  
      <div class="actions">
        <button @click="AddRecipe">Add Recipe</button>
      </div>
  
      <div class="recipes">
        <RecipeCard 
          v-for="recipe in recipes" 
          :key="recipe.recipeId" 
          :uuid="recipe.recipeId" 
          :picUrl="recipe.imagePath" 
          :recipeName="recipe.title" 
          :recipeDesc="recipe.description" 
          :creator="recipe.userName" 
          :cookingTime="recipe.cookingTime" 
          :preparationTime="recipe.preparationTime" 
          :stars="recipe.stars" 
          :ratingsCount="recipe.ratingAmount"
          :isCreator="recipe.isCreator"
        />
      </div>
  
      <div class="pagination">
        <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1">Prev</button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages">Next</button>
      </div>
    </div>
  </template>
  

  <script>
  import { LogOut, User } from 'lucide-vue-next';
  import RecipeCard from './RecipeCard.vue';
  import axios from 'axios';
  import { ref, computed } from 'vue';
  
  const USERAPIURL = import.meta.env.VITE_BACKEND_API_URL + `/users/`;
  const APIURL = import.meta.env.VITE_BACKEND_API_URL + `/recipes/public/`;
  
  export default {
    props: ['id'],
    components: {
      RecipeCard,
      User
    },
    setup(props) {
      const user = ref({ firstName: '', lastName: '', email: '' });
      const recipes = ref([]);
      const token = localStorage.getItem('token');
  
      const currentPage = ref(1);
      const pageSize = ref(3);
      const totalItems = ref(0);
  
      const totalPages = computed(() => Math.ceil(totalItems.value / pageSize.value));
  
      const getUser = async () => {
        try {
          const response = await axios.get(USERAPIURL + props.id, {
            headers: { "Authorization": `Bearer ${token}` }
          });
          user.value = response.data;
        } catch (error) {
          console.error('Error fetching user:', error);
        }
      };
  
      const getRecipes = async () => {
        try {
          const response = await axios.get(APIURL + props.id, {
            headers: { "Authorization": `Bearer ${token}` },
            params: {
              page: currentPage.value,
              size: pageSize.value
            }
          });
          recipes.value = response.data.items;
          totalItems.value = response.data.total;
          recipes.value.forEach(recipe => {
            recipe.isCreator = recipe.userId === localStorage.getItem('userId');
          });
        } catch (error) {
          console.error('Error fetching recipes:', error);
        }
      };
  
      const changePage = (newPage) => {
        if (newPage >= 1 && newPage <= totalPages.value) {
          currentPage.value = newPage;
          getRecipes();
        }
      };
  
      const LogOut = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('userId');
        localStorage.removeItem('username');
        localStorage.removeItem('email');
        window.location.href = '/home';
      };
  
      const AddRecipe = () => {
        window.location.href = '/add-recipe';
      };
  
      getUser();
      getRecipes();
  
      return {
        user,
        recipes,
        currentPage,
        totalPages,
        changePage,
        LogOut,
        AddRecipe
      };
    }
  };
  </script>
  
<style scoped>
.profile-container {
    display: flex;
    flex-direction: column;
    padding: 20px;
    background-color: #f0f2f5;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.profile {
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #fff;
    width: 100%;
    max-width: 400px;
    text-align: center;
    margin-bottom: 20px;
}

button {
    padding: 10px 20px;
    margin: 10px 5px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

button:hover {
    background-color: #0056b3;
}

.logout-btn {
    background-color: #dc3545;
}

.logout-btn:hover {
    background-color: #c82333;
}

.recipes {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: stretch;
    gap: 20px;
}

h3 {
    margin-bottom: 20px;
    color: #333;
}
</style>
