import pytest

from beistats_core.models.teams import Team
from beistats_core.requests import TeamRequest


@pytest.mark.asyncio
async def test_create_team(team_request: TeamRequest):
    team = await Team.create(team_request)
    assert team.name == team_request.name
    assert team.created_at
    assert team.updated_at
    assert not team.deactivated_at
    await team.async_delete()


@pytest.mark.asyncio
async def test_update_team(team: Team):
    last_update = team.updated_at
    update_request = TeamRequest(name='Leones')
    await team.update(update_request)
    assert team.updated_at > last_update
    assert not team.deactivated_at
    assert team.name == update_request.name


@pytest.mark.asyncio
async def test_deactivate_team(team: Team):
    assert not team.deactivated_at
    await team.deactivate()
    assert team.deactivated_at
