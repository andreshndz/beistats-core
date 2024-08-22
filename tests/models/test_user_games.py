import pytest

from beistats_core.models.teams import Team
from beistats_core.models.user_games import UserGame
from beistats_core.models.users import User
from beistats_core.requests import UserGameRequest


@pytest.mark.asyncio
async def test_create_user_game(user: User, team: Team):
    user_game_request = UserGameRequest(
        user_id=user.id,
        team_id=team.id,
        at_bat=3,
        h=1,
        k=1,
        bb=1,
        sb=0,
    )
    user_game = await UserGame.create(user, team, user_game_request)
    assert user_game.id
    assert user_game.user.id == user.id
    assert user_game.team.id == team.id
    assert user_game.created_at
    await user_game.async_delete()
