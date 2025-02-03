from db.session import session
from db.model import User, Recipe, Ingredient, PreparationStep, RecipeIngredient, Category, RecipeCategory, Rating, Unit
import uuid
from api.model import UserDB, RecipeDB, IngredientDB, PreparationStepDB, CategoryDB, RatingSchema, IngredientSchema, PreparationStepSchema, CategorySchema, RecipeSchema
from fastapi_pagination import paginate

async def create_user(user: UserDB):
    ex_user = session.query(User).filter(User.userId == user.userId).first()
    if ex_user is not None:
        return None
    db_user = User(
        userId=user.userId,
        email=user.email,
        firstName=user.firstName,
        lastName=user.lastName,
    )
    session.add(db_user)
    session.commit()
    return db_user


async def get_user(user_id: str):
    return session.query(User).filter(User.userId == user_id).first()

async def get_users():
    return paginate(session.query(User).all())

async def update_user(user_id: str, user: User):
    db_user = session.query(User).filter(User.userId == user_id).first()
    if db_user is None:
        return None
    db_user.email = user.email
    db_user.firstName = user.firstName
    db_user.lastName = user.lastName
    session.commit()
    return db_user


async def delete_user(user_id: str):
    db_user = session.query(User).filter(User.userId == user_id).first()
    if db_user is None:
        return None
    session.delete(db_user)
    session.commit()
    return db_user


async def get_user_recipes(user_id: str):
    db_user = session.query(User).filter(User.userId == user_id).first()
    if db_user is None:
        return None
    return db_user.recipes


async def get_user_ratings(user_id: str):
    db_user = session.query(User).filter(User.userId == user_id).first()
    if db_user is None:
        return None
    return db_user.ratings


#-------------------------Recipes-------------------------	


async def create_recipe(recipe: RecipeSchema):
    db_recipe = Recipe(
        title=recipe.title,
        description=recipe.description,
        cookingTime=recipe.cookingTime,
        preparationTime=recipe.preparationTime,
        imagePath=recipe.imagePath,
        userId=recipe.userId
    )
    session.add(db_recipe)
    session.commit()
    return db_recipe


async def get_recipe(recipe_id: uuid.UUID):
    return session.query(Recipe).filter(Recipe.recipeId == recipe_id).first()

async def get_recipes():
    return session.query(Recipe).all()


async def update_recipe(recipe_id: uuid.UUID, recipe: Recipe):
    db_recipe = session.query(Recipe).filter(Recipe.recipeId == recipe_id).first()
    if db_recipe is None:
        return None
    db_recipe.title = recipe.title
    db_recipe.description = recipe.description
    db_recipe.cookingTime = recipe.cookingTime
    db_recipe.preparationTime = recipe.preparationTime
    db_recipe.imagePath = recipe.imagePath
    db_recipe.userId = recipe.userId
    session.commit()
    return db_recipe


async def delete_recipe(recipe_id: uuid.UUID):
    db_recipe = session.query(Recipe).filter(Recipe.recipeId == recipe_id).first()
    if db_recipe is None:
        return None
    session.delete(db_recipe)
    session.commit()
    return db_recipe


async def get_recipe_user(recipeId: uuid.UUID):
    recipe = session.query(Recipe).filter(Recipe.recipeId == recipeId).first()
    if not recipe:
        return None
    return recipe.user


async def get_recipe_preparation_steps(recipeId: uuid.UUID):
    recipe = session.query(Recipe).filter(Recipe.recipeId == recipeId).first()
    if not recipe:
        return None
    return recipe.steps


async def get_recipe_ingredients(recipeId: uuid.UUID):
    recipe = session.query(Recipe).filter(Recipe.recipeId == recipeId).first()
    if not recipe:
        return None
    return recipe.ingredients


async def get_recipe_categories(recipeId: uuid.UUID):
    recipe = session.query(Recipe).filter(Recipe.recipeId == recipeId).first()
    if not recipe:
        return None
    return recipe.categories


async def get_recipe_ratings(recipeId: uuid.UUID):
    recipe = session.query(Recipe).filter(Recipe.recipeId == recipeId).first()
    if not recipe:
        return None
    return recipe.ratings


async def add_recipe_to_category(recipeId: uuid.UUID, categoryId: uuid.UUID):
    recipe = session.query(Recipe).filter(Recipe.recipeId == recipeId).first()
    category = session.query(Category).filter(Category.categoryId == categoryId).first()
    if not recipe or not category:
        return None
    recipe_category = RecipeCategory(
        recipeId=recipeId,
        categoryId=categoryId
    )
    session.add(recipe_category)
    session.commit()
    return recipe_category


async def remove_recipe_from_category(recipeId: uuid.UUID, categoryId: uuid.UUID):
    recipe_category = session.query(RecipeCategory).filter(RecipeCategory.recipeId == recipeId, RecipeCategory.categoryId == categoryId).first()
    if not recipe_category:
        return None
    session.delete(recipe_category)
    session.commit()
    return recipe_category


