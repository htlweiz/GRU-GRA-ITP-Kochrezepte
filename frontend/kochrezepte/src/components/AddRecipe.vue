<template>
    <div class="add-recipe">
        <h2>Add a New Recipe</h2>
        <form @submit.prevent="submitRecipe">
            <div>
                <label for="title">Title:</label>
                <input type="text" v-model="recipe.title" id="title" required />
            </div>
            <div>
                <label for="description">Description:</label>
                <textarea type="text" v-model="recipe.description" id="description" required></textarea>
            </div>
            <div>
                <label for="cookingTime">Cooking Time:</label>
                <input type="number" v-model.number="recipe.cookingTime" id="cookingTime" required style="width: 80px; margin-right: 10px;" />
                <label for="preparationTime">Preparation Time:</label>
                <input type="number" v-model.number="recipe.preparationTime" id="preparationTime" required style="width: 80px;" />
            </div>
            <button type="submit">Add Recipe</button>
        </form>
    </div>
</template>

<script>

import axios from 'axios';

const APIURL = import.meta.env.VITE_BACKEND_API_URL + `/recipes/`;

export default {
    data() {
        return {
            recipe: {
                title: '',
                description: '',
                cookingTime: 0,
                preparationTime: 0,
                imagePath: '',
                userId: localStorage.getItem('userId')
            },
            token: localStorage.getItem('token')
        };
    },
    methods: {
        submitRecipe() {
            // Handle the form submission logic here

            const response = axios.post(APIURL, this.recipe, {
                headers: {
                    "Authorization": this.token
                }
            });

            console.log('Recipe submitted:', this.recipe);
            // Reset the form
            this.recipe = {
                title: '',
                description: '',
                cookingTime: 0,
                preparationTime: 0
            };
        }
    }
};
</script>

<style scoped>
.add-recipe {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    
}

.add-recipe h2 {
    text-align: center;
    margin-bottom: 20px;
    color: #333;
}

.add-recipe form div {
    margin-bottom: 15px;
}

.add-recipe label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    color: #555;
}

.add-recipe input,
.add-recipe textarea {
    width: calc(100% - 20px);
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
    background-color: white;
    color: black;
}

.add-recipe button {
    display: block;
    width: 100%;
    padding: 10px;
    background-color: #28a745;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
}

.add-recipe button:hover {
    background-color: #218838;
}

@media (max-width: 600px) {
    .add-recipe {
        padding: 10px;
    }

    .add-recipe input,
    .add-recipe textarea {
        width: calc(100% - 10px);
    }
}

</style>