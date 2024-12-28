from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from ..models.user import User
# from .route_utilities import validate_model, create_model
import requests
import os

users_bp = Blueprint("users_bp", __name__, url_prefix="/users")

@users_bp.post("")
def create_user():
    request_body = request.get_json()

    return create_model(User, request_body)

@users_bp.get("")
def get_all_users():
    query = db.select(User).order_by(User.username)
    users = db.session.scalars(query)

    results_list = []
    results_list = [user.to_dict() for user in users]

    return results_list

@users_bp.get("/<user_id>")
def get_single_user(user_id):
    user = validate_model(User, user_id)

    response = {"user": user.to_dict()}

    return response, 200

@users_bp.put("/<user_id>")
def update_user(user_id):
    user = validate_model(User, user_id)

    request_body = request.get_json()

    if "username" in request_body:
        user.username = request_body["username"]
    if "email" in request_body:
        user.email = request_body["email"]
    if "password" in request_body:
        user.password = request_body["password"]

    db.session.commit()

    return {"user": user.to_dict()}

@users_bp.delete("/<user_id>")
def delete_user(user_id):
    user = validate_model(User, user_id)

    db.session.delete(user)
    db.session.commit()

    response = {"details": f"User {user_id} \"{user.username}\" successfully deleted"}

    return response


def validate_model(cls, model_id):

    # checks for valid input
    try: 
        model_id = int(model_id)
    except: 
        abort(make_response({"message": f"{cls.__name__} id {model_id} is invalid"}, 400))


    # returns user with the corresponding user_id
    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found."}, 404))

    return model

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
        
    except KeyError as error:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()

    return {cls.__name__.lower(): new_model.to_dict()}, 201