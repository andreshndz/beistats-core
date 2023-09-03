import datetime as dt

from mongoengine import (
    DateTimeField,
    IntField,
    LazyReferenceField,
    StringField,
)
from mongoengine_plus.aio import AsyncDocument
from mongoengine_plus.models import BaseModel, uuid_field

from . import User


class UserGame(AsyncDocument, BaseModel):
    """
    Stores stats about a user in a single game
    """

    meta = {'collection': 'user_games'}

    id = StringField(primary_key=True, default=uuid_field('UG'))
    user = LazyReferenceField(User, required=True)
    team_name = StringField(required=True)
    at_bat = IntField(required=True, min_value=0)
    h = IntField(required=True, min_value=0)
    k = IntField(required=True, min_value=0)
    bb = IntField(required=True, min_value=0)
    sb = IntField(required=True, min_value=0)
    created_at = DateTimeField(default=dt.datetime.utcnow)
