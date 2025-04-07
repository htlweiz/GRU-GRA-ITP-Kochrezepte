<template>
    <div class="recipes-page max-w-6xl mx-auto px-4 py-8">
      <div class="recipes flex flex-wrap justify-center gap-6">
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
        />
      </div>
  
      <div class="pagination mt-10 flex justify-center gap-3 items-center">
        <button
          @click="changePage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="px-4 py-2 bg-gray-300 hover:bg-gray-400 text-sm rounded disabled:opacity-50"
        >
          Prev
        </button>
  
        <span class="text-sm">Page {{ currentPage }} of {{ totalPages }}</span>
  
        <button
          @click="changePage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="px-4 py-2 bg-gray-300 hover:bg-gray-400 text-sm rounded disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted, computed } from 'vue'; 
  import RecipeCard from './RecipeCard.vue';
  import axios from 'axios';
  
  const APIURL = import.meta.env.VITE_BACKEND_API_URL + `/recipes/public/`;
  
  export default {
    components: {
      RecipeCard,
    },
    setup() {
      const recipes = ref([]);
      const currentPage = ref(1);
      const pageSize = ref(4);
      const totalItems = ref(0);
  
      const totalPages = computed(() => {
        return Math.ceil(totalItems.value / pageSize.value);
      });
  
      const fetchRecipes = () => {
        axios
          .get(APIURL, {
            params: {
              page: currentPage.value,
              size: pageSize.value,
            },
          })
          .then((response) => {
            recipes.value = response.data.items;
            totalItems.value = response.data.total;
          })
          .catch((error) => {
            console.error('Failed to fetch recipes:', error);
          });
      };
  
      const changePage = (newPage) => {
        if (newPage >= 1 && newPage <= totalPages.value) {
          currentPage.value = newPage;
          fetchRecipes();
        }
      };
  
      onMounted(() => {
        fetchRecipes();
      });
  
      return {
        recipes,
        currentPage,
        totalPages,
        changePage,
      };
    },
  };
  </script>
  
  <style scoped>
  .recipes {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1.5rem;    
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
  
  </style>
  