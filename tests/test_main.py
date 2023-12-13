import json

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_index(client):
    """Test the index endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the app"}


def test_get_first_five_rows(client):
    """Test the endpoint to get the first 5 rows."""
    response = client.get("/shows/")
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_get_show_by_id(client):
    """Test the endpoint to get a show by its ID."""
    # Assuming there is a show with show_id 'example_id' in your dataset
    response = client.get("/shows/example_id")
    assert response.status_code == 200
    assert response.json()["show_id"] == "example_id"


def test_create_show(client):
    """Test the endpoint to create a new show."""
    new_show = {
        "show_id": "new_show_id",
        "type": "Movie",
        "title": "New Show",
        "release_year": 2022,
        "duration": "1h30m",
        "listed_in": "Comedy",
        "description": "A new show",
    }

    response = client.post("/shows/", json=new_show)
    assert response.status_code == 201
    assert response.json() == new_show

    # Clean up: Delete the created show
    response = client.delete("/shows/new_show_id")
    assert response.status_code == 200


def test_update_show(client):
    """Test the endpoint to update a show."""
    show_id = "example_id"
    updated_show = {
        "show_id": show_id,
        "type": "TV Show",
        "title": "Updated Show",
        "release_year": 2023,
        "duration": "2 seasons",
        "listed_in": "Drama",
        "description": "An updated show",
    }

    response = client.put(f"/shows/{show_id}", json=updated_show)
    assert response.status_code == 200
    assert response.json() == updated_show


def test_delete_show(client):
    """Test the endpoint to delete a show."""
    # Assuming there is a show with show_id 'example_id' in your dataset
    show_id = "example_id"

    response = client.delete(f"/shows/{show_id}")
    assert response.status_code == 200
    assert response.json()["show_id"] == show_id
