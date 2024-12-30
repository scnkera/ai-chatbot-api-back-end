import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os
from app.models.user import User
from app.models.character import Character
from app.models.training_message import Training_Message
from datetime import datetime

load_dotenv()

@pytest.fixture
def app():
    # create the app with a test configuration
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

# This fixture gets called in every test that
# references "one_task"
# This fixture creates a task and saves it in the database
@pytest.fixture
def one_user(app):
    new_user = User(
        username="kristenstern12", 
        email="christinegidffd@yahoo.com",
        password="baalugawahel",
        created_at="2024-12-27T22:44:52.395567"
        )
    db.session.add(new_user)
    db.session.commit()


@pytest.fixture
def one_character(app):
    new_character = Character(
        name="Snoop Dog", 
        description="Rapper, singer, cook, and icon",
        created_at="2024-12-27T22:44:52.395567"
        )
    db.session.add(new_character)
    db.session.commit()

@pytest.fixture
def one_training_message(app):
    character = Character.query.first()
    if character is None:
        # Create a default character with a description
        character = Character(
            name="Snoop Dog", 
            description="Rapper, singer, cook, and icon",
            created_at="2024-12-27T22:44:52.395567"
            )
        db.session.add(character)
        db.session.commit()

    new_training_message = Training_Message(
        message="I love ice cream",
        created_at="2024-12-27T22:44:52.395567"
        )
    db.session.add(new_training_message)
    db.session.commit()

# @pytest.fixture
# def one_training_message(app):
#     new_training_message = Training_Message(
#         character_id="kristenstern12", 
#         character="christinegidffd@yahoo.com",
#         message="baalugawahel",
#         created_at="2024-12-27T22:44:52.395567"
#         )
#     db.session.add(new_training_message)
#     db.session.commit()


# This fixture gets called in every test that
# references "three_users"
# This fixture creates three users and saves
# them in the database

@pytest.fixture
def three_users(app):
    db.session.add_all([
        User(
            username="smartiepants405", 
            email="",
            password="",
            created_at=None
            ),
        User(
            username="dolphinfin33", 
            email="",
            password="",
            created_at=None
            ),
        User(
            username="spicegirlspop0", 
            email="",
            password="",
            created_at=None
            )
    ])
    db.session.commit()


# This fixture gets called in every test that
# references "completed_user"
# This fixture creates a user with a
# valid completed_at date
@pytest.fixture
def completed_user(app):
    new_user = User(
        username="kristenstern12", 
        email="christinegidffd@yahoo.com",
        password="baalugawahel",
        created_at=datetime.utcnow()
        )
    db.session.add(new_user)
    db.session.commit()


# This fixture gets called in every test that
# references "one_training_message"
# This fixture creates a training_message and saves it in the database
# @pytest.fixture
# def one_training_message(app, db):
#     # Create a default character if needed
#     character = Character.query.first()
#     if character is None:
#         character = Character(name="Default Character", description="A default description")
#         db.session.add(character)
#         db.session.commit()
    
#     # Create a training message for that character
#     training_message = TrainingMessage(
#         character_id=character.id, 
#         message="Sample message", 
#         created_at=datetime.now()
#     )
#     db.session.add(training_message)
#     db.session.commit()

#     return training_message


# This fixture gets called in every test that
# references "one_user_belongs_to_one_training_message"
# This fixture creates a user and a training_message
# It associates the training_message and user, so that the
# training_message has this user, and the user belongs to one training_message
@pytest.fixture
def one_user_belongs_to_one_training_message(app, one_training_message, one_user):
    user = User.query.first()
    training_message = Training_Message.query.first()
    training_message.users.append(user)
    db.session.commit()

