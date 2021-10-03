from datetime import datetime
from typing import Union, List

from pydantic import BaseModel, Field


class RunGroup(BaseModel):
    name: str = Field(max_length=64)

    class Config:
        orm_mode = True


class RunGroupIn(RunGroup):
    pass


class RunGroupView(RunGroup):
    created_at: datetime
    modified_at: datetime
    id: int


class RunGroupViewList(BaseModel):
    items: List[RunGroupView]
    total: int


class RunGroupPatch(BaseModel):
    name: str = Field(None, max_length=64)
