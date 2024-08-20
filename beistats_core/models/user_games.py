import datetime as dt

from mongoengine import (
    DateTimeField,
    IntField,
    LazyReferenceField,
    StringField,
)
from mongoengine_plus.aio import AsyncDocument
from mongoengine_plus.models import BaseModel, uuid_field

from ..requests import UserGameRequest
from .teams import Team
from .users import User


class UserGame(AsyncDocument, BaseModel):
    """
    Stores stats about a user in a single game
    """

    meta = {'collection': 'user_games'}

    id = StringField(primary_key=True, default=uuid_field('UG'))
    user = LazyReferenceField(User, required=True)
    team = LazyReferenceField(Team, required=True)
    at_bat = IntField(required=True, min_value=0)
    h = IntField(required=True, min_value=0)
    k = IntField(required=True, min_value=0)
    bb = IntField(required=True, min_value=0)
    sb = IntField(required=True, min_value=0)
    created_at = DateTimeField(default=dt.datetime.utcnow)

    @classmethod
    async def create(
        cls, user: User, team: Team, user_game_request: UserGameRequest
    ):
        new_game = cls(
            user=user,
            team=team,
            **user_game_request.dict(exclude={'user_id', 'team_id'}),
        )
        await new_game.async_save()

        # Calculate whole statistics
        return new_game

    def to_dict(self):
        return dict(
            id=self.id,
            user_id=self.user.id,
            team_id=self.team.id,
            at_bat=self.at_bat,
            h=self.h,
            k=self.k,
            bb=self.bb,
            sb=self.sb,
            created_at=self.created_at.isoformat(),
        )
