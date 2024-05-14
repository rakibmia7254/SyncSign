from flask import Blueprint, request, jsonify
import secrets

api_bp = Blueprint('api', __name__)

from . import routes