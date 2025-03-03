import json
from jose import jwt

import api.categories as categories
import uuid

def test01_create_category(monkeypatch, test_app):
    cat = {"name": "Test Category"}
    res_cat = {"categoryId": str(uuid.uuid4()), "name": "Test Category"}

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(categories, "validate_token", mock_validate_token)

    async def mock_create_category(category):
        return res_cat
    
    monkeypatch.setattr(categories.crud, "create_category", mock_create_category)

    response = test_app.post("/categories/", data=json.dumps(cat), headers={"Content-Type": "application/json", "Authorization": "Bearer token"})

    assert response.status_code == 201
    assert response.json() == res_cat
    

def test02_create_category_already_exists(monkeypatch, test_app):
    cat = {"name": "Test Category"}

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(categories, "validate_token", mock_validate_token)

    async def mock_create_category(category):
        return None
    
    monkeypatch.setattr(categories.crud, "create_category", mock_create_category)

    response = test_app.post("/categories/", data=json.dumps(cat), headers={"Content-Type": "application/json", "Authorization": "Bearer token"})

    assert response.status_code == 409
    assert response.json() == {"detail": "Category already exists"}


def test03_create_category_invalid_token(test_app):
    cat = {"name": "Test Category"}

    response = test_app.post("/categories/", data=json.dumps(cat), headers={"Content-Type": "application/json", "Authorization": "Bearer token"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test04_read_category(monkeypatch, test_app):
    cat_id = str(uuid.uuid4())
    cat = {"categoryId": cat_id, "name": "Test Category"}

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(categories, "validate_token", mock_validate_token)

    async def mock_get_category(category_id):
        return cat
    
    monkeypatch.setattr(categories.crud, "get_category", mock_get_category)

    response = test_app.get(f"/categories/{cat_id}", headers={"Content-Type": "application/json", "Authorization": "Bearer token"})

    assert response.status_code == 200
    assert response.json() == cat


def test05_read_category_not_found(monkeypatch, test_app):
    cat_id = str(uuid.uuid4())

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(categories, "validate_token", mock_validate_token)

    async def mock_get_category(category_id):
        return None
    
    monkeypatch.setattr(categories.crud, "get_category", mock_get_category)

    response = test_app.get(f"/categories/{cat_id}", headers={"Content-Type": "application/json", "Authorization": "Bearer token"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}


def test06_read_categories(monkeypatch, test_app):
    cats = [{"categoryId": str(uuid.uuid4()), "name": "Test Category"}]

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(categories, "validate_token", mock_validate_token)

    async def mock_get_categories():
        return cats
    
    monkeypatch.setattr(categories.crud, "get_categories", mock_get_categories)

    response = test_app.get("/categories/", headers={"Content-Type": "application/json", "Authorization": "Bearer invalid"})

    assert response.status_code == 200
    assert response.json() == cats


def test07_read_categories_invalid_token(test_app):
    response = test_app.get("/categories/", headers={"Content-Type": "application/json", "Authorization": "Bearer invalid"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test08_update_category(monkeypatch, test_app):
    cat_id = str(uuid.uuid4())
    cat = {"name": "Test Category"}
    res_cat = {"categoryId": cat_id, "name": "Test Category"}

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(categories, "validate_token", mock_validate_token)

    async def mock_update_category(category_id, category):
        return res_cat

    monkeypatch.setattr(categories.crud, "update_category", mock_update_category)

    response = test_app.put(f"/categories/{cat_id}", data=json.dumps(cat), headers={"Content-Type": "application/json", "Authorization": "Bearer token"})

    assert response.status_code == 200
    assert response.json() == res_cat


def test09_update_category_not_found(monkeypatch, test_app):
    cat_id = str(uuid.uuid4())
    cat = {"name": "Test Category"}

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(categories, "validate_token", mock_validate_token)

    async def mock_update_category(category_id, category):
        return None

    monkeypatch.setattr(categories.crud, "update_category", mock_update_category)

    response = test_app.put(f"/categories/{cat_id}", data=json.dumps(cat), headers={"Content-Type": "application/json", "Authorization": "Bearer token"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}


def test10_update_category_invalid_token(test_app):
    cat_id = str(uuid.uuid4())
    cat = {"name": "Test Category"}

    response = test_app.put(f"/categories/{cat_id}", data=json.dumps(cat), headers={"Content-Type": "application/json", "Authorization": "Bearer invalid"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test11_delete_category(monkeypatch, test_app):
    cat_id = str(uuid.uuid4())
    cat = {"categoryId": cat_id, "name": "Test Category"}

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(categories, "validate_token", mock_validate_token)

    async def mock_delete_category(category_id):
        return cat
    
    monkeypatch.setattr(categories.crud, "delete_category", mock_delete_category)

    response = test_app.delete(f"/categories/{cat_id}", headers={"Content-Type": "application/json", "Authorization": "Bearer token"})

    assert response.status_code == 200
    assert response.json() == cat


def test12_delete_category_not_found(monkeypatch, test_app):
    cat_id = str(uuid.uuid4())

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(categories, "validate_token", mock_validate_token)

    async def mock_delete_category(category_id):
        return None
    
    monkeypatch.setattr(categories.crud, "delete_category", mock_delete_category)

    response = test_app.delete(f"/categories/{cat_id}", headers={"Content-Type": "application/json", "Authorization": "Bearer token"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}


def test13_delete_category_invalid_token(monkeypatch, test_app):
    cat_id = str(uuid.uuid4())
    cat = {"categoryId": cat_id, "name": "Test Category"}

    async def mock_delete_category(category_id):
        return cat
    
    monkeypatch.setattr(categories.crud, "delete_category", mock_delete_category)


    response = test_app.delete(f"/categories/{cat_id}", headers={"Content-Type": "application/json", "Authorization": "Bearer invalid"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test14_get_recipes_for_category(monkeypatch, test_app):
    cat_id = str(uuid.uuid4())
    recipes = [{"recipeId": str(uuid.uuid4()), "title": "Test Recipe", "description": "test", "cookingTime": 10, "preparationTime": 10, "imagePath": "test.jpg", "userId": "test"}]

    async def mock_get_category_recipes(category_id):
        return recipes

    monkeypatch.setattr(categories.crud, "get_category_recipes", mock_get_category_recipes)

    response = test_app.get(f"/categories/{cat_id}/recipes/", headers={"Content-Type": "application/json"})

    assert response.status_code == 200
    assert response.json() == recipes