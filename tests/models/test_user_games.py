import pytest

from beistats_core.models.user_games import UserGame
from beistats_core.requests import UserGameRequest


@pytest.mark.asyncio
async def test_create_user_game(team_info: dict):
    team = team_info['team']
    user_game_request = UserGameRequest(
        team_id=team.id,
        at_bat=3,
        h=1,
        double=0,
        triple=0,
        hr=0,
        rbi=2,
        r=1,
        k=1,
        bb=1,
        sb=0,
    )
    user_game = await UserGame.create(team.user_id, user_game_request)
    assert user_game.id
    assert user_game.user_id == team.user_id
    assert user_game.team_id == team.id
    assert user_game.created_at
    await user_game.async_delete()
