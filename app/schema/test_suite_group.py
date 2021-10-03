from datetime import datetime
from typing import List, Union

from pydantic import BaseModel, Field


class TestSuiteGroup(BaseModel):
    name: str = Field(max_length=64)

    class Config:
        orm_mode = True


class TestSuiteGroupIn(TestSuiteGroup):
    pass


class TestSuiteGroupView(TestSuiteGroup):
    created_at: datetime
    modified_at: datetime
    id: int


class TestSuiteGroupViewList(BaseModel):
    items: List[TestSuiteGroupView]
    total: int


class TestSuiteGroupPatch(BaseModel):
    name: str = Field(None, max_length=64)
