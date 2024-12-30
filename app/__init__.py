from flask import Flask
from flask_cors import CORS
import os
from .routes.user_routes import users_bp
from .routes.character_routes import characters_bp
from .routes.training_message_routes import training_messages_bp
from .db import db, migrate
from .models import user
from .models import character
from .models import training_message

# Import models, blueprints, and anything else needed to set up the app or database


def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        app.config.update(config)

    # Initialize app with SQLAlchemy db and Migrate
    db.init_app(app)
    migrate.init_app(app, db)


    # Register Blueprints 
    app.register_blueprint(users_bp)
    app.register_blueprint(characters_bp)
    app.register_blueprint(training_messages_bp)

    CORS(app)
    return app