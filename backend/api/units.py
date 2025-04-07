from api.model import *
from crud import crud
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

@router.get("/units/", response_model=list[Unit])
async def read_units():
    """
    Retrieve a list of units according to the enum.

    Returns:
        list[dict]: A list of unit data.
    """

    return [unit.value for unit in Unit]