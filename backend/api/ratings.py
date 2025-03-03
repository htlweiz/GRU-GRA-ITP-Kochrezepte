from api.model import RatingSchema
from crud import crud
from fastapi import APIRouter, Depends, HTTPException
import uuid
import httpx
import os
from api.users import oauth2_scheme, validate_token

router = APIRouter()

@router.post("/ratings/", response_model=RatingSchema, status_code=201)
async def create_rating(rating: RatingSchema):
    """
    Create a new rating in the database.

    Args:
        rating (Rating): The rating object containing rating details.

    Returns:
        Rating: The created rating object.
    """
    
    db_rating = await crud.create_rating(rating)
    return db_rating


@router.get("/ratings/{recipeId}/{userId}", response_model=RatingSchema)
async def read_rating(recipeId: uuid.UUID, userId: str):
    """
    Retrieve a rating by its rating ID.

    Args:
        rating_id (uuid.UUID): The unique identifier of the rating to retrieve.

    Returns:
        dict: The rating data if found.
    """
    
    db_rating = await crud.get_rating(recipeId, userId)
    if db_rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return db_rating


@router.get("/ratings/", response_model=list[RatingSchema])
async def read_ratings():
    """
    Retrieve a list of ratings from the database.

    Returns:
        list[dict]: A list of rating data.
    """
    
    db_ratings = await crud.get_ratings()
    return db_ratings

@router.put("/ratings/{recipeId}/{userId}", response_model=RatingSchema)
async def update_rating(recipeId: uuid.UUID, userId: str, rating: RatingSchema):
    """
    Update a rating in the database.

    Args:
        recipeId (uuid.UUID): The unique identifier of the recipe of the rating to update.
        userId (uuid.UUID): The unique identifier of the user of the rating to update.
        rating (Rating): The rating object containing updated rating details.

    Returns:
        Rating: The updated rating object.
    """
    
    db_rating = await crud.update_rating(recipeId, userId, rating)
    if db_rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return db_rating


@router.delete("/ratings/{recipeId}/{userId}", response_model=RatingSchema)
async def delete_rating(recipeId: uuid.UUID, userId: str):
    """
    Delete a rating from the database.
    
    Args:
        recipe_id (uuid.UUID): The unique identifier of the recipe of the rating to delete.
        user_id (uuid.UUID): The unique identifier of the user of the rating to delete.

    Returns:
        Rating: The deleted rating object.
    """

    db_rating = await crud.delete_rating(recipeId, userId)
    if db_rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return db_rating