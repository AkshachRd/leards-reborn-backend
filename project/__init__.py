"""
Welcome to the documentation for the Leards API!

## Introduction

The Leards API is an API (Application Programming Interface) for creating **cards** that helps out to learn a new
language.

## Key Functionality

The Leards API has the following functionality:

1. Getting word's translations.
2. Work with cards, decks, and folders:
  * Create a new card/deck/folder
  * Update a card/deck/folder
  * Delete a card/deck/folder
  * Get all user's model
3. Authorization.
4. <More to come!>

## Key Modules

This project is written using Python 3.10.1.

The project utilizes the following modules:

* **Flask**: micro-framework for web application development which includes the following dependencies:
  * **click**: package for creating command-line interfaces (CLI)
  * **itsdangerous**: cryptographically sign data
  * **Jinja2**: templating engine
  * **MarkupSafe**: escapes characters so text is safe to use in HTML and XML
  * **Werkzeug**: set of utilities for creating a Python application that can talk to a WSGI server
* **APIFairy**: API framework for Flask which includes the following dependencies:
  * **Flask-Marshmallow** - Flask extension for using Marshmallow (object serialization/deserialization library)
  * **Flask-HTTPAuth** - Flask extension for HTTP authentication
  * **apispec** - API specification generator that supports the OpenAPI specification
* **pytest**: framework for testing Python projects
"""

from apifairy import APIFairy
from flask import Flask
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_marshmallow import Marshmallow
from .database import db

apifairy = APIFairy()
ma = Marshmallow()
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


def create_app():
    app = Flask(__name__)

    app.config['APIFAIRY_TITLE'] = 'Leards API'
    app.config['APIFAIRY_VERSION'] = '0.1'
    app.config['APIFAIRY_UI'] = 'elements'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'path_to_db?check_same_thread=False'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    initialize_extensions(app)
    register_blueprints(app)
    return app


def initialize_extensions(app):
    apifairy.init_app(app)
    ma.init_app(app)
    db.init_app(app)


def register_blueprints(app):
    from project.parser_api import parser_api_blueprint
    from project.user_api import user_api_blueprint
    app.register_blueprint(parser_api_blueprint, url_prefix='/parser')
    app.register_blueprint(user_api_blueprint, url_prefix='/user')
