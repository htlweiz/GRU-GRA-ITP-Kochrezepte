<template>
    <div class="update-recipe">
        <h2>Update Recipe</h2>
        <form @submit.prevent="updateRecipe">
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
                <label>Update Ingredients:</label>
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

            <button type="submit">Update Recipe</button>
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
    props: ['id'],
    name: 'UpdateRecipe',
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
            token: localStorage.getItem('token'),
            recipeId: null
        };
    },
    methods: {
        updateRecipe() {
            console.log('Updating recipe:', this.recipe);
            console.log(this.token);
            axios.put(APIURL + `/recipes/` + this.recipeId, this.recipe, {
                headers: { "Authorization": `Bearer ${this.token}` }
            })
            .then(() => {
                this.updateIngredients();
                this.updatePreparationSteps();
                $toast.success('Recipe updated successfully!');
            })
            .catch(error => console.error(error));
        },
        updateIngredients() {
            console.log('Updating ingredients for recipe ID:', this.recipeId);
            this.selectedIngredients.forEach(ingredient => {
                axios.post(APIURL + `/recipes/` + this.recipeId + `/ingredient/` + ingredient.ingredientId, {
                    amount: ingredient.amount,
                    unit: ingredient.unit
                }, {
                    headers: { "Authorization": `Bearer ${this.token}` }
                })
                .then(() => {
                    console.log('Ingredient updated:', ingredient);
                })
                .catch(error => console.error(error));
            });
        },
        updatePreparationSteps() {
            console.log('Updating preparation steps:', this.preparation_steps);
            this.preparation_steps.forEach(step => {
                if (step.stepId == undefined)
                {
                    console.log('Creating new preparation step:', step);
                    axios.post(APIURL + `/preparation_steps/`, {
                        description: step.description,
                        stepNumber: step.stepNumber,
                        recipeId: this.recipeId
                    }, {
                        headers: { "Authorization": `Bearer ${this.token}` }
                    })
                }
                axios.put(APIURL + `/preparation_steps/` + step.stepId, step, {
                    headers: { "Authorization": `Bearer ${this.token}` }
                })
                .then(() => {
                    console.log('Preparation step updated:', step);
                })
                .catch(error => console.error(error));
            });
        },
        fetchRecipe() {
            axios.get(APIURL + `/recipes/` + this.recipeId, {
                headers: { "Authorization": this.token }
            })
            .then((response) => {
                this.recipe = response.data;
                this.fetchIngredients();
                this.fetchPreparationSteps();

                console.log('Fetched recipe:', this.recipe);
            })
            .catch(error => console.error(error));
        },
        fetchPreparationSteps() {
            axios.get(APIURL + `/recipes/` + this.recipeId + `/preparation_steps/`, {
                headers: { "Authorization": this.token }
            })
            .then((response) => {
                this.preparation_steps = response.data;
                console.log('Fetched preparation steps:', this.preparation_steps);
            })
            .catch(error => console.error(error));
        },
        fetchIngredients() {
            axios.get(APIURL + `/recipes/` + this.recipeId + `/ingredients/`, {
                headers: { "Authorization": this.token }
            })
            .then((response) => {
                this.selectedIngredients = response.data;
                console.log('Fetched ingredients:', this.selectedIngredients);
            })
            .catch(error => console.error(error));
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
        getUnits() {
            return axios.get(APIURL + `/units/`)
                .then((response) => {
                    this.units = response.data
                })
                .catch(error => console.error(error));
        }
    },
    mounted() {
        this.recipeId = this.$route.params.id;
        this.fetchRecipe();
        this.getIngredients();
        this.getUnits();
    }
};
</script>
<style scoped>
.update-recipe {
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.update-recipe h2 {
    text-align: center;
    margin-bottom: 20px;
    color: #333;
    font-size: 24px;
    font-weight: bold;
}

.update-recipe form div {
    margin-bottom: 15px;
    width: 100%;
}

.update-recipe label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    color: #555;
}

.update-recipe input,
.update-recipe textarea {
    width: calc(100% - 20px);
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
    background-color: white;
    color: black;
    font-size: 14px;
}

.update-recipe button {
    padding: 10px 20px;
    background-color: #28a745;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s ease;
}

.update-recipe button:hover {
    background-color: #218838;
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

ul li input[type="number"] {
    width: 60px;
    padding: 5px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
}

ul li select {
    padding: 5px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
}

.preparation-steps {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 100%;
}

.preparation-steps textarea {
    width: calc(100% - 20px);
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
    font-size: 14px;
}

.preparation-steps button {
    background-color: #dc3545;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 5px 10px;
    cursor: pointer;
    font-size: 12px;
    transition: background-color 0.3s ease;
}

.preparation-steps button:hover {
    background-color: #c82333;
}

</style>