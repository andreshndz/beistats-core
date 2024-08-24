import datetime as dt

from mongoengine import DateTimeField, StringField
from mongoengine_plus.aio import AsyncDocument
from mongoengine_plus.models import BaseModel, uuid_field
from mongoengine_plus.models.event_handlers import updated_at

from ..requests import TeamRequest


@updated_at.apply
class Team(AsyncDocument, BaseModel):
    """
    Team basic data in a collection
    """

    meta = {'collection': 'teams', 'ordering': ['-created_at']}

    id = StringField(primary_key=True, default=uuid_field('TE'))
    user_id = StringField(required=True)
    name = StringField(required=True)
    created_at = DateTimeField(default=dt.datetime.utcnow)
    updated_at = DateTimeField()
    deactivated_at = DateTimeField()

    @classmethod
    async def create(cls, team_request: TeamRequest, user_id: str):
        new_team = cls(user_id=user_id, **team_request.dict())
        await new_team.async_save()
        return new_team

    async def update(self, team_request: TeamRequest):
        self.name = team_request.name
        self.updated_at = dt.datetime.utcnow()
        await self.async_save()

    async def deactivate(self):
        self.deactivated_at = dt.datetime.utcnow()
        await self.async_save()
