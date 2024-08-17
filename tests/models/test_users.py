import pytest

from beistats_core.models.users import User
from beistats_core.requests import UserCreateRequest, UserUpdateRequest


@pytest.mark.asyncio
async def test_create_user(create_user_request: UserCreateRequest):
    user = await User.create(create_user_request)
    assert user.first_name == create_user_request.first_name
    assert user.last_name == create_user_request.last_name
    assert user.type == create_user_request.type
    assert user.phone_number == create_user_request.phone_number
    assert user.email_address == create_user_request.email_address
    assert user.created_at
    assert user.updated_at
    assert not user.deactivated_at


@pytest.mark.asyncio
async def test_update_user(user: User):
    last_update = user.updated_at
    update_request = UserUpdateRequest(first_name='Pablo', last_name='Lopez')
    await user.update(update_request)
    assert user.updated_at > last_update
    assert not user.deactivated_at
    assert user.first_name == update_request.first_name
    assert user.last_name == update_request.last_name


@pytest.mark.asyncio
async def test_deactivate_user(user: User):
    assert not user.deactivated_at
    await user.deactivate()
    assert user.deactivated_at
