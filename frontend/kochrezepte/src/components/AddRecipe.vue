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
                <textarea v-model="recipe.description" id="description" required></textarea>
            </div>
            <div>
                <label for="cookingTime">Cooking Time (min):</label>
                <input type="number" v-model.number="recipe.cookingTime" id="cookingTime"/>
                <label for="preparationTime">Preparation Time (min):</label>
                <input type="number" v-model.number="recipe.preparationTime" id="preparationTime"/>
            </div>

            <div>
                <label for="imagePath">Image Path:</label>
                <input type="text" v-model="recipe.imagePath" id="imagePath" required />
            </div>

            <div>
                <label>Add Ingredients:</label>
                <multiselect
                    v-model="selectedIngredients"
                    :options="ingredients"
                    :multiple="true"
                    :searchable="true"
                    :close-on-select="false"
                    :show-labels="false"
                    track-by="ingredientId"
                    label="name"
                    placeholder="Search and select ingredients"
                    @select="onSelectIngredient"
                >
                    <template #option="{ option }">
                        <div class="custom-option">
                            <span>{{ option.name }}</span>
                        </div>
                    </template>
                </multiselect>
            </div>

            <div v-if="selectedIngredients.length">
                <h4>Selected Ingredients:</h4>
                <ul>
                    <li v-for="(ingredient, index) in selectedIngredients" :key="ingredient.ingredientId">
                        {{ ingredient.name }} 
                        <input 
                            type="number" 
                            v-model="ingredient.amount" 
                            placeholder="amount"   
                            style="width: 60px;"
                        />
                        <select v-model="ingredient.unit">
                            <option v-for="unit in units" :key="unit" :value="unit">
                                {{ unit }}
                            </option>
                        </select>
                        <button type="button" @click="removeIngredient(index)"> </button>
                    </li>
                </ul>
            </div>

            
            <button type="button" @click="addStep">Add Step</button>

            <div class="preparation-steps">
                
                <div v-for="(step, index) in preparation_steps" :key="index">
                    <label>Step {{ index + 1 }}</label>
                    <textarea v-model="step.description" placeholder="Enter step description"></textarea>
                    <button type="button" @click="removeStep(index)">
                        <X class="icon" />
                    </button>
                </div>
            </div>

            <button type="submit">Add Recipe</button>
        </form>
    </div>
</template>

<script>
import Multiselect from "vue-multiselect";
import axios from 'axios';
import { useToast } from 'vue-toast-notification';

import { Plus, X } from "lucide-vue-next";

const $toast = useToast();
const APIURL = import.meta.env.VITE_BACKEND_API_URL;
export default {
    components: { Multiselect, X, Plus },
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
            ingredients: [], 
            selectedIngredients: [],
            preparation_steps: [{ description: '', stepNumber: 1, recipeId: '' }],
            units: [],
            token: localStorage.getItem('token')
        };
    },
    methods: {
        submitRecipe() {
            this.recipe.userId = localStorage.getItem('userId');
            console.log('Submitting recipe:', this.recipe);
            axios.post(APIURL + `/recipes/`, this.recipe, {
                headers: { "Authorization": this.token }
            })
            .then((response) => {
                this.submitIngredients(response.data.recipeId);
                this.submitPreparationSteps(response.data.recipeId);
                this.resetForm();
            })
            .catch(error => console.error(error));

        },
        submitIngredients(id) {
            console.log('Submitting ingredients for recipe ID:', id);
            console.log('Selected ingredients:', this.selectedIngredients);
            console.log(this.selectedIngredients)
            this.selectedIngredients.forEach(ingredient => {
                const ingredientsubmit = {
                    amount: ingredient.amount,
                    unit: ingredient.unit
                };
                axios.post(APIURL + `/recipes/` + id + `/ingredient/` + ingredient.ingredientId + `/?amount=` + ingredient.amount + `&unit=`+ ingredient.unit , {
                    headers: { "Authorization": this.token }
                })
                .then(() => {
                    console.log('Ingredient submitted:', ingredient);
                })
                .catch(error => console.error(error));
            });
        },
        submitPreparationSteps(id) {
            console.log('Preparation steps:', this.preparation_steps);
            const preparation_steps = this.preparation_steps.map(step => ({
                description: step.description,
                stepNumber: step.stepNumber,
                recipeId: id
            }));
            preparation_steps.forEach(step => {
                axios.post(APIURL + `/preparation_steps/`, step ,{
                    headers: { "Authorization": this.token }
                })
                .then(() => {
                    console.log('Preparation step submitted:', step);
                })
                .catch(error => console.error(error));
            });
        },
        getIngredients() {
            axios.get(APIURL + `/ingredients/`)
                .then((response) => {
                    this.ingredients = response.data;
                })
                .catch(error => console.error(error));
        },
        onSelectIngredient(ingredient) {
            if (!this.selectedIngredients.some(i => i.ingredientId === ingredient.ingredientId)) {
                this.selectedIngredients.push({ 
                    ingredientId: ingredient.ingredientId, 
                    name: ingredient.name, 
                    quantity: 1, 
                    unit: "g" 
                });
            }
        },
        removeIngredient(index) {
            this.selectedIngredients.splice(index, 1);
        },
        addStep() {
            this.preparation_steps.push({ 
                stepNumber: this.preparation_steps.length + 1, 
                description: "" 
            });
        },
        removeStep(index) {
            this.preparation_steps.splice(index, 1);
            this.preparation_steps.forEach((step, i) => step.stepNumber = i + 1);
        },
        resetForm() {
            this.recipe = { title: '', description: '', cookingTime: 0, preparationTime: 0 };
            this.selectedIngredients = [];
            this.preparation_steps = [{ description: '', stepNumber: 1 }];
        },
        getUnits() {
            return axios.get(APIURL + `/units/`)
                .then((response) => {
                    this.units = response.data
                })
                .catch(error => console.error(error));
        }
    },
    mounted() {
        this.getIngredients();
        this.getUnits()
    }
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.css"></style>

<style scoped>
.add-recipe {
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 100%;
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

.multiselect__option {
    display: flex;
    align-items: center;
    gap: 8px;
}

.multiselect__option input[type="checkbox"] {
    width: 16px;
    height: 16px;
    accent-color: #28a745;
    cursor: pointer;
}

.multiselect__option span {
    font-size: 14px;
    color: #333;
}

ul {
    list-style: none;
    padding: 0;
}

ul li {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 5px;
}

.preparation-steps {
    display: flex;
    flex-direction: row;
}
</style>
