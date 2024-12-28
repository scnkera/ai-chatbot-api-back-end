from app.models.user import User
from datetime import datetime
import pytest
from app import db

def test_get_users_no_saved_users(client):
    # Act
    response = client.get("/users")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_users_one_saved_users(client, one_user):
    # Act
    response = client.get("/users")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "username": "kristenstern12",
            "email": "christinegidffd@yahoo.com",
            "password": "baalugawahel",
            "created_at": "2024-12-27T22:44:52.395567"
        }
    ]

def test_get_user(client, one_user):
    # Act
    response = client.get("/users/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "user" in response_body
    assert response_body == {
        "user": {
            "id": 1,
            "username": "kristenstern12",
            "email": "christinegidffd@yahoo.com",
            "password": "baalugawahel",
            "created_at": "2024-12-27T22:44:52.395567"
        }
    }


def test_get_user_not_found(client):
    # Act
    response = client.get("/users/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message":"User 1 not found."}


def test_create_user(client):
    # Act
    response = client.post("/users", json={
        "username": "kristenstern12",
        "email": "christinegidffd@yahoo.com",
        "password": "baalugawahel",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "user" in response_body

    user_data = response_body["user"]
    assert user_data["username"] == "kristenstern12"
    assert user_data["email"] == "christinegidffd@yahoo.com"
    assert user_data["password"] == "baalugawahel"

    assert "id" in user_data
    assert "created_at" in user_data 

    try:
        datetime.fromisoformat(user_data["created_at"])
    except ValueError:
        assert False, "created_at is not a valid ISO 8601 datetime string"

def test_delete_user(client, one_user):
    # Act
    response = client.delete("/users/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'User 1 "kristenstern12" successfully deleted'
    }
    assert db.session.get(User, 1) is None

def test_delete_user_not_found(client):
    # Act
    response = client.delete("/users/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message":"User 1 not found."}
    assert User.query.all() == []

def test_update_user(client, one_user):
    # Act
    response = client.put("/users/1", json={
        "username": "Updated User Title",
        "email": "Updated Test Description",
        "password": "Updated Password",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "user" in response_body
    assert response_body == {
        "user": {
            "id": 1,
            "username": "Updated User Title",
            "email": "Updated Test Description",
            "password": "Updated Password",
            "created_at": response_body["user"]["created_at"],  # Ignore this field by matching dynamically
        }
    }

    user = db.session.get(User, 1)
    assert user.username == "Updated User Title"
    assert user.email == "Updated Test Description"
    assert user.password == "Updated Password"


def test_update_user_not_found(client):
    # Act
    response = client.put("/users/1", json={
        "username": "Updated User Title",
        "email": "Updated Test Description",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message":"User 1 not found."}

def test_create_user_must_contain_username(client):
    # Act
    response = client.post("/users", json={
        "email": "Test Owner"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert User.query.all() == []


def test_create_user_must_contain_email(client):
    # Act
    response = client.post("/users", json={
        "username": "A Brand New User"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert User.query.all() == []

def test_validate_model_invalid_id(client):
    # Act
    response = client.get("/users/invalid_id")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "User id invalid_id is invalid"}
