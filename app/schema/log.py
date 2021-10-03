from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from app.models.case import Statuses
from app.models.log import Level


class Log(BaseModel):
    name: str = Field(max_length=32)
    level: Level
    text: str
    status: Statuses = Statuses.pending
    report_id: int

    class Config:
        orm_mode = True


class LogIn(Log):
    pass


class LogView(Log):
    created_at: datetime
    modified_at: datetime
    id: int


class LogViewList(BaseModel):
    items: List[Log]
    total: int


class LogPatch(BaseModel):
    name: str = Field(None, max_length=32)
    level: Level = None
    text: str = None
    status: Statuses = None
    report_id: int = None
