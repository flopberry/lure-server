from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from app.models.case import Statuses
from app.models.log import Level
from app.models.report import ReportType


class Report(BaseModel):
    name: str = Field(max_length=32)
    case_id: int
    type: ReportType

    class Config:
        orm_mode = True


class ReportIn(Report):
    pass


class ReportView(Report):
    created_at: datetime
    modified_at: datetime
    id: int


class ReportViewList(BaseModel):
    items: List[ReportView]
    total: int


class ReportPatch(BaseModel):
    name: str = Field(None, max_length=32)
    case_id: int = None
    type: ReportType = None
