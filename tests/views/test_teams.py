def test_create_team(client):
    response = client.post('/teams', json={'name': 'Trabuco'})
    breakpoint()
    assert response.status_code == 200
    json = response.json()
    assert json['id']
    assert json['name'] == 'Trabuco'
