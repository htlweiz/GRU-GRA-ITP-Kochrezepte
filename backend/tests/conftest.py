import pytest
from starlette.testclient import TestClient

from api.main import app


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client  # testing happens here
