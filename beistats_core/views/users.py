from fastapi import APIRouter, HTTPException

from ..models.users import User
from ..requests import UserCreateRequest, UserUpdateRequest


app = APIRouter()

@app.get('/users')
def get_users():
    return {'users': []}

@app.post('/users')
async def create_users(user_request: UserCreateRequest):
    user = await User.create(user_request)
    return user

@app.patch('/users/{user_id}')
async def update_user(user_request: UserUpdateRequest):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        await user.update(user_request)
        return user

@app.delete('/users/{user_id}')
async def deactivate_user():
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        await user.deactivate()
        return user
