from typing import Optional

from pydantic import BaseModel


class BaseQueryParams(BaseModel):
    page: Optional[int] = 1
    size: Optional[int] = 10

    @property
    def offset(self):
        return (self.page - 1) * self.size


class UserGamesQueryParams(BaseQueryParams):
    user_id: Optional[str] = None
    team_id: Optional[str] = None
