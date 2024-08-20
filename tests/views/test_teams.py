from beistats_core.models.teams import Team
from beistats_core.requests import TeamRequest


def test_get_teams(client):
    response = client.get('/teams')
    assert response.status_code == 200
    assert response.json() == {'teams': []}


def test_create_team(client):
    response = client.post('/teams', json={'name': 'Trabuco'})
    assert response.status_code == 200
    json = response.json()
    assert all([json[key] for key in ['id', 'updated_at', 'created_at']])
    assert not json['deactivated_at']
    assert json['name'] == 'Trabuco'


def test_update_team_not_found(client, team: Team):
    update_team_request = TeamRequest(name='Yankees')
    response = client.patch(
        '/teams/invalid_id', json=update_team_request.dict()
    )
    assert response.status_code == 404
    assert response.json()['detail'] == 'Team not found'


def test_update_team_successfully(client, team: Team):
    update_team_request = TeamRequest(name='Yankees')
    response = client.patch(
        f'/teams/{team.id}', json=update_team_request.dict()
    )
    assert response.status_code == 200
    json = response.json()
    assert all([json[key] for key in ['id', 'updated_at', 'created_at']])
    assert not json['deactivated_at']
    assert json['id'] == team.id
    assert json['name'] == 'Yankees'


def test_deactivate_team_successfully(client, team: Team):
    assert not team.deactivated_at
    response = client.delete(f'/teams/{team.id}')
    assert response.status_code == 200
    json = response.json()
    assert all(
        [
            json[key]
            for key in ['id', 'updated_at', 'created_at', 'deactivated_at']
        ]
    )


def test_deactivate_team_not_found(client):
    response = client.delete(f'/teams/invalid_id')
    assert response.status_code == 404
    json = response.json()
    assert json['detail'] == 'Team not found'
