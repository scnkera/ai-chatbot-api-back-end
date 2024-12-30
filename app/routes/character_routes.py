from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from ..models.character import Character
from .route_utilities import validate_model, create_model
import requests
import os

characters_bp = Blueprint("characters_bp", __name__, url_prefix="/characters")

@characters_bp.post("")
def create_character():
    request_body = request.get_json()

    return create_model(Character, request_body)

@characters_bp.get("")
def get_all_characters():
    query = db.select(Character).order_by(Character.name)
    characters = db.session.scalars(query)

    results_list = []
    results_list = [character.to_dict() for character in characters]

    return results_list

@characters_bp.get("/<character_id>")
def get_single_character(character_id):
    character = validate_model(Character, character_id)

    response = {"character": character.to_dict()}

    return response, 200

@characters_bp.put("/<character_id>")
def update_character(character_id):
    character = validate_model(Character, character_id)

    request_body = request.get_json()

    if "name" in request_body:
        character.name = request_body["name"]
    if "description" in request_body:
        character.description = request_body["description"]

    db.session.commit()

    return {"character": character.to_dict()}

@characters_bp.delete("/<character_id>")
def delete_character(character_id):
    character = validate_model(Character, character_id)

    db.session.delete(character)
    db.session.commit()

    response = {"details": f"Character {character_id} \"{character.name}\" successfully deleted"}

    return response
