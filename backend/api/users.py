from api.model import UserDB
from crud import crud
from fastapi import APIRouter, Depends, HTTPException
import uuid
import httpx
from fastapi.security import OAuth2PasswordBearer
import os

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
TOKEN_VALIDATION_URL=os.getenv("TOKEN_VALIDATION_URL")

async def validate_token(token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            TOKEN_VALIDATION_URL,
            headers={"Authorization": f"Bearer {token}"}
        )
        return response.status_code == 200


@router.post("/users/", response_model=UserDB, status_code=201)
async def create_user(user: UserDB, token: str = Depends(oauth2_scheme)):
    """
    Create a new user in the database.

    Args:
        user (User): The user object containing user details.
        token (str, optional): The OAuth2 token for authentication. Defaults to Depends(oauth2_scheme).

    Raises:
        HTTPException: If the token is invalid (status code 401).

    Returns:
        User: The created user object.
    """
    if not validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    db_user = await crud.create_user(user)
    return db_user


@router.get("/users/{user_id}", response_model=UserDB)
async def read_user(user_id: uuid.UUID, token: str = Depends(oauth2_scheme)):
    """
    Retrieve a user by their user ID.

    Args:
        user_id (uuid.UUID): The unique identifier of the user to retrieve.
        token (str, optional): The OAuth2 token for authentication. Defaults to Depends(oauth2_scheme).

    Raises:
        HTTPException: If the token is invalid (status code 401).
        HTTPException: If the user is not found (status code 404).

    Returns:
        dict: The user data if found and authenticated.
    """
    if not validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    db_user = await crud.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users/", response_model=list[UserDB])
async def read_users(token: str = Depends(oauth2_scheme)):
    """
    Retrieve a list of users from the database.

    Args:
        token (str): The OAuth2 token used for authentication.

    Raises:
        HTTPException: If the token is invalid (status code 401).

    Returns:
        List[User]: A list of user objects retrieved from the database.
    """
    if not validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    db_users = await crud.get_users()
    return db_users


@router.put("/users/{user_id}", response_model=UserDB)
async def update_user(user_id: uuid.UUID, user: UserDB, token: str = Depends(oauth2_scheme)):
    """Updates a user in the database

    Args:
        user_id (uuid.UUID): The id of the user to update
        user (User): The updated user
        token (str, optional): The validation token

    Raises:
        HTTPException: If the user is not found (status code 404)
        HTTPException: If the token is invalid (status code 401)

    Returns:
        UserDB: The updated user
    """
    if not validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    db_user = await crud.update_user(user_id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/users/{user_id}", response_model=UserDB)
async def delete_user(user_id: uuid.UUID, token: str = Depends(oauth2_scheme)):
    """Deletes a user from the database

    Args:
        user_id (uuid.UUID): The id of the user to delete
        token (str, optional): The validation token

    Raises:
        HTTPException: If the user is not found (status code 404)
        HTPException: If the token is invalid (status code 401)

    Returns:
        UserDB: The deleted user
    """
    db_user = await crud.delete_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
