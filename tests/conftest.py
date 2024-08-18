import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from beistats_core.app import app
from beistats_core.models.teams import Team
from beistats_core.models.users import User
from beistats_core.requests import TeamRequest, UserCreateRequest


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def create_user_request():
    return UserCreateRequest(
        first_name='Pedro',
        last_name='Perez',
        phone_number='+525512345678',
        email_address='pperez@test.com',
    )


@pytest.fixture
def team_request():
    return TeamRequest(name='Trabuco')


@pytest_asyncio.fixture
async def user(create_user_request: UserCreateRequest):
    user = await User.create(create_user_request)
    yield user
    await user.async_delete()


@pytest_asyncio.fixture
async def team(team_request: TeamRequest):
    team = await Team.create(team_request)
    yield team
    await team.async_delete()
