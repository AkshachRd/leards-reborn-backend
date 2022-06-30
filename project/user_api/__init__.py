"""
The 'user_api' blueprint handles the API for managing user's model.
Specifically, this blueprint allows for user to get/put their model
from db.
"""
from flask import Blueprint

user_api_blueprint = Blueprint('user_api', __name__, template_folder='templates')

from . import authentication, routes
