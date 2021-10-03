from datetime import datetime
from typing import List, Union

from pydantic import BaseModel, Field


class Test(BaseModel):
    name: str = Field(max_length=256)
    test_suite_id: int

    class Config:
        orm_mode = True


class TestIn(Test):
    pass


class TestView(Test):
    created_at: datetime
    modified_at: datetime
    id: int


class TestViewList(BaseModel):
    items: List[TestView]
    total: int


class TestPatch(BaseModel):
    name: str = Field(None, max_length=256)
    test_suite_id: int = None
