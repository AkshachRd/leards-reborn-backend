from apifairy import other_responses, response, body, authenticate

from project import basic_auth, token_auth
from project.database import db
from . import user_api_blueprint
from .schemas import UserSchema, UserModelSchema, NewUserSchema, TokenSchema
from .user import fetch_user
from project.models import User

# -------
# Schemas
# -------


user_model_schema = UserModelSchema()


@user_api_blueprint.get('/')
@authenticate(token_auth)
@response(user_model_schema, 200)
@other_responses({400: "The user's id was not provided"})
def fetch_model():
    """Get user model"""
    user = token_auth.current_user()
    return fetch_user(user.id_user)


new_user_schema = NewUserSchema()
user_schema = UserSchema()
token_schema = TokenSchema()


@user_api_blueprint.post('/sign-up')
@body(new_user_schema)
@response(user_schema, 201)
def sign_up(kwargs):
    """Create a new user"""
    new_user = User(**kwargs)
    token = new_user.generate_auth_token()
    db.session.add(new_user)
    db.session.commit()
    return dict(token=token)


@user_api_blueprint.post('/get-auth-token')
@authenticate(basic_auth)
@response(token_schema)
@other_responses({401: 'Invalid username or password'})
def get_auth_token():
    """Get authentication token"""
    user = basic_auth.current_user()
    token = user.generate_auth_token()
    db.session.add(user)
    db.session.commit()
    return dict(token=token)
