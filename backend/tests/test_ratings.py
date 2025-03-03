import json
from jose import jwt

import api.ratings as ratings
import uuid


def test01_create_rating(monkeypatch, test_app):
    rating = {
        "userId": str(uuid.uuid4()),
        "recipeId": str(uuid.uuid4()),
        "stars": 5
    }
    res_rating = {
        "userId": rating["userId"],
        "recipeId": rating["recipeId"],
        "stars": rating["stars"]
    }

    async def mock_create_rating(rating):
        return res_rating

    monkeypatch.setattr(ratings.crud, "create_rating", mock_create_rating)

    response = test_app.post("/ratings/", data=json.dumps(rating))

    assert response.status_code == 201
    assert response.json() == res_rating


def test02_read_rating(monkeypatch, test_app):
    recipeId = str(uuid.uuid4())
    userId = str(uuid.uuid4())
    rating = {
        "userId": str(uuid.uuid4()),
        "recipeId": str(uuid.uuid4()),
        "stars": 5
    }

    async def mock_get_rating(recipeId, userId):
        return rating

    monkeypatch.setattr(ratings.crud, "get_rating", mock_get_rating)

    response = test_app.get(f"/ratings/{recipeId}/{userId}")

    assert response.status_code == 200
    assert response.json() == rating


def test03_read_rating_not_found(monkeypatch, test_app):
    recipeId = str(uuid.uuid4())
    userId = str(uuid.uuid4())

    async def mock_get_rating(recipeId, userId):
        return None
    
    monkeypatch.setattr(ratings.crud, "get_rating", mock_get_rating)
    
    response = test_app.get(f"/ratings/{recipeId}/{userId}")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Rating not found"


def test04_read_ratings(monkeypatch, test_app):
    ratings_list= [
        {
            "userId": str(uuid.uuid4()),
            "recipeId": str(uuid.uuid4()),
            "stars": 5
        },
        {
            "userId": str(uuid.uuid4()),
            "recipeId": str(uuid.uuid4()),
            "stars": 4
        }
    ]

    async def mock_get_ratings():
        return ratings_list

    monkeypatch.setattr(ratings.crud, "get_ratings", mock_get_ratings)

    response = test_app.get("/ratings/")

    assert response.status_code == 200
    assert response.json() == ratings_list


def test05_update_rating(monkeypatch, test_app):
    rating = {
        "userId": str(uuid.uuid4()),
        "recipeId": str(uuid.uuid4()),
        "stars": 5
    }

    async def mock_update_rating(rating_id, userId, rating):
        return rating

    monkeypatch.setattr(ratings.crud, "update_rating", mock_update_rating)

    response = test_app.put(f"/ratings/{rating['recipeId']}/{rating['userId']}", data=json.dumps(rating))

    assert response.status_code == 200
    assert response.json() == rating


def test06_update_rating_not_found(monkeypatch, test_app):
    rating = {
        "userId": str(uuid.uuid4()),
        "recipeId": str(uuid.uuid4()),
        "stars": 5
    }

    async def mock_update_rating(rating_id, userId, rating):
        return None

    monkeypatch.setattr(ratings.crud, "update_rating", mock_update_rating)

    response = test_app.put(f"/ratings/{rating['recipeId']}/{rating['userId']}", data=json.dumps(rating))

    assert response.status_code == 404
    assert response.json()["detail"] == "Rating not found"


def test07_delete_user(monkeypatch, test_app):
    rating = {
        "userId": str(uuid.uuid4()),
        "recipeId": str(uuid.uuid4()),
        "stars": 5
    }

    async def mock_delete_rating(rating_id, userId):
        return rating

    monkeypatch.setattr(ratings.crud, "delete_rating", mock_delete_rating)

    response = test_app.delete(f"/ratings/{rating['recipeId']}/{rating['userId']}")

    assert response.status_code == 200
    assert response.json() == rating


def test08_delete_rating_not_found(monkeypatch, test_app):
    rating = {
        "userId": str(uuid.uuid4()),
        "recipeId": str(uuid.uuid4()),
        "stars": 5
    }

    async def mock_delete_rating(rating_id, userId):
        return None

    monkeypatch.setattr(ratings.crud, "delete_rating", mock_delete_rating)

    response = test_app.delete(f"/ratings/{rating['recipeId']}/{rating['userId']}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Rating not found"