from fastapi import HTTPException

from ..app import app
from ..models import Team, User, UserGame
from ..requests import GameRequest


@app.get('/user-games')
def get_user_games():
    return {'games': []}


@app.post('/user-games')
async def create_user_game(game_request: GameRequest):
    try:
        user = User.objects.get(id=game_request.user_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=400, detail="User not found")
    
    try:
        team = Team.objects.get(id=game_request.team_id)
    except Team.DoesNotExist:
        raise HTTPException(status_code=400, detail="Team not found")
    
    user_game = await Game.create(user, team, game_request)
    return user_game