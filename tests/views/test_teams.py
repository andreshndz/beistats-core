from beistats_core.requests import TeamRequest


def test_get_teams(client, team_info: dict):
    response = client.get('/teams', headers=team_info['headers'])
    assert response.status_code == 200
    teams = response.json()['teams']
    assert len(teams) == 1
    assert teams[0]['id'] == team_info['team'].id


def test_create_team(client, user_info: dict):
    response = client.post(
        '/teams', json={'name': 'Trabuco'}, headers=user_info['headers']
    )
    assert response.status_code == 200
    json = response.json()
    assert all([json[key] for key in ['id', 'updated_at', 'created_at']])
    assert not json['deactivated_at']
    assert json['name'] == 'Trabuco'
    assert json['user_id'] == user_info['user'].id


def test_update_team_not_found(client, team_info: dict):
    update_team_request = TeamRequest(name='Yankees')
    response = client.patch(
        '/teams/invalid_id',
        json=update_team_request.dict(),
        headers=team_info['headers'],
    )
    assert response.status_code == 404
    assert response.json()['detail'] == 'Team not found'


def test_update_team_successfully(client, team_info: dict):
    update_team_request = TeamRequest(name='Yankees')
    team = team_info['team']
    response = client.patch(
        f'/teams/{team.id}',
        json=update_team_request.dict(),
        headers=team_info['headers'],
    )
    assert response.status_code == 200
    json = response.json()
    assert all([json[key] for key in ['id', 'updated_at', 'created_at']])
    assert not json['deactivated_at']
    assert json['id'] == team.id
    assert json['name'] == 'Yankees'
    assert json['user_id'] == team.user_id


def test_deactivate_team_successfully(client, team_info: dict):
    team = team_info['team']
    assert not team.deactivated_at
    response = client.delete(f'/teams/{team.id}', headers=team_info['headers'])
    assert response.status_code == 200
    json = response.json()
    assert all(
        [
            json[key]
            for key in ['id', 'updated_at', 'created_at', 'deactivated_at']
        ]
    )


def test_deactivate_team_not_found(client, team_info: dict):
    response = client.delete(
        f'/teams/invalid_id', headers=team_info['headers']
    )
    assert response.status_code == 404
    json = response.json()
    assert json['detail'] == 'Team not found'
