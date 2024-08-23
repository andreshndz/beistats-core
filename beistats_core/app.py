import os

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from mongoengine import connect

app = FastAPI(title='beistats_core')

database_uri = os.getenv('DATABASE_URI', 'mongomock://localhost/test')
connect(host=database_uri)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'secret_key')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
MAX_SESSION_MINUTES = 30


@app.get('/')
def health_check():
    return {'beistats_core': 'I am healthy'}


from beistats_core.views import (  # isort:skip # NOQA
    login,
    teams,
    user_games,
    users,
)
