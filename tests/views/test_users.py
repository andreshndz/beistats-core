from beistats_core.models.users import User
from beistats_core.requests import UserCreateRequest


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


def test_deactivate_user_successfully(client, user: User):
    assert not user.deactivated_at
    response = client.delete(f'/users/{user.id}')
    assert response.status_code == 200
    json = response.json()
    assert all(
        [
            json[key]
            for key in ['id', 'updated_at', 'created_at', 'deactivated_at']
        ]
    )


def test_deactivate_user_not_found(client):
    response = client.delete(f'/users/invalid_id')
    assert response.status_code == 404
    json = response.json()
    assert json['detail'] == 'User not found'
