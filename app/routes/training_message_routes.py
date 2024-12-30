from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from ..models.character import Character
from ..models.training_message import Training_Message
from .route_utilities import validate_model, create_model
import requests
import os

training_messages_bp = Blueprint("training_messages_bp", __name__, url_prefix="/training_messages")

@training_messages_bp.post("")
def create_training_message():
    request_body = request.get_json()

    return create_model(Training_Message, request_body)

@training_messages_bp.get("")
def get_all_training_messages():
    # query = db.select(Training_Message).order_by(Training_Message.characters)
    query = db.select(Training_Message).join(Training_Message.character).order_by(Character.id)
    training_messages = db.session.scalars(query)

    results_list = []
    results_list = [training_message.to_dict() for training_message in training_messages]

    return results_list

@training_messages_bp.get("/<training_message_id>")
def get_single_training_message(training_message_id):
    training_message = validate_model(Training_Message, training_message_id)

    response = {"training_message": training_message.to_dict()}

    return response, 200

@training_messages_bp.put("/<training_message_id>")
def update_training_message(training_message_id):
    training_message = validate_model(Training_Message, training_message_id)

    request_body = request.get_json()

    if "character_id" in request_body:
        training_message.character_id = request_body["character_id"]
    if "character" in request_body:
        training_message.character = request_body["character"]
    if "message" in request_body:
        training_message.password = request_body["message"]

    db.session.commit()

    return {"training_message": training_message.to_dict()}

@training_messages_bp.delete("/<training_message_id>")
def delete_training_message(training_message_id):
    training_message = validate_model(Training_Message, training_message_id)

    db.session.delete(training_message)
    db.session.commit()

    response = {"details": f"Training_Message {training_message_id} from character {training_message.character} \"{training_message.message}\" successfully deleted"}

    return response

