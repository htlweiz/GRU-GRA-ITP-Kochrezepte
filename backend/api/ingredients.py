from api.model import *
from crud import crud
from fastapi import APIRouter, Depends, HTTPException
import uuid
import httpx
import os
from api.users import oauth2_scheme, validate_token

router = APIRouter()


@router.post("/ingredients/", response_model=IngredientDB, status_code=201)
async def create_ingredient(ingredient: IngredientSchema):
    """
    Create a new ingredient in the database.

    Args:
        ingredient (Ingredient): The ingredient object containing ingredient details.

    Returns:
        Ingredient: The created ingredient object.
    """
    
    db_ingredient = await crud.create_ingredient(ingredient)
    if not db_ingredient:
        raise HTTPException(status_code=409, detail="Ingredient already exists")
    return db_ingredient


@router.get("/ingredients/{ingredient_id}", response_model=IngredientDB)
async def read_ingredient(ingredient_id: uuid.UUID):
    """
    Retrieve an ingredient by its ingredient ID.

    Args:
        ingredient_id (uuid.UUID): The unique identifier of the ingredient to retrieve.

    Returns:
        dict: The ingredient data if found.
    """
    
    db_ingredient = await crud.get_ingredient(ingredient_id)
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return db_ingredient


@router.get("/ingredients/", response_model=list[IngredientDB])
async def read_ingredients():
    """
    Retrieve a list of ingredients from the database.

    Returns:
        list[dict]: A list of ingredient data.
    """
    
    db_ingredients = await crud.get_ingredients()
    return db_ingredients


@router.put("/ingredients/{ingredient_id}", response_model=IngredientDB)
async def update_ingredient(ingredient_id: uuid.UUID, ingredient: IngredientSchema):
    """
    Update an ingredient in the database.

    Args:
        ingredient_id (uuid.UUID): The unique identifier of the ingredient to update.
        ingredient (Ingredient): The updated ingredient object.

    Returns:
        Ingredient: The updated ingredient object.
    """
    
    db_ingredient = await crud.update_ingredient(ingredient_id, ingredient)
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return db_ingredient


@router.delete("/ingredients/{ingredient_id}", response_model=IngredientDB)
async def delete_ingredient(ingredient_id: uuid.UUID):
    """
    Delete an ingredient from the database.

    Args:
        ingredient_id (uuid.UUID): The unique identifier of the ingredient to delete.
    """
    
    db_ingredient = await crud.delete_ingredient(ingredient_id)
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return db_ingredient