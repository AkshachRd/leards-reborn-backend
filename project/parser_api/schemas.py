from project import ma


class PartOfSpeechBaseSchema(ma.Schema):
    definitions = ma.Dict(keys=ma.String(),
                          values=ma.List(ma.String(),
                                         allow_null=True)
                          )
    translations = ma.List(ma.String())


class NounSchema(PartOfSpeechBaseSchema):
    countable = ma.Bool()
    plural = ma.String(allow_null=True)


class VerbSchema(PartOfSpeechBaseSchema):
    presentParticiple = ma.String(allow_null=True)
    pastParticiple = ma.String(allow_null=True)
    simplePresent = ma.String(allow_null=True)
    simplePast = ma.String(allow_null=True)


class AdjectiveSchema(PartOfSpeechBaseSchema):
    comparable = ma.Dict(comparative=ma.String(allow_null=True),
                         superlative=ma.String(allow_null=True)
                         )


class AdverbSchema(AdjectiveSchema):
    pass


class PrepositionSchema(PartOfSpeechBaseSchema):
    pass


class ConjunctionSchema(PartOfSpeechBaseSchema):
    pass


class DeterminerSchema(PartOfSpeechBaseSchema):
    plural = ma.String(allow_null=True)


class PronounSchema(DeterminerSchema):
    pass


class InterjectionSchema(PartOfSpeechBaseSchema):
    pass


class PartsOfSpeechSchema(ma.Schema):
    noun = ma.Nested(NounSchema, missing=None, allow_null=True)
    verb = ma.Nested(VerbSchema, missing=None, allow_null=True)
    adjective = ma.Nested(AdjectiveSchema, missing=None, allow_null=True)
    adverb = ma.Nested(AdverbSchema, missing=None, allow_null=True)
    preposition = ma.Nested(PrepositionSchema, missing=None, allow_null=True)
    conjunction = ma.Nested(ConjunctionSchema, missing=None, allow_null=True)
    determiner = ma.Nested(DeterminerSchema, missing=None, allow_null=True)
    pronoun = ma.Nested(PronounSchema, missing=None, allow_null=True)
    interjection = ma.Nested(InterjectionSchema, missing=None, allow_null=True)


class AudioAndTranscriptionSchema(ma.Schema):
    uk = ma.String(missing=None, allow_null=True)
    us = ma.String(missing=None, allow_null=True)


class PronunciationSchema(ma.Schema):
    audio = ma.Nested(AudioAndTranscriptionSchema)
    transcription = ma.Nested(AudioAndTranscriptionSchema)