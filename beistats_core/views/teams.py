from fastapi import Depends, HTTPException

from ..app import app
from ..models.teams import Team
from ..queries import BaseQueryParams
from ..requests import TeamRequest
from .utils import get_authenticated_user


@app.get('/teams')
def get_teams(
    params: BaseQueryParams = Depends(),
    user_id: str = Depends(get_authenticated_user),
):
    query = (
        Team.objects(user_id=user_id).skip(params.offset).limit(params.size)
    )
    return {'teams': [team.to_dict() for team in query.all()]}


@app.post('/teams')
async def create_team(
    team_request: TeamRequest, user_id: str = Depends(get_authenticated_user)
):
    team = await Team.create(team_request, user_id)
    return team.to_dict()


@app.patch('/teams/{team_id}')
async def update_team(
    team_id: str,
    team_request: TeamRequest,
    user_id: str = Depends(get_authenticated_user),
):
    try:
        team = Team.objects.get(id=team_id, user_id=user_id)
    except Team.DoesNotExist:
        raise HTTPException(status_code=404, detail='Team not found')
    else:
        await team.update(team_request)
        return team.to_dict()


@app.delete('/teams/{team_id}')
async def deactivate_team(
    team_id: str, user_id: str = Depends(get_authenticated_user)
):
    try:
        team = Team.objects.get(id=team_id, user_id=user_id)
    except Team.DoesNotExist:
        raise HTTPException(status_code=404, detail="Team not found")
    else:
        await team.deactivate()
        return team.to_dict()


# @app.get('/user-teams')
# def get_user_teams(
#     params: BaseQueryParams = Depends(),
#     user_id: str = Depends(get_authenticated_user)
# ):
#     query = Team.objects.skip(params.offset).limit(params.size)
#     return {'teams': [team.to_dict() for team in query.all()]}
