from mongoengine import (
    DateTimeField,
    DoesNotExist,
    EmbeddedDocumentField,
    IntField,
    LazyReferenceField,
    ListField,
    StringField,
    URLField,
)
from mongoengine_plus.aio import AsyncDocument
from mongoengine_plus.models import BaseModel, uuid_field
from mongoengine_plus.models.event_handlers import updated_at


class Game(AsyncDocument, BaseModel):
    meta = {'collection': 'games'}

    id = StringField(primary_key=True, default=uuid_field('GA'))
    user = LazyReferenceField(User, required=True)
    team_name = StringField(required=True)
    at_bat = IntField(required=True, min_value=0)
    h = IntField(required=True, min_value=0)
    k = IntField(required=True, min_value=0)
    bb = IntField(required=True, min_value=0)
    sb = IntField(required=True, min_value=0)
    created_at = DateTimeField(default=dt.datetime.utcnow)
