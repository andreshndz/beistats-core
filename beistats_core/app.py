import os

from fastapi import FastAPI
from mongoengine import connect

app = FastAPI(title='beistats_core')

database_uri = os.getenv('DATABASE_URI', 'mongomock://localhost/test')
connect(host=database_uri)


@app.get('/')
def health_check():
    return {'beistats_core': 'I am healthy'}


from beistats_core.views import teams, user_games, users  # isort:skip # NOQA
