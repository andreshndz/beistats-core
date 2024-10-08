import pytest

from beistats_core.models import Team, UserTeamStatistic
from beistats_core.requests import TeamRequest


@pytest.mark.asyncio
async def test_create_team(team_request: TeamRequest):
    team = await Team.create(team_request, 'US1')
    assert team.name == team_request.name
    assert team.user_id == 'US1'
    assert team.created_at
    assert team.updated_at
    assert not team.deactivated_at
    await team.async_delete()
    assert await UserTeamStatistic.objects.async_get(
        user_id='US1', team_id=team.id
    )


@pytest.mark.asyncio
async def test_update_team(team_info: dict):
    team = team_info['team']
    last_update = team.updated_at
    update_request = TeamRequest(name='Leones')
    await team.update(update_request)
    assert team.updated_at > last_update
    assert not team.deactivated_at
    assert team.name == update_request.name


@pytest.mark.asyncio
async def test_deactivate_team(team_info: dict):
    team = team_info['team']
    assert not team.deactivated_at
    await team.deactivate()
    assert team.deactivated_at
