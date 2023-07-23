from typing import Union

from fastapi import FastAPI

app = FastAPI(title='beistats_core')


@app.get('/')
def health_check():
    return {'beistats_core': 'I am healthy'}

from .views import *