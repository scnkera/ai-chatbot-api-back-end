from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from ..models.bot_response import BotResponse
from .route_utilities import validate_model, create_model
import requests
import os

bot_response_bp = Blueprint("characters_bp", __name__, url_prefix="/characters")
