from fastapi import Depends, HTTPException

from ..app import app
from ..models import Team, User, UserGame
from ..queries import UserGamesQueryParams
from ..requests import UserGameRequest
from .utils import get_authenticated_user


@app.get('/user-games')
def get_user_games(
    params: UserGamesQueryParams = Depends(),
    user_id: str = Depends(get_authenticated_user),
):
    query = (
        UserGame.objects(user_id=user_id)
        .skip(params.offset)
        .limit(params.size)
    )
    if params.team_id:
        query = query.filter(team_id=params.team_id)
    return {'user_games': [user_game.to_dict() for user_game in query.all()]}


@app.post('/user-games')
async def create_user_game(
    user_game_request: UserGameRequest,
    user_id: str = Depends(get_authenticated_user),
):
    try:
        await User.objects.async_get(id=user_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=400, detail="User not found")

    try:
        await Team.objects.async_get(
            id=user_game_request.team_id, user_id=user_id
        )
    except Team.DoesNotExist:
        raise HTTPException(status_code=400, detail="Team not found")

    user_game = await UserGame.create(user_id, user_game_request)
    return user_game.to_dict()
