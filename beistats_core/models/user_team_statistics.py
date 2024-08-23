import datetime as dt

from mongoengine import (
    DateTimeField,
    IntField,
    LazyReferenceField,
    StringField,
)
from mongoengine_plus.aio import AsyncDocument
from mongoengine_plus.models import BaseModel, uuid_field
from mongoengine_plus.models.event_handlers import updated_at

from .teams import Team


@updated_at.apply
class UserTeamStatistic(AsyncDocument, BaseModel):
    """
    Team User stats
    """

    meta = {'collection': 'user_team_statistics', 'ordering': ['-created_at']}

    id = StringField(primary_key=True, default=uuid_field('ST'))
    team = LazyReferenceField(Team, required=True)
    ab = IntField(required=True, min_value=0)
    avg = IntField(required=True, min_value=0)
    rbi = IntField(required=True, min_value=0)
    obp = IntField(required=True, min_value=0)
    sb = IntField(required=True, min_value=0)
    created_at = DateTimeField(default=dt.datetime.utcnow)
    updated_at = DateTimeField()