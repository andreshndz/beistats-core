import datetime as dt

from mongoengine import DateTimeField, IntField, StringField
from mongoengine_plus.aio import AsyncDocument
from mongoengine_plus.models import BaseModel, uuid_field
from mongoengine_plus.models.event_handlers import updated_at

from ..requests import UserGameRequest


@updated_at.apply
class UserTeamStatistic(AsyncDocument, BaseModel):
    """
    Team User stats
    """

    meta = {'collection': 'user_team_statistics', 'ordering': ['-created_at']}

    id = StringField(primary_key=True, default=uuid_field('ST'))
    team_id = StringField(required=True)
    user_id = StringField(required=True)
    ab = IntField(required=True, min_value=0, default=0)
    h = IntField(required=True, min_value=0, default=0)
    double = IntField(required=True, min_value=0, default=0)
    triple = IntField(required=True, min_value=0, default=0)
    hr = IntField(required=True, min_value=0, default=0)
    r = IntField(required=True, min_value=0, default=0)
    bb = IntField(required=True, min_value=0, default=0)
    k = IntField(required=True, min_value=0, default=0)
    avg = IntField(required=True, min_value=0, default=0)
    slg = IntField(required=True, min_value=0, default=0)
    obp = IntField(required=True, min_value=0, default=0)
    rbi = IntField(required=True, min_value=0, default=0)
    sb = IntField(required=True, min_value=0, default=0)
    created_at = DateTimeField(default=dt.datetime.utcnow)
    updated_at = DateTimeField()

    async def calculate_stats(self, user_game_request: UserGameRequest):
        self.ab += user_game_request.at_bat
        self.h += user_game_request.h
        self.bb += user_game_request.bb
        self.k += user_game_request.k
        self.double += user_game_request.double
        self.triple += user_game_request.triple
        self.hr += user_game_request.hr
        self.rbi += user_game_request.rbi
        self.r += user_game_request.r
        self.sb += user_game_request.sb

        self.avg = int(
            (self.h + self.double + self.triple + self.hr) / self.ab * 1000
        )
        self.slg = int(
            (self.h + 2 * self.double + 3 * self.triple + 4 * self.hr)
            / self.ab
            * 1000
        )
        await self.async_save()
