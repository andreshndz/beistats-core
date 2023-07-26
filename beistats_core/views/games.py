from ..app import app


@app.get('/games')
def get_games():
    return {'games': []}
