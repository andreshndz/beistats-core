import datetime as dt

from mongoengine import DateTimeField, IntField, StringField
from mongoengine_plus.aio import AsyncDocument
from mongoengine_plus.models import BaseModel, uuid_field

from ..requests import UserGameRequest
from .user_team_statistics import UserTeamStatistic


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
    double = IntField(required=True, min_value=0)
    triple = IntField(required=True, min_value=0)
    hr = IntField(required=True, min_value=0)
    r = IntField(required=True, min_value=0)
    rbi = IntField(required=True, min_value=0)
    k = IntField(required=True, min_value=0)
    bb = IntField(required=True, min_value=0)
    sb = IntField(required=True, min_value=0)
    created_at = DateTimeField(default=dt.datetime.utcnow)

    @classmethod
    async def create(cls, user_id: str, user_game_request: UserGameRequest):
        new_game = cls(user_id=user_id, **user_game_request.dict())
        await new_game.async_save()

        # Calculate whole statistics
        uts = UserTeamStatistic.objects.get(
            user_id=user_id, team_id=new_game.team_id
        )
        await uts.calculate_stats(user_game_request)
        return new_game
