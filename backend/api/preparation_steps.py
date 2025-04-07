from api.model import PreparationStepDB, PreparationStepSchema
from crud import crud
from fastapi import APIRouter, Depends, HTTPException
import uuid
import httpx
import os
from api.users import oauth2_scheme, validate_token

router = APIRouter()


@router.post("/preparation_steps/", response_model=PreparationStepDB, status_code=201)
async def create_preparation_step(preparation_step: PreparationStepSchema):
    """
    Create a new preparation step in the database.

    Args:
        preparation_step (PreparationStep): The preparation step object containing preparation step details.

    Returns:
        PreparationStep: The created preparation step object.
    """
    
    db_preparation_step = await crud.create_preparation_step(preparation_step)
    return db_preparation_step


@router.get("/preparation_steps/{preparation_step_id}", response_model=PreparationStepDB)
async def read_preparation_step(preparation_step_id: uuid.UUID):
    """
    Retrieve a preparation step by its preparation step ID.

    Args:
        preparation_step_id (uuid.UUID): The unique identifier of the preparation step to retrieve.

    Returns:
        dict: The preparation step data if found.
    """
    
    db_preparation_step = await crud.get_preparation_step(preparation_step_id)
    if db_preparation_step is None:
        raise HTTPException(status_code=404, detail="Preparation step not found")
    return db_preparation_step


@router.get("/preparation_steps/", response_model=list[PreparationStepDB])
async def read_preparation_steps():
    """
    Retrieve a list of preparation steps from the database.

    Returns:
        list[dict]: A list of preparation step data.
    """
    
    db_preparation_steps = await crud.get_preparation_steps()
    return db_preparation_steps


@router.put("/preparation_steps/{preparation_step_id}", response_model=PreparationStepDB)
async def update_preparation_step(preparation_step_id: uuid.UUID, preparation_step: PreparationStepSchema):
    """
    Update a preparation step in the database.

    Args:
        preparation_step_id (uuid.UUID): The unique identifier of the preparation step to update.
        preparation_step (PreparationStep): The updated preparation step object.

    Returns:
        PreparationStep: The updated preparation step object.
    """
    
    db_preparation_step = await crud.update_preparation_step(preparation_step_id, preparation_step)
    if db_preparation_step is None:
        raise HTTPException(status_code=404, detail="Preparation step not found")
    return db_preparation_step


@router.delete("/preparation_steps/{preparation_step_id}", response_model=PreparationStepDB)
async def delete_preparation_step(preparation_step_id: uuid.UUID):
    """
    Delete a preparation step from the database.

    Args:
        preparation_step_id (uuid.UUID): The unique identifier of the preparation step to delete.

    Returns:
        PreparationStep: The deleted preparation step object.
    """
    
    db_preparation_step = await crud.delete_preparation_step(preparation_step_id)
    if db_preparation_step is None:
        raise HTTPException(status_code=404, detail="Preparation step not found")
    return db_preparation_step