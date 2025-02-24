<template>
    <div class="recipes">
        <RecipeCard v-for="recipe in recipes" :key="recipe.recipeId" :uuid="recipe.recipeId" :picUrl="recipe.imagePath" :recipeName="recipe.title" :recipeDesc="recipe.description" :creator="recipe.userName" :cookingTime="recipe.cookingTime" :preparationTime="recipe.preparationTime" :stars=recipe.stars :ratingsCount=recipe.ratingAmount />
    </div>
</template>

<script>
import { onMounted } from 'vue';
import RecipeCard from './RecipeCard.vue'
import { ref } from 'vue';
import axios from 'axios';


const APIURL = import.meta.env.VITE_BACKEND_API_URL + `/recipes/public/`;

export default {
    components: {
        RecipeCard
    },
    setup() {
        const recipes = ref([]);
        onMounted(() => {
            getRecipes();
        });

        const getRecipes = () => {
            console.log(APIURL);
            axios.get(APIURL)
                .then((response) => {
                    recipes.value = response.data['items']; // TODO: Pagination
                    console.log(recipes.value);
                })
                .catch((error) => {
                    console.error(error);
                });
        };

        return {
            recipes,
            getRecipes
        };
    },
    methods: {
        getRecipes() {
            console.log(APIURL);
            axios.get(APIURL)
                .then((response) => {
                    recipes = response.data['items']; // TODO: Pagination
                    console.log(recipes);
                    for (var i in recipes)
                    {
                    console.log(recipes[i]);
                    }
                })
                .catch((error) => {
                    console.error(error);
                });
        },
    },
    created() {
        this.getRecipes();
        if (localStorage.getItem('reloaded')) {
            localStorage.removeItem('reloaded');
        } else {
            localStorage.setItem('reloaded', '1');
            location.reload();
        }
    },
};


</script>

<style scoped>

.recipes {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: stretch;
}



</style>
