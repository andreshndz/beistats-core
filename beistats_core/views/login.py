from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException

from ..app import ALGORITHM, JWT_SECRET_KEY, MAX_SESSION_MINUTES, app
from ..models import User
from ..requests import LoginRequest


@app.post('/login')
async def login(login_request: LoginRequest):
    # Won't take in care about password now. Just email
    try:
        user = await User.objects.async_get(
            email_address=login_request.email_address
        )
    except (User.DoesNotExist, User.MultipleObjectsReturned):
        raise HTTPException(status_code=400, detail='Invalid Data')

    # Create Access Token
    expire = datetime.utcnow() + timedelta(minutes=MAX_SESSION_MINUTES)
    to_encode = {'sub': user.id, 'exp': expire}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return {'token': encoded_jwt}
