from beistats_core.models.teams import Team
from beistats_core.models.users import User
from beistats_core.requests import UserGameRequest


def test_create_user_game_invalid_user(client, user: User, team: Team):
    user_game_request = UserGameRequest(
        user_id='invalid',
        team_id=team.id,
        at_bat=3,
        h=1,
        k=1,
        bb=1,
        sb=0,
    )
    response = client.post('/user-games', json=user_game_request.dict())
    assert response.status_code == 400
    json = response.json()
    assert json['detail'] == 'User not found'


def test_create_user_game_invalid_team(client, user: User, team: Team):
    user_game_request = UserGameRequest(
        user_id=user.id,
        team_id='invalid',
        at_bat=3,
        h=1,
        k=1,
        bb=1,
        sb=0,
    )
    response = client.post('/user-games', json=user_game_request.dict())
    assert response.status_code == 400
    json = response.json()
    assert json['detail'] == 'Team not found'


def test_create_user_game_sucessfully(client, user: User, team: Team):
    user_game_request = UserGameRequest(
        user_id=user.id,
        team_id=team.id,
        at_bat=3,
        h=1,
        k=1,
        bb=1,
        sb=0,
    )
    response = client.post('/user-games', json=user_game_request.dict())
    assert response.status_code == 200
    json = response.json()
    valid_fields = [
        'id',
        'user_id',
        'team_id',
        'at_bat',
        'h',
        'k',
        'bb',
        'sb',
        'created_at',
    ]
    assert all([key in json for key in valid_fields])
