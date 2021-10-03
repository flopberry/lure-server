from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from app.models.case import Statuses


class Case(BaseModel):
    name: str = Field(max_length=128)
    test_id: int
    status: Statuses = Statuses.pending

    class Config:
        orm_mode = True


class CaseIn(Case):
    pass


class CaseView(Case):
    created_at: datetime
    modified_at: datetime
    id: int


class CaseViewList(BaseModel):
    items: List[CaseView]
    total: int


class CasePatch(BaseModel):
    name: str = Field(None, max_length=256)
    test_id: int = None
