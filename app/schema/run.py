from datetime import datetime
from typing import Union, List

from pydantic import BaseModel, Field


class Run(BaseModel):
    name: str = Field(max_length=64)
    group_id: Union[int, None] = None

    class Config:
        orm_mode = True


class RunIn(Run):
    pass


class RunView(Run):
    created_at: datetime
    modified_at: datetime
    id: int


class RunViewList(BaseModel):
    items: List[RunView]
    total: int


class RunPatch(BaseModel):
    name: str = Field(None, max_length=64)
    group_id: Union[int, None] = None
