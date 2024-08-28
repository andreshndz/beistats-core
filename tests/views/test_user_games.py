from beistats_core.models.user_games import UserGame
from beistats_core.requests import UserGameRequest


def test_get_user_games(client, user_game_info: dict):
    user_game = user_game_info['user_game']
    headers = user_game_info['headers']
    response = client.get('/user-games', headers=headers)
    assert response.status_code == 200
    assert len(response.json()['user_games']) == 1

    # Sending team_id
    response = client.get(
        f'/user-games?team_id={user_game.team_id}', headers=headers
    )
    assert response.status_code == 200
    assert len(response.json()['user_games']) == 1

    # Sending wrong team_id
    response = client.get('/user-games?team_id=bad', headers=headers)
    assert response.status_code == 200
    assert len(response.json()['user_games']) == 0


def test_create_user_game_invalid_user_authenticated(
    client, team_info: dict, bad_credentials: dict
):
    # Create invalid headers
    headers = bad_credentials

    # Run test with invalid headers
    user_game_request = UserGameRequest(
        team_id='invalid',
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
    response = client.post(
        '/user-games', json=user_game_request.dict(), headers=headers
    )
    assert response.status_code == 400
    json = response.json()
    assert json['detail'] == 'User not found'


def test_create_user_game_invalid_team(client, team_info: dict):
    headers = team_info['headers']
    user_game_request = UserGameRequest(
        team_id='invalid',
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
    response = client.post(
        '/user-games', json=user_game_request.dict(), headers=headers
    )
    assert response.status_code == 400
    json = response.json()
    assert json['detail'] == 'Team not found'


def test_create_user_game_sucessfully(client, team_info: dict):
    team = team_info['team']
    user_game_request = UserGameRequest(
        team_id=team.id,
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
    headers = team_info['headers']
    response = client.post(
        '/user-games', json=user_game_request.dict(), headers=headers
    )
    assert response.status_code == 200
    json = response.json()
    valid_fields = [
        'id',
        'user_id',
        'team_id',
        'at_bat',
        'h',
        'double',
        'triple',
        'hr',
        'rbi',
        'r',
        'k',
        'bb',
        'sb',
        'created_at',
    ]
    assert all([key in json for key in valid_fields])
    assert json['team_id'] == team.id
    assert json['user_id'] == team.user_id
    UserGame.objects.delete()
