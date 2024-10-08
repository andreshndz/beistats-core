import pytest

from beistats_core.models import UserTeamStatistic
from beistats_core.requests import UserGameRequest


@pytest.mark.asyncio
async def test_calculate_stats():
    uts = UserTeamStatistic(user_id='US1', team_id='TE1')
    await uts.async_save()
    user_game_request = UserGameRequest(
        team_id=uts.team_id,
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
    await uts.calculate_stats(user_game_request)
    assert uts.ab == 3
    assert uts.h == 1
    assert uts.double == 0
    assert uts.triple == 0
    assert uts.hr == 0
    assert uts.rbi == 2
    assert uts.r == 1
    assert uts.k == 1
    assert uts.bb == 1
    assert uts.sb == 0
    assert uts.avg == 333
    assert uts.slg == 333
    await uts.async_delete()
