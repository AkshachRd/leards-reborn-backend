from marshmallow_union import Union

from project import ma


class UserSchema(ma.Schema):
    """Schema defining the attributes of a user."""
    id = ma.String()
    name = ma.String()
    email = ma.Email()


class UnionMemberMixin:
    def dump(self, *arg, **kwargs):
        """Raise if obj is not valid, will make union skip to next member."""
        errors = self.validate(*arg, **kwargs)
        if errors:
            raise ValueError(errors)
        return super().dump(*arg, **kwargs)


class WordSchema(ma.Schema):
    id = ma.String()
    name = ma.String()
    translations = ma.List(ma.String)


class ContainerSchema(ma.Schema):
    id = ma.String()
    name = ma.String()


class DeckSchema(UnionMemberMixin, ContainerSchema):
    cards = ma.List(ma.Nested(WordSchema))


class FolderSchema(UnionMemberMixin, ContainerSchema):
    children = ma.List(Union([ma.Nested(lambda: FolderSchema), ma.Nested(DeckSchema)]))


class UserModelSchema(ma.Schema):
    """Schema defining the attributes in a user's model."""
    user = ma.Nested(UserSchema)
    state = ma.Nested(FolderSchema)


class NewUserSchema(ma.Schema):
    """Schema defining the attributes when creating a new user."""
    name = ma.String()
    email = ma.String()
    password = ma.String()


class TokenSchema(ma.Schema):
    """Schema defining the attributes of a token."""
    token = ma.String()
