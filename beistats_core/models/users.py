import datetime as dt

from mongoengine import DateTimeField, EmailField, StringField
from mongoengine_plus.aio import AsyncDocument
from mongoengine_plus.models import BaseModel, uuid_field
from mongoengine_plus.models.event_handlers import updated_at
from mongoengine_plus.types import EnumField

from ..requests import UserCreateRequest, UserUpdateRequest
from ..types import UserType


@updated_at.apply
class User(AsyncDocument, BaseModel):
    """
    User basic data in a collection
    """

    meta = {'collection': 'users'}

    id = StringField(primary_key=True, default=uuid_field('US'))
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    phone_number = StringField(required=True)
    email_address = EmailField(required=True)
    created_at = DateTimeField(default=dt.datetime.utcnow)
    updated_at = DateTimeField()
    deactivated_at = DateTimeField()
    type = EnumField(UserType, required=True)

    @classmethod
    async def create(cls, user_request: UserCreateRequest):
        new_user = cls(**user_request.dict())
        await new_user.async_save()
        return new_user

    async def update(self, user_request: UserUpdateRequest):
        self.first_name = (
            user_request.first_name
            if user_request.first_name
            else self.first_name
        )
        self.last_name = (
            user_request.last_name
            if user_request.last_name
            else self.last_name
        )
        self.updated_at = dt.datetime.utcnow()
        await self.async_save()

    async def deactivate(self):
        self.deactivated_at = dt.datetime.utcnow()
        await self.async_save()
