import jwt
from fastapi import Depends, HTTPException
from jwt import PyJWTError

from ..app import ALGORITHM, JWT_SECRET_KEY, oauth2_scheme


def get_authenticated_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    except PyJWTError:
        raise HTTPException(
            status_code=401,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    else:
        user_id: str = payload.get('sub')
        return user_id
