import json
from jose import jwt

import api.ingredients as ingredients
import uuid

def test01_create_ingredient(monkeypatch, test_app):
    ing = {"name": "Test Ingredient"}
    res_ing = {"ingredientId": str(uuid.uuid4()), "name": "Test Ingredient"}

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(ingredients, "validate_token", mock_validate_token)

    async def mock_create_ingredient(ingredient):
        return res_ing
    
    monkeypatch.setattr(ingredients.crud, "create_ingredient", mock_create_ingredient)

    response = test_app.post("/ingredients/", data=json.dumps(ing), headers={"Content-Type": "application/json", "Authorization": "Bearer token"})

    assert response.status_code == 201
    assert response.json() == res_ing


def test02_read_ingredient(monkeypatch, test_app):
    ing_id = str(uuid.uuid4())
    ing = {"ingredientId": ing_id, "name": "Test Ingredient"}

    async def mock_get_ingredient(ingredient_id):
        return ing
    
    monkeypatch.setattr(ingredients.crud, "get_ingredient", mock_get_ingredient)

    response = test_app.get(f"/ingredients/{ing_id}")

    assert response.status_code == 200
    assert response.json() == ing


def test03_read_ingredient_not_found(monkeypatch, test_app):
    ing_id = str(uuid.uuid4())

    async def mock_get_ingredient(ingredient_id):
        return None
    
    monkeypatch.setattr(ingredients.crud, "get_ingredient", mock_get_ingredient)

    response = test_app.get(f"/ingredients/{ing_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Ingredient not found"}


def test04_read_ingredients(monkeypatch, test_app):
    ings = [{"ingredientId": str(uuid.uuid4()), "name": "Test Ingredient"}]

    async def mock_get_ingredients():
        return ings
    
    monkeypatch.setattr(ingredients.crud, "get_ingredients", mock_get_ingredients)

    response = test_app.get("/ingredients/")

    assert response.status_code == 200
    assert response.json() == ings


def test05_update_ingredient(monkeypatch, test_app):
    ing_id = str(uuid.uuid4())
    ing = {"name": "Test Ingredient"}
    res_ing = {"ingredientId": ing_id, "name": "Test Ingredient"}

    async def mock_update_ingredient(ingredient_id, ingredient):
        return res_ing
    
    monkeypatch.setattr(ingredients.crud, "update_ingredient", mock_update_ingredient)

    response = test_app.put(f"/ingredients/{ing_id}", data=json.dumps(ing), headers={"Content-Type": "application/json", "Authorization": "Bearer token"})

    assert response.status_code == 200
    assert response.json() == res_ing


def test06_update_ingredient_not_found(monkeypatch, test_app):
    ing_id = str(uuid.uuid4())
    ing = {"name": "Test Ingredient"}

    async def mock_update_ingredient(ingredient_id, ingredient):
        return None
    
    monkeypatch.setattr(ingredients.crud, "update_ingredient", mock_update_ingredient)

    response = test_app.put(f"/ingredients/{ing_id}", data=json.dumps(ing), headers={"Content-Type": "application/json", "Authorization": "Bearer token"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Ingredient not found"}


def test07_delete_ingredient(monkeypatch, test_app):
    ing_id = str(uuid.uuid4())
    ing = {"ingredientId": ing_id, "name": "Test Ingredient"}

    async def mock_delete_ingredient(ingredient_id):
        return ing
    
    monkeypatch.setattr(ingredients.crud, "delete_ingredient", mock_delete_ingredient)

    response = test_app.delete(f"/ingredients/{ing_id}", headers={"Authorization": "Bearer token"})

    assert response.status_code == 200
    assert response.json() == ing


def test08_delete_ingredient_not_found(monkeypatch, test_app):
    ing_id = str(uuid.uuid4())

    async def mock_delete_ingredient(ingredient_id):
        return None
    
    monkeypatch.setattr(ingredients.crud, "delete_ingredient", mock_delete_ingredient)

    response = test_app.delete(f"/ingredients/{ing_id}", headers={"Authorization": "Bearer token"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Ingredient not found"}