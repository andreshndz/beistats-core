import datetime as dt

from mongoengine import DateTimeField, LazyReferenceField, StringField
from mongoengine_plus.aio import AsyncDocument
from mongoengine_plus.models import BaseModel, uuid_field
from mongoengine_plus.models.event_handlers import updated_at

from . import User


@updated_at.apply
class League(AsyncDocument, BaseModel):
    """
    League basic data in a collection
    """

    meta = {'collection': 'leagues'}

    id = StringField(primary_key=True, default=uuid_field('LE'))
    name = StringField(required=True)
    created_by = LazyReferenceField(User, required=True)
    created_at = DateTimeField(default=dt.datetime.utcnow)
    updated_at = DateTimeField()
