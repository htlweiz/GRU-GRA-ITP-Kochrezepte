<template>
    <div class="profile-container">
        <div class="profile">
            <User size="50" />
            <h2>{{ user.firstName }} {{ user.lastName }}</h2>
            <p>{{ user.email }}</p>
            <button class="logout-btn" @click="LogOut">Log Out</button>
        </div>
        <div>
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
    </div>
</template>

<script>
import { LogOut, User } from 'lucide-vue-next';
import RecipeCard from './RecipeCard.vue';
import axios from 'axios';

const USERAPIURL = import.meta.env.VITE_BACKEND_API_URL + `/users/`;
const APIURL = import.meta.env.VITE_BACKEND_API_URL + `/recipes/public/`;

export default {
    props: ['id'],
    components: {
        RecipeCard,
        User
    },
    data() {
        return {
            user: {
                firstName: '',
                lastName: '',
                email: ''
            },
            recipes: [],
            token: localStorage.getItem('token')
        };
    },
    methods: {
        async getUser() {
            try {
                const response = await axios.get(USERAPIURL + this.id, {
                    headers: { "Authorization": `Bearer ${this.token}` }
                });
                this.user = response.data;
            } catch (error) {
                console.error('Error fetching user:', error);
            }
        },
        async getRecipes() {
            try {
                const response = await axios.get(APIURL + this.id, {
                    headers: { "Authorization": `Bearer ${this.token}` }
                });
                this.recipes = response.data.items;
                this.recipes.forEach(recipe => {
                    recipe.isCreator = recipe.userId === localStorage.getItem('userId');
                });
            } catch (error) {
                console.error('Error fetching recipes:', error);
            }
        },
        LogOut() {
            localStorage.removeItem('token');
            localStorage.removeItem('userId');
            localStorage.removeItem('username');
            localStorage.removeItem('email');
            this.$router.push('/home');
        },
        AddRecipe() {
            this.$router.push('/add-recipe');
        }
    },
    mounted() {
        this.getUser();
        this.getRecipes();
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
