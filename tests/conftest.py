from datetime import datetime, timedelta

import jwt
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from beistats_core.app import (
    ALGORITHM,
    JWT_SECRET_KEY,
    MAX_SESSION_MINUTES,
    app,
)
from beistats_core.models.teams import Team
from beistats_core.models.user_games import UserGame
from beistats_core.models.users import User
from beistats_core.requests import (
    TeamRequest,
    UserCreateRequest,
    UserGameRequest,
)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def bad_credentials():
    expire = datetime.utcnow() + timedelta(minutes=MAX_SESSION_MINUTES)
    to_encode = {'sub': 'not_valid_user', 'exp': expire}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return {'Authorization': f'Bearer {encoded_jwt}'}


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
async def user_info(user: User):
    expire = datetime.utcnow() + timedelta(minutes=MAX_SESSION_MINUTES)
    to_encode = {'sub': user.id, 'exp': expire}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    headers = {'Authorization': f'Bearer {encoded_jwt}'}
    yield dict(user=user, headers=headers)


@pytest_asyncio.fixture
async def team_info(team_request: TeamRequest, user_info: dict):
    team = await Team.create(team_request, user_info['user'].id)
    yield dict(team=team, headers=user_info['headers'])
    await team.async_delete()


@pytest_asyncio.fixture
async def user_game_info(team_info: dict):
    team = team_info['team']
    user_game_request = UserGameRequest(
        team_id=team.id,
        at_bat=3,
        h=1,
        k=1,
        bb=1,
        sb=0,
    )
    user_game = await UserGame.create(team.user_id, user_game_request)
    yield dict(user_game=user_game, headers=team_info['headers'])
    await user_game.async_delete()
