import datetime as dt

from mongoengine import DateTimeField, StringField
from mongoengine_plus.aio import AsyncDocument
from mongoengine_plus.models import BaseModel, uuid_field
from mongoengine_plus.models.event_handlers import updated_at
from mongoengine_plus.types import EnumField

from .types import UserType


@updated_at.apply
class User(AsyncDocument, BaseModel):
    """
    User basic data in a collection
    """

    meta = {'collection': 'users'}

    id = StringField(primary_key=True, default=uuid_field('US'))
    name = StringField(required=True)
    phone_number = StringField(required=True)
    email_address = StringField(required=True)
    created_at = DateTimeField(default=dt.datetime.utcnow)
    updated_at = DateTimeField()
    type = EnumField(UserType, required=True)
