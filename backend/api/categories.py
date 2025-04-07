from api.model import RecipeDB, UserDB, PreparationStepDB, IngredientDB, CategoryDB, RatingSchema, RecipeSchema, CategorySchema
from crud import crud
from fastapi import APIRouter, Depends, HTTPException
import uuid
import httpx
import os
from api.users import oauth2_scheme, validate_token

router = APIRouter()

@router.post("/categories/", response_model=CategoryDB, status_code=201)
async def create_category(category: CategorySchema, token: str = Depends(oauth2_scheme)):
    """
    Create a new category in the database.

    Args:
        category (Category): The category object containing category details.

    Returns:
        Category: The created category object.
    """

    if not await validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db_category = await crud.create_category(category)
    if not db_category:
        raise HTTPException(status_code=409, detail="Category already exists")
    return db_category


@router.get("/categories/{category_id}", response_model=CategoryDB)
async def read_category(category_id: uuid.UUID):
    """
    Retrieve a category by its category ID.

    Args:
        category_id (uuid.UUID): The unique identifier of the category to retrieve.

    Returns:
        dict: The category data if found.
    """

    db_category = await crud.get_category(category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.get("/categories/", response_model=list[CategoryDB])
async def read_categories(token: str = Depends(oauth2_scheme)):
    """
    Retrieve a list of categories from the database.

    Returns:
        list[dict]: A list of category data.
    """

    if not await validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db_categories = await crud.get_categories()
    return db_categories


@router.put("/categories/{category_id}", response_model=CategoryDB)
async def update_category(category_id: uuid.UUID, category: CategorySchema, token: str = Depends(oauth2_scheme)):
    """
    Update a category in the database.

    Args:
        category_id (uuid.UUID): The unique identifier of the category to update.
        category (Category): The category object containing updated category details.

    Returns:
        Category: The updated category object.
    """

    if not await validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db_category = await crud.update_category(category_id, category)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.delete("/categories/{category_id}", response_model=CategoryDB)
async def delete_category(category_id: uuid.UUID, token: str = Depends(oauth2_scheme)):
    """
    Delete a category from the database.

    Args:
        category_id (uuid.UUID): The unique identifier of the category to delete.

    Returns:
        Category: The deleted category object.
    """

    if not await validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db_category = await crud.delete_category(category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.get("/categories/{category_id}/recipes/", response_model=list[RecipeDB])
async def read_category_recipes(category_id: uuid.UUID):
    """
    Retrieve a list of recipes for a category.

    Args:
        category_id (uuid.UUID): The unique identifier of the category to retrieve recipes for.

    Returns:
        list[dict]: A list of recipes for the category.
    """
    
    db_recipes = await crud.get_category_recipes(category_id)
    return db_recipes
