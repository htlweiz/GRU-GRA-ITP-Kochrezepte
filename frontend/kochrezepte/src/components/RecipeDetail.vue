<template>
  <div class="recipe-container">
    <img class="image-right" src="../../public/image.jpg"/>
    
    <div class="recipe-detail-right">
      <h2>{{ this.recipe.title }}</h2>
      <p>
        {{ this.recipe.description }}
      </p>
      <div class="time-container">
        <div class="time-box">
          <Clock size=24 />
          <div class="time-text">
            <h4> Koch-/Backzeit: {{ this.recipe.cookingTime }} min</h4>
          </div>
        </div>
        <div class="time-box">
          <Clock size=24 />
          <div class="time-text">
            <h4> Zubereitungszeit: {{this.recipe.preparationTime}} min</h4>
          </div>
        </div>
        <div class="time-box">
          <Clock size=24 />
          <div class="time-text">
            <h4> Gesamtzeit: {{this.recipe.cookingTime + this.recipe.preparationTime}} min</h4>
          </div>
        </div>
      </div>
      
      <div class="star-rating">
        <star-rating
          :rating="this.recipe.stars"
          :round-start-rating="false"
          :max-rating="5"
          :animate="true"
          :star-size="20"
          :active-on-click="true"
          @update:rating="setRating"
        ></star-rating>
        <h5>({{this.recipe.ratingAmount}})</h5>
      </div>
      <div class="creator">
        <User size="24" />
        <p>{{ this.recipe.userName }}</p>
      </div>
      <div class="ingredients-preparation-container">
      <div class="ingredients-box">
        <h3>Zutaten</h3>
        <div class="ingredients-list">
          <span v-for="(i, index) in IngredientsItems" :key="i.ingredientId">
            {{ i.amount ? i.amount + " " + i.unit : "" }} <strong>{{ truncate(i.name, 50) }}</strong>
          </span>
        </div>
      </div>
    <div class="preparation-box">
      <h3>Zubereitung</h3>
      <div class="preparation-list">
        <span v-for="(i) in PreparationItems" :key="i.stepId">
          <strong>{{ i.stepNumber }}.</strong> {{ i.description }}
        </span>
      </div>
    </div>
  </div>
  </div>
  </div>
</template>

<script>
import StarRating from "vue-star-rating";
import { User, Clock } from "lucide-vue-next";
import axios from "axios";
import {ref, onMounted} from 'vue';
import { defineProps } from 'vue';

const APIURL = import.meta.env.VITE_BACKEND_API_URL + `/recipes/`;

export default {
  props: ['id'],
  data() {
    return {
      recipe: {
        title: '',
        description: '',
        cookingTime: 0,
        preparationTime: 0,
        stars: 0,
        ratingAmount: 0,
      },
      IngredientsItems: {description: "", recipeId: "", stepId: "",stepNumber: 0},
      PreparationItems: {amount: 0, recipeId: "", ingredientId: "", unit: "", name: ""},
      rating: 0,
    };
  },
  setup() {
    const recipe = ref({});
    const IngredientsItems = ref({});
    const PreparationItems = ref({});
  },
  components: {
    StarRating,
    User,
    Clock,
  },
  methods: {
    getRecipe() {
      axios.get(APIURL + this.id)
        .then((response) => {
          this.recipe = response.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getIngredients(recipeId) {
      axios.get(APIURL + recipeId + '/ingredients/')
        .then((response) => {
          this.IngredientsItems = response.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getPreparationSteps(recipeId)
    {
      axios.get(APIURL + recipeId + '/preparation_steps/')
        .then((response) => {
          this.PreparationItems = response.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    truncate(text, length) {
      return text.length > length ? text.substring(0, length) + '...' : text;
    },
    setRating(rating) {
      this.rating = rating
      console.log(rating)
    }
  },
  created() {
    this.getRecipe();
    this.getIngredients(this.id);
    this.getPreparationSteps(this.id);
  },
  onMounted()
  {
    this.getRecipe();
    this.getIngredients(this.id);
    this.getPreparationSteps(this.id);
  }

};

</script>

<style scoped>
.recipe-container {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
}

.image-right {
  width: 40%;
  height: auto;
  object-fit: cover;
}

.recipe-detail-right {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 10px;
  width: 55%;
}

h2 {
  font-weight: 600;
  color: #2e3a59;
  margin-bottom: 5px;
}

p {
  color: #2e3a59;
  font-style: italic;
  margin: 0;
}

.time-container {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.time-box {
  display: flex;
  align-items: center;
  background-color: #e3e1e0;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 14px;
}

.time-text {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.time-box h4 {
  font-size: 14px;
  margin: 0;
}

.clock-icon {
  width: 18px;
  height: 18px;
}

.creator {
  display: flex;
  align-items: center;
}


.star-rating
{
  padding-left: 10px;
  display: flex;
  align-items: center;
  color: #2e3a59;
  gap: 5px;
}

.ingredients-preparation-container {
  display: flex;
  justify-content: space-between;
  gap: 50px;
  align-items: flex-start;
  flex-wrap: wrap;
}

.ingredients-box, .preparation-box {
  width: 50%;
  min-width: 250px;
  padding: 20px;
  box-sizing: border-box;
  border: 1px solid #ddd; /* Dünner Rand für ein elegantes Aussehen */
  border-radius: 8px; /* Abgerundete Ecken für weicheren Look */
  background-color: #f9f9f9; /* Heller Hintergrund, um es hervorzuheben */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Leichter Schatten für 3D-Effekt */
  transition: transform 0.2s ease, box-shadow 0.2s ease; /* Sanfter Übergang für interaktive Effekte */
}

.ingredients-box{
  width: fit-content;
}

.ingredients-box:hover, .preparation-box:hover {
  transform: translateY(-4px); /* Etwas Anhebung beim Hover */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); /* Etwas stärkerer Schatten beim Hover */
}

.ingredients-list, .preparation-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.ingredients-list li, .preparation-list li {
  word-wrap: break-word;
  overflow-wrap: break-word;
}

@media (max-width: 768px) {
  .ingredients-preparation-container {
    flex-direction: column;
    gap: 20px;
  }

  .ingredients-box, .preparation-box {
    width: 100%;
  }
}



</style>
