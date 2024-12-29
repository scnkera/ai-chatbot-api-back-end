from app.models.character import Character
from datetime import datetime
import pytest
from app import db

def test_get_characters_no_saved_characters(client):
    # Act
    response = client.get("/characters")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_characters_one_saved_characters(client, one_character):
    # Act
    response = client.get("/characters")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "name": "Snoop Dog",
            "description": "Rapper, singer, cook, and icon",
            "created_at": "2024-12-27T22:44:52.395567"
        }
    ]

def test_get_character(client, one_character):
    # Act
    response = client.get("/characters/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "character" in response_body
    assert response_body == {
        "character": {
            "id": 1,
            "name": "Snoop Dog",
            "description": "Rapper, singer, cook, and icon",
            "created_at": "2024-12-27T22:44:52.395567"
        }
    }


def test_get_character_not_found(client):
    # Act
    response = client.get("/characters/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message":"Character 1 not found."}


def test_create_character(client):
    # Act
    response = client.post("/characters", json={
        "name": "Snoop Dog",
        "description": "Rapper, singer, cook, and icon",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "character" in response_body

    character_data = response_body["character"]
    assert character_data["name"] == "Snoop Dog"
    assert character_data["description"] == "Rapper, singer, cook, and icon"

    assert "id" in character_data
    assert "created_at" in character_data 

    try:
        datetime.fromisoformat(character_data["created_at"])
    except ValueError:
        assert False, "created_at is not a valid ISO 8601 datetime string"

def test_delete_character(client, one_character):
    # Act
    response = client.delete("/characters/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Character 1 "Snoop Dog" successfully deleted'
    }
    assert db.session.get(Character, 1) is None

def test_delete_character_not_found(client):
    # Act
    response = client.delete("/characters/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message":"Character 1 not found."}
    assert Character.query.all() == []

def test_update_character(client, one_character):
    # Act
    response = client.put("/characters/1", json={
        "name": "Updated Character Name",
        "description": "Updated Test Description",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "character" in response_body
    assert response_body == {
        "character": {
            "id": 1,
            "name": "Updated Character Name",
            "description": "Updated Test Description",
            "created_at": response_body["character"]["created_at"],  # Ignore this field by matching dynamically
        }
    }

    character = db.session.get(Character, 1)
    assert character.name == "Updated Character Title"
    assert character.description == "Updated Test Description"


def test_update_character_not_found(client):
    # Act
    response = client.put("/characters/1", json={
        "name": "Updated Character Title",
        "description": "Updated Test Description",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message":"Character 1 not found."}

def test_create_character_must_contain_name(client):
    # Act
    response = client.post("/characters", json={
        "description": "Test Owner"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert Character.query.all() == []


def test_create_character_must_contain_description(client):
    # Act
    response = client.post("/characters", json={
        "name": "A Brand New Character"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert Character.query.all() == []

def test_validate_model_invalid_id(client):
    # Act
    response = client.get("/characters/invalid_id")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Character id invalid_id is invalid"}
