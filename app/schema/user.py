from datetime import datetime

from pydantic import BaseModel, Field

from app.models.user import Roles


class User(BaseModel):
    login: str = Field(max_length=32)

    class Config:
        orm_mode = True


class UserIn(User):
    password: str = Field(max_length=64)


class UserView(User):
    role: Roles
    token: str = Field(max_length=32)
    created_at: datetime
    modified_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str
