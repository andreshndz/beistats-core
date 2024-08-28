from typing import Optional

from pydantic import BaseModel, NonNegativeInt, ValidationInfo, field_validator

from .types import UserType


class LoginRequest(BaseModel):
    email_address: str
    password: str


class UserCreateRequest(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email_address: str
    type: UserType = UserType.player


class UserUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    # you can select multiple fields, or use '*' to select all fields
    @field_validator('first_name', 'last_name')
    @classmethod
    def check_alphanumeric(cls, v: str, info: ValidationInfo) -> str:
        print(v, info)
        return v

    """
    @validator("title", "body", pre=True, always=True)
    def check_at_least_one_not_none(cls, v1, v2):
        assert (
                isinstance(values.get('title'), str)
                and values.get('title') is not None
            ) or (
                isinstance(values.get('body'), str)
                and values.get('body') is not None
            ),
            "At least one of 'title' or 'body' must have a non-None value"
        return v1, v2
    """


class TeamRequest(BaseModel):
    name: str


class UserGameRequest(BaseModel):
    team_id: str
    at_bat: NonNegativeInt
    h: NonNegativeInt
    double: NonNegativeInt
    triple: NonNegativeInt
    hr: NonNegativeInt
    r: NonNegativeInt
    rbi: NonNegativeInt
    k: NonNegativeInt
    bb: NonNegativeInt
    sb: NonNegativeInt
