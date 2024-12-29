import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os
from app.models.user import User
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
    new_user = User(
        username="Snoop Dog", 
        description="Rapper, singer, cook, and icon",
        created_at="2024-12-27T22:44:52.395567"
        )
    db.session.add(new_user)
    db.session.commit()


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
# references "one_goal"
# This fixture creates a goal and saves it in the database
@pytest.fixture
def one_goal(app):
    new_goal = Goal(title="Build a habit of going outside daily")
    db.session.add(new_goal)
    db.session.commit()


# This fixture gets called in every test that
# references "one_user_belongs_to_one_goal"
# This fixture creates a user and a goal
# It associates the goal and user, so that the
# goal has this user, and the user belongs to one goal
@pytest.fixture
def one_user_belongs_to_one_goal(app, one_goal, one_user):
    user = User.query.first()
    goal = Goal.query.first()
    goal.users.append(user)
    db.session.commit()

