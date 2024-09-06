from fastapi import Depends, HTTPException

from ..app import app
from ..models import User
from ..requests import UserCreateRequest, UserUpdateRequest
from .utils import get_authenticated_user


@app.get('/users/me')
async def get_user(
    user_id: str = Depends(get_authenticated_user),
):
    user = await User.objects.async_get(id=user_id)
    return dict(user=await user.me_dict())


@app.post('/users')
async def create_users(user_request: UserCreateRequest):
    if await User.objects(
        email_address=user_request.email_address
    ).async_count():
        raise HTTPException(status_code=400, detail='Email already exist')
    user = await User.create(user_request)
    return user.to_dict()


@app.patch('/users/{url_user_id}')
async def update_user(
    url_user_id: str,
    user_request: UserUpdateRequest,
    user_id: str = Depends(get_authenticated_user),
):
    if url_user_id != 'me' and url_user_id != user_id:
        raise HTTPException(status_code=403, detail="Can't make this action")
    try:
        user = await User.objects.async_get(id=user_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail='User not found')
    else:
        await user.update(user_request)
        return user.to_dict()


@app.delete('/users/{url_user_id}')
async def deactivate_user(
    url_user_id: str, user_id: str = Depends(get_authenticated_user)
):
    if url_user_id != 'me' and url_user_id != user_id:
        raise HTTPException(status_code=403, detail="Can't make this action")
    try:
        user = await User.objects.async_get(id=user_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail='User not found')
    else:
        await user.deactivate()
        return user.to_dict()
