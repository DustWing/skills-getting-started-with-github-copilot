import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy

@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: Save original activities and restore after test
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original))

@pytest.fixture
def client():
    # Arrange: Provide a fresh TestClient for each test
    return TestClient(app)
