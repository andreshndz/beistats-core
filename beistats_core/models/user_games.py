import datetime as dt

from mongoengine import DateTimeField, IntField, StringField
from mongoengine_plus.aio import AsyncDocument
from mongoengine_plus.models import BaseModel, uuid_field

from ..requests import UserGameRequest


class UserGame(AsyncDocument, BaseModel):
    """
    Stores stats about a user in a single game
    """

    meta = {'collection': 'user_games', 'ordering': ['-created_at']}

    id = StringField(primary_key=True, default=uuid_field('UG'))
    user_id = StringField(required=True)
    team_id = StringField(required=True)
    at_bat = IntField(required=True, min_value=0)
    h = IntField(required=True, min_value=0)
    k = IntField(required=True, min_value=0)
    bb = IntField(required=True, min_value=0)
    sb = IntField(required=True, min_value=0)
    created_at = DateTimeField(default=dt.datetime.utcnow)

    @classmethod
    async def create(cls, user_id: str, user_game_request: UserGameRequest):
        new_game = cls(user_id=user_id, **user_game_request.dict())
        await new_game.async_save()

        # Calculate whole statistics
        return new_game
