from .database import db
from uuid import uuid4
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import secrets


class User(db.Model):
    __tablename__ = 'user'

    id_user = db.Column(db.String(36), default=str(uuid4()), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hashed = db.Column(db.String(128), nullable=False)
    auth_token = db.Column(db.String(64), index=True)
    auth_token_expiration = db.Column(db.DateTime)
    id_root_folder = db.Column(db.String(36), db.ForeignKey('folder.id_folder'))

    def __init__(self, name: str, email: str, password: str):
        """Create a new User object."""
        self.name = name
        self.email = email
        self.password_hashed = self._generate_password_hash(password)

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password_hashed, password_plaintext)

    def set_password(self, password_plaintext: str):
        self.password_hashed = self._generate_password_hash(password_plaintext)

    @staticmethod
    def _generate_password_hash(password_plaintext):
        return generate_password_hash(password_plaintext)

    def generate_auth_token(self):
        self.auth_token = secrets.token_urlsafe()
        self.auth_token_expiration = datetime.utcnow() + timedelta(minutes=60)
        return self.auth_token

    @staticmethod
    def verify_auth_token(auth_token):
        user = User.query.filter_by(auth_token=auth_token).first()
        if user and user.auth_token_expiration > datetime.utcnow():
            return user

    def revoke_auth_token(self):
        self.auth_token_expiration = datetime.utcnow()

    def __repr__(self):
        return '<User %r>' % self.name


class Card(db.Model):
    __tablename__ = 'card'

    id_card = db.Column(db.String(36), default=str(uuid4()), primary_key=True)
    front_side = db.Column(db.String(255), nullable=False)
    back_side = db.Column(db.String(255), nullable=False)
    id_deck = db.Column(db.String(36), db.ForeignKey('deck.id_deck'), nullable=False)

    def __init__(self, front_side: str, back_side: str, id_deck: str):
        self.front_side = front_side
        self.back_side = back_side
        self.id_deck = id_deck

    def update(self, front_side: str, back_side: str):
        self.front_side = front_side
        self.back_side = back_side

    def __repr__(self):
        return '<Card %r %r>' % (self.front_side, self.back_side)


class Deck(db.Model):
    __tablename__ = 'deck'

    id_deck = db.Column(db.String(36), default=str(uuid4()), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    id_folder = db.Column(db.String(36), db.ForeignKey('folder.id_folder'), nullable=False)

    cards = db.relationship('Card', backref='deck')

    def __init__(self, name: str, id_folder: str):
        self.name = name
        self.id_folder = id_folder

    def __repr__(self):
        return '<Deck %r>' % self.name


class Folder(db.Model):
    __tablename__ = 'folder'

    id_folder = db.Column(db.String(36), default=str(uuid4()), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    id_parent_folder = db.Column(db.String(36), db.ForeignKey('folder.id_folder'))

    decks = db.relationship('Deck', backref='folder')

    def __init__(self, name: str, id_parent_folder: str | None = None):
        self.name = name
        self.id_parent_folder = id_parent_folder

    def __repr__(self):
        return '<Folder %r>' % self.name
