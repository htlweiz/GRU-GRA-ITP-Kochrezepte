<template>
    <div class="recipes">
        <RecipeCard picUrl="../../public/image.jpg" recipeName="Spaghetti Carbonarra" recipeDesc="Das italienische Rezept Spaghetti Carbonara ist überall bekannt und beliebt. Hier werden Speck, Eier und Parmesan verwendet.Das italienische Rezept Spaghetti Carbonara ist überall bekannt und beliebt. Hier werden Speck, Eier und Parmesan verwendet.Das italienische Rezept Spaghetti Carbonara ist überall bekannt und beliebt. Hier werden Speck, Eier und Parmesan verwendet." creator="Hans" stars="3"/>
    
        <RecipeCard picUrl="../../public/image.jpg" recipeName="Spaghetti Carbonarra" recipeDesc="Das italienische Rezept Spaghetti Carbonara ist überall bekannt und beliebt. Hier werden Speck, Eier und Parmesan verwendet.Das italienische Rezept Spaghetti Carbonara ist überall bekannt und beliebt. Hier werden Speck, Eier und Parmesan verwendet.Das italienische Rezept Spaghetti Carbonara ist überall bekannt und beliebt. Hier werden Speck, Eier und Parmesan verwendet." creator="Hans" stars="3"/>
        
        <RecipeCard picUrl="../../public/image.jpg" recipeName="Spaghetti Carbonarra nach Gruber Maxsches Art asdjahbskdjhasd" recipeDesc="Das italienische Rezept Spaghetti Carbonara ist überall bekannt und beliebt. Hier werden Speck, Eier und Parmesan verwendet.Das italienische Rezept Spaghetti Carbonara ist überall bekannt und beliebt. Hier werden Speck, Eier und Parmesan verwendet.Das italienische Rezept Spaghetti Carbonara ist überall bekannt und beliebt. Hier werden Speck, Eier und Parmesan verwendet." cookingTime="20" creator="Hans" stars="3" ratingsCount="10"/>
        
    
</div>
</template>

<script>
import { onMounted } from 'vue';
import RecipeCard from './RecipeCard.vue'

export default {
    components: {
        RecipeCard
    },
    methods:
    {
        
    },

    setup() {
        onMounted(() => {
                if (localStorage.getItem('reloaded')) {
                    localStorage.removeItem('reloaded');
                } else {
                    localStorage.setItem('reloaded', '1');
                    location.reload();
                }
            });
        }

    
}

</script>

<style scoped>

.recipes {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: stretch;
}



</style>
