"""
The 'parser_api' blueprint handles the API for managing parser.
Specifically, this blueprint allows for user to get info about
entered word.
"""
from flask import Blueprint
from . import routes

parser_api_blueprint = Blueprint('parser_api', __name__, template_folder='templates')
