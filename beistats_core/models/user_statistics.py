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


class UserStatistic(AsyncDocument, BaseModel):
    meta = {'collection': 'user_statistics'}

    id = StringField(primary_key=True, default=uuid_field('ST'))
    user = LazyReferenceField(User, required=True)
    team_name = StringField(required=True)
    avg = IntField(required=True, min_value=0)
    rbi = IntField(required=True, min_value=0)
    obp = IntField(required=True, min_value=0)
    sb = IntField(required=True, min_value=0)
    created_at = DateTimeField(default=dt.datetime.utcnow)
