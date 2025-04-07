import json
from api.model import UserDB
from jose import jwt

import api.users as users
import uuid
from fastapi_pagination import Page

def test01_create_user(monkeypatch, test_app):
    user = {"userId": str(uuid.uuid4()), "firstName": "John", "lastName": "Doe", "email": "test@gmail.com"}
    token = jwt.encode(
        {
            "sub": "123",
            "aud": "audience",
            "exp": 1600000000
        },
        "secret",
        algorithm="HS256"
    )

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(users, "validate_token", mock_validate_token)

    async def mock_create_user(user):
        return user
    
    monkeypatch.setattr(users.crud, "create_user", mock_create_user)


    response = test_app.post("/users/", data=json.dumps(user), headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
   
    assert response.status_code == 201
    assert response.json() == user


def test02_create_user_user_exists(monkeypatch, test_app):
    user = {"userId": str(uuid.uuid4()), "firstName": "John", "lastName": "Doe", "email": "test@gmail.com"}
    token = jwt.encode(
        {
            "sub": "123",
            "aud": "audience",
            "exp": 1600000000
        },
        "secret",
        algorithm="HS256"
    )

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(users, "validate_token", mock_validate_token)

    async def mock_create_user(user):
        return None
    
    monkeypatch.setattr(users.crud, "create_user", mock_create_user)

    response = test_app.post("/users/", data=json.dumps(user), headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    assert response.status_code == 409


def test03_read_user(monkeypatch, test_app):
    user = {"userId": str(uuid.uuid4()), "firstName": "John", "lastName": "Doe", "email": "test@gmail.com"}
    token = jwt.encode(
        {
            "sub": "123",
            "aud": "audience",
            "exp": 1600000000
        },
        "secret",
        algorithm="HS256"
    )

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(users, "validate_token", mock_validate_token)

    async def mock_get_user(userId):
        return user
    
    monkeypatch.setattr(users.crud, "get_user", mock_get_user)

    response = test_app.get(f"/users/{str(uuid.uuid4())}", headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    assert response.status_code == 200


def test04_read_user_invalid_token(test_app):
    token = "invalid_token"

    response = test_app.get(f"/users/{str(uuid.uuid4())}", headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test05_read_user_not_found(monkeypatch, test_app):
    token = jwt.encode(
        {
            "sub": "123",
            "aud": "audience",
            "exp": 1600000000
        },
        "secret",
        algorithm="HS256"
    )

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(users, "validate_token", mock_validate_token)

    async def mock_get_user(userId):
        return None

    monkeypatch.setattr(users.crud, "get_user", mock_get_user)

    response = test_app.get(f"/users/{str(uuid.uuid4())}", headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test06_read_users(monkeypatch, test_app):
    users_list = [{"userId": str(uuid.uuid4()), "firstName": "John", "lastName": "Doe", "email": "test@gmail.com"},
            {"userId": str(uuid.uuid4()),"firstName": "John", "lastName": "Doe", "email": "test@gmail.com"}]
    
    token = jwt.encode(
        {
            "sub": "123",
            "aud": "audience",
            "exp": 1600000000
        },
        "secret",
        algorithm="HS256"
    )

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(users, "validate_token", mock_validate_token)

    async def mock_get_users():
        return Page(items=users_list, page=1, pages=None, size=2, total=2)

    monkeypatch.setattr(users.crud, "get_users", mock_get_users)

    response = test_app.get(f"/users/?page=1&size=2", headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == Page(items=users_list, page=1, pages=None, size=2, total=2).dict()


def test07_read_users_invalid_token(test_app):
    token = "invalid_token"

    response = test_app.get(f"/users/", headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test08_update_user(monkeypatch, test_app):
    user = {"userId": str(uuid.uuid4()), "firstName": "John", "lastName": "Doe", "email": "test@gmail.com"}
    token = jwt.encode(
        {
            "sub": "123",
            "aud": "audience",
            "exp": 1600000000
        },
        "secret",
        algorithm="HS256"
    )

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(users, "validate_token", mock_validate_token)

    async def mock_update_user(userId, user_):
        return user

    monkeypatch.setattr(users.crud, "update_user", mock_update_user)

    response = test_app.put(f"/users/{user['userId']}", data=json.dumps(user), headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == user


def test09_update_user_invalid_token(test_app):
    user = {"userId": str(uuid.uuid4()), "firstName": "John", "lastName": "Doe", "email": "test@gmail.com"}
    token = "invalid_token"

    response = test_app.put(f"/users/{str(uuid.uuid4())}", data=json.dumps(user), headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test10_update_user_not_found(monkeypatch, test_app):
    user = {"userId": str(uuid.uuid4()), "firstName": "John", "lastName": "Doe", "email": "test@gmail.com"}
    token = jwt.encode(
        {
            "sub": "123",
            "aud": "audience",
            "exp": 1600000000
        },
        "secret",
        algorithm="HS256"
    )

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(users, "validate_token", mock_validate_token)

    async def mock_update_user(userId, user_):
        return None

    monkeypatch.setattr(users.crud, "update_user", mock_update_user)

    response = test_app.put(f"/users/{user['userId']}", data=json.dumps(user), headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test11_delete_user(monkeypatch, test_app):
    user = {"userId": str(uuid.uuid4()), "firstName": "John", "lastName": "Doe", "email": "test@gmail.com"}
    token = jwt.encode(
        {
            "sub": "123",
            "aud": "audience",
            "exp": 1600000000
        },
        "secret",
        algorithm="HS256"
    )

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(users, "validate_token", mock_validate_token)

    async def mock_delete_user(userId):
        return user

    monkeypatch.setattr(users.crud, "delete_user", mock_delete_user)

    response = test_app.delete(f"/users/{user['userId']}", headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == user


def test12_delete_user_invalid_token(test_app):
    token = "invalid_token"

    response = test_app.delete(f"/users/{str(uuid.uuid4())}", headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test13_delete_user_not_found(monkeypatch, test_app):
    user = {"userId": str(uuid.uuid4()), "firstName": "John", "lastName": "Doe", "email": "test@gmail.com"}
    token = jwt.encode(
        {
            "sub": "123",
            "aud": "audience",
            "exp": 1600000000
        },
        "secret",
        algorithm="HS256"
    )

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(users, "validate_token", mock_validate_token)

    async def mock_delete_user(userId):
        return None

    monkeypatch.setattr(users.crud, "delete_user", mock_delete_user)

    response = test_app.delete(f"/users/{user['userId']}", headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test14_get_user_recipes(monkeypatch, test_app):
    recipes = [{"recipeId": str(uuid.uuid4()), "title": "Recipe", "description": "Description", "cookingTime": 1, "preparationTime": 1, "imagePath": "test", "userId": str(uuid.uuid4())}]

    token = jwt.encode(
        {
            "sub": "123",
            "aud": "audience",
            "exp": 1600000000
        },
        "secret",
        algorithm="HS256"
    )

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(users, "validate_token", mock_validate_token)

    async def mock_get_user_recipes(userId):
        return recipes

    monkeypatch.setattr(users.crud, "get_user_recipes", mock_get_user_recipes)

    response = test_app.get(f"/users/{str(uuid.uuid4())}/recipes/", headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == recipes


def test15_get_user_recipes_invalid_token(test_app):
    token = "invalid_token"

    response = test_app.get(f"/users/{str(uuid.uuid4())}/recipes/", headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test16_get_user_recipes_not_found(monkeypatch, test_app):

    token = jwt.encode(
        {
            "sub": "123",
            "aud": "audience",
            "exp": 1600000000
        },
        "secret",
        algorithm="HS256"
    )

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(users, "validate_token", mock_validate_token)

    async def mock_get_user_recipes(userId):
        return None
    
    monkeypatch.setattr(users.crud, "get_user_recipes", mock_get_user_recipes)

    response = test_app.get(f"/users/{str(uuid.uuid4())}/recipes/", headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test17_get_user_ratings(monkeypatch, test_app):
    ratings = [{"userId": str(uuid.uuid4()), "recipeId": str(uuid.uuid4()), "stars": 5}]

    token = jwt.encode(
        {
            "sub": "123",
            "aud": "audience",
            "exp": 1600000000
        },
        "secret",
        algorithm="HS256"
    )

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(users, "validate_token", mock_validate_token)

    async def mock_get_user_ratings(userId):
        return ratings

    monkeypatch.setattr(users.crud, "get_user_ratings", mock_get_user_ratings)

    response = test_app.get(f"/users/{str(uuid.uuid4())}/ratings/", headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == ratings


def test18_get_user_ratings_not_found(monkeypatch, test_app):
    token = jwt.encode(
        {
            "sub": "123",
            "aud": "audience",
            "exp": 1600000000
        },
        "secret",
        algorithm="HS256"
    )

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(users, "validate_token", mock_validate_token)
    
    async def mock_get_user_ratings(userId):
        return None

    monkeypatch.setattr(users.crud, "get_user_ratings", mock_get_user_ratings)

    response = test_app.get(f"/users/{str(uuid.uuid4())}/ratings/", headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test19_get_user_ratings_invalid_token(test_app):
    token = "invalid_token"

    response = test_app.get(f"/users/{str(uuid.uuid4())}/ratings/", headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}