from datetime import datetime
from typing import List, Union

from pydantic import BaseModel, Field


class TestSuite(BaseModel):
    name: str = Field(max_length=64)
    run_id: int
    group_id: Union[int, None] = None

    class Config:
        orm_mode = True


class TestSuiteIn(TestSuite):
    pass


class TestSuiteView(TestSuite):
    created_at: datetime
    modified_at: datetime
    id: int


class TestSuiteViewList(BaseModel):
    items: List[TestSuiteView]
    total: int


class TestSuitePatch(BaseModel):
    name: str = Field(None, max_length=64)
    run_id: int = None
    group_id: Union[int, None] = None
