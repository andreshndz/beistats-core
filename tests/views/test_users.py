import pytest

from beistats_core.models.users import User
from beistats_core.requests import UserCreateRequest, UserUpdateRequest


def test_get_me(client, user_info: dict):
    response = client.get('/users/me', headers=user_info['headers'])
    assert response.status_code == 200
    user_response = response.json()['user']
    assert user_response['id'] == user_info['user'].id


def test_create_user(client, create_user_request: UserCreateRequest):
    response = client.post('/users', json=create_user_request.dict())
    assert response.status_code == 200
    json = response.json()
    valid_fields = [
        'id',
        'first_name',
        'last_name',
        'phone_number',
        'email_address',
        'updated_at',
        'created_at',
    ]
    assert all([json[key] for key in valid_fields])
    assert not json['deactivated_at']


def test_update_user_forbidden(client, user_info: dict):
    update_user_request = UserUpdateRequest(
        first_name='Luis', last_name='Badillo'
    )
    response = client.patch(
        '/users/invalid_id',
        json=update_user_request.dict(),
        headers=user_info['headers'],
    )
    assert response.status_code == 403
    assert response.json()['detail'] == "Can't make this action"


def test_update_user_not_found(client, user_info: dict, bad_credentials: dict):
    update_user_request = UserUpdateRequest(
        first_name='Luis', last_name='Badillo'
    )
    response = client.patch(
        '/users/not_valid_user',
        json=update_user_request.dict(),
        headers=bad_credentials,
    )
    assert response.status_code == 404
    assert response.json()['detail'] == 'User not found'


@pytest.mark.parametrize('use_me', [True, False])
def test_update_user(use_me: bool, client, user_info: dict):
    user: User = user_info['user']
    update_user_request = UserUpdateRequest(
        first_name='Luis', last_name='Badillo'
    )
    url_user_id = 'me' if use_me else user.id
    response = client.patch(
        f'/users/{url_user_id}',
        json=update_user_request.dict(),
        headers=user_info['headers'],
    )
    assert response.status_code == 200
    json = response.json()
    valid_fields = [
        'id',
        'first_name',
        'last_name',
        'phone_number',
        'email_address',
        'updated_at',
        'created_at',
    ]
    assert all([json[key] for key in valid_fields])
    assert not json['deactivated_at']


@pytest.mark.parametrize('use_me', [True, False])
def test_deactivate_user_successfully(use_me: bool, client, user_info: dict):
    user = user_info['user']
    assert not user.deactivated_at
    url_user_id = 'me' if use_me else user.id
    response = client.delete(
        f'/users/{url_user_id}', headers=user_info['headers']
    )
    assert response.status_code == 200
    json = response.json()
    assert all(
        [
            json[key]
            for key in ['id', 'updated_at', 'created_at', 'deactivated_at']
        ]
    )


def test_deactivate_user_forbidden(client, user_info: dict):
    response = client.delete(
        f'/users/invalid_id', headers=user_info['headers']
    )
    assert response.status_code == 403
    json = response.json()
    assert json['detail'] == "Can't make this action"


def test_deactivate_user_not_found(client, bad_credentials: dict):
    response = client.delete(f'/users/not_valid_user', headers=bad_credentials)
    assert response.status_code == 404
    json = response.json()
    assert json['detail'] == 'User not found'
