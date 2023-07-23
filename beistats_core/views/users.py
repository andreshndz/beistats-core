from ..app import app

@app.get('/users')
def get_users():
    return {'users': []}