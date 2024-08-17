import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from beistats_core.app import app
from beistats_core.models.users import User
from beistats_core.requests import UserCreateRequest


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


@pytest_asyncio.fixture
async def user(create_user_request: UserCreateRequest):
    user = await User.create(create_user_request)
    yield user
    await user.async_delete()
