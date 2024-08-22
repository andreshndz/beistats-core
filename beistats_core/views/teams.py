from fastapi import Depends, HTTPException

from ..app import app
from ..models.teams import Team
from ..queries import BaseQueryParams
from ..requests import TeamRequest


@app.get('/teams')
def get_teams(params: BaseQueryParams = Depends()):
    query = Team.objects.skip(params.offset).limit(params.size)
    return {'teams': [team.to_dict() for team in query.all()]}


@app.post('/teams')
async def create_team(team_request: TeamRequest):
    team = await Team.create(team_request)
    return team.to_dict()


@app.patch('/teams/{team_id}')
async def update_team(team_id: str, team_request: TeamRequest):
    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        raise HTTPException(status_code=404, detail="Team not found")
    else:
        await team.update(team_request)
        return team.to_dict()


@app.delete('/teams/{team_id}')
async def deactivate_team(team_id: str):
    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        raise HTTPException(status_code=404, detail="Team not found")
    else:
        await team.deactivate()
        return team.to_dict()