async def add_ingredient_to_recipe(recipeId: uuid.UUID, ingredientId: uuid.UUID, amount: int, unit: str):
    recipe = session.query(Recipe).filter(Recipe.recipeId == recipeId).first()
    ingredient = session.query(Ingredient).filter(Ingredient.ingredientId == ingredientId).first()
    if not recipe or not ingredient:
        return None
    recipe_ingredient = RecipeIngredient(
        recipeId=recipeId,
        ingredientId=ingredientId,
        amount=amount,
        unit=unit
    )
    session.add(recipe_ingredient)
    session.commit()
    return recipe_ingredient


async def remove_ingredient_from_recipe(recipeId: uuid.UUID, ingredientId: uuid.UUID):
    recipe_ingredient = session.query(RecipeIngredient).filter(RecipeIngredient.recipeId == recipeId, RecipeIngredient.ingredientId == ingredientId).first()
    if not recipe_ingredient:
        return None
    session.delete(recipe_ingredient)
    session.commit()
    return recipe_ingredient


#-------------------------Preparation Steps-------------------------


async def create_preparation_step(step: PreparationStepSchema):
    db_step = PreparationStep(
        recipeId=step.recipeId,
        stepNumber=step.stepNumber,
        description=step.description
    )
    session.add(db_step)
    session.commit()
    return db_step


async def get_preparation_step(step_id: uuid.UUID):
    return session.query(PreparationStep).filter(PreparationStep.stepId == step_id).first()


async def get_preparation_steps():
    return session.query(PreparationStep).all()


async def update_preparation_step(step_id: uuid.UUID, step: PreparationStep):
    db_step = session.query(PreparationStep).filter(PreparationStep.stepId == step_id).first()
    if db_step is None:
        return None
    db_step.recipeId = step.recipeId
    db_step.stepNumber = step.stepNumber
    db_step.description = step.description
    session.commit()
    return db_step


async def delete_preparation_step(step_id: uuid.UUID):
    db_step = session.query(PreparationStep).filter(PreparationStep.stepId == step_id).first()
    if db_step is None:
        return None
    session.delete(db_step)
    session.commit()
    return db_step


#-------------------------Ingredients----------------------------


async def create_ingredient(ingredient: IngredientSchema):
    ex_ingredient = session.query(Ingredient).filter(Ingredient.name == ingredient.name).first()
    if ex_ingredient is not None:
        return None
    db_ingredient = Ingredient(
        name=ingredient.name
    )
    session.add(db_ingredient)
    session.commit()
    return db_ingredient


async def get_ingredient(ingredient_id: uuid.UUID):
    return session.query(Ingredient).filter(Ingredient.ingredientId == ingredient_id).first()

async def get_ingredients():
    return session.query(Ingredient).all()

async def update_ingredient(ingredient_id: uuid.UUID, ingredient: IngredientSchema):
    db_ingredient = session.query(Ingredient).filter(Ingredient.ingredientId == ingredient_id).first()
    if db_ingredient is None:
        return None
    db_ingredient.name = ingredient.name
    session.commit()
    return db_ingredient


async def delete_ingredient(ingredient_id: uuid.UUID):
    db_ingredient = session.query(Ingredient).filter(Ingredient.ingredientId == ingredient_id).first()
    if db_ingredient is None:
        return None
    session.delete(db_ingredient)
    session.commit()
    return db_ingredient

#-------------------------Categories----------------------------


async def create_category(category: CategorySchema):
    ex_category = session.query(Category).filter(Category.name == category.name).first()
    if ex_category is not None:
        return None
    db_category = Category(
        name=category.name
    )
    session.add(db_category)
    session.commit()
    return db_category


async def get_category(category_id: uuid.UUID):
    return session.query(Category).filter(Category.categoryId == category_id).first()


async def get_categories():
    return session.query(Category).all()


async def update_category(category_id: uuid.UUID, category: Category):
        db_category = session.query(Category).filter(Category.categoryId == category_id).first()
        if db_category is None:
            return None
        db_category.name = category.name
        session.commit()
        return db_category


async def delete_category(category_id: uuid.UUID):
    db_category = session.query(Category).filter(Category.categoryId == category_id).first()
    if db_category is None:
        return None
    session.delete(db_category)
    session.commit()
    return db_category


async def get_category_recipes(categoryId: uuid.UUID):
    category = session.query(Category).filter(Category.categoryId == categoryId).first()
    if not category:
        return None
    return category.recipes


#-------------------------Ratings----------------------------


async def create_rating(rating: RatingSchema):
    db_rating = Rating(
        rating=rating.stars,
        userId=rating.userId,
        recipeId=rating.recipeId
    )
    session.add(db_rating)
    session.commit()
    return db_rating


async def get_rating(recipe_id: uuid.UUID, user_id: str):
    return session.query(Rating).filter(Rating.recipeId == recipe_id, Rating.userId == user_id).first()


async def get_ratings():
    return session.query(Rating).all()


async def update_rating(recipe_id: uuid.UUID, user_id: str, rating: Rating):
    db_rating = session.query(Rating).filter(Rating.recipeId == recipe_id, Rating.userId == user_id).first()
    if db_rating is None:
        return None
    db_rating.stars = rating.stars
    session.commit()
    return db_rating