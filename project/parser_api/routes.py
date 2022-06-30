from apifairy import other_responses, response, authenticate
from flask import abort
import sys

from project import ma, token_auth
from .schemas import PronunciationSchema, PartsOfSpeechSchema
from . import parser_api_blueprint

sys.path.insert(0, 'G:/')
from englishwiktionaryparser import EnglishWiktionaryParser

# -------
# Schemas
# -------


class WordInfoSchema(ma.Schema):
    """Schema defining the attributes in a word info."""
    id = ma.String()
    word = ma.String()
    translations = ma.List(ma.String())
    pronunciation = ma.Nested(PronunciationSchema)
    partsOfSpeech = ma.Nested(PartsOfSpeechSchema)


word_info_schema = WordInfoSchema()


@parser_api_blueprint.get('/<string:word>')
@authenticate(token_auth)
@response(word_info_schema, 200)
@other_responses({404: 'Unknown word'})
def get_word_info(word):
    """Return word info"""
    parser = EnglishWiktionaryParser()
    word_data = parser.fetch(word)

    if not word_data:
        abort(404)

    return word_data[0]
