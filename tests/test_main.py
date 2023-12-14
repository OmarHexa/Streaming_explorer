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
    # Assuming there is a show with show_id 's1' in your dataset
    response = client.get("/shows/s1")
    assert response.status_code == 200
    assert response.json()["show_id"] == "s1"


def test_create_show(client):
    """Test the endpoint to create a new show."""
    new_show = {
        "show_id": "s9999",
        "type": "Movie",
        "title": "New Show",
        "director": "unknown",
        "cast": "unknown",
        "country": "unknown",
        "date_added": "unknown",
        "release_year": 2022,
        "rating": "unknown",
        "duration": "1h30m",
        "listed_in": "Comedy",
        "description": "A new show",
    }

    response = client.post("/shows/", json=new_show)
    assert response.status_code == 201
    assert response.json() == new_show

    # # Clean up: Delete the created show
    # response = client.delete("/shows/s9999")
    # assert response.status_code == 200


def test_update_show(client):
    """Test the endpoint to update a show."""
    show_id = "s9999"
    updated_show = {
        "show_id": show_id,
        "type": "Movie",
        "title": "New Show",
        "director": "unknown",
        "cast": "unknown",
        "country": "unknown",
        "date_added": "unknown",
        "release_year": 2022,
        "rating": "unknown",
        "duration": "1h30m",
        "listed_in": "Comedy",
        "description": "A new show",
    }

    response = client.put(f"/shows/{show_id}", json=updated_show)
    assert response.status_code == 200
    assert response.json() == updated_show


def test_delete_show(client):
    """Test the endpoint to delete a show."""
    show_id = "s9999"

    response = client.delete(f"/shows/{show_id}")
    assert response.status_code == 200
    assert response.json()["show_id"] == show_id
