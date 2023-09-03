import datetime as dt

from mongoengine import DateTimeField, LazyReferenceField, StringField
from mongoengine_plus.aio import AsyncDocument
from mongoengine_plus.models import BaseModel, uuid_field
from mongoengine_plus.models.event_handlers import updated_at

from . import League


@updated_at.apply
class Team(AsyncDocument, BaseModel):
    """
    Team basic data in a collection
    """

    meta = {'collection': 'teams'}

    id = StringField(primary_key=True, default=uuid_field('TE'))
    name = StringField(required=True)
    league = LazyReferenceField(League, required=True)
    created_at = DateTimeField(default=dt.datetime.utcnow)
    updated_at = DateTimeField()
