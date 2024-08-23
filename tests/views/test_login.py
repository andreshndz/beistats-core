import jwt

from beistats_core.app import ALGORITHM, JWT_SECRET_KEY
from beistats_core.models.users import User
from beistats_core.requests import LoginRequest


def test_login_successfully(client, user: User):
    login_request = LoginRequest(
        email_address=user.email_address, password='1234'
    )
    response = client.post('/login', json=login_request.dict())
    assert response.status_code == 200
    token = response.json()['token']
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    assert payload.get('sub') == user.id


def test_login_invalid(client):
    login_request = LoginRequest(
        email_address='fake@test.com', password='1234'
    )
    response = client.post('/login', json=login_request.dict())
    assert response.status_code == 400
    assert response.json()['detail'] == 'Invalid Data'
