from app.models.training_message import Training_Message
from datetime import datetime
import pytest
from app import db

def test_get_training_messages_no_saved_training_messages(client):
    # Act
    response = client.get("/training_messages")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_training_messages_one_saved_training_messages(client, one_training_message):
    # Act
    response = client.get("/training_messages")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "message": "I love ice cream",
            "created_at": "2024-12-27T22:44:52.395567"
        }
    ]

@pytest.mark.skip
def test_get_training_message(client, one_training_message):
    # Act
    response = client.get("/training_messages/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "training_message" in response_body
    assert response_body == {
        "training_message": {
            "id": 1,
            "training_messagename": "kristenstern12",
            "email": "christinegidffd@yahoo.com",
            "password": "baalugawahel",
            "created_at": "2024-12-27T22:44:52.395567"
        }
    }

@pytest.mark.skip
def test_get_training_message_not_found(client):
    # Act
    response = client.get("/training_messages/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message":"Training_Message 1 not found."}

@pytest.mark.skip
def test_create_training_message(client):
    # Act
    response = client.post("/training_messages", json={
        "character_id": "character_id",
        "character": "christinegidffd@yahoo.com",
        "message": "insert message",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "training_message" in response_body

    training_message_data = response_body["training_message"]
    assert training_message_data["character_id"] == "kristenstern12"
    assert training_message_data["character"] == "christinegidffd@yahoo.com"
    assert training_message_data["message"] == "I love ice cream"

    assert "id" in training_message_data
    assert "created_at" in training_message_data 

    try:
        datetime.fromisoformat(training_message_data["created_at"])
    except ValueError:
        assert False, "created_at is not a valid ISO 8601 datetime string"

@pytest.mark.skip
def test_delete_training_message(client, one_training_message):
    # Act
    response = client.delete("/training_messages/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Training_Message 1 "kristenstern12" successfully deleted'
    }
    assert db.session.get(Training_Message, 1) is None

@pytest.mark.skip
def test_delete_training_message_not_found(client):
    # Act
    response = client.delete("/training_messages/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message":"Training_Message 1 not found."}
    assert Training_Message.query.all() == []

@pytest.mark.skip
def test_update_training_message(client, one_training_message):
    # Act
    response = client.put("/training_messages/1", json={
        "character_id": "Updated Character ID",
        "character": "Updated Character",
        "message": "Updated Test Message",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "training_message" in response_body
    assert response_body == {
        "training_message": {
            "id": 1,
            "character_id": "character_id",
            "character": "christinegidffd@yahoo.com",
            "message": "insert message",
            "created_at": response_body["training_message"]["created_at"],  # Ignore this field by matching dynamically
        }
    }

    training_message = db.session.get(Training_Message, 1)
    assert training_message.character_id == "Updated Character ID"
    assert training_message.character == "Updated Character"
    assert training_message.message == "Updated Test Message"

@pytest.mark.skip(reason="currently configuring")
def test_create_goal_missing_message(client):
    # Act
    response = client.post("/training_message", json={})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "details": "Invalid data"
    }

# not other
@pytest.mark.skip
def test_update_training_message_not_found(client):
    # Act
    response = client.put("/training_messages/1", json={
        "character_id": "Updated Character ID",
        "character": "Updated Character",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message":"Training_Message 1 not found."}


@pytest.mark.skip
def test_create_training_message_must_contain_training_message(client):
    # Act
    response = client.post("/training_messages", json={
        "email": "Test Owner"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert Training_Message.query.all() == []

@pytest.mark.skip
def test_create_training_message_must_contain_email(client):
    # Act
    response = client.post("/training_messages", json={
        "message": "A Brand New Training_Message"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert Training_Message.query.all() == []


@pytest.mark.skip
def test_validate_model_invalid_id(client):
    # Act
    response = client.get("/training_messages/invalid_id")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Training_Message id invalid_id is invalid"}

