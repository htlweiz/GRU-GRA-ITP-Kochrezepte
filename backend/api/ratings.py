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


@router.get("/ratings/{rating_id}", response_model=RatingSchema)
async def read_rating(rating_id: uuid.UUID):
    """
    Retrieve a rating by its rating ID.

    Args:
        rating_id (uuid.UUID): The unique identifier of the rating to retrieve.

    Returns:
        dict: The rating data if found.
    """
    
    db_rating = await crud.get_rating(rating_id)
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

@router.put("/ratings/{rating_id}", response_model=RatingSchema)
async def update_rating(recipeId: uuid.UUID, userId: uuid.UUID, rating: RatingSchema):
    """
    Update a rating in the database.

    Args:
        rating_id (uuid.UUID): The unique identifier of the rating to update.
        rating (Rating): The rating object containing updated rating details.

    Returns:
        Rating: The updated rating object.
    """
    
    db_rating = await crud.update_rating(recipeId, userId, rating)
    if db_rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return db_rating