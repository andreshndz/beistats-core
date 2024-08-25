from fastapi import Depends, HTTPException

from ..app import app
from ..models import User
from ..queries import BaseQueryParams
from ..requests import UserCreateRequest, UserUpdateRequest


@app.get('/users')
def get_users(params: BaseQueryParams = Depends()):
    query = User.objects.skip(params.offset).limit(params.size)
    return {'users': [user.to_dict() for user in query.all()]}


@app.post('/users')
async def create_users(user_request: UserCreateRequest):
    user = await User.create(user_request)
    return user.to_dict()


@app.patch('/users/{user_id}')
async def update_user(user_id: str, user_request: UserUpdateRequest):
    try:
        user = await User.objects.async_get(id=user_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        await user.update(user_request)
        return user.to_dict()


@app.delete('/users/{user_id}')
async def deactivate_user(user_id: str):
    try:
        user = await User.objects.async_get(id=user_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        await user.deactivate()
        return user.to_dict()
