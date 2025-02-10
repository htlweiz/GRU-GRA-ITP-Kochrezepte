from api.model import RecipeDB, UserDB, PreparationStepDB, IngredientDB, CategoryDB, RatingSchema, RecipeSchema, RecipeIngredientSchema
from crud import crud
from fastapi import APIRouter, Depends, HTTPException
import uuid
import httpx
import os
from fastapi.security import OAuth2PasswordBearer
from api.users import oauth2_scheme, validate_token
from fastapi_pagination import Page


router = APIRouter()


@router.post("/recipes/", response_model=RecipeDB, status_code=201)
async def create_recipe(recipe: RecipeSchema, token: str = Depends(oauth2_scheme)):
    """
    Create a new recipe in the database.

    Args:
        recipe (Recipe): The recipe object containing recipe details.

    Returns:
        Recipe: The created recipe object.
    """

    if not await validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db_recipe = await crud.create_recipe(recipe)
    return db_recipe

@router.get("/recipes/{recipe_id}", response_model=RecipeDB)
async def read_recipe(recipe_id: uuid.UUID, token: str = Depends(oauth2_scheme)):
    """
    Retrieve a recipe by its recipe ID.

    Args:
        recipe_id (uuid.UUID): The unique identifier of the recipe to retrieve.

    Returns:
        dict: The recipe data if found.
    """

    if not await validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db_recipe = await crud.get_recipe(recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe


@router.get("/recipes/", response_model=Page[RecipeDB])
async def read_recipes(token: str = Depends(oauth2_scheme)):
    """
    Retrieve a list of recipes from the database.

    Args:
        token (str): The OAuth2 token used for authentication.

    Returns:
        list[dict]: A list of recipe data.
    """

    if not await validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db_recipes = await crud.get_recipes()
    return db_recipes


@router.put("/recipes/{recipe_id}", response_model=RecipeDB)
async def update_recipe(recipe_id: uuid.UUID, recipe: RecipeDB, token: str = Depends(oauth2_scheme)):
    """
    Update a recipe in the database.

    Args:
        recipe_id (uuid.UUID): The unique identifier of the recipe to update.
        recipe (Recipe): The updated recipe object.

    Returns:
        Recipe: The updated recipe object.
    """

    if not await validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db_recipe = await crud.update_recipe(recipe_id, recipe)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe


@router.delete("/recipes/{recipe_id}", response_model=RecipeDB)
async def delete_recipe(recipe_id: uuid.UUID, token: str = Depends(oauth2_scheme)):
    """
    Delete a recipe from the database.

    Args:
        recipe_id (uuid.UUID): The unique identifier of the recipe to delete.

    Returns:
        Recipe: The deleted recipe object.
    """

    if not await validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db_recipe = await crud.delete_recipe(recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe


@router.get("/recipes/{recipe_id}/preparation_steps/", response_model=list[PreparationStepDB])
async def read_preparation_steps(recipe_id: uuid.UUID, token: str = Depends(oauth2_scheme)):
    """
    Retrieve a list of preparation steps for a recipe.

    Args:
        recipe_id (uuid.UUID): The unique identifier of the recipe to retrieve steps for.

    Returns:
        list[dict]: A list of preparation steps for the recipe.
    """

    if not await validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db_steps = await crud.get_recipe_preparation_steps(recipe_id)
    return db_steps


@router.get("/recipes/{recipe_id}/ingredients/", response_model=list[RecipeIngredientSchema])
async def read_ingredients(recipe_id: uuid.UUID, token: str = Depends(oauth2_scheme)):
    """
    Retrieve a list of ingredients for a recipe.

    Args:
        recipe_id (uuid.UUID): The unique identifier of the recipe to retrieve ingredients for.

    Returns:
        list[dict]: A list of ingredients for the recipe.
    """

    if not await validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db_ingredients = await crud.get_recipe_ingredients(recipe_id)
    return db_ingredients


@router.get("/recipes/{recipe_id}/categories/", response_model=list[CategoryDB])
async def read_categories(recipe_id: uuid.UUID, token: str = Depends(oauth2_scheme)):
    """
    Retrieve a list of categories for a recipe.

    Args:
        recipe_id (uuid.UUID): The unique identifier of the recipe to retrieve categories for.

    Returns:
        list[dict]: A list of categories for the recipe.
    """

    if not await validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db_categories = await crud.get_recipe_categories(recipe_id)
    return db_categories


@router.get("/recipes/{recipe_id}/ratings/", response_model=list[RatingSchema])
async def read_ratings(recipe_id: uuid.UUID, token: str = Depends(oauth2_scheme)):
    """
    Retrieve a list of ratings for a recipe.

    Args:
        recipe_id (uuid.UUID): The unique identifier of the recipe to retrieve ratings for.

    Returns:
        list[dict]: A list of ratings for the recipe.
    """

    if not await validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db_ratings = await crud.get_recipe_ratings(recipe_id)
    return db_ratings


@router.get("/recipes/{recipe_id}/user/", response_model=UserDB)
async def read_user(recipe_id: uuid.UUID, token: str = Depends(oauth2_scheme)):
    """
    Retrieve the user associated with a recipe.

    Args:
        recipe_id (uuid.UUID): The unique identifier of the recipe to retrieve the user for.

    Returns:
        dict: The user associated with the recipe.
    """

    if not await validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db_user = await crud.get_recipe_user(recipe_id)
    return db_user


@router.post("/recipes/{recipe_id}/category/{category_id}")
async def add_recipe_to_category(recipe_id: uuid.UUID, category_id: uuid.UUID, token: str = Depends(oauth2_scheme)):
    """
    Add a recipe to a category.

    Args:
        recipe_id (uuid.UUID): The unique identifier of the recipe to add to the category.
        category_id (uuid.UUID): The unique identifier of the category to add the recipe to.
    
    Returns:
        dict: The updated recipe object.
    """

    if not await validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")

    db_recipe = await crud.add_recipe_to_category(recipe_id, category_id)
    return db_recipe


@router.delete("/recipes/{recipe_id}/category/{category_id}")
async def remove_recipe_from_category(recipe_id: uuid.UUID, category_id: uuid.UUID, token: str = Depends(oauth2_scheme)):
    """
    Remove a recipe from a category.

    Args:
        recipe_id (uuid.UUID): The unique identifier of the recipe to remove from the category.
        category_id (uuid.UUID): The unique identifier of the category to remove the recipe from.
    
    Returns:
        dict: The updated recipe object.
    """

    if not await validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")

    db_recipe = await crud.remove_recipe_from_category(recipe_id, category_id)
    return db_recipe


@router.post("/recipes/{recipe_id}/ingredient/{ingredientId}")
async def add_recipe_ingredient(recipe_id: uuid.UUID, ingredientId: uuid.UUID, token: str = Depends(oauth2_scheme)):
    """
    Add an ingredient to a recipe.

    Args:
        recipe_id (uuid.UUID): The unique identifier of the recipe to add the ingredient to.
        ingredientId (uuid.UUID): The unique identifier of the ingredient to add to the recipe.
    
    Returns:
        dict: The updated recipe object.
    """

    if not await validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")

    db_recipe = await crud.add_ingredient_to_recipe(recipe_id, ingredientId)
    return db_recipe


@router.delete("/recipes/{recipe_id}/ingredient/{ingredientId}")
async def remove_recipe_ingredient(recipe_id: uuid.UUID, ingredientId: uuid.UUID, token: str = Depends(oauth2_scheme)):
    """
    Remove an ingredient from a recipe.

    Args:
        recipe_id (uuid.UUID): The unique identifier of the recipe to remove the ingredient from.
        ingredientId (uuid.UUID): The unique identifier of the ingredient to remove from the recipe.
    
    Returns:
        dict: The updated recipe object.
    """

    if not await validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")

    db_recipe = await crud.remove_ingredient_from_recipe(recipe_id, ingredientId)
    return db_recipe
