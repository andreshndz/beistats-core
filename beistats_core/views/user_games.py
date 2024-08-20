from fastapi import HTTPException

from ..app import app
from ..models.teams import Team
from ..models.user_games import UserGame
from ..models.users import User
from ..requests import UserGameRequest


@app.get('/user-games')
def get_user_games():
    return {'games': []}


@app.post('/user-games')
async def create_user_game(user_game_request: UserGameRequest):
    try:
        user = User.objects.get(id=user_game_request.user_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=400, detail="User not found")

    try:
        team = Team.objects.get(id=user_game_request.team_id)
    except Team.DoesNotExist:
        raise HTTPException(status_code=400, detail="Team not found")

    user_game = await UserGame.create(user, team, user_game_request)
    return user_game.to_dict()
