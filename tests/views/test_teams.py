from beistats_core.models.teams import Team


def test_create_team(client):
    response = client.post('/teams', json={'name': 'Trabuco'})
    assert response.status_code == 200
    json = response.json()
    assert all([json[key] for key in ['id', 'updated_at', 'created_at']])
    assert not json['deactivated_at']
    assert json['name'] == 'Trabuco'


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
