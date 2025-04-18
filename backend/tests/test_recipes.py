import json
from jose import jwt

import api.recipes as recipes
import uuid
from fastapi_pagination import Page

def test01_create_recipe(monkeypatch, test_app):
    recipe = {"title": "Test Recipe", "description": "Test Description", "cookingTime": 30, "preparationTime": 15, "imagePath": "test.jpg", "userId": "testuser"}
    res_recipe = {"recipeId": str(uuid.uuid4()), "title": "Test Recipe", "description": "Test Description", "cookingTime": 30, "preparationTime": 15, "imagePath": "test.jpg", "userId": "testuser"}

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
    
    monkeypatch.setattr(recipes, "validate_token", mock_validate_token)

    async def mock_create_recipe(recipe):
        return res_recipe
    
    monkeypatch.setattr(recipes.crud, "create_recipe", mock_create_recipe)

    response = test_app.post("/recipes/", data=json.dumps(recipe), headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    assert response.status_code == 201
    assert response.json() == res_recipe


def test02_read_recipe(monkeypatch, test_app):
    recipe = {"recipeId": str(uuid.uuid4()), "title": "Test Recipe", "description": "Test Description", "cookingTime": 30, "preparationTime": 15, "imagePath": "test.jpg", "userId": "testuser", "stars": 3, "ratingAmount": 1, "userName": "chef"}

    async def mock_get_recipe(recipe_id):
        return recipe
    
    monkeypatch.setattr(recipes.crud, "get_recipe", mock_get_recipe)

    response = test_app.get(f"/recipes/{recipe['recipeId']}", headers={"Content-Type": "application/json"})

    assert response.status_code == 200
    assert response.json() == recipe


def test03_read_recipe_not_found(monkeypatch, test_app):
    recipe_id = str(uuid.uuid4())

    async def mock_get_recipe(recipe_id):
        return None
    
    monkeypatch.setattr(recipes.crud, "get_recipe", mock_get_recipe)

    response = test_app.get(f"/recipes/{recipe_id}", headers={"Content-Type": "application/json"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Recipe not found"}


def test04_read_recipes(monkeypatch, test_app):
    recipes_list = [{"recipeId": str(uuid.uuid4()), "title": "Test Recipe", "description": "Test Description", "cookingTime": 30, "preparationTime": 15, "imagePath": "test.jpg", "userId": "testuser"}]

    async def mock_get_recipes():
        return Page(items=recipes_list, page=1, pages=None, size=2, total=1)
    
    monkeypatch.setattr(recipes.crud, "get_recipes", mock_get_recipes)

    response = test_app.get("/recipes/?page=1&size=2", headers={"Content-Type": "application/json"})

    assert response.status_code == 200
    assert response.json() == Page(items=recipes_list, page=1, pages=None, size=2, total=1).dict()
    

def test05_update_recipe(monkeypatch, test_app):
    recipe = {"recipeId": str(uuid.uuid4()), "title": "Test Recipe", "description": "Test Description", "cookingTime": 30, "preparationTime": 15, "imagePath": "test.jpg", "userId": "testuser"}
    updated_recipe = {"recipeId": str(uuid.uuid4()), "title": "Updated Recipe", "description": "Updated Description", "cookingTime": 45, "preparationTime": 20, "imagePath": "updated.jpg", "userId": "testuser"}
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
    
    monkeypatch.setattr(recipes, "validate_token", mock_validate_token) 

    async def mock_update_recipe(recipe_id, recipe):
        return updated_recipe
    
    monkeypatch.setattr(recipes.crud, "update_recipe", mock_update_recipe)

    response = test_app.put(f"/recipes/{recipe['recipeId']}", data=json.dumps(updated_recipe), headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == updated_recipe


def test06_update_recipe_not_found(monkeypatch, test_app):
    recipe_id = str(uuid.uuid4())
    updated_recipe = {"recipeId": str(uuid.uuid4()), "title": "Updated Recipe", "description": "Updated Description", "cookingTime": 45, "preparationTime": 20, "imagePath": "updated.jpg", "userId": "testuser"}
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
    
    monkeypatch.setattr(recipes, "validate_token", mock_validate_token) 

    async def mock_update_recipe(recipe_id, recipe):
        return None
    
    monkeypatch.setattr(recipes.crud, "update_recipe", mock_update_recipe)

    response = test_app.put(f"/recipes/{recipe_id}", data=json.dumps(updated_recipe), headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Recipe not found"}


def test07_update_recipe_invalid_token(test_app):
    recipe = {"recipeId": str(uuid.uuid4()), "title": "Test Recipe", "description": "Test Description", "cookingTime": 30, "preparationTime": 15, "imagePath": "test.jpg", "userId": "testuser"}
    updated_recipe = {"recipeId": str(uuid.uuid4()), "title": "Updated Recipe", "description": "Updated Description", "cookingTime": 45, "preparationTime": 20, "imagePath": "updated.jpg", "userId": "testuser"}
    token = "invalid"

    response = test_app.put(f"/recipes/{recipe['recipeId']}", data=json.dumps(updated_recipe), headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test08_delete_recipe(monkeypatch, test_app):
    recipe = {"recipeId": str(uuid.uuid4()), "title": "Test Recipe", "description": "Test Description", "cookingTime": 30, "preparationTime": 15, "imagePath": "test.jpg", "userId": "testuser"}
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
    
    monkeypatch.setattr(recipes, "validate_token", mock_validate_token) 

    async def mock_delete_recipe(recipe_id):
        return recipe
    
    monkeypatch.setattr(recipes.crud, "delete_recipe", mock_delete_recipe)

    response = test_app.delete(f"/recipes/{recipe['recipeId']}", headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == recipe


def test09_delete_recipe_not_found(monkeypatch, test_app):
    recipe_id = str(uuid.uuid4())
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
    
    monkeypatch.setattr(recipes, "validate_token", mock_validate_token)

    async def mock_delete_recipe(recipe_id):
        return None
    
    monkeypatch.setattr(recipes.crud, "delete_recipe", mock_delete_recipe)

    response = test_app.delete(f"/recipes/{recipe_id}", headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Recipe not found"}


def test10_delete_recipe_invalid_token(test_app):
    recipe_id = str(uuid.uuid4())
    token = "invalid"

    response = test_app.delete(f"/recipes/{recipe_id}", headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test11_read_preparation_steps(monkeypatch, test_app):
    recipe_id = str(uuid.uuid4())
    steps = [{"stepId": str(uuid.uuid4()), "recipeId": recipe_id, "stepNumber": 1, "description": "Test Step 1"}, {"stepId": str(uuid.uuid4()), "recipeId": recipe_id, "stepNumber": 2, "description": "Test Step 2"}]
    
    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(recipes, "validate_token", mock_validate_token)

    async def mock_get_recipe_preparation_steps(recipe_id):
        return steps
    
    monkeypatch.setattr(recipes.crud, "get_recipe_preparation_steps", mock_get_recipe_preparation_steps)

    response = test_app.get(f"/recipes/{recipe_id}/preparation_steps/", headers={"Content-Type": "application/json", "Authorization": "Bearer token"})

    assert response.status_code == 200
    assert response.json() == steps



def test12_read_ingredients(monkeypatch, test_app):
    recipe_id = str(uuid.uuid4())
    ingredients = [{"recipeId": recipe_id, "ingredientId": str(uuid.uuid4()), "amount": 1, "unit": "g", "name": "Test Ingredient"}]
    
    async def mock_get_recipe_ingredients(recipe_id):
        return ingredients
    
    monkeypatch.setattr(recipes.crud, "get_recipe_ingredients", mock_get_recipe_ingredients)

    response = test_app.get(f"/recipes/{recipe_id}/ingredients/", headers={"Content-Type": "application/json"})

    assert response.status_code == 200
    assert response.json() == ingredients


def test13_read_categories(monkeypatch, test_app):
    recipe_id = str(uuid.uuid4())
    categories = [{"categoryId": str(uuid.uuid4()), "name": "Test Category"}]
    
    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(recipes, "validate_token", mock_validate_token)

    async def mock_get_recipe_categories(recipe_id):
        return categories
    
    monkeypatch.setattr(recipes.crud, "get_recipe_categories", mock_get_recipe_categories)

    response = test_app.get(f"/recipes/{recipe_id}/categories/", headers={"Content-Type": "application/json", "Authorization": "Bearer token"})

    assert response.status_code == 200
    assert response.json() == categories


def test14_read_categories_invalid_token(test_app):
    recipe_id = str(uuid.uuid4())

    response = test_app.get(f"/recipes/{recipe_id}/categories/", headers={"Content-Type": "application/json", "Authorization": "Bearer invalid"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test15_read_ratings(monkeypatch, test_app):
    recipe_id = str(uuid.uuid4())
    ratings = [{"recipeId": recipe_id, "userId": "testuser", "stars": 5}]
    
    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(recipes, "validate_token", mock_validate_token)

    async def mock_get_recipe_ratings(recipe_id):
        return ratings
    
    monkeypatch.setattr(recipes.crud, "get_recipe_ratings", mock_get_recipe_ratings)

    response = test_app.get(f"/recipes/{recipe_id}/ratings/", headers={"Content-Type": "application/json", "Authorization": "Bearer token"})

    assert response.status_code == 200
    assert response.json() == ratings


def test16_read_ratings_invalid_token(test_app):
    recipe_id = str(uuid.uuid4())

    response = test_app.get(f"/recipes/{recipe_id}/ratings/", headers={"Content-Type": "application/json", "Authorization": "Bearer invalid"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test17_read_user(monkeypatch, test_app):
    user = {"userId": str(uuid.uuid4()), "firstName": "John", "lastName": "Doe", "email": "test@gmail.com"}

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(recipes, "validate_token", mock_validate_token)

    async def mock_get_user(recipeId):
        return user
    
    monkeypatch.setattr(recipes.crud, "get_recipe_user", mock_get_user)

    response = test_app.get(f"/recipes/{str(uuid.uuid4())}/user/", headers={"Content-Type": "application/json", "Authorization": "Bearer token"})

    assert response.status_code == 200
    assert response.json() == user


def test18_read_user_invalid_token(test_app):
    response = test_app.get(f"/recipes/{str(uuid.uuid4())}/user/", headers={"Content-Type": "application/json", "Authorization": "Bearer invalid"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test19_add_recipe_to_category(monkeypatch, test_app):
    recipe_id = str(uuid.uuid4())
    category_id = str(uuid.uuid4())

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(recipes, "validate_token", mock_validate_token)

    async def mock_add_recipe_to_category(recipe_id, category_id):
        return 200
    
    monkeypatch.setattr(recipes.crud, "add_recipe_to_category", mock_add_recipe_to_category)

    response = test_app.post(f"/recipes/{recipe_id}/category/{category_id}", headers={"Content-Type": "application/json", "Authorization": "Bearer token"})

    assert response.status_code == 200


def test20_remove_recipe_from_category(monkeypatch, test_app):
    recipe_id = str(uuid.uuid4())
    category_id = str(uuid.uuid4())

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(recipes, "validate_token", mock_validate_token)

    async def mock_remove_recipe_from_category(recipe_id, category_id):
        return 200
    
    monkeypatch.setattr(recipes.crud, "remove_recipe_from_category", mock_remove_recipe_from_category)

    response = test_app.delete(f"/recipes/{recipe_id}/category/{category_id}", headers={"Content-Type": "application/json", "Authorization": "Bearer token"})

    assert response.status_code == 200


def test21_remove_recipe_from_category_invalid_token(monkeypatch, test_app):

    async def mock_validate_token(token):
        return None
    
    monkeypatch.setattr(recipes, "validate_token", mock_validate_token)

    response = test_app.delete(f"/recipes/{str(uuid.uuid4())}/category/{str(uuid.uuid4())}", headers={"Content-Type": "application/json", "Authorization": "Bearer invalid"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test22_add_ingredient_to_recipe(monkeypatch, test_app):
    recipe_id = str(uuid.uuid4())
    ingredient_id = str(uuid.uuid4())


    async def mock_add_recipe_ingredient(recipe_id, ingredient_id, amount, unit):
        return 200
    
    monkeypatch.setattr(recipes.crud, "add_ingredient_to_recipe", mock_add_recipe_ingredient)

    response = test_app.post(f"/recipes/{recipe_id}/ingredient/{ingredient_id}?amount=1&unit=g", headers={"Content-Type": "application/json", "Authorization": "Bearer token"})

    assert response.status_code == 200


def test23_remove_ingredient_from_recipe(monkeypatch, test_app):
    recipe_id = str(uuid.uuid4())
    ingredient_id = str(uuid.uuid4())

    async def mock_validate_token(token):
        return 200
    
    monkeypatch.setattr(recipes, "validate_token", mock_validate_token)

    async def mock_remove_recipe_ingredient(recipe_id, ingredient_id):
        return 200
    
    monkeypatch.setattr(recipes.crud, "remove_ingredient_from_recipe", mock_remove_recipe_ingredient)

    response = test_app.delete(f"/recipes/{recipe_id}/ingredient/{ingredient_id}", headers={"Content-Type": "application/json", "Authorization": "Bearer token"})

    assert response.status_code == 200


def test24_remove_ingredient_from_recipe_invalid_token(test_app):
    response = test_app.delete(f"/recipes/{str(uuid.uuid4())}/ingredient/{str(uuid.uuid4())}", headers={"Content-Type": "application/json", "Authorization": "Bearer invalid"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test25_get_public_recipes(monkeypatch, test_app):
    recipes_list = [{"recipeId": str(uuid.uuid4()), "title": "Test Recipe", "description": "Test Description", "cookingTime": 30, "preparationTime": 15, "imagePath": "test.jpg", "userId": "testuser", "stars": 3, "ratingAmount": 1, "userName": "chef"}]
    
    async def mock_get_public_recipes():
        return Page(items=recipes_list, page=1, pages=None, size=10, total=1)
    
    monkeypatch.setattr(recipes.crud, "get_public_recipes", mock_get_public_recipes)
    
    response = test_app.get("/recipes/public/?page=1&size=2", headers={"Content-Type": "application/json"})

    assert response.status_code == 200
    assert response.json() == Page(items=recipes_list, page=1, pages=None, size=10, total=1).dict()


def test25_get_public_recipes_user(monkeypatch, test_app):
    recipes_list = [{"recipeId": str(uuid.uuid4()), "title": "Test Recipe", "description": "Test Description", "cookingTime": 30, "preparationTime": 15, "imagePath": "test.jpg", "userId": "testuser", "stars": 3, "ratingAmount": 1, "userName": "chef"}]
    
    async def mock_get_public_recipes_user(userid):
        return Page(items=recipes_list, page=1, pages=None, size=10, total=1)
    
    monkeypatch.setattr(recipes.crud, "get_public_recipes_user", mock_get_public_recipes_user)
    
    response = test_app.get(f"/recipes/public/{str(uuid.uuid4())}?page=1&size=2", headers={"Content-Type": "application/json"})

    assert response.status_code == 200
    assert response.json() == Page(items=recipes_list, page=1, pages=None, size=10, total=1).dict()


def test_26_get_public_recipes(monkeypatch, test_app):
    recipes_list = [{"recipeId": str(uuid.uuid4()), "title": "Test Recipe", "description": "Test Description", "cookingTime": 30, "preparationTime": 15, "imagePath": "test.jpg", "userId": "testuser", "stars": 3, "ratingAmount": 1, "userName": "chef"}]
    
    async def mock_get_public_recipes():
        return Page(items=recipes_list, page=1, pages=None, size=10, total=1)
    
    monkeypatch.setattr(recipes.crud, "get_public_recipes", mock_get_public_recipes)
    
    response = test_app.get(f"/recipes/public/?page=1&size=2", headers={"Content-Type": "application/json"})

    assert response.status_code == 200
    assert response.json() == Page(items=recipes_list, page=1, pages=None, size=10, total=1).dict()