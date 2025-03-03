import json
from jose import jwt

import api.preparation_steps as preparation_steps
import uuid


def test01_create_preparation_step(monkeypatch, test_app):
    preparation_step = {
        "recipeId": str(uuid.uuid4()),
        "stepNumber": 1,
        "description": "test"
    }
    res_prep_step = {
        "stepId": str(uuid.uuid4()),
        "recipeId": preparation_step["recipeId"],
        "stepNumber": preparation_step["stepNumber"],
        "description": preparation_step["description"]}

    async def mock_create_preparation_step(preparation_step):
        return res_prep_step

    monkeypatch.setattr(preparation_steps.crud, "create_preparation_step", mock_create_preparation_step)

    response = test_app.post("/preparation_steps/", data=json.dumps(preparation_step))

    assert response.status_code == 201
    assert response.json() == res_prep_step


def test02_read_preparation_step(monkeypatch, test_app):
    preparation_step_id = str(uuid.uuid4())
    preparation_step = {
        "stepId": preparation_step_id,
        "recipeId": str(uuid.uuid4()),
        "stepNumber": 1,
        "description": "test"
    }

    async def mock_get_preparation_step(preparation_step_id):
        return preparation_step

    monkeypatch.setattr(preparation_steps.crud, "get_preparation_step", mock_get_preparation_step)

    response = test_app.get(f"/preparation_steps/{preparation_step_id}")

    assert response.status_code == 200
    assert response.json() == preparation_step


def test03_read_preparation_step_not_found(monkeypatch, test_app):
    preparation_step_id = str(uuid.uuid4())

    async def mock_get_preparation_step(preparation_step_id):
        return None
    
    monkeypatch.setattr(preparation_steps.crud, "get_preparation_step", mock_get_preparation_step)
    
    response = test_app.get(f"/preparation_steps/{preparation_step_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Preparation step not found"}


def test04_read_preparation_steps(monkeypatch, test_app):
    preparation_steps_list = [
        {
            "stepId": str(uuid.uuid4()),
            "recipeId": str(uuid.uuid4()),
            "stepNumber": 1,
            "description": "test"
        },
        {
            "stepId": str(uuid.uuid4()),
            "recipeId": str(uuid.uuid4()),
            "stepNumber": 2,
            "description": "test"
        }
    ]

    async def mock_get_preparation_steps():
        return preparation_steps_list

    monkeypatch.setattr(preparation_steps.crud, "get_preparation_steps", mock_get_preparation_steps)

    response = test_app.get("/preparation_steps/")

    assert response.status_code == 200
    assert response.json() == preparation_steps_list


def test05_update_preparation_step(monkeypatch, test_app):
    preparation_step_id = str(uuid.uuid4())
    res_preparation_step = {
        "stepId": preparation_step_id,
        "recipeId": str(uuid.uuid4()),
        "stepNumber": 1,
        "description": "test"
    }
    preparation_step = {
        "recipeId": res_preparation_step["recipeId"],
        "stepNumber": 1,
        "description": "test"
    }

    async def mock_update_preparation_step(preparation_step_id, preparation_step):
        return res_preparation_step

    monkeypatch.setattr(preparation_steps.crud, "update_preparation_step", mock_update_preparation_step)

    response = test_app.put(f"/preparation_steps/{preparation_step_id}", data=json.dumps(preparation_step))

    assert response.status_code == 200
    assert response.json() == res_preparation_step


def test06_update_preparation_step_not_found(monkeypatch, test_app):
    preparation_step_id = str(uuid.uuid4())
    preparation_step = {
        "recipeId": str(uuid.uuid4()),
        "stepNumber": 1,
        "description": "test"
    }

    async def mock_update_preparation_step(preparation_step_id, preparation_step):
        return None

    monkeypatch.setattr(preparation_steps.crud, "update_preparation_step", mock_update_preparation_step)

    response = test_app.put(f"/preparation_steps/{preparation_step_id}", data=json.dumps(preparation_step))

    assert response.status_code == 404
    assert response.json() == {"detail": "Preparation step not found"}


def test07_delete_preparation_step(monkeypatch, test_app):
    preparation_step_id = str(uuid.uuid4())
    preparation_step = {
        "stepId": preparation_step_id,
        "recipeId": str(uuid.uuid4()),
        "stepNumber": 1,
        "description": "test"
    }

    async def mock_delete_preparation_step(preparation_step_id):
        return preparation_step

    monkeypatch.setattr(preparation_steps.crud, "delete_preparation_step", mock_delete_preparation_step)

    response = test_app.delete(f"/preparation_steps/{preparation_step_id}")

    assert response.status_code == 200
    assert response.json() == preparation_step


def test08_delete_preparation_step_not_found(monkeypatch, test_app):
    preparation_step_id = str(uuid.uuid4())

    async def mock_delete_preparation_step(preparation_step_id):
        return None

    monkeypatch.setattr(preparation_steps.crud, "delete_preparation_step", mock_delete_preparation_step)

    response = test_app.delete(f"/preparation_steps/{preparation_step_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Preparation step not found"}