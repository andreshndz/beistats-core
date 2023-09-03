from mongoengine import DateTimeField, LazyReferenceField, StringField
from mongoengine_plus.aio import AsyncDocument
from mongoengine_plus.models import BaseModel, uuid_field

from . import Team


class Game(AsyncDocument, BaseModel):
    """
    Game basic data in a collection
    """

    meta = {'collection': 'games'}

    id = StringField(primary_key=True, default=uuid_field('GA'))
    away = LazyReferenceField(Team, required=True)
    home = LazyReferenceField(Team, required=True)
    date = DateTimeField(required=True)
