import jwt
import pytest
from fastapi import HTTPException

from beistats_core.app import ALGORITHM
from beistats_core.views.utils import get_authenticated_user


def test_not_valid_jwt():
    to_encode = {'sub': 'US1'}
    encoded_jwt = jwt.encode(to_encode, 'not-valid-key', algorithm=ALGORITHM)
    with pytest.raises(HTTPException) as exc:
        get_authenticated_user(encoded_jwt)
    exception = exc._excinfo[1]
    assert exception.detail == 'Could not validate credentials'
    assert exception.status_code == 401
