from apifairy import arguments, other_responses, response
from flask import abort, request
import json
import sys

from project import ma
from .schemas import PronunciationSchema, PartsOfSpeechSchema
from . import parser_api_blueprint

sys.path.insert(0, 'G:/')
from englishwiktionaryparser import EnglishWiktionaryParser

# -------
# Schemas
# -------


class NewWordInfoSchema(ma.Schema):
    """Schema defining the attributes when fetching word's info."""
    word = ma.String(required=True)


class WordInfoSchema(ma.Schema):
    """Schema defining the attributes in a word info."""
    id = ma.String()
    word = ma.String()
    translations = ma.List(ma.String())
    pronunciation = ma.Nested(PronunciationSchema)
    partsOfSpeech = ma.Nested(PartsOfSpeechSchema)


new_word_info_schema = NewWordInfoSchema()
word_info_schema = WordInfoSchema()


@parser_api_blueprint.get('/')
@arguments(new_word_info_schema)
@response(word_info_schema, 200)
@other_responses({404: {'message': 'Unknown word'}})
def get_word_info(data):
    """Return word info"""
    parser = EnglishWiktionaryParser()
    # word_data = parser.fetch(request.args.get('word'))
    word_data = parser.fetch(data['word'])

    if not word_data:
        abort(404)
    print(json.dumps(word_data[0]))
    return word_data[0]
